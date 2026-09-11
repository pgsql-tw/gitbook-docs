import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from translation_pipeline import Queue, PageFailure, GlobalFailure, parts, structural_errors, write_text, git, digest, PENDING, STATUS

PAGE = 'appendixes/contrib/passwordcheck.md'
SOURCE = '## F.24. Test [#](#TEST)\n\nEnglish `identifier`.\n\n### F.24.1. Title\n\nMore English.\n'
TARGET = '<a id="TEST"></a>\n\n## F.24. 測試 [#](#TEST)\n\n中文 `identifier`。\n\n### F.24.1. 標題\n\n其他中文。\n'


class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='pg18-pipeline-test-')
        self.root = Path(self.tmp.name)
        git(self.root, 'init', '-b', '18')
        git(self.root, 'config', 'user.name', 'Test')
        git(self.root, 'config', 'user.email', 'test@example.invalid')
        write_text(self.root / PAGE, SOURCE)
        write_text(self.root / PENDING, f'待譯頁面：1 頁。\n- [ ] `{PAGE}` — Test\n')
        write_text(self.root / 'SUMMARY.md', f'* [Test]({PAGE})\n')
        write_text(self.root / STATUS, 'Initial\n')
        git(self.root, 'add', '--', PAGE, PENDING, 'SUMMARY.md', STATUS)
        git(self.root, 'commit', '-m', 'baseline')
        self.q = Queue(self.root)
        self.q.init()

    def tearDown(self):
        self.q.db.close()
        self.tmp.cleanup()

    def state(self):
        state = dict(baseline=SOURCE, base_hash=digest(SOURCE), source={'sha256': 'source'}, policy_hash='policy',
                     start_head=git(self.root, 'rev-parse', 'HEAD'),
                     approval=dict(page_hash=digest(TARGET), source_hash='source', policy_hash='policy'))
        self.q.workdir(PAGE).mkdir(parents=True, exist_ok=True)
        return state

    def test_heading_sections_stable_when_anchor_added(self):
        self.assertEqual(len(parts(SOURCE)), len(parts(TARGET)))
        self.assertEqual(structural_errors(SOURCE, TARGET, PAGE), [])

    def test_code_heading_not_split(self):
        text = SOURCE + '\n```sql\n### not a heading\nSELECT 1;\n```\n'
        self.assertEqual(len(parts(text)), 2)

    def test_table_heading_not_split(self):
        self.assertEqual(len(parts(SOURCE + '\n<table>\n### not a heading\n</table>')), 2)

    def test_generic_fences_all_protected(self):
        a = SOURCE + '\n```\nSELECT 1;\n```\n'
        b = TARGET + '\n```\nSELECT 2;\n```\n'
        self.assertIn('changed protected fences', structural_errors(a, b, PAGE))

    def test_restart_does_not_duplicate_queue(self):
        self.q.init()
        self.assertEqual(self.q.counts(), {'pending': 1})

    def test_collaborator_claim_returns_to_queue(self):
        import agent_handoff as h
        h.claim(self.root, PAGE, 'claude')
        self.q.sync_collaborators()
        self.assertEqual(self.q.counts(), {'delegated': 1})
        h.release(self.root, PAGE, 'claude')
        self.q.sync_collaborators()
        self.assertEqual(self.q.counts(), {'pending': 1})

    def test_expired_claim_returns_to_queue(self):
        import agent_handoff as h
        h.claim(self.root, PAGE, 'claude')
        self.q.sync_collaborators()
        h.claim(self.root, PAGE, 'claude', ttl_hours=-1)
        self.q.sync_collaborators()
        self.assertEqual(self.q.counts(), {'pending': 1})

    def test_checkbox_without_commit_is_not_completion(self):
        write_text(self.root / PENDING, f'待譯頁面：0 頁。\n- [x] `{PAGE}` — Test\n')
        with self.assertRaisesRegex(GlobalFailure, 'matching committed'):
            self.q.sync_collaborators()

    def test_external_commit_reconciled(self):
        self.q.publish(PAGE, self.state(), TARGET)
        self.q.update(PAGE, 'pending')
        self.q.sync_collaborators()
        self.assertEqual(self.q.counts(), {'done': 1})

    def test_publish_refuses_other_claim(self):
        import agent_handoff as h
        h.claim(self.root, PAGE, 'claude')
        with self.assertRaisesRegex(GlobalFailure, 'claimed'):
            self.q.publish(PAGE, self.state(), TARGET)

    def test_definition_fences_are_protected(self):
        a = SOURCE + '\n: ```sql\n  SELECT 1;\n  ```\n'
        b = TARGET + '\n: ```sql\n  SELECT 2;\n  ```\n'
        self.assertIn('changed protected fences', structural_errors(a, b, PAGE))

    def test_stale_approval(self):
        state = self.state()
        state['approval']['page_hash'] = 'wrong'
        with self.assertRaisesRegex(GlobalFailure, 'approval'):
            self.q.publish(PAGE, state, TARGET)

    def test_user_file_conflict(self):
        state = self.state()
        write_text(self.root / PAGE, 'user edit')
        with self.assertRaisesRegex(GlobalFailure, 'user changed'):
            self.q.publish(PAGE, state, TARGET)

    def test_user_index_preserved(self):
        write_text(self.root / 'other.txt', 'user edit')
        git(self.root, 'add', 'other.txt')
        with self.assertRaisesRegex(GlobalFailure, 'index'):
            self.q.publish(PAGE, self.state(), TARGET)
        self.assertEqual(git(self.root, 'diff', '--cached', '--name-only'), 'other.txt')

    def test_commit_and_reconcile(self):
        state = self.state()
        self.q.publish(PAGE, state, TARGET)
        self.q.publish(PAGE, state, TARGET)
        self.assertEqual(git(self.root, 'rev-list', '--count', 'HEAD'), '2')
        self.assertEqual(self.q.counts(), {'done': 1})
        self.assertIn('待譯頁面：0 頁。', (self.root / PENDING).read_text(encoding='utf-8'))

    def test_recover_after_stage_before_commit(self):
        state = self.state()
        original = git
        def crash(root, *args):
            if args[0] == 'commit':
                raise GlobalFailure('simulated crash')
            return original(root, *args)
        with patch('translation_pipeline.git', side_effect=crash):
            with self.assertRaisesRegex(GlobalFailure, 'simulated'):
                self.q.publish(PAGE, state, TARGET)
        saved = json.loads((self.q.workdir(PAGE) / 'manifest.json').read_text(encoding='utf-8'))
        self.q.publish(PAGE, saved, TARGET)
        self.assertEqual(git(self.root, 'rev-list', '--count', 'HEAD'), '2')

    def test_events_durable_until_ack(self):
        self.q.event('test_event', PAGE)
        self.assertEqual(self.q.db.execute('SELECT COUNT(*) FROM events WHERE acknowledged=0').fetchone()[0], 2)


if __name__ == '__main__':
    unittest.main()
