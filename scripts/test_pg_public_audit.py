import copy
import unittest

from pg_public_audit import authored_links, expected_links, public_url, compare_case, check_results


class PublicAuditTests(unittest.TestCase):
    def test_separate_sidebar_reveals_still_require_visible_unique_indented_items(self):
        case = {'path': '/19/child', 'navTargets': ['/19/parent', '/19/child']}
        record = {'url': 'https://example.org/19/child', 'documentWidth': 1440, 'viewportWidth': 1440,
                  'sidebarProbe': [
                      {'path': '/19/parent', 'visible': True, 'x': 20, 'textX': 20,
                       'measurement': 'individually_revealed'},
                      {'path': '/19/child', 'visible': True, 'x': 40, 'textX': 40,
                       'measurement': 'individually_revealed'}]}
        self.assertEqual(compare_case(case, record, origin='https://example.org'), [])
        for variant in ['hidden', 'missing', 'duplicate', 'flat', 'right_sidebar']:
            bad = copy.deepcopy(record)
            if variant == 'hidden': bad['sidebarProbe'][0]['visible'] = False
            elif variant == 'missing': bad['sidebarProbe'].pop(0)
            elif variant == 'duplicate': bad['sidebarProbe'].append(dict(bad['sidebarProbe'][0]))
            elif variant == 'flat': bad['sidebarProbe'][1]['textX'] = 20
            else: bad['sidebarProbe'][0]['x'] = 1180
            self.assertIn('sidebar', compare_case(case, bad, origin='https://example.org'), variant)

    def test_authored_links_include_autolinks_reference_uses_and_html(self):
        text = '[a][ref] [b][ref]\n\n[ref]: target.md#T\n\n<https://example.org/>\n<a href="x.md">x</a>\n'
        self.assertCountEqual(authored_links(text), ['target.md#T', 'target.md#T', 'https://example.org/', 'x.md'])

    def test_examples_and_inline_code_never_become_authored_links(self):
        text = '```md\n[x](bad.md)\n```\n\n<pre><a href="bad.md">x</a></pre>\n\n`[x](bad.md)`\n[x](ok.md)'
        self.assertEqual(authored_links(text), ['ok.md'])

    def test_leading_inline_identifiers_do_not_hide_prose_links(self):
        text = '`isn` prose [table](isn.md#ISN-FUNCTIONS). More `isn`.\n\n' \
               '[`IMPORT FOREIGN SCHEMA`](command.md) and <a href="api.md"><code>api()</code></a>'
        self.assertCountEqual(authored_links(text), ['isn.md#ISN-FUNCTIONS', 'command.md', 'api.md'])

    def test_html_code_context_and_literal_html_in_inline_examples(self):
        text = '<code>[example](hidden.md)</code> [visible](ok.md)\n\n' \
               '`<a href="hidden.md">x</a>`\n\n<pre><code><a href="hidden.md">x</a></code></pre>'
        self.assertEqual(authored_links(text), ['ok.md'])

    def test_version_and_interface_are_explicit_per_page(self):
        result = expected_links('child.md', '[x](child.md#root)', origin='https://example.org', major=19,
                                routes={'child.md': '/19/manual/child'}, interface_links=['https://example.org/19/manual'])
        self.assertEqual(result, {'https://example.org/19/manual/child#root': 1, 'https://example.org/19/manual': 1})
        self.assertNotIn('https://example.org/19/parent#zhu-yi', result)
        with self.assertRaisesRegex(ValueError, 'observed'):
            public_url('a.md', 'unknown.md', origin='https://example.org', major=19, routes={})
        with self.assertRaisesRegex(ValueError, 'major'):
            public_url('a.md', 'a.md', origin='https://example.org', major=19, routes={'a.md': '/18/a'})

    def test_content_comparison_preserves_code_whitespace_and_table_order(self):
        c = {'name': 'a', 'path': '/19/a', 'expected': {'allCodeTexts': ['  SELECT 1;'], 'tableRows': [['A'], ['B']]}}
        r = {'url': 'https://example.org/19/a', 'documentWidth': 390, 'viewportWidth': 390,
             'allCodeTexts': ['SELECT 1;'], 'tableRows': [['B'], ['A']]}
        self.assertCountEqual(compare_case(c, r, origin='https://example.org'), ['allCodeTexts', 'tableRows'])

    def test_hash_without_target_is_failure(self):
        c = {'name': 'a', 'path': '/19/a#target', 'anchor': 'target'}
        r = {'url': 'https://example.org/19/a#target', 'documentWidth': 390, 'viewportWidth': 390,
             'idExists': False, 'anchorCount': 0, 'anchorTop': None, 'viewportHeight': 844}
        self.assertIn('direct', compare_case(c, r, origin='https://example.org'))

    def test_body_reference_cannot_be_satisfied_by_heading_selflink(self):
        c = {'name': 'a', 'path': '/19/a', 'batchTargets': [{'anchor': 'root', 'kind': 'body'}]}
        r = {'url': 'https://example.org/19/a', 'documentWidth': 390, 'viewportWidth': 390,
             'batchJumps': [{'anchor': 'root', 'clicked': True, 'hash': '#root', 'idCount': 1,
                             'targetTop': 10, 'viewportHeight': 844, 'inHeading': True}]}
        self.assertIn('body_click', compare_case(c, r, origin='https://example.org'))

    def test_incomplete_stale_and_duplicate_runs_are_rejected(self):
        bundle = {'origin': 'https://example.org', 'major': 19, 'source_commit': 'new',
                  'cases': [{'name': 'a', 'path': '/19/a'}]}
        record = {'screenshot': 'a.png', 'url': 'https://example.org/19/a', 'documentWidth': 390, 'viewportWidth': 390}
        run = {'status': 'complete', 'origin': bundle['origin'], 'major': '19', 'source_commit': 'new',
               'bundle_sha256': 'criteria', 'cases_requested': ['a'], 'results': [record]}
        self.assertTrue(check_results(bundle, [run], 'criteria')['passed'])
        for key, value in [('status', 'running'), ('source_commit', 'old'), ('bundle_sha256', 'old-criteria'), ('major', '18')]:
            bad = copy.deepcopy(run); bad[key] = value
            self.assertFalse(check_results(bundle, [bad], 'criteria')['passed'])
        self.assertFalse(check_results(bundle, [run, run], 'criteria')['passed'])

    def test_unrecognized_expectation_is_not_silently_skipped(self):
        with self.assertRaisesRegex(ValueError, 'Unknown expected'):
            compare_case({'path': '/19/a', 'expected': {'allCodTexts': []}},
                         {'url': 'https://example.org/19/a', 'documentWidth': 1, 'viewportWidth': 1}, origin='https://example.org')


if __name__ == '__main__':
    unittest.main()
