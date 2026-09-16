import unittest
from translation_packets import SourceIndex, packet, groups


class Tests(unittest.TestCase):
    def setUp(self):
        self.parts = ['## Page [#](#ROOT)\nIntro', '### First [#](#ONE)\nTable', '### Warning\nDanger', '### Next [#](#TWO)\nExample']
        self.body = ('<div class="sect1" id="ROOT"><p>Intro &amp; conditions</p>'
                     '<div class="sect2" id="ONE"><table><tr><td>ALL DATA</td></tr></table>'
                     '<div class="warning"><p>Never omit this warning.</p></div></div>'
                     '<div class="sect2" id="TWO"><pre>SELECT 1;\n-- comment</pre></div></div>')
        self.html = '<nav>UNRELATED NAV</nav>' + self.body + '<footer>UNRELATED FOOTER</footer>'

    def test_lossless_body_without_navigation(self):
        index = SourceIndex(self.html, self.parts)
        self.assertIsNone(index.fallback)
        snippets = index.excerpts(range(4))
        self.assertEqual(''.join(s['html'] for s in snippets), self.body)
        for s in snippets:
            self.assertEqual(s['html'], self.html[s['start_char']:s['end_char']])
        self.assertEqual(len(snippets), 3)

    def test_unanchored_warning_uses_parent_source(self):
        index = SourceIndex(self.html, self.parts)
        self.assertEqual(index.section_keys[1], index.section_keys[2])
        self.assertIn('Never omit', index.excerpts([2])[0]['html'])
        self.assertIn('<table>', index.excerpts([1])[0]['html'])

    def test_missing_anchor_falls_back_to_whole_body(self):
        index = SourceIndex(self.html, self.parts + ['### Missing [#](#MISSING)'])
        self.assertIsNotNone(index.fallback)
        self.assertEqual(index.excerpts([4])[0]['html'], self.body)

    def test_unknown_container_uses_full_snapshot(self):
        index = SourceIndex('<article>Keep everything</article>', self.parts)
        self.assertEqual(index.excerpts([0])[0]['html'], index.html)

    def test_multiple_roots_do_not_drop_siblings(self):
        html = '<div class="sect1" id="A">one</div><div class="sect1" id="B">two</div>'
        index = SourceIndex(html, ['## A [#](#A)', '### B [#](#B)'])
        self.assertIsNotNone(index.fallback)
        self.assertEqual(index.excerpts([0])[0]['html'], html)

    def test_unclosed_container_falls_back(self):
        html = '<div class="sect1">before<div class="sect1" id="ROOT">child</div>'
        index = SourceIndex(html, self.parts)
        self.assertEqual(index.excerpts([0])[0]['html'], html)

    def test_duplicate_anchor_falls_back(self):
        html = self.html.replace('<p>Intro', '<div id="ONE"></div><p>Intro')
        self.assertIsNotNone(SourceIndex(html, self.parts).fallback)

    def test_groups_cover_every_section_once(self):
        index = SourceIndex(self.html, self.parts)
        result = list(groups(index, self.parts, self.parts, list(range(4)), {}, budget=250))
        self.assertEqual([i for group in result for i in group], list(range(4)))
        self.assertGreater(len(result), 1)
        self.assertEqual(list(groups(index, self.parts, self.parts, list(range(4)), {}, budget=10000)), [[0, 1, 2, 3]])

    def test_oversize_section_is_never_truncated(self):
        index = SourceIndex(self.html, self.parts)
        result = list(groups(index, self.parts, self.parts, [0], {}, budget=1))
        self.assertEqual(result, [[0]])
        self.assertEqual(packet(index, self.parts, self.parts, result[0], {})['sections'][0]['original'], self.parts[0])

    def test_unchanged_draft_is_not_repeated(self):
        index = SourceIndex(self.html, self.parts)
        section = packet(index, self.parts, self.parts, [0], {})['sections'][0]
        self.assertTrue(section['translation_matches_original'])
        self.assertIsNone(section['translation'])


if __name__ == '__main__':
    unittest.main()
