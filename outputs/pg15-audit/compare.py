"""Compare chapter and immediate-section structure, preserving uncertainty."""
import csv
import json
import re
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
data = json.loads((OUT / 'official-toc.json').read_text(encoding='utf-8'))
entries = list(csv.DictReader((OUT / 'inventory.csv').open(encoding='utf-8-sig')))
def norm(s):
    s = re.sub(r'^(?:\d+(?:\.\d+)*|[A-Z](?:\.\d+)*)\.?\s+', '', s)
    return re.sub(r'[^a-z0-9]', '', s.lower())
def num(s):
    m = re.match(r'(\d+|[A-Z])\.', s)
    return m[1] if m else None

rows = []
for top in data['index']['toc']:
    n = num(top['title'])
    # Preface has numbered sections 1–5 too; only root titles without a dot subdivision.
    if not n or top['href'] in ['intro-whatis.html', 'history.html', 'notation.html', 'resources.html', 'bug-reporting.html']:
        continue
    local = next((e for e in entries if e['level'] == '1' and num(e['title']) == n and ((n.isdigit() and e['part'] != '前言') or (not n.isdigit() and e['part'].startswith('VIII.')))), None)
    if not local:
        continue
    chapter = next(c for c in data['chapters'] if c['page'] == top['href'])
    children = [e for e in entries if e['chapter'] == local['chapter'] and e['level'] == '2']
    official = [x for x in chapter['toc'] if re.match(r'^'+re.escape(n)+r'\.\d+\.\s', x['title'])]
    used = set()
    pending = []
    for x in official:
        hit = next((e for e in children if e['path'] not in used and (norm(e['title']) == norm(x['title']) or norm(Path(e['path']).stem) == norm(x['title']))), None)
        if hit:
            used.add(hit['path'])
            rows.append(dict(chapter=local['chapter'], official=x['title'], url=data['base']+x['href'], local=hit['path'], local_title=hit['title'], match='title/path'))
        else:
            pending.append(x)
    for x in pending:
        # Existing English object names under another chapter indicate reorganization.
        relocated = next((e for e in entries if e['path'] not in used and norm(e['title']) == norm(x['title'])), None) if 'pg_' in x['title'] else None
        if relocated:
            rows.append(dict(chapter=local['chapter'], official=x['title'], url=data['base']+x['href'], local=relocated['path'], local_title=relocated['title'], match='other-chapter-review'))
            continue
        suffix = re.match(r'^\w+\.(\d+)', x['title'])[1]
        hit = next((e for e in children if e['path'] not in used and re.match(r'^\w+\.'+suffix+r'\.', e['title']) and re.search(r'[\u4e00-\u9fff]', e['title'])), None)
        if hit:
            used.add(hit['path'])
        rows.append(dict(chapter=local['chapter'], official=x['title'], url=data['base']+x['href'], local=hit['path'] if hit else '', local_title=hit['title'] if hit else '', match='number-only-review' if hit else 'unmapped-review'))

# SQL and command reference names are stable, so exact normalized title matching is useful.
for page, folder in [('sql-commands.html','reference/sql-commands/'), ('reference-client.html','reference/client-applications/'), ('reference-server.html','reference/server-applications/')]:
    chapter = next(c for c in data['chapters'] if c['page'] == page)
    local = [e for e in entries if e['path'].startswith(folder)]
    for x in chapter['toc']:
        if '#' in x['href']:
            continue
        hit = next((e for e in local if norm(e['title']) == norm(x['title'])), None)
        rows.append(dict(chapter=page, official=x['title'], url=data['base']+x['href'], local=hit['path'] if hit else '', local_title=hit['title'] if hit else '', match='title/path' if hit else 'unmapped-review'))
with (OUT/'section-comparison.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
lines=['# 官方直接子節比對候選清單', '', '以 2026-09-06 下載的 PostgreSQL 15.19 目錄比對。只列章的直接子節及 Reference 指令；不是全文差異。', '', '「未映射」不直接等於缺譯：可能併在父頁、譯名不同或編號移位。number-only-review 只按編號推定，須逐節核對。詳見 section-comparison.csv。', '']
for chapter in dict.fromkeys(r['chapter'] for r in rows):
    missing=[r for r in rows if r['chapter']==chapter and r['match']=='unmapped-review']
    if missing:
        lines += ['## '+chapter, ''] + ['- ['+r['official']+']('+r['url']+')' for r in missing]+['']
(OUT/'unmapped-sections.md').write_text('\n'.join(lines),encoding='utf-8')
stats=[]
for e in entries:
    if e['level'] != '1':
        continue
    descendants=[x for x in entries if x['chapter']==e['chapter']]
    counts=Counter(x['status'] for x in descendants)
    stats.append(dict(chapter=e['chapter'], path=e['path'], pages=len(descendants), **{k:counts[k] for k in ['heading-only-leaf','heading-only-container','no-chinese-prose','mixed-review','chinese-review']}))
with (OUT/'chapter-inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(stats[0])); w.writeheader(); w.writerows(stats)
print(Counter(r['match'] for r in rows))
print('Unmapped candidates by chapter:', Counter(r['chapter'] for r in rows if r['match']=='unmapped-review'))
