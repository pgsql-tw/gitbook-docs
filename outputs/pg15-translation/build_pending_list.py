"""Build a conservative queue of imported PostgreSQL 15 pages needing translation."""
from collections import defaultdict
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
plan = json.loads((ROOT / 'outputs/pg15-fill/plan.json').read_text(encoding='utf-8'))
groups = defaultdict(list)
for node in plan['nodes']:
    if node['action'] == 'preserve':
        continue
    path = ROOT / node['path']
    text = path.read_text(encoding='utf-8-sig')
    prose = re.sub(r'```.*?```', '', text, flags=re.S)
    prose = re.sub(r'<[^>]+>|`[^`]*`|\[[^]]*\]\([^)]*\)', '', prose)
    english = len(re.findall(r'\b[A-Za-z]{2,}\b', prose))
    han = len(re.findall(r'[\u4e00-\u9fff]', prose))
    if english <= han:
        continue
    groups[node['path'].split('/')[0]].append((english, node['path'], node['title']))

lines = [
    '# 待翻譯頁面清單',
    '',
    '依 PostgreSQL 15.19 匯入頁面的中英文文字比例產生。程式碼、HTML 標籤、連結文字不列入統計；此清單是翻譯排程，不是內容正確性或版本審校的判定。',
    '',
    f'待譯頁面：{sum(map(len, groups.values()))}。每一頁完成翻譯後，重新執行本程式以更新清單。',
    '',
]
for group in sorted(groups):
    lines += [f'## {group}', '']
    for words, path, title in sorted(groups[group], key=lambda x: (x[0], x[1])):
        lines.append(f'- [ ] `{path}` — {title}（約 {words} 個英文字詞）')
    lines.append('')
(ROOT / 'outputs/pg15-translation/pending-pages.md').write_text('\n'.join(lines), encoding='utf-8')
print(sum(map(len, groups.values())))
