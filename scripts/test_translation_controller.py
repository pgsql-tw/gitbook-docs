"""Offline fault injection uses disposable Git repositories, never the real page."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from translation_controller import Controller, PAGE, TRACKERS, digest, exclusive, structural_errors

SOURCE = '''<a id="LTREE"></a>
## ltree [#](#LTREE)
English prose `ltree`.
```
foo English explanation
```
```
*{n} English explanation
```
```
@ English explanation
```
```
SELECT 1;
```
'''
TRANSLATED = SOURCE.replace('English prose', '正體中文說明').replace('English explanation', '中文說明')


class TestController(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='translation-controller-test-')
        self.root = Path(self.temp.name)
        self.c = Controller(self.root)
        self.c.git('init')
        self.c.git('config', 'user.name', 'Controller Test')
        self.c.git('config', 'user.email', 'controller-test@example.invalid')
        self.put(PAGE, SOURCE)
        for path in TRACKERS:
            self.put(path, 'initial\n')
        self.c.git('add', '--', PAGE, *TRACKERS)
        self.c.git('commit', '-m', 'fixture')
        self.c.init()

    def tearDown(self):
        self.temp.cleanup()

    def put(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')

    def ready(self):
        self.put(PAGE, TRANSLATED)
        self.c.observe()
        self.c.approve(digest(TRANSLATED), 'Fixture semantic review')
        self.put(TRACKERS[1], f'待譯頁面：0 頁。\n- [x] `{PAGE}`\n')

    def test_two_empty_runs_fail(self):
        self.assertFalse(self.c.observe())
        self.assertFalse(self.c.observe())
        self.assertEqual(self.c.state()['phase'], 'failed_no_progress')

    def test_checkpoint_only_is_not_progress(self):
        self.put(TRACKERS[2], 'pretend progress')
        self.assertFalse(self.c.observe())

    def test_restart_keeps_partial_text_and_counter(self):
        self.put(PAGE, SOURCE + '\n部分翻譯\n')
        self.c.observe()
        before = self.c.state()
        restarted = Controller(self.root)
        self.assertEqual(restarted.init(), before)
        self.assertEqual((self.root / PAGE).read_text(encoding='utf-8'), SOURCE + '\n部分翻譯\n')
        restarted.observe()
        self.assertEqual(restarted.state()['no_progress'], 1)

    def test_approval_is_required(self):
        self.put(PAGE, TRANSLATED)
        with self.assertRaisesRegex(RuntimeError, 'semantic review'):
            self.c.finalize()

    def test_stale_approval_rejected(self):
        self.ready()
        self.put(PAGE, TRANSLATED + '\n變更\n')
        with self.assertRaisesRegex(RuntimeError, 'changed after review'):
            self.c.finalize()

    def test_bad_review_hash_rejected(self):
        self.put(PAGE, TRANSLATED)
        with self.assertRaisesRegex(RuntimeError, 'stale'):
            self.c.approve('wrong', 'review')

    def test_sql_mutation_rejected(self):
        self.assertIn('changed protected fences', structural_errors(SOURCE, TRANSLATED.replace('SELECT 1', 'SELECT 2')))

    def test_inline_identifier_mutation_rejected(self):
        self.assertIn('changed protected markdown_code', structural_errors(SOURCE, TRANSLATED.replace('`ltree`', '`text`')))

    def test_explanatory_translation_allowed(self):
        self.assertEqual(structural_errors(SOURCE, TRANSLATED), [])

    def test_inline_code_can_reorder_for_chinese_grammar(self):
        self.assertEqual(structural_errors(SOURCE + '`a` then `b`', TRANSLATED + '`b` 再 `a`'), [])

    def test_table_summary_is_translatable_but_structure_is_protected(self):
        source = SOURCE + '<table summary="Functions"><tr><td>Text</td></tr></table>'
        translated = TRANSLATED + '<table summary="函式"><tr><td>文字</td></tr></table>'
        self.assertEqual(structural_errors(source, translated), [])
        self.assertIn('changed protected tags', structural_errors(source, translated.replace('</td>', '')))

    def test_missing_anchor_rejected(self):
        self.assertTrue(structural_errors(SOURCE, TRANSLATED.replace('<a id="LTREE"></a>', '')))

    def test_unrelated_staged_work_preserved(self):
        self.ready()
        self.put('unrelated.txt', 'user work')
        self.c.git('add', 'unrelated.txt')
        with self.assertRaisesRegex(RuntimeError, 'index is not empty'):
            self.c.finalize()
        self.assertEqual(self.c.git('diff', '--cached', '--name-only'), 'unrelated.txt')

    def test_commit_then_crash_reconciles_without_duplicate(self):
        self.ready()
        precommit = self.c.state()
        commit = self.c.finalize()
        # Simulate process dying after git commit but before saving completed state.
        self.c.save(precommit)
        restarted = Controller(self.root)
        self.assertEqual(restarted.finalize(), commit)
        self.assertEqual(restarted.git('rev-list', '--count', 'HEAD'), '2')

    def test_counter_mismatch_blocks_commit(self):
        self.ready()
        self.put(TRACKERS[1], f'待譯頁面：99 頁。\n- [x] `{PAGE}`\n')
        with self.assertRaisesRegex(RuntimeError, 'count is inconsistent'):
            self.c.finalize()

    def test_auth_failure_is_durable(self):
        with patch('translation_controller.shutil.which', return_value='codex'), patch(
                'translation_controller.subprocess.run', return_value=subprocess.CompletedProcess([], 1)):
            self.assertFalse(self.c.run_cli())
        self.assertEqual(Controller(self.root).state()['phase'], 'failed_auth')

    def test_log_permission_error_still_reports_to_stdout(self):
        with patch('pathlib.Path.open', side_effect=PermissionError('denied')), patch('builtins.print') as output:
            self.c.emit('failed', reason='original error')
        record = json.loads(output.call_args.args[0])
        self.assertEqual(record['reason'], 'original error')
        self.assertIn('event_log_error', record)

    def fake_cli(self, responses):
        calls = []
        test = self
        class Process:
            returncode = 0
            def __init__(self, command, **kwargs):
                self.command = command
                calls.append(command)
            def communicate(self, prompt, timeout):
                response, text = responses[len(calls) - 1]
                if text is not None:
                    test.put(PAGE, text)
                Path(self.command[self.command.index('-o') + 1]).write_text(
                    json.dumps(response), encoding='utf-8')
        return Process, calls

    def test_cli_claim_done_without_change_retries_and_fails(self):
        response = {'status': 'candidate_complete', 'remaining': [], 'summary': 'done'}
        process, calls = self.fake_cli([(response, None), (response, None)])
        with patch('translation_controller.shutil.which', return_value='codex'), patch(
                'translation_controller.subprocess.run', return_value=subprocess.CompletedProcess([], 0)), patch(
                'translation_controller.subprocess.Popen', side_effect=process):
            self.assertFalse(self.c.run_cli())
        self.assertEqual(len(calls), 2)
        self.assertEqual(self.c.state()['phase'], 'failed_no_progress')

    def test_cli_partial_immediately_continues_then_requires_review(self):
        partial = {'status': 'partial', 'remaining': ['F.22.6'], 'summary': 'partial'}
        complete = {'status': 'candidate_complete', 'remaining': [], 'summary': 'candidate'}
        process, calls = self.fake_cli([(partial, SOURCE + '\n部分\n'), (complete, TRANSLATED)])
        with patch('translation_controller.shutil.which', return_value='codex'), patch(
                'translation_controller.subprocess.run', return_value=subprocess.CompletedProcess([], 0)), patch(
                'translation_controller.subprocess.Popen', side_effect=process):
            self.assertTrue(self.c.run_cli())
        self.assertEqual(len(calls), 2)
        self.assertIsNone(self.c.state()['approval'])
        self.assertEqual(self.c.git('rev-list', '--count', 'HEAD'), '1')

    def test_cli_invalid_result_is_failure(self):
        process, calls = self.fake_cli([({'summary': 'done'}, TRANSLATED)])
        with patch('translation_controller.shutil.which', return_value='codex'), patch(
                'translation_controller.subprocess.run', return_value=subprocess.CompletedProcess([], 0)), patch(
                'translation_controller.subprocess.Popen', side_effect=process):
            self.assertFalse(self.c.run_cli())
        self.assertEqual(self.c.state()['phase'], 'invalid_worker_result')

    def test_cli_bad_structure_retries_before_review(self):
        response = {'status': 'candidate_complete', 'remaining': [], 'summary': 'candidate'}
        process, calls = self.fake_cli([(response, TRANSLATED.replace('<a id="LTREE"></a>', '')),
                                       (response, TRANSLATED)])
        with patch('translation_controller.shutil.which', return_value='codex'), patch(
                'translation_controller.subprocess.run', return_value=subprocess.CompletedProcess([], 0)), patch(
                'translation_controller.subprocess.Popen', side_effect=process):
            self.assertTrue(self.c.run_cli())
        self.assertEqual(len(calls), 2)
        self.assertEqual(self.c.state()['phase'], 'awaiting_review')

    def test_single_writer_and_crash_release(self):
        lock = self.c.runtime / 'writer.lock'
        with exclusive(lock):
            with self.assertRaises(OSError):
                with exclusive(lock):
                    pass
        child = subprocess.run(['python', '-c',
            'import os,sys; from pathlib import Path; from translation_controller import exclusive; '
            'ctx=exclusive(Path(sys.argv[1])); ctx.__enter__(); os._exit(7)', str(lock)],
            cwd=Path(__file__).parent)
        self.assertEqual(child.returncode, 7)
        with exclusive(lock):
            pass


if __name__ == '__main__':
    unittest.main()
