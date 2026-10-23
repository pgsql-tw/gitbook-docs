"""Lossless, ID-aligned four-column packets for the supported SQL feature table.

Only presentation changes: no candidate bytes or review requirements are changed.
"""
from html.parser import HTMLParser
import hashlib
import re

VERSION = 'feature-row-packets-v1'
PAGE = 'appendixes/features/features-sql-standard.md'


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


class CellText(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.data = []
        self.feed(text)

    def handle_data(self, text):
        self.data.append(text)


def split_table(text):
    tables = [m for m in re.finditer(r'<table\b[^>]*>.*?</table>', text, re.S | re.I)
              if re.search(r'\bE091-06\b', m[0])]
    if len(tables) != 1:
        raise ValueError('Expected exactly one supported-features table')
    table = tables[0]
    rows, gaps, cursor = [], [], 0
    for row in re.finditer(r'<tr\b[^>]*>.*?</tr>', table[0], re.S | re.I):
        gaps.append(table[0][cursor:row.start()])
        cells = []
        for cell in re.finditer(r'<t[dh]\b[^>]*>(.*?)</t[dh]>', row[0], re.S | re.I):
            parser = CellText(cell[1])
            cells.append(re.sub(r'\s+', ' ', ''.join(parser.data)).strip())
        if len(cells) != 4:
            raise ValueError('Feature table row must have exactly four cells')
        rows.append(dict(cells=cells, raw_html=row[0]))
        cursor = row.end()
    gaps.append(table[0][cursor:])
    if not rows:
        raise ValueError('Empty feature table')
    rebuilt = ''.join(gaps[i] + r['raw_html'] for i, r in enumerate(rows)) + gaps[-1]
    if rebuilt != table[0]:
        raise ValueError('Lossless table reconstruction failed')
    ids = [r['cells'][0] for r in rows[1:]]
    if any(not re.fullmatch(r'[A-Z]\d{3}(?:-\d+)?', value) for value in ids):
        raise ValueError('Unrecognized feature ID')
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate feature ID')
    return dict(before=text[:table.start()], after=text[table.end():],
                gaps=gaps, header=rows[0], rows=rows[1:], ids=ids,
                document_sha256=sha(text), table_sha256=sha(table[0]))


def build(original, translation, official_body, rows_per_packet=40):
    if type(rows_per_packet) is not int or rows_per_packet < 1:
        raise ValueError('Invalid rows-per-packet')
    docs = {name: split_table(value) for name, value in (
        ('original', original), ('translation', translation), ('official', official_body))}
    expected = docs['official']['ids']
    if any(d['ids'] != expected for d in docs.values()):
        raise ValueError('Feature IDs or order differ across original, candidate and official source')
    manifest = dict(version=VERSION, feature_count=len(expected), ids=expected,
                    document_sha256={k:d['document_sha256'] for k,d in docs.items()},
                    table_sha256={k:d['table_sha256'] for k,d in docs.items()})
    units = [dict(unit=0, kind='prose_headers_and_table_structure',
                  documents={k:{field:d[field] for field in ('before','after','gaps','header')}
                             for k,d in docs.items()})]
    covered = []
    for start in range(0, len(expected), rows_per_packet):
        stop = min(start + rows_per_packet, len(expected))
        ids = expected[start:stop]
        units.append(dict(unit=len(units), kind='feature_rows', first_row=start+1,
                          last_row=stop, ids=ids,
                          rows=[dict(id=expected[i], ordinal=i+1,
                                     **{k:d['rows'][i] for k,d in docs.items()})
                                for i in range(start,stop)]))
        covered.extend(ids)
    if covered != expected or len(covered) != len(set(covered)):
        raise ValueError('Incomplete or duplicate packet coverage')
    return manifest, units
