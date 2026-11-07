"""Regression checks for false alignment and partial-change coverage."""
import unittest
from revision_review_packets import Terms, spans, covered

class Boundaries(unittest.TestCase):
    def test_non_definition_anchor_ends_unit(self):
        text='<a id="OPT"></a>\n`opt`\n:   translated\n\n<a id="TABLE"></a>\ntable explanation\n'
        units=spans(text,[dict(anchor='OPT')])
        self.assertEqual(text[units[0]['start']:units[0]['end']],text[:text.index('<a id="TABLE"')])
        self.assertFalse(covered(text.index('table explanation'),len(text),units))

    def test_heading_ends_last_unit(self):
        text='<a id="OPT"></a>\n`opt`\n:   translated\n\n## Notes\nother prose\n'
        units=spans(text,[dict(anchor='OPT')])
        self.assertEqual(units[0]['end'],text.index('## Notes'))

    def test_partial_overlap_is_unresolved(self):
        self.assertFalse(covered(3,12,[dict(start=0,end=8)]))
        self.assertFalse(covered(0,12,[dict(start=0,end=5),dict(start=6,end=12)]))
        self.assertTrue(covered(0,12,[dict(start=0,end=5),dict(start=5,end=12)]))

    def test_complete_source_entry_keeps_exception(self):
        html='<dl><dt id="OPT">opt</dt><dd><p>condition</p><p>exception</p></dd></dl>'
        entry=Terms(html).entries[0]
        self.assertEqual(html[entry['start']:entry['end']],'<dt id="OPT">opt</dt><dd><p>condition</p><p>exception</p></dd>')

if __name__=='__main__': unittest.main()
