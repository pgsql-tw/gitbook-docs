import unittest
import json
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import patch

from final_site_audit import inspect, sha, scan


class SiteAuditTests(unittest.TestCase):
    def test_html_and_markdown_links(self):
        d = inspect('<a id="A"></a>\n\n[x](other.md#B)\n\n<img src="a.png">')
        self.assertEqual(d['ids'], ['A'])
        self.assertCountEqual([x[0] for x in d['links']], ['other.md#B', 'a.png'])

    def test_definition_list_fence_is_not_html(self):
        d = inspect(':   ```html\n<a id="fake" href="missing.md"></a>\n    ```\n\n<a id="real"></a>')
        self.assertEqual(d['ids'], ['real'])
        self.assertEqual(d['links'], [])

    def test_normal_code_is_not_link(self):
        self.assertEqual(inspect('```md\n[x](missing.md)\n```')['links'], [])

    def test_reference_link(self):
        self.assertEqual(inspect('[x][ref]\n\n[ref]: target.md')['links'][0][0], 'target.md')

    def test_duplicate_anchor_preserved(self):
        self.assertEqual(inspect('<a id="a"></a><a id="a"></a>')['ids'], ['a', 'a'])

    def test_hash_stable(self):
        self.assertEqual(len(sha('中文')), 64)

    def test_frontmatter_not_setext_heading(self):
        self.assertEqual(inspect('---\ndescription: example\n---\n\n# Title')['headings'], ['Title'])

    def test_indented_parameter_anchor_exists_in_source(self):
        d = inspect('parameter\n:   description\n\n    <a id="PARAMETER"></a>')
        self.assertEqual(d['ids'], ['PARAMETER'])

    def test_inline_html_example_is_not_anchor(self):
        self.assertEqual(inspect('Use `<a id="fake"></a>` here')['ids'], [])


class ScanConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-b', '19')
        (self.root / 'docs').mkdir()
        (self.root / 'SUMMARY.md').write_text('* [A](docs/a.md)\n', encoding='utf-8')
        (self.root / 'docs/a.md').write_text('# A\n\n<a id="a"></a>\n', encoding='utf-8')
        state = self.root / 'outputs/pg-translation'
        state.mkdir(parents=True)
        (state / 'pending-pages.md').write_text('', encoding='utf-8')
        self.git('add', 'SUMMARY.md', 'docs/a.md')
        self.git('-c', 'user.name=Audit fixture', '-c', 'user.email=fixture@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-m', 'fixture')

    def git(self, *args):
        return subprocess.check_output(['git', '-c', 'core.fsmonitor=false', *args], cwd=self.root, stderr=subprocess.PIPE)

    def test_summary_declared_untracked_page_is_fully_scanned(self):
        (self.root / 'docs/new.md').write_text('# New\n\n[x](missing.md)\n', encoding='utf-8')
        (self.root / 'SUMMARY.md').write_text('* [A](docs/a.md)\n* [New](docs/new.md)\n', encoding='utf-8')
        result = scan(self.root, self.root / 'outputs/scan')
        self.assertTrue(result['scan_valid'])
        self.assertEqual(result['site_pages'], 2)
        self.assertEqual(result['tracked_site_pages'], 1)
        self.assertEqual(result['untracked_summary_pages'], ['docs/new.md'])
        self.assertTrue(any(f['kind'] == 'missing_local_target' and f['page'] == 'docs/new.md' for f in result['findings']))

    def test_same_head_worktree_mutation_invalidates_report(self):
        head = self.git('rev-parse', 'HEAD')
        def mutate(*args, **kwargs):
            (self.root / 'docs/a.md').write_text('# Changed', encoding='utf-8')
            return []
        with patch('final_site_audit.zh_lint.lint', side_effect=mutate):
            result = scan(self.root, self.root / 'outputs/scan')
        self.assertEqual(self.git('rev-parse', 'HEAD'), head)
        self.assertFalse(result['scan_valid'])
        self.assertEqual(result['input_consistency']['changed_inputs'][0]['path'], 'docs/a.md')
        self.assertFalse(json.loads((self.root / 'outputs/scan/scan.json').read_text())['scan_valid'])

    def test_new_summary_member_during_scan_invalidates_inventory(self):
        def mutate(*args, **kwargs):
            (self.root / 'docs/b.md').write_text('# B', encoding='utf-8')
            (self.root / 'SUMMARY.md').write_text('* [A](docs/a.md)\n* [B](docs/b.md)\n', encoding='utf-8')
            return []
        with patch('final_site_audit.zh_lint.lint', side_effect=mutate):
            result = scan(self.root, self.root / 'outputs/scan')
        self.assertFalse(result['scan_valid'])
        self.assertTrue(any(x['name'] == 'site_pages' for x in result['input_consistency']['inventory_changes']))

    def test_linked_asset_mutation_is_not_missed(self):
        (self.root / 'docs/image.png').write_bytes(b'original image')
        (self.root / 'docs/a.md').write_text('# A\n\n![figure](image.png)\n', encoding='utf-8')
        def mutate(*args, **kwargs):
            (self.root / 'docs/image.png').unlink()
            return []
        with patch('final_site_audit.zh_lint.lint', side_effect=mutate):
            result = scan(self.root, self.root / 'outputs/scan')
        self.assertFalse(result['scan_valid'])
        self.assertIn('docs/image.png', [x['path'] for x in result['input_consistency']['changed_inputs']])


if __name__ == '__main__':
    unittest.main()
