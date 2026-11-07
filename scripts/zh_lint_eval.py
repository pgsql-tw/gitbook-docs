"""Test plan T2-T5 for zh_lint against Codex review history. Read-only; resumable.

  python scripts/zh_lint_eval.py run [--budget SECONDS]   # lint submissions into cache (repeat until done)
  python scripts/zh_lint_eval.py score                     # compute metrics + FP sample
"""
import argparse, collections, glob, json, os, random, re, sys, time
from pathlib import Path
from pg_project import translation_path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import zh_lint

CATS = [('meta', r'頁尾|核對日期|provenance|擷取|原文版本|來源快照|版本標示'),
        ('untranslated', r'未翻譯|仍保留英文|未完整翻譯|保留英文'),
        ('anchor', r'錨點|anchor'),
        ('terminology', r'術語|專案用語')]


def category(msg):
    for name, pat in CATS:
        if re.search(pat, msg, re.I):
            return name
    return 'semantic'

INBOX = translation_path(Path.cwd(), 'agents/inbox/claude')
OUT = Path('outputs/zh-lint')
CACHE = OUT / 'cache.jsonl'
SPLIT = '2026-09-24'          # dev <= 2026-09-23 < held-out
CAT_PREFIX = {'meta': 'footer.', 'anchor': 'anchor.', 'untranslated': 'untranslated.', 'terminology': 'term.'}


def read(p):
    return Path(p).read_text(encoding='utf-8-sig').replace('\r\n', '\n')


def manifests():
    path = OUT / 'manifest-index.json'
    if path.exists():
        return json.loads(read(path))
    idx = {}
    for f in glob.glob(str(translation_path(Path.cwd(), 'pipeline-runtime/pages/*/manifest.json'))):
        try:
            m = json.loads(read(f))
        except Exception:
            continue
        src = os.path.join(os.path.dirname(f), 'draft', 'source.html')
        if not m.get('page') or not os.path.exists(src):
            continue
        s = m.get('source')
        s = json.loads(s) if isinstance(s, str) else (s or {})
        t = os.path.getmtime(f)
        if m['page'] not in idx or t > idx[m['page']]['t']:
            idx[m['page']] = dict(t=t, manifest=f, source=src, snapshot=(s.get('retrieved') or '')[:10])
    path.write_text(json.dumps(idx), encoding='utf-8')
    return idx


def submissions():
    subs = []
    for kind in ('_rejected', '_published'):
        for d in sorted((INBOX / kind).iterdir()):
            if (d / 'page.md').exists() and (d / 'meta.json').exists() and (d / 'result.json').exists():
                meta = json.loads(read(d / 'meta.json'))
                res = json.loads(read(d / 'result.json'))
                subs.append(dict(dir=str(d), kind=kind, page=meta.get('page') or res.get('page'),
                                 ts=d.name.rsplit('--', 1)[1], res=res))
    return subs


def run(args):
    OUT.mkdir(parents=True, exist_ok=True)
    idx = manifests()
    done = set()
    if CACHE.exists():
        done = {json.loads(l)['dir'] for l in open(CACHE, encoding='utf-8')}
    t0, n = time.monotonic(), 0
    baselines = {}
    with open(CACHE, 'a', encoding='utf-8') as f:
        for s in submissions():
            if s['dir'] in done:
                continue
            if time.monotonic() - t0 > args.budget:
                break
            info = idx.get(s['page'])
            if info and s['page'] not in baselines:
                baselines[s['page']] = json.loads(read(info['manifest'])).get('baseline')
            d = Path(s['dir'])
            started = time.monotonic()
            findings = zh_lint.lint(read(d / 'page.md'), json.loads(read(d / 'meta.json')),
                                    baselines.get(s['page']), read(info['source']) if info else None,
                                    info['snapshot'] if info else None)
            f.write(json.dumps(dict(dir=s['dir'], seconds=round(time.monotonic() - started, 3), has_source=bool(info),
                                    findings=findings), ensure_ascii=False) + '\n')
            n += 1
    total = len(submissions())
    print(json.dumps(dict(linted_now=n, cached=len(done) + n, total=total)))


def score(args):
    cache = {}
    for l in open(CACHE, encoding='utf-8'):
        r = json.loads(l); cache[r['dir']] = r
    subs = submissions()
    by_page = collections.defaultdict(list)
    for s in subs:
        by_page[s['page']].append(s)
    for v in by_page.values():
        v.sort(key=lambda s: s['ts'])
    # ---- T2 recall + T4 resolution
    t2 = collections.defaultdict(lambda: collections.Counter())
    misses, caught_examples = collections.defaultdict(list), []
    for page, lst in by_page.items():
        for i, s in enumerate(lst):
            if s['kind'] != '_rejected' or s['res'].get('by') != 'codex' or s['dir'] not in cache:
                continue
            fs = cache[s['dir']]['findings']
            nxt = lst[i + 1] if i + 1 < len(lst) else None
            for e in s['res']['errors']:
                m = re.match(r'Section (\d+):\s*(.*)', e, re.S)
                if not m:
                    continue
                cat = category(m[2])
                if cat not in CAT_PREFIX:
                    continue
                sec = int(m[1]); split = 'dev' if s['res']['at'][:10] < SPLIT else 'heldout'
                key = f'{split}/{cat}'
                pre = CAT_PREFIX[cat]
                hit = [f for f in fs if f['check'].startswith(pre) and f['level'] == 'error' and (cat == 'meta' or f['section'] == sec)]
                warn_hit = [f for f in fs if f['check'].startswith(pre) and f['level'] == 'warn' and (cat == 'meta' or f['section'] == sec)]
                any_hit = [f for f in fs if f['level'] == 'error' and f['section'] == sec]
                t2[key]['total'] += 1
                t2[key]['caught'] += bool(hit)
                t2[key]['caught_incl_warn'] += bool(hit or warn_hit)
                t2[key]['any_error_same_section'] += bool(any_hit)
                if hit:
                    caught_examples.append(dict(split=split, cat=cat, reason=m[2][:120], finding=hit[0]['msg'][:120]))
                    if nxt and nxt['dir'] in cache:
                        still = [f for f in cache[nxt['dir']]['findings'] if f['check'] == hit[0]['check'] and f['level'] == 'error'
                                 and (cat == 'meta' or f['section'] == sec)]
                        t2[key]['next_available'] += 1
                        t2[key]['resolved_next'] += not still
                else:
                    misses[key].append(dict(reason=m[2][:160], warn=[w['msg'][:80] for w in warn_hit][:2], dir=s['dir'][-60:]))
    recall = {k: dict(v, recall=round(v['caught'] / v['total'], 3), recall_incl_warn=round(v['caught_incl_warn'] / v['total'], 3),
                      resolution=round(v['resolved_next'] / v['next_available'], 3) if v['next_available'] else None)
              for k, v in sorted(t2.items())}
    # ---- T3 false positives on accepted (last published) versions
    finals = [lst[-1] for lst in by_page.values() if lst and lst[-1]['kind'] == '_published' and lst[-1]['dir'] in cache]
    errs = [(s, f) for s in finals for f in cache[s['dir']]['findings'] if f['level'] == 'error']
    warns = [(s, f) for s in finals for f in cache[s['dir']]['findings'] if f['level'] == 'warn']
    per_check = collections.Counter(f['check'] for _, f in errs)
    pages_with_err = len({s['dir'] for s, _ in errs})
    rnd = random.Random(args.seed)
    seen = set()
    if args.exclude and Path(args.exclude).exists():
        seen = {(x['dir'], x['line'], x['check']) for x in json.loads(read(args.exclude))}
    pool = [(s, f) for s, f in errs if (s['dir'], f['line'], f['check']) not in seen]
    sample = rnd.sample(pool, min(30, len(pool)))
    # ---- T5 performance
    secs = [r['seconds'] for r in cache.values()]
    summary = dict(version=zh_lint.VERSION, rules=zh_lint.RULES['version'], split=f'dev < {SPLIT} <= heldout',
                   T2_T4=recall, T3=dict(accepted_pages=len(finals), pages_with_error=pages_with_err, errors=len(errs),
                                         errors_per_check=dict(per_check.most_common()), warnings=len(warns),
                                         warnings_per_check=dict(collections.Counter(f['check'] for _, f in warns).most_common())),
                   T5=dict(submissions=len(secs), mean_seconds=round(sum(secs) / len(secs), 3), max_seconds=max(secs),
                           with_official_html=sum(r['has_source'] for r in cache.values())))
    (OUT / 'eval.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT / 'misses.json').write_text(json.dumps(misses, ensure_ascii=False, indent=1), encoding='utf-8')
    with open(OUT / f'fp-sample-{args.tag}.md', 'w', encoding='utf-8') as f:
        f.write('# T3 誤報抽查樣本（已接受版本中的 error，隨機 30 則）\n\n| # | 頁面 | 行 | 檢查 | 訊息 | 判定 |\n|---|---|---|---|---|---|\n')
        for k, (s, x) in enumerate(sample, 1):
            f.write(f"| {k} | {s['page']} | {x['line']} | {x['check']} | {x['msg'][:90].replace('|', '／')} | |\n")
    json.dump([dict(dir=s['dir'], **x) for s, x in sample], open(OUT / f'fp-sample-{args.tag}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['run', 'score'])
    ap.add_argument('--budget', type=float, default=140)
    ap.add_argument('--seed', type=int, default=20261011)
    ap.add_argument('--exclude')
    ap.add_argument('--tag', default='A')
    a = ap.parse_args()
    (run if a.cmd == 'run' else score)(a)
