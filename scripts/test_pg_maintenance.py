import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

import pg_maintenance as io
import pg_link_rewrite as rewrite


TARGET = [{'from': {'page': 'a.md', 'fragment': 'OLD'},
           'to': {'page': 'child/item.md', 'fragment': 'new'}}]


class MaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_atomic_failure_keeps_previous_json(self):
        p = self.root / 'result.json'
        io.atomic_json(p, {'status': 'running', 'results': [1]})
        with patch.object(io.os, 'replace', side_effect=OSError('disk failure')):
            with self.assertRaises(OSError):
                io.atomic_json(p, {'status': 'complete'})
        self.assertEqual(json.loads(p.read_text()), {'status': 'running', 'results': [1]})
        self.assertEqual(list(self.root.glob('*.tmp')), [])

    def test_concurrent_json_readers_never_see_truncation(self):
        p = self.root / 'result.json'
        io.atomic_json(p, {'sequence': 0, 'payload': '資料' * 50})
        stop, errors = threading.Event(), []
        def reader():
            while not stop.is_set():
                try:
                    value = io.read_json(p)
                    if value['payload'] != '資料' * 50:
                        errors.append('corrupted payload')
                except Exception as e:
                    errors.append(str(e))
        thread = threading.Thread(target=reader)
        thread.start()
        try:
            for i in range(25):
                io.atomic_json(p, {'sequence': i, 'payload': '資料' * 50})
        finally:
            stop.set(); thread.join()
        self.assertFalse(errors)

    def test_snapshot_retains_read_bytes_and_detects_worktree_change(self):
        p = self.root / 'a.md'; p.write_text('before')
        snapshot = io.InputSnapshot(self.root); snapshot.capture(['a.md'])
        p.write_text('after')
        self.assertEqual(snapshot.text(p), 'before')
        self.assertFalse(snapshot.verify()['valid'])
        self.assertEqual(snapshot.verify()['changed_inputs'][0]['path'], 'a.md')

    def test_malformed_json_is_reported_not_retried_as_partial_output(self):
        p = self.root / 'bad.json'; p.write_text('{broken')
        with self.assertRaises(json.JSONDecodeError):
            io.read_json(p)
        self.assertEqual(p.read_text(), '{broken')
        self.assertFalse(Path(str(p) + '.io.lock').exists())

    def test_snapshot_detects_new_inventory_member_and_deleted_file(self):
        p = self.root / 'a.md'; p.write_text('a')
        snapshot = io.InputSnapshot(self.root)
        snapshot.inventory('pages', lambda: [f.name for f in self.root.glob('*.md')])
        snapshot.capture(['a.md']); p.unlink(); (self.root / 'b.md').write_text('b')
        report = snapshot.verify()
        self.assertFalse(report['valid'])
        self.assertEqual(report['inventory_changes'][0], {'name': 'pages', 'added': ['b.md'], 'removed': ['a.md']})

    def test_exact_destination_keeps_unrelated_selflinks(self):
        text = '[keep](a.md#OTHER) [move](a.md#OLD) [other file](b.md#OLD)'
        actual, edits = rewrite.rewrite_links(text, 'a.md', 'a.md', TARGET)
        self.assertEqual(actual, '[keep](a.md#OTHER) [move](child/item.md#new) [other file](b.md#OLD)')
        self.assertEqual(len(edits), 1)

    def test_relocation_rebases_links_but_preserves_every_example(self):
        examples = '\n```md\n[x](a.md#OLD)\n```\n\n<pre>[x](a.md#OLD)</pre>\n\n`[x](a.md#OLD)`\n'
        text = '[table](a.md#OLD) [neighbor](b.md#B)' + examples
        actual, edits = rewrite.rewrite_links(text, 'a.md', 'child/item.md', TARGET)
        self.assertEqual(actual, '[table](#new) [neighbor](../b.md#B)' + examples)
        self.assertEqual(len(edits), 2)

    def test_reference_destination_html_titles_and_crlf_survive(self):
        text = '\ufeff[x][r]\r\n\r\n[r]: a.md#OLD "title"\r\n<a data-href="a.md#OLD" href=\'a.md#OLD\'>x</a>\r\n'
        actual, edits = rewrite.rewrite_links(text, 'a.md', 'a.md', TARGET)
        self.assertEqual(actual, text.replace('[r]: a.md#OLD', '[r]: child/item.md#new').replace("href='a.md#OLD'", "href='child/item.md#new'"))
        self.assertEqual(len(edits), 2)

    def test_html_attributes_comments_and_balanced_markdown_destinations(self):
        text = '<a title="href=\'a.md#OLD\' > note" href=a.md#OLD>x</a>\n<!-- [x](a.md#OLD) -->'
        changed, edits = rewrite.rewrite_links(text, 'a.md', 'a.md', TARGET)
        self.assertEqual(changed, text.replace(' href=a.md#OLD', ' href=child/item.md#new'))
        self.assertEqual(len(edits), 1)
        text = '[x](path(with).md#OLD "title")'
        targets = [{'from': {'page': 'path(with).md', 'fragment': 'OLD'}, 'to': {'page': 'new.md', 'fragment': 'new'}}]
        self.assertEqual(rewrite.rewrite_links(text, 'a.md', 'a.md', targets)[0], '[x](new.md#new "title")')

    def test_literal_path_delimiters_are_encoded(self):
        target = [{'from': {'page': 'a.md', 'fragment': 'OLD'},
                   'to': {'page': 'child/a#b.md', 'fragment': 'part%one'}}]
        self.assertEqual(rewrite.rewrite_links('[x](a.md#OLD)', 'a.md', 'a.md', target)[0],
                         '[x](child/a%23b.md#part%25one)')

    def make_plan(self):
        for name in ['a.md', 'b.md']:
            (self.root / name).write_bytes(b'\xef\xbb\xbf[x](a.md#OLD)\r\n')
        return rewrite.build_plan(self.root, {'files': ['a.md', 'b.md'], 'targets': TARGET,
                                              'expected_changes': {'a.md': 1, 'b.md': 1}})

    def test_plan_is_readonly_and_stale_second_file_prevents_first_write(self):
        plan = self.make_plan()
        before = (self.root / 'a.md').read_bytes()
        (self.root / 'b.md').write_text('other work')
        with self.assertRaisesRegex(ValueError, 'Stale candidate'):
            rewrite.apply_plan(self.root, plan, self.root / 'outputs/report.json')
        self.assertEqual((self.root / 'a.md').read_bytes(), before)
        self.assertEqual((self.root / 'b.md').read_text(), 'other work')

    def test_apply_verifies_preview_and_preserves_encoding(self):
        plan = self.make_plan()
        rewrite.apply_plan(self.root, plan, self.root / 'outputs/report.json')
        self.assertEqual((self.root / 'a.md').read_bytes(), b'\xef\xbb\xbf[x](child/item.md#new)\r\n')
        self.assertEqual(json.loads((self.root / 'outputs/report.json').read_text())['status'], 'complete')
        self.assertFalse((self.root / 'outputs/pg-maintenance/rewrite.lock').exists())

    def test_failure_rolls_back_only_own_generated_changes(self):
        plan = self.make_plan(); before = (self.root / 'a.md').read_bytes()
        real = rewrite.atomic_write
        def fail_second(path, data):
            if Path(path).name == 'b.md':
                raise OSError('disk failure')
            real(path, data)
        with patch.object(rewrite, 'atomic_write', side_effect=fail_second):
            with self.assertRaises(OSError):
                rewrite.apply_plan(self.root, plan, self.root / 'outputs/report.json')
        self.assertEqual((self.root / 'a.md').read_bytes(), before)

    def test_concurrent_edit_is_not_overwritten_during_rollback(self):
        plan = self.make_plan(); real = rewrite.atomic_write
        def fail_second(path, data):
            if Path(path).name == 'b.md':
                (self.root / 'a.md').write_text('concurrent work')
                raise OSError('failure')
            real(path, data)
        with patch.object(rewrite, 'atomic_write', side_effect=fail_second):
            with self.assertRaises(OSError):
                rewrite.apply_plan(self.root, plan, self.root / 'outputs/report.json')
        self.assertEqual((self.root / 'a.md').read_text(), 'concurrent work')
        self.assertEqual(json.loads((self.root / 'outputs/report.json').read_text())['rollback_conflicts'], ['a.md'])

    def test_unreviewed_or_tampered_plan_never_writes(self):
        plan = self.make_plan(); plan['files'][0]['edits'][0]['after'] = 'other.md'
        with self.assertRaisesRegex(ValueError, 'verification'):
            rewrite.apply_plan(self.root, plan, self.root / 'outputs/report.json')
        self.assertIn(b'a.md#OLD', (self.root / 'a.md').read_bytes())

    def test_scope_paths_cannot_escape_or_alias_git(self):
        for name in ['../outside.md', '.git/config', 'sub/../a.md', './a.md']:
            with self.assertRaises(ValueError):
                rewrite.safe_path(self.root, name)


if __name__ == '__main__':
    unittest.main()
