import json
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from translation_pipeline import Queue, PageFailure, GlobalFailure, parts, structural_errors, write_text, git, digest, PENDING, STATUS, emit_json
from translation_pipeline import worker_failure, structural_details, retry_hint

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

    def test_event_output_uses_utf8_when_windows_stream_is_cp950(self):
        raw = io.BytesIO()
        cp950 = io.TextIOWrapper(raw, encoding='cp950', errors='strict')
        emit_json({'evidence': 'nonbreaking\u00a0space'}, stream=cp950)
        self.assertIn('nonbreaking\u00a0space'.encode('utf-8'), raw.getvalue())

    def test_code_heading_not_split(self):
        text = SOURCE + '\n```sql\n### not a heading\nSELECT 1;\n```\n'
        self.assertEqual(len(parts(text)), 2)

    def test_table_heading_not_split(self):
        self.assertEqual(len(parts(SOURCE + '\n<table>\n### not a heading\n</table>')), 2)

    def test_generic_fences_all_protected(self):
        a = SOURCE + '\n```\nSELECT 1;\n```\n'
        b = TARGET + '\n```\nSELECT 2;\n```\n'
        self.assertIn('changed protected fences', structural_errors(a, b, PAGE))

    def test_structural_details_name_the_changed_spans(self):
        broken = TARGET.replace('`identifier`', '`identifiers` 與 `extra`')
        errors = structural_errors(SOURCE, broken, PAGE)
        self.assertIn('changed protected inline', errors)
        detailed = structural_details(SOURCE, broken, PAGE, errors)
        self.assertEqual(len(detailed), len(errors))
        joined = '\n'.join(detailed)
        # 標籤前綴不變，後面補上具體差異，下一輪才不必整頁重譯。
        self.assertTrue(any(d.startswith('changed protected inline') for d in detailed))
        self.assertIn('identifier', joined)
        self.assertIn('identifiers', joined)
        self.assertIn('extra', joined)

    def test_structural_details_report_reordered_content(self):
        source = SOURCE + '\n<table><tr><td><code>a</code> then <code>b</code></td></tr></table>\n'
        current = TARGET + '\n<table><tr><td><code>b</code> 在 <code>a</code> 之後</td></tr></table>\n'
        detailed = structural_details(source, current, PAGE)
        self.assertTrue(any('changed protected html_code' in d and '順序' in d for d in detailed))

    def test_structural_details_list_missing_anchors(self):
        source = SOURCE.replace('More English.', '<a id="id-1.2.3"></a>\n\nMore English.')
        detailed = structural_details(source, TARGET, PAGE)
        self.assertTrue(any(d.startswith('missing original anchors') and 'id-1.2.3' in d for d in detailed))

    def test_retry_hint_extracted_from_usage_limit_message(self):
        self.assertEqual(retry_hint("You've hit your usage limit. Try again at 1:55 PM."), '1:55 PM')
        self.assertIsNone(retry_hint('worker exited without a structured error'))

    def test_heading_anchor_belongs_to_its_own_section(self):
        text = (SOURCE + '\n<a id="SECOND"></a>\n\n### F.24.2. Second [#](#SECOND)\n\nMore.\n')
        sections = parts(text)
        # 錨點與它標示的標題必須落在同一段，審查者才看得到連結目標。
        holder = [i for i, p in enumerate(sections) if '<a id="SECOND"></a>' in p]
        heading = [i for i, p in enumerate(sections) if '[#](#SECOND)' in p]
        self.assertEqual(holder, heading)
        self.assertEqual(''.join(sections), text)

    def test_anchor_move_does_not_change_section_count(self):
        plain = SOURCE + '\n### F.24.2. Second [#](#SECOND)\n\nMore.\n'
        anchored = SOURCE + '\n<a id="SECOND"></a>\n\n### F.24.2. Second [#](#SECOND)\n\nMore.\n'
        self.assertEqual(len(parts(plain)), len(parts(anchored)))
        self.assertEqual(''.join(parts(anchored)), anchored)

    def test_inbox_review_packet_carries_submission_provenance(self):
        state = self.state()
        state['source'] = dict(url='https://www.postgresql.org/docs/18/x.html', sha256='source', retrieved='2026-09-13')
        state['submission'] = dict(page=PAGE, agent='claude', retrieved='2026-09-12')
        workspace = self.q.workdir(PAGE) / 'draft'
        workspace.mkdir(parents=True, exist_ok=True)
        write_text(workspace / 'source.html', '<html><body><div class="sect1" id="TEST"><p>x</p></div></body></html>')
        with patch.object(Queue, 'workdir', lambda self, page: self.rt / 'pages' / 'fixed'):
            pass
        captured = {}
        original = Queue.packed_context

        def spy(self, page, state, current, ids, role):
            text = original(self, page, state, current, ids, role)
            captured['text'] = text
            return text

        with patch.object(Queue, 'packed_context', spy):
            try:
                self.q.packed_context(PAGE, state, TARGET, [0], 'reviewer')
            except Exception as error:  # 來源快照雜湊不符時仍應保留 submission 欄位
                self.assertIn('source snapshot', str(error))
        from translation_packets import packet, SourceIndex
        index = SourceIndex('<html><body><div class="sect1" id="TEST"><p>x</p></div></body></html>', parts(SOURCE))
        value = packet(index, parts(SOURCE), parts(TARGET), [0], state['source'], state['submission'])
        self.assertEqual(value['submission']['retrieved'], '2026-09-12')

    def test_restart_does_not_duplicate_queue(self):
        self.q.init()
        self.assertEqual(self.q.counts(), {'pending': 1})

    def test_usage_failure_uses_terminal_event_not_document_output(self):
        log = json.dumps({'type': 'item.completed', 'item': {'text': 'usage limit in source'}})
        self.assertEqual(worker_failure(log)[0], 'worker_failed')
        log += '\n' + json.dumps({'type': 'turn.failed', 'error': {'message': "You've hit your usage limit. Try again later."}})
        kind, message = worker_failure(log)
        self.assertEqual(kind, 'usage_limit')
        self.assertNotIn('source', message)

    def test_inbox_is_bounded_and_reported_before_next_page(self):
        result = {'page': PAGE, 'outcome': 'review_rejected', 'errors': ['warning omitted']}
        with patch('agent_handoff.publish', return_value=[result]) as publish:
            self.q.process_inbox()
        self.assertEqual(publish.call_args.kwargs['limit'], 1)
        event = self.q.db.execute("SELECT payload FROM events WHERE type='inbox_publish_result'").fetchone()
        self.assertEqual(json.loads(event[0])['result'], result)

    def test_review_cache_requires_whole_document_context(self):
        state = self.review_state()
        target = self.q.workdir(PAGE) / 'draft' / PAGE
        write_text(target, TARGET)
        responses = [dict(reviews=[dict(passed=True, section=i, issues=[], evidence='fixture checks') for i in range(2)])]
        with patch.object(self.q, 'immutable'), patch.object(self.q, 'call', side_effect=responses) as call:
            self.assertEqual(self.q.review(PAGE, state, TARGET), [])
            self.assertEqual(call.call_count, 1)
        with patch.object(self.q, 'call') as call:
            self.assertEqual(self.q.review(PAGE, state, TARGET), [])
            call.assert_not_called()
        changed = TARGET + '\n補充中文。\n'
        write_text(target, changed)
        with patch.object(self.q, 'immutable'), patch.object(self.q, 'call', side_effect=responses) as call:
            self.assertEqual(self.q.review(PAGE, state, changed), [])
            self.assertEqual(call.call_count, 1)

    def review_state(self):
        state = self.state()
        state['reviews'] = []
        draft = self.q.workdir(PAGE) / 'draft'
        html = '<nav>navigation</nav><div class="sect1" id="TEST"><p>English identifier. More English.</p></div>'
        write_text(draft / 'source.html', html)
        write_text(draft / 'SKILL.md', 'Trusted fixture skill')
        write_text(draft / 'style.md', 'Trusted fixture style')
        write_text(draft / PAGE, TARGET)
        state['source'] = dict(sha256=digest(html), url='https://www.postgresql.org/docs/18/test.html')
        return state

    def test_group_review_requires_every_section(self):
        state = self.review_state()
        response = dict(reviews=[dict(section=0, passed=True, issues=[], evidence='only first')])
        with patch.object(self.q, 'immutable'), patch.object(self.q, 'call', return_value=response):
            with self.assertRaisesRegex(PageFailure, 'coverage'):
                self.q.review(PAGE, state, TARGET)
        self.assertEqual(state['reviews'], [])

    def test_packet_prompt_has_one_copy_and_keeps_fallback_available(self):
        state = self.review_state()
        text = self.q.packed_context(PAGE, state, TARGET, [0, 1], 'reviewer')
        value = json.loads(text[text.index('{'):])
        self.assertEqual(value['sections'][0]['original'], parts(SOURCE)[0])
        self.assertEqual(len(value['official_excerpts']), 1)
        self.assertNotIn('<nav>', value['official_excerpts'][0]['html'])
        self.assertIn('source.html remains available', text)
        self.assertNotIn('Read SKILL.md', self.q.common_prompt(PAGE))

    def test_packet_rejects_changed_source(self):
        state = self.review_state()
        write_text(self.q.workdir(PAGE) / 'draft/source.html', 'changed')
        with self.assertRaisesRegex(GlobalFailure, 'source snapshot changed'):
            self.q.packed_context(PAGE, state, TARGET, [0], 'reviewer')

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
