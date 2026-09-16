"""Lossless source excerpts and bounded review packets; no model or network calls."""
from html.parser import HTMLParser
import hashlib
import json
import re

VERSION = 'source-packets-v1'
DEFAULT_BUDGET = 12000


def estimate_tokens(text):
    """Scheduling heuristic, NOT billing/tokenizer output. Never truncates content."""
    ascii_count = sum(ord(c) < 128 for c in text)
    return int((ascii_count + 2) / 3 + (len(text) - ascii_count) * 1.5) + 1


class DivSpans(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text, self.stack, self.spans = text, [], []
        self.offsets = [0]
        for line in text.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.feed(text)
        self.close()

    def character_position(self):
        line, col = self.getpos()
        return self.offsets[line - 1] + col

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.stack.append((self.character_position(), dict(attrs)))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag == 'div' and self.stack:
            start, attrs = self.stack.pop()
            end = self.text.find('>', self.character_position()) + 1
            self.spans.append((start, end, attrs))


class SourceIndex:
    def __init__(self, html, originals):
        self.html = html
        self.sha256 = hashlib.sha256(html.encode('utf-8')).hexdigest()
        parsed = DivSpans(html)
        spans = parsed.spans
        content_classes = {'sect1', 'chapter', 'refentry', 'appendix', 'preface', 'part', 'book', 'reference'}
        roots = [s for s in spans if content_classes.intersection((s[2].get('class') or '').split())]
        if parsed.stack or (roots and not any(all(a <= x[0] and x[1] <= b for x in roots) for a, b, _ in roots)):
            roots = []
        self.body = min(roots, key=lambda s: (s[0], -s[1]))[:2] if roots else (0, len(html))
        self.fallback = None if roots else 'no recognized document container; full snapshot included'
        ids = {}
        for start, end, attrs in spans:
            if self.body[0] <= start < end <= self.body[1] and attrs.get('id'):
                ids.setdefault(attrs['id'], []).append(start)
        anchors, inherited = [], None
        for part in originals:
            heading = re.search(r'^#{2,6}[^\n]*\[#\]\(#([^\)]+)\)', part, re.M)
            if heading:
                inherited = heading[1]
            anchors.append(inherited)
        unique = list(dict.fromkeys(a for a in anchors if a))
        if any(len(ids.get(a, [])) != 1 for a in unique):
            self.fallback = 'ambiguous or missing heading anchor; document body included'
        starts = [ids[a][0] for a in unique if a in ids]
        if starts != sorted(set(starts)):
            self.fallback = 'heading order mismatch; document body included'
        if not unique:
            self.fallback = 'no heading anchors; document body included'
        self.ranges = {}
        self.section_keys = []
        if self.fallback:
            self.ranges['document'] = self.body
            self.section_keys = ['document'] * len(originals)
        else:
            # Include the root preamble, and partition without dropping bytes.
            starts[0] = self.body[0]
            for i, anchor in enumerate(unique):
                self.ranges[anchor] = (starts[i], starts[i + 1] if i + 1 < len(starts) else self.body[1])
            self.section_keys = [a or unique[0] for a in anchors]

    def excerpts(self, sections):
        result = []
        for key in dict.fromkeys(self.section_keys[i] for i in sections):
            start, end = self.ranges[key]
            result.append(dict(anchor=key, start_char=start, end_char=end,
                               start_line=self.html.count('\n', 0, start) + 1,
                               end_line=self.html.count('\n', 0, end) + 1,
                               html=self.html[start:end]))
        return result


def packet(index, originals, translations, ids, source, submission=None):
    return dict(version=VERSION, source=source, submission=submission, snapshot_sha256=index.sha256,
                fallback=index.fallback,
                outline=[dict(section=i, heading=next((l for l in p.splitlines() if l.startswith('#')), 'intro'))
                         for i, p in enumerate(originals)],
                sections=[dict(id=i, original=originals[i],
                               translation=None if translations[i] == originals[i] else translations[i],
                               translation_matches_original=translations[i] == originals[i]) for i in ids],
                official_excerpts=index.excerpts(ids))


def render(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def groups(index, originals, translations, ids, source, budget=DEFAULT_BUDGET, overhead=0):
    """Greedy complete sections, counting shared source excerpts once per group."""
    if budget <= 0:
        raise ValueError('budget must be positive')
    current = []
    for idx in ids:
        candidate = current + [idx]
        size = overhead + estimate_tokens(render(packet(index, originals, translations, candidate, source)))
        if current and size > budget:
            yield current
            current = [idx]
        else:
            current = candidate
    if current:
        yield current
