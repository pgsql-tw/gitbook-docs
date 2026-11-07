"""Build a labelled evaluation set for local advisory screening from real Codex rejections.

Unit = one heading section (translation_pipeline.parts). Labels come from history, not
from the model designer:
  positive      Codex cited a semantic problem in Section N of a rejected submission.
  hard negative Section N of the *next* submission of the same page, after the fix,
                which Codex then accepted (published, or rejected without citing N).
  easy negative Sections of published submissions that never received a semantic citation.
Split is by page (hash), so no page appears in both dev and held-out.
No model or network calls; read-only on agent history.
"""
import collections, glob, hashlib, json, random, re, sys
from pathlib import Path
from pg_project import translation_path
sys.path.insert(0, 'scripts')
from translation_pipeline import parts
from translation_packets import estimate_tokens

ROOT = translation_path(Path.cwd(), 'agents/inbox/claude')
OUT = Path('outputs/local-review-screening')
MAX_TOKENS = 9000           # heuristic estimate of en+zh; server runs with 16K context
PER_PAGE_POS = 3            # cap so a few pages with many rounds do not dominate
EASY_NEG = 60
CATS = [('meta', r'頁尾|核對日期|provenance|擷取|原文版本|來源快照|版本標示'),
        ('anchor', r'錨點|anchor|\bid\b'),
        ('untranslated', r'未翻譯|仍保留英文|未完整翻譯|保留英文'),
        ('terminology', r'術語|專案用語|一致')]

def category(msg):
    for name, pat in CATS:
        if re.search(pat, msg, re.I):
            return name
    return 'semantic'

def read(p):
    return Path(p).read_text(encoding='utf-8-sig').replace('\r\n', '\n')

def split_of(page):
    return 'dev' if int(hashlib.sha256(page.encode()).hexdigest(), 16) % 10 < 3 else 'heldout'

def main():
    manifests = {}
    for f in glob.glob(str(translation_path(Path.cwd(), 'pipeline-runtime/pages/*/manifest.json'))):
        m = json.loads(read(f))
        if m.get('page') and m.get('baseline'):
            prev = manifests.get(m['page'])
            if not prev or Path(f).stat().st_mtime > prev[0]:
                manifests[m['page']] = (Path(f).stat().st_mtime, m['baseline'])
    subs = collections.defaultdict(list)
    for kind in ('_rejected', '_published'):
        for d in (ROOT / kind).iterdir():
            if (d / 'page.md').exists() and (d / 'result.json').exists():
                slug, ts = d.name.rsplit('--', 1)
                res = json.loads(read(d / 'result.json'))
                subs[res.get('page') or slug.replace('__', '/')].append(dict(ts=ts, kind=kind, dir=d, res=res))
    items, stats = [], collections.Counter()
    cited_pages_sections = collections.defaultdict(set)
    for page, lst in subs.items():
        lst.sort(key=lambda s: s['ts'])
        if page not in manifests:
            stats['no_manifest_page'] += 1; continue
        en = parts(manifests[page][1])
        pos_count = 0
        for i, s in enumerate(lst):
            if s['kind'] != '_rejected' or s['res'].get('by') != 'codex':
                continue
            cited = collections.defaultdict(list)
            for e in s['res']['errors']:
                m = re.match(r'Section (\d+):\s*(.*)', e, re.S)
                if m:
                    stats['cat_' + category(m[2])] += 1
                    cited[int(m[1])].append((category(m[2]), m[2]))
                    cited_pages_sections[page].add(int(m[1]))
            zh = parts(read(s['dir'] / 'page.md'))
            if len(zh) != len(en):
                stats['section_count_mismatch'] += 1; continue
            nxt = lst[i + 1] if i + 1 < len(lst) else None
            nzh = parts(read(nxt['dir'] / 'page.md')) if nxt else None
            for n, msgs in sorted(cited.items()):
                sem = [m for c, m in msgs if c == 'semantic']
                if not sem or n >= len(en):
                    continue
                if estimate_tokens(en[n] + zh[n]) > MAX_TOKENS:
                    stats['too_long'] += 1; continue
                if pos_count >= PER_PAGE_POS:
                    stats['page_cap'] += 1; continue
                pos_count += 1
                pid = f'{page}#{n}@{s["ts"]}'
                items.append(dict(id=pid, label=1, kind='positive', page=page, section=n, en=en[n], zh=zh[n],
                                  gold=sem, other_cited=[m for c, m in msgs if c != 'semantic'], submission=str(s['dir'])))
                # Hard negative: the fixed text of the same section, accepted at the next review.
                if nzh and len(nzh) == len(en) and nzh[n] != zh[n]:
                    ncited = {int(m[1]) for e in nxt['res'].get('errors', []) for m in [re.match(r'Section (\d+):', e)] if m}
                    if nxt['kind'] == '_published' or (nxt['res'].get('by') == 'codex' and n not in ncited):
                        items.append(dict(id=f'{page}#{n}@{nxt["ts"]}', label=0, kind='hard_negative', pair=pid, page=page,
                                          section=n, en=en[n], zh=nzh[n], submission=str(nxt['dir'])))
    # Easy negatives: published sections on pages with no semantic citation in that section ever.
    random.seed(20261011)
    pool = []
    for page, lst in subs.items():
        pub = [s for s in lst if s['kind'] == '_published']
        if not pub or page not in manifests:
            continue
        s = pub[-1]; en = parts(manifests[page][1]); zh = parts(read(s['dir'] / 'page.md'))
        if len(zh) != len(en):
            continue
        for n in range(len(en)):
            if n in cited_pages_sections[page] or zh[n] == en[n] or len(en[n]) < 400:
                continue
            if estimate_tokens(en[n] + zh[n]) <= MAX_TOKENS:
                pool.append(dict(id=f'{page}#{n}@{s["ts"]}', label=0, kind='easy_negative', page=page, section=n,
                                 en=en[n], zh=zh[n], submission=str(s['dir'])))
    items += random.sample(pool, min(EASY_NEG, len(pool)))
    for it in items:
        it['split'] = split_of(it['page'])
    OUT.mkdir(parents=True, exist_ok=True)
    for split in ('dev', 'heldout'):
        with open(OUT / f'{split}.jsonl', 'w', encoding='utf-8') as f:
            for it in items:
                if it['split'] == split:
                    f.write(json.dumps(it, ensure_ascii=False) + '\n')
    summary = dict(stats=stats, counts={f'{sp}/{k}': sum(1 for i in items if i['split'] == sp and i['kind'] == k)
                                       for sp in ('dev', 'heldout') for k in ('positive', 'hard_negative', 'easy_negative')},
                   pages={sp: len({i['page'] for i in items if i['split'] == sp}) for sp in ('dev', 'heldout')})
    (OUT / 'dataset-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
