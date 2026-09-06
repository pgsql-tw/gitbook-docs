"""Replace PostgreSQL manual hyperlinks with GitBook-relative links.

Only Markdown and HTML hyperlinks are changed. URLs in code fences, prose, and
external destinations remain untouched. A link is rewritten only when its page
is represented by a path in the branch-15 import map.
"""
import hashlib
import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / 'outputs/pg15-fill/plan.json'
REPORT = Path(__file__).resolve().parent / 'manual-link-rewrite.json'
HOST = 'www.postgresql.org'
VERSIONS = {'current', 'devel', '10', '11', '12', '13', '14', '15'}

nodes = json.loads(PLAN.read_text(encoding='utf-8'))['nodes']
pages = {node['page']: node['path'] for node in nodes}
sources = {node['path']: node['page'] for node in nodes}

def internal(destination: str, source: Path) -> str | None:
    u = urlsplit(destination)
    if u.scheme not in {'http', 'https'} or u.netloc != HOST:
        return None
    m = re.fullmatch(r'/docs/([^/]+)/(.+)', u.path)
    if not m or m[1] not in VERSIONS or m[2] not in pages:
        return None
    target = ROOT / pages[m[2]]
    relative = os.path.relpath(target, source.parent).replace('\\', '/')
    return relative + (f'#{u.fragment}' if u.fragment else '')

# Markdown inline links and HTML href attributes. Capture only destinations;
# this intentionally leaves raw URLs and code examples as historical source.
MARKDOWN = re.compile(r'(?P<prefix>\]\()(?P<url>https?://www\.postgresql\.org/docs/[^)\s]+)(?P<suffix>\))')
HTML = re.compile(r'(?P<prefix>\bhref=["\'])(?P<url>https?://www\.postgresql\.org/docs/[^"\']+)(?P<suffix>["\'])')

report = {'files_changed': 0, 'links_rewritten': 0, 'unmapped_official_pages': {}, 'files': []}
for path in sorted(ROOT.rglob('*.md')):
    if '.git' in path.parts or 'outputs' in path.parts:
        continue
    original = path.read_text(encoding='utf-8-sig')
    text = original
    # Imported pages carry a source citation. It is deliberately external:
    # it documents the exact upstream page rather than navigating the book.
    relpath = path.relative_to(ROOT).as_posix()
    if relpath in sources:
        pattern = re.compile(r'(\[PostgreSQL 15\.19 Documentation\]\()[^)]+(\))')
        text, restored = pattern.subn(r'\1' + 'https://www.postgresql.org/docs/15/' + sources[relpath] + r'\2', text)
        if restored and text != original:
            report.setdefault('source_citations_restored', 0)
            report['source_citations_restored'] += restored
    replaced = [0]
    def change(m):
        line_start = text.rfind('\n', 0, m.start()) + 1
        if '[PostgreSQL 15.19 Documentation]' in text[line_start:m.start()]:
            return m.group(0)
        value = internal(m['url'], path)
        if value is None:
            u = urlsplit(m['url'])
            mm = re.fullmatch(r'/docs/([^/]+)/(.+)', u.path)
            if mm and mm[1] in VERSIONS:
                report['unmapped_official_pages'][mm[2]] = report['unmapped_official_pages'].get(mm[2], 0) + 1
            return m.group(0)
        replaced[0] += 1
        return m['prefix'] + value + m['suffix']
    output = HTML.sub(change, MARKDOWN.sub(change, text))
    if output != original:
        path.write_text(output, encoding='utf-8')
        report['files_changed'] += 1
        report['links_rewritten'] += replaced[0]
        report['files'].append({'path': path.relative_to(ROOT).as_posix(), 'links': replaced[0],
                                'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})

REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: report[k] for k in ('files_changed', 'links_rewritten')}, ensure_ascii=False))
print('Unmapped official pages:', len(report['unmapped_official_pages']))
