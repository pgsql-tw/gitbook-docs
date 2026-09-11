"""agent_handoff 的隔離測試：只在暫存 git repo 中執行，不碰真實 checkout。"""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import agent_handoff as h

PAGE = 'tutorial/tutorial-start/tutorial-install.md'
OTHER = 'tutorial/tutorial-start/tutorial-arch.md'
SOURCE = ('## 1.1. Installation [#](#TUTORIAL-INSTALL)\n\nSet `PGHOST` first. See [Chapter 17](../x/README.md).\n\n'
          '---\n\n原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-install.html)'
          '（英文原文，待翻譯）\n')
TARGET = ('<a id="TUTORIAL-INSTALL"></a>\n\n## 1.1. 安裝 [#](#TUTORIAL-INSTALL)\n\n請先設定 `PGHOST`。'
          '請參閱[第 17 章](../x/README.md)。\n\n---\n\n原文：[PostgreSQL 18.6 Documentation]'
          '(https://www.postgresql.org/docs/18/tutorial-install.html)（原文版本：18.6；核對日期：2026-09-11）\n')


class Tests(unittest.TestCase):
    def setUp(self):
        self.review_patch = patch('agent_handoff.semantic_review', return_value=[])
        self.review_patch.start()
        self.addCleanup(self.review_patch.stop)
        self.tmp = tempfile.TemporaryDirectory(prefix='pg18-handoff-test-')
        self.root = Path(self.tmp.name)
        h.git(self.root, 'init', '-b', '18')
        h.git(self.root, 'config', 'user.name', 'Test')
        h.git(self.root, 'config', 'user.email', 'test@example.invalid')
        h.git(self.root, 'config', 'core.autocrlf', 'true')
        h.write_styled(self.root / PAGE, SOURCE)
        h.write_styled(self.root / OTHER, SOURCE.replace('TUTORIAL-INSTALL', 'TUTORIAL-ARCH'))
        pending = (f'# 清單\n\n待譯頁面：2 頁。\n\n- [x] `a.md` — A\n- [ ] `{OTHER}` — 1.2. Arch #\n'
                   f'- [ ] `{PAGE}` — 1.1. Installation #\n')
        h.write_styled(self.root / h.PENDING, pending, (True, True))  # BOM + CRLF，同真實檔案
        h.write_styled(self.root / h.SUMMARY, f'* [1.2. Arch #]({OTHER})\n* [1.1. Installation #]({PAGE})\n',
                       (False, True))
        h.git(self.root, 'add', '-A')
        h.git(self.root, 'commit', '-m', 'baseline')

    def tearDown(self):
        self.tmp.cleanup()

    def submit(self, text=TARGET, agent='claude', base=None, **extra):
        item = h.inbox_dir(self.root, agent) / h.slug(PAGE)
        item.mkdir(parents=True, exist_ok=True)
        h.write_styled(item / 'page.md', text)
        meta = dict(page=PAGE, agent=agent, base_sha256=base or h.digest(h.read(self.root / PAGE)),
                    page_sha256=h.digest(text), source_url='https://www.postgresql.org/docs/18/tutorial-install.html',
                    source_version='18.6', retrieved='2026-09-11', submitted_at=h.stamp(),
                    self_review='checked', trailers=['Co-Authored-By: Claude <noreply@anthropic.com>'])
        meta.update(extra)
        h.write_json(item / 'meta.json', meta)
        return item

    def test_claim_is_exclusive_and_visible(self):
        h.claim(self.root, PAGE, 'claude')
        self.assertTrue(h.is_claimed_by_other(self.root, PAGE, 'codex'))
        self.assertFalse(h.is_claimed_by_other(self.root, PAGE, 'claude'))
        with self.assertRaises(RuntimeError):
            h.claim(self.root, PAGE, 'codex')
        h.claim(self.root, PAGE, 'claude')  # 自己續期可行

    def test_expired_claim_can_be_taken_over(self):
        h.claim(self.root, PAGE, 'claude', ttl_hours=-1)
        self.assertIsNone(h.claim_owner(self.root, PAGE))
        h.claim(self.root, PAGE, 'codex')
        self.assertEqual(h.claim_owner(self.root, PAGE), 'codex')

    def test_cannot_claim_done_page(self):
        with self.assertRaises(RuntimeError):
            h.claim(self.root, 'a.md', 'claude')

    def test_semantic_rejection_prevents_commit(self):
        self.submit()
        result = h.publish(self.root, reviewer=lambda *args: ['omitted warning'])
        self.assertEqual(result[0]['outcome'], 'review_rejected')
        self.assertEqual(h.git(self.root, 'rev-list', '--count', 'HEAD'), '1')
        self.assertEqual(h.read(self.root / PAGE), SOURCE)

    def test_commit_failure_preserves_index_and_candidate(self):
        item = self.submit()
        original = h.git
        def crash(root, *args, **kwargs):
            if args[0] == 'commit':
                raise RuntimeError('simulated failure')
            return original(root, *args, **kwargs)
        with patch('agent_handoff.git', side_effect=crash):
            with self.assertRaisesRegex(RuntimeError, 'simulated'):
                h.publish(self.root)
        self.assertEqual(h.read(self.root / PAGE), TARGET)
        self.assertIn(PAGE, h.git(self.root, 'diff', '--cached', '--name-only'))
        self.assertTrue((item / 'publish-failure.json').exists())

    def test_post_commit_crash_reconciles(self):
        self.submit()
        original = h.move_item
        with patch('agent_handoff.move_item', side_effect=RuntimeError('crash')):
            with self.assertRaisesRegex(RuntimeError, 'crash'):
                h.publish(self.root)
        result = h.publish(self.root)
        self.assertEqual(result[0]['outcome'], 'reconciled')
        self.assertEqual(h.git(self.root, 'rev-list', '--count', 'HEAD'), '2')

    def test_publish_commits_one_page_with_author_and_trailers(self):
        h.claim(self.root, PAGE, 'claude')
        item = self.submit()
        result = h.publish(self.root)
        self.assertEqual(result[0]['outcome'], 'published', result)
        log = h.git(self.root, 'log', '-1', '--format=%an <%ae>%n%s%n%b')
        self.assertIn('Claude <noreply@anthropic.com>', log)
        self.assertIn('文件(pg18)：翻譯 tutorial-install', log)
        self.assertIn('Translation-Page-SHA256: ' + h.digest(TARGET), log)
        self.assertIn('Co-Authored-By: Claude', log)
        self.assertEqual(h.read(self.root / PAGE), TARGET)
        pending_raw = (self.root / h.PENDING).read_bytes()
        self.assertTrue(pending_raw.startswith(b'\xef\xbb\xbf') and b'\r\n' in pending_raw)
        pending = h.read(self.root / h.PENDING)
        self.assertIn(f'- [x] `{PAGE}` — 1.1. 安裝 #', pending)
        self.assertIn('待譯頁面：1 頁。', pending)
        self.assertIn(f'[1.1. 安裝 #]({PAGE})', h.read(self.root / h.SUMMARY))
        self.assertFalse(item.exists())
        self.assertEqual(len(list((item.parent / '_published').iterdir())), 1)
        self.assertIsNone(h.load_claim(self.root, PAGE))
        self.assertEqual(h.git(self.root, 'status', '--porcelain', '--', PAGE, h.PENDING, h.SUMMARY), '')
        self.assertEqual(h.git(self.root, 'show', '--name-only', '--format=', 'HEAD').splitlines(),
                         sorted([PAGE, h.PENDING, h.SUMMARY]))

    def test_republish_is_reconciled_not_duplicated(self):
        self.submit()
        h.publish(self.root)
        head = h.git(self.root, 'rev-parse', 'HEAD')
        # 模擬 commit 後、搬移 inbox 前中斷：同一份稿件再次出現
        h.git(self.root, 'checkout', '-q', 'HEAD~1', '--', h.PENDING)
        h.git(self.root, 'commit', '-qm', 'reopen list for test')
        self.submit(base=h.digest(TARGET))
        # An explicit later reopen is not a post-commit crash. Preserve that
        # decision instead of silently closing the list or duplicating the page.
        with self.assertRaisesRegex(RuntimeError, 'reopened'):
            h.publish(self.root)
        self.assertEqual(h.git(self.root, 'diff', '--cached', '--name-only'), '')

    def test_stale_base_is_rejected_with_message(self):
        item = self.submit(base='0' * 64)
        result = h.publish(self.root)
        self.assertEqual(result[0]['outcome'], 'rejected')
        self.assertTrue(any('stale base' in e for e in result[0]['errors']))
        self.assertTrue((item.parent / '_rejected').exists())
        msgs = list((self.root / h.AGENTS / 'messages').glob('*--to-claude--*.md'))
        self.assertEqual(len(msgs), 1)
        self.assertEqual(h.git(self.root, 'rev-list', '--count', 'HEAD'), '1')

    def test_claim_by_other_agent_is_rejected(self):
        h.claim(self.root, PAGE, 'codex')
        result = h.publish(self.root)  # 沒有 inbox 時不做事
        self.assertEqual(result, [])
        self.submit()
        result = h.publish(self.root)
        self.assertIn('page is claimed by codex', result[0]['errors'])

    def test_structural_change_is_rejected(self):
        broken = TARGET.replace('`PGHOST`', 'PGHOST')
        self.submit(text=broken)
        result = h.publish(self.root)
        self.assertEqual(result[0]['outcome'], 'rejected')
        self.assertTrue(any('protected' in e for e in result[0]['errors']), result)

    def test_untranslated_marker_is_rejected(self):
        self.submit(text=TARGET.replace('）\n', '）（英文原文，待翻譯）\n'))
        result = h.publish(self.root)
        self.assertIn('untranslated marker remains', result[0]['errors'])

    def test_dirty_publish_target_blocks_without_side_effects(self):
        self.submit()
        h.write_styled(self.root / h.SUMMARY, 'dirty\n')
        with self.assertRaises(RuntimeError):
            h.publish(self.root)
        self.assertEqual(h.read(self.root / h.SUMMARY), 'dirty\n')
        self.assertEqual(h.git(self.root, 'rev-list', '--count', 'HEAD'), '1')

    def test_staged_user_work_blocks_publish(self):
        self.submit()
        h.write_styled(self.root / 'x.md', 'user\n')
        h.git(self.root, 'add', 'x.md')
        with self.assertRaises(RuntimeError):
            h.publish(self.root)

    def test_dry_run_changes_nothing(self):
        item = self.submit()
        result = h.publish(self.root, dry_run=True)
        self.assertEqual(result[0]['outcome'], 'would_publish')
        self.assertTrue(item.exists())
        self.assertEqual(h.read(self.root / PAGE), SOURCE)

    def test_status_and_message(self):
        h.claim(self.root, OTHER, 'codex')
        self.submit()
        h.message(self.root, 'claude', 'codex', '測試 主旨', '內容')
        s = h.status(self.root)
        self.assertEqual(s['remaining'], 2)
        self.assertEqual(s['bottom'][0], PAGE)
        self.assertEqual(s['inbox'], {'claude': 1})
        self.assertEqual(s['messages_by_recipient'], {'codex': 1})
        self.assertTrue(s['claims'][0]['valid'])

    def test_inline_code_wrapped_across_lines_is_tolerated(self):
        base = 'Use `pg_config\n--sharedir` to find it.\nThen `a` and `b`.\n'
        good = '請用 `pg_config --sharedir` 查詢。接著 `a` 與 `b`。\n'
        bad = '請用 `pg_config --sharedir` 查詢。接著 `a` 與 b。\n'
        self.assertNotIn('changed protected inline', h.structural_errors(base, good, 'x.md'))
        self.assertIn('changed protected inline', h.structural_errors(base, bad, 'x.md'))

    def test_definition_list_fence_is_parsed(self):
        base = 'Cross join\n:   ```\n\n    T1 CROSS JOIN T2\n    ```\n\n    For every row.\n\nNext\n:   ```\n\n    X\n    ```\n'
        good = '交叉聯結\n:   ```\n\n    T1 CROSS JOIN T2\n    ```\n\n    對每一筆資料列。\n\nNext\n:   ```\n\n    X\n    ```\n'
        bad = good.replace('T1 CROSS JOIN T2', 'T1 CROSS JOIN T3')
        self.assertNotIn('changed protected fences', h.structural_errors(base, good, 'x.md'))
        self.assertIn('changed protected fences', h.structural_errors(base, bad, 'x.md'))

    def test_readme_paths_allowed(self):
        self.assertEqual(h.slug('tutorial/README.md'), 'tutorial__README.md')

    def test_invalid_paths_rejected(self):
        for bad in ('../etc/passwd.md', 'outputs/pg18-translation/pending-pages.md', 'a b.md'):
            with self.assertRaises(ValueError):
                h.slug(bad)


if __name__ == '__main__':
    unittest.main()
