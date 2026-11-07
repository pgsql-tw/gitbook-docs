"""Advisory local pre-submission screening + evaluation harness.

The local model is a *screener*, not a reviewer:
  * it never passes or rejects a page; it only lists suspected semantic problems;
  * every reported issue must quote the Chinese and English text verbatim; the program
    drops any issue whose quotes are not found (hallucination guard);
  * only generic error classes are in the prompt -- no case-specific rulings or answers.

Usage (server must be running at --url):
  python scripts/local_screen.py eval  --set dev     [--limit N]
  python scripts/local_screen.py eval  --set heldout
  python scripts/local_screen.py score --set heldout
Stdlib only, Windows/Linux compatible. Resumable: finished ids are skipped.
"""
import argparse, difflib, json, random, re, time, urllib.request
from pathlib import Path

OUT = Path('outputs/local-review-screening')
SYSTEM = """你是 PostgreSQL 官方手冊英翻正體中文的「初篩員」。你的任務是找出譯文中「可能改變技術語意」的地方，交給人工與正式審查員複核。你不決定通過或退件。

只回報下列類型（type 欄位用括號內代碼）：
1. 否定或肯定範圍錯置、漏掉否定（negation）
2. 情態改變：can/may/might/should/must/will 的可能性、必要性、建議性被改強或改弱（modality）
3. 數量、邊界、比較：under/at least/up to/more than/only 等邊界或數字不一致（boundary）
4. 主詞、受詞、所有關係或權限關係顛倒或錯置（role）
5. 因果、條件、先後順序方向錯誤；but/however 等轉折被改成順接（logic）
6. 漏譯會影響語意的條件、例外、限定詞或整句（omission）
7. 增加原文沒有的限定、結論或解釋，改變了適用範圍（addition）
8. 技術指涉錯誤：把 A 物件說成 B 物件，例如 client 與 server、表與索引、目前使用者與擁有者（reference）

不要回報：措辭偏好、語氣、文風、標點、用字選擇（只要語意相同）、程式碼與識別字、連結、錨點、標題格式、頁尾或日期、原文保留的英文術語。若沒有把握是語意問題，就不要回報。沒有問題時 issues 為空陣列，這是常見且正確的結果。

每個 issue 必須包含：
- zh_quote：從譯文逐字複製的片段（8–60 字，必須一字不差出現在譯文中）
- en_quote：從英文原文逐字複製的對應片段（必須一字不差出現在原文中）
- explanation：一句話說明語意差在哪裡
最多回報 3 個最有把握的 issue。只輸出指定 JSON。"""
SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['issues'], 'properties': {'issues': {
    'type': 'array', 'maxItems': 3, 'items': {'type': 'object', 'additionalProperties': False,
    'required': ['type', 'zh_quote', 'en_quote', 'explanation'], 'properties': {
        'type': {'type': 'string', 'enum': ['negation', 'modality', 'boundary', 'role', 'logic', 'omission', 'addition', 'reference']},
        'zh_quote': {'type': 'string'}, 'en_quote': {'type': 'string'}, 'explanation': {'type': 'string'}}}}}}
MAX_INPUT_TOKENS = 13000

SYSTEM_V2 = """你是 PostgreSQL 官方手冊英翻正體中文的「初篩員」。只找「中英文描述了不同技術事實」的地方；你不決定通過或退件。

判斷方法：對每個疑點，分別用一句白話寫出「英文說了什麼事實」(en_says) 與「譯文讓讀者理解成什麼事實」(zh_says)。只有當兩句描述的事實確實不同（範圍、條件、可能性、數量、誰對誰做什麼、因果方向、有無某項限制）時才回報。

以下一律不是問題，絕對不要回報：
- 同一事實的不同用字或譯名（例如某詞可譯 A 也可譯 B）、語氣稍強或稍弱但事實相同、語序、文風、標點
- 你認為譯文正確但「可以更好」的地方
- 程式碼、識別字、連結、錨點、標題格式、頁尾、日期、保留英文的術語
如果你的 explanation 會出現「語意正確」「可能」「建議改為」這類說法，代表它不是語意問題，不要回報。

大多數章節沒有語意問題；這時 issues 必須是空陣列。寧可漏報，不要誤報。最多回報 2 個。
欄位：type、zh_quote（譯文逐字片段 8–60 字）、en_quote（原文逐字片段）、en_says、zh_says、confidence（high 或 low）。只輸出指定 JSON。"""
SCHEMA_V2 = {'type': 'object', 'additionalProperties': False, 'required': ['issues'], 'properties': {'issues': {
    'type': 'array', 'maxItems': 2, 'items': {'type': 'object', 'additionalProperties': False,
    'required': ['type', 'zh_quote', 'en_quote', 'en_says', 'zh_says', 'confidence'], 'properties': {
        'type': {'type': 'string', 'enum': ['negation', 'modality', 'boundary', 'role', 'logic', 'omission', 'addition', 'reference']},
        'zh_quote': {'type': 'string'}, 'en_quote': {'type': 'string'}, 'en_says': {'type': 'string'}, 'zh_says': {'type': 'string'},
        'confidence': {'type': 'string', 'enum': ['high', 'low']}}}}}}
PROMPTS = {'screen-v1': (SYSTEM, SCHEMA, 900), 'screen-v2': (SYSTEM_V2, SCHEMA_V2, 700)}


def norm(s):
    return re.sub(r'\s+', '', s)


def call(url, path, body, timeout=600):
    req = urllib.request.Request(url + path, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def screen(url, en, zh, prompt='screen-v1'):
    """Return dict(issues_verified, issues_dropped, raw, usage, seconds). Never a pass/fail decision."""
    system, schema, max_tokens = PROMPTS[prompt]
    messages = [{'role': 'system', 'content': system},
                {'role': 'user', 'content': f'<英文原文>\n{en}\n</英文原文>\n\n<譯文>\n{zh}\n</譯文>'}]
    n = len(call(url, '/tokenize', {'content': system + en + zh, 'add_special': False})['tokens'])
    if n > MAX_INPUT_TOKENS:
        return dict(skipped=f'input {n} tokens exceeds {MAX_INPUT_TOKENS}; needs cloud review', input_tokens=n)
    body = {'messages': messages, 'temperature': 0, 'max_tokens': max_tokens, 'stream': False,
            'chat_template_kwargs': {'enable_thinking': False},
            'response_format': {'type': 'json_schema', 'json_schema': {'name': 'screen', 'schema': schema}}}
    t = time.monotonic()
    raw = call(url, '/v1/chat/completions', body)
    sec = round(time.monotonic() - t, 2)
    try:
        issues = json.loads(raw['choices'][0]['message']['content'])['issues']
    except Exception as exc:  # malformed output is reported, never treated as "clean"
        return dict(error=f'unparseable output: {exc}', seconds=sec, input_tokens=n)
    ok, dropped = [], []
    nzh, nen = norm(zh), norm(en)
    for i in issues:
        zq, eq = norm(i.get('zh_quote', '')), norm(i.get('en_quote', ''))
        reason = None
        if len(zq) < 4 or zq not in nzh:
            reason = 'zh_quote not found verbatim'
        elif len(eq) < 3 or eq not in nen:
            reason = 'en_quote not found verbatim'
        elif i.get('confidence') == 'low':
            reason = 'low confidence (advisory output keeps high only)'
        elif 'en_says' in i and norm(i['en_says']) == norm(i['zh_says']):
            reason = 'en_says equals zh_says'
        (dropped if reason else ok).append(dict(i, drop_reason=reason) if reason else i)
    return dict(issues=ok, dropped=dropped, seconds=sec, input_tokens=n,
                usage=raw.get('usage'), timings={k: raw.get('timings', {}).get(k) for k in ('prompt_per_second', 'predicted_per_second')})


def load(split):
    return [json.loads(l) for l in open(OUT / f'{split}.jsonl', encoding='utf-8')]


def sample(items, n_pos, n_easy, seed=20261011):
    """Positives with a hard-negative pair, at most one per page; plus their pairs and easy negatives."""
    rnd = random.Random(seed)
    pairs = {i['pair']: i for i in items if i['kind'] == 'hard_negative'}
    pos = [i for i in items if i['kind'] == 'positive' and i['id'] in pairs]
    rnd.shuffle(pos)
    chosen, pages = [], set()
    for p in pos:
        if p['page'] not in pages and len(chosen) < n_pos:
            chosen.append(p); pages.add(p['page'])
    easy = [i for i in items if i['kind'] == 'easy_negative']
    rnd.shuffle(easy)
    out = []
    for p in chosen:
        out += [p, pairs[p['id']]]
    return out + easy[:n_easy]


def changed_spans(a, b):
    """Character ranges of a that the fix (a -> b) replaced or deleted; insertions get a 1-char span."""
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return [(i, max(j, i + 1)) for tag, i, j, _, _ in sm.get_opcodes() if tag != 'equal']


def quote_span(text, quote):
    """Locate a quote in text tolerating whitespace differences; None if absent."""
    q = norm(quote)
    if not q:
        return None
    m = re.search(r'\s*'.join(map(re.escape, q)), text)
    return (m.start(), m.end()) if m else None


def evaluate(args):
    items = load(args.set)
    picked = sample(items, *({'dev': (10, 5), 'heldout': (40, 20)}[args.set]))
    if args.limit:
        picked = picked[:args.limit]
    res_path = OUT / f'results-{args.set}-{args.prompt}.jsonl'
    done = set()
    if res_path.exists():
        done = {json.loads(l)['id'] for l in open(res_path, encoding='utf-8')}
    with open(res_path, 'a', encoding='utf-8') as f:
        for k, it in enumerate(picked):
            if it['id'] in done:
                continue
            try:
                r = screen(args.url, it['en'], it['zh'], args.prompt)
            except Exception as exc:
                r = dict(error=str(exc))
            row = dict(id=it['id'], kind=it['kind'], label=it['label'], prompt=args.prompt, **r)
            f.write(json.dumps(row, ensure_ascii=False) + '\n'); f.flush()
            print(f"[{k+1}/{len(picked)}] {it['kind']:<13} flagged={len(r.get('issues', [])) > 0} "
                  f"dropped={len(r.get('dropped', []))} {r.get('seconds', '-')}s {r.get('skipped') or r.get('error') or ''}", flush=True)
    score(args)


def score(args):
    items = {i['id']: i for i in load(args.set)}
    rows = [json.loads(l) for l in open(OUT / f'results-{args.set}-{args.prompt}.jsonl', encoding='utf-8')]
    valid = [r for r in rows if 'issues' in r]
    flagged = lambda r: bool(r['issues'])
    by = lambda k: [r for r in valid if r['kind'] == k]
    pos, hard, easy = by('positive'), by('hard_negative'), by('easy_negative')
    rate = lambda xs: (round(sum(map(flagged, xs)) / len(xs), 3) if xs else None)
    pair_of = {i['pair']: i['id'] for i in items.values() if i.get('pair')}
    res = {r['id']: r for r in valid}
    # Localisation: a verified zh_quote overlaps text that the fix actually changed.
    loc, disc, chance, resolved = 0, 0, 0.0, 0
    for p in pos:
        h = res.get(pair_of.get(p['id']))
        if flagged(p) and pair_of.get(p['id']):
            a, b = items[p['id']]['zh'], items[pair_of[p['id']]]['zh']
            sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
            ops = [(i, max(j, i + 1), k, max(l, k + 1)) for tag, i, j, k, l in sm.get_opcodes() if tag != 'equal']
            qs = [quote_span(a, i['zh_quote']) for i in p['issues']]
            hit_ops = [o for o in ops if any(q and q[0] < o[1] and o[0] < q[1] for q in qs)]
            if hit_ops:
                loc += 1
                # resolved: the fixed version carries no flag over the same (fixed) region
                hq = [quote_span(b, i['zh_quote']) for i in (h or {}).get('issues', [])]
                if not any(q and q[0] < o[3] and o[2] < q[1] for o in hit_ops for q in hq):
                    resolved += 1
            # chance baseline: same-length quotes placed uniformly at random
            miss = 1.0
            for q in qs:
                if not q:
                    continue
                L, n = q[1] - q[0], len(a)
                starts = max(1, n - L + 1)
                hits = sum(1 for st in range(0, starts) if any(st < o[1] and o[0] < st + L for o in ops))
                miss *= 1 - hits / starts
            chance += 1 - miss
        if h and flagged(p) and not flagged(h):
            disc += 1
    n_drop = sum(len(r.get('dropped', [])) for r in valid)
    n_iss = sum(len(r['issues']) for r in valid) + n_drop
    tp = sum(map(flagged, pos)); fp = sum(map(flagged, hard + easy))
    summary = dict(set=args.set, prompt=args.prompt, rows=len(rows), valid=len(valid),
                   skipped=sum('skipped' in r for r in rows), errors=sum('error' in r for r in rows),
                   recall_section=rate(pos), localized_recall=round(loc / len(pos), 3) if pos else None,
                   flag_rate_hard_negative=rate(hard), flag_rate_easy_negative=rate(easy),
                   precision_in_sample=round(tp / (tp + fp), 3) if tp + fp else None,
                   localized_chance_baseline=round(chance / len(pos), 3) if pos else None,
                   localized_and_resolved=round(resolved / len(pos), 3) if pos else None,
                   pair_discrimination=round(disc / len(pos), 3) if pos else None,
                   quote_drop_rate=round(sum(1 for r in valid for d in r.get('dropped', []) if 'quote' in d['drop_reason']) / n_iss, 3) if n_iss else None,
                   other_drops=sum(1 for r in valid for d in r.get('dropped', []) if 'quote' not in d['drop_reason']),
                   mean_seconds=round(sum(r.get('seconds', 0) for r in valid) / len(valid), 2) if valid else None,
                   counts=dict(positive=len(pos), hard_negative=len(hard), easy_negative=len(easy)),
                   by_type={t: sum(1 for r in valid for i in r['issues'] if i['type'] == t) for t in SCHEMA['properties']['issues']['items']['properties']['type']['enum']})
    (OUT / f'score-{args.set}-{args.prompt}.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['eval', 'score'])
    ap.add_argument('--set', choices=['dev', 'heldout'], required=True)
    ap.add_argument('--limit', type=int)
    ap.add_argument('--url', default='http://127.0.0.1:18080')
    ap.add_argument('--prompt', choices=['screen-v1', 'screen-v2'], default='screen-v1')
    a = ap.parse_args()
    (evaluate if a.cmd == 'eval' else score)(a)
