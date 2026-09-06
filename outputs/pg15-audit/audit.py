"""Inventory GitBook and cache PostgreSQL 15 chapter TOCs; stdlib only.

Run from the repository root: python outputs/pg15-audit/audit.py [--fetch]
Language flags are triage heuristics, never translation-completion scores.
"""
import csv
import json
import re
import sys
import subprocess
from datetime import datetime, timezone
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BASE = 'https://www.postgresql.org/docs/15/'

class TocParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.link = None
        self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'div':
            if self.depth:
                self.depth += 1
            elif 'toc' in a.get('class', '').split():
                self.depth = 1
        if self.depth and tag == 'a':
            self.link = [a.get('href', ''), '']
    def handle_data(self, data):
        if self.link is not None:
            self.link[1] += data
    def handle_endtag(self, tag):
        if tag == 'a' and self.link is not None:
            self.links.append(dict(zip(('href', 'title'), self.link)))
            self.link = None
        if tag == 'div' and self.depth:
            self.depth -= 1

def fetch(page):
    with urllib.request.urlopen(BASE + page, timeout=45) as response:
        raw = response.read().decode('utf-8')
    p = TocParser()
    p.feed(raw)
    return {'page': page, 'title': re.search(r'<title>(.*?)</title>', raw, re.S)[1], 'toc': p.links}

if '--fetch' in sys.argv:
    index = fetch('index.html')
    pages = sorted({x['href'].split('#')[0] for x in index['toc'] if x['href'].endswith('.html')})
    with ThreadPoolExecutor(max_workers=6) as pool:
        chapters = list(pool.map(fetch, pages))
    (OUT / 'official-toc.json').write_text(json.dumps({'base': BASE, 'fetched_at': datetime.now(timezone.utc).isoformat(), 'index': index, 'chapters': chapters}, ensure_ascii=False, indent=2), encoding='utf-8')

entries = []
part = chapter = ''
for line_no, line in enumerate((ROOT / 'SUMMARY.md').read_text(encoding='utf-8-sig').splitlines(), 1):
    m = re.match(r'(\s*)\* \[(.*?)\]\((.*?)\)', line)
    if not m:
        continue
    indent, title, path = m.groups()
    title, path = title.replace('\\_', '_'), path.replace('\\_', '_')
    level = len(indent) // 2
    if level == 0:
        part, chapter = title, title
    elif level == 1:
        chapter = title
    entries.append(dict(line=line_no, level=level, part=part, chapter=chapter, title=title, path=path))

for i, e in enumerate(entries):
    p = ROOT / e['path']
    e['exists'] = p.is_file()
    text = p.read_text(encoding='utf-8-sig') if p.is_file() else ''
    body = re.sub(r'\A---\n.*?\n---\n', '', text, flags=re.S)
    body = re.sub(r'^#+ .*$', '', body, flags=re.M)
    e['has_children'] = i + 1 < len(entries) and entries[i+1]['level'] > e['level']
    e['body_chars'] = len(body.strip())
    prose = re.sub(r'```.*?```', '', body, flags=re.S)
    prose = re.sub(r'`[^`]*`|https?://[^\s)]+|\{%.*?%\}', '', prose)
    e['han_chars'] = len(re.findall(r'[\u4e00-\u9fff]', prose))
    e['latin_words'] = len(re.findall(r'\b[A-Za-z]{2,}\b', prose))
    english_paragraphs = [p for p in re.split(r'\n\s*\n', prose) if len(re.findall(r'\b[A-Za-z]{2,}\b', p)) >= 20 and not re.search(r'[\u4e00-\u9fff]', p)]
    e['english_blocks'] = len(english_paragraphs)
    e['status'] = ('missing-file' if not e['exists'] else
                   'heading-only-container' if not e['body_chars'] and e['has_children'] else
                   'heading-only-leaf' if not e['body_chars'] else
                   'no-chinese-prose' if not e['han_chars'] else
                   'mixed-review' if english_paragraphs else 'chinese-review')
    e['source_versions'] = ','.join(sorted(set(re.findall(r'postgresql\.org/docs/([^/]+)/', text))))

with (OUT / 'inventory.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(entries[0]))
    w.writeheader()
    w.writerows(entries)
listed = {e['path'] for e in entries}
tracked = __import__('subprocess').check_output(['git', 'ls-files', '*.md'], cwd=ROOT, text=True).splitlines()
summary = {'entries': len(entries), 'unique_paths': len(listed), 'statuses': dict(Counter(e['status'] for e in entries)),
           'unlisted_markdown': [p for p in tracked if p not in listed and p != 'SUMMARY.md'],
           'parts': {part: dict(Counter(e['status'] for e in entries if e['part'] == part)) for part in dict.fromkeys(e['part'] for e in entries)}}
(OUT / 'inventory-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
