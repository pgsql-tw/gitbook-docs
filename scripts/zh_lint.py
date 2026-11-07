"""Deterministic pre-submission checks for the zh-TW PostgreSQL manual.

No model and no network. Every finding is reproducible and carries a check code,
level (error / warn), section index (translation_pipeline.parts), line and message.

  python scripts/zh_lint.py PAGE.md [--meta meta.json] [--baseline en.md]
                            [--source official.html] [--snapshot-date YYYY-MM-DD]
                            [--page rel/path.md --auto] [--json]

--auto looks up the English baseline, official HTML and snapshot date for --page in
outputs/pg-translation/pipeline-runtime/pages/*/manifest.json when available.
Exit status 1 when any error-level finding exists. Rules: scripts/zh_lint_rules.json.
"""
import argparse, bisect, glob, json, os, re, sys
from html.parser import HTMLParser
from pathlib import Path
from pg_project import translation_path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from translation_pipeline import parts  # noqa: E402
from agent_handoff import code_fences  # noqa: E402

RULES = json.loads((HERE / 'zh_lint_rules.json').read_text(encoding='utf-8'))
VERSION = 'zh-lint-v6'
CJK = '㐀-䶿一-鿿'
FILL = '¤'  # mask char: not space, not CJK, not letter
FOOTER = re.compile(r'^原文：\[PostgreSQL ([\d.]+) Documentation\]\(([^)\s]+)\)（原文版本：([^；）]+)；核對日期：(\d{4}-\d{2}-\d{2})）[ \t]*$', re.M)
SIMPLIFIED = set(RULES['simplified'])
HEAD_ALLOW = set(RULES['heading_allow'])
PROSE_ERR = set(RULES['prose_error_words'])
PROSE_ALLOW = {w.lower() for w in RULES['prose_allow']}
XREF = re.compile(r'^(Section|Chapter|Table|Figure|Example|Appendix|Part|Step)s?\s+[\dA-Z]')
SQL_PHRASES = r'\b(with(out)? time zone|double precision|character varying|bit varying)\b'
DUP_WORDS = '|'.join(['因此', '所以', '但是', '然而', '並且', '而且', '如果', '例如', '此外', '另外', '不過', '因為', '由於', '也就是', '就是', '亦即', '其中', '的', '了', '是', '在', '和', '與', '或'])


def read(path):
    return Path(path).read_text(encoding='utf-8-sig').replace('\r\n', '\n')


def mask(text):
    """Same-length copy with code, HTML tags, link targets and URLs replaced by FILL (newlines kept)."""
    chars = list(text)

    def blank(a, b):
        for k in range(a, b):
            if chars[k] != '\n':
                chars[k] = FILL
    fences = code_fences(text)
    for start, end, _ in fences:
        blank(start, end)
    outside = ''.join(chars)
    for pat, flags in ((r'<p class="func_signature">.*?</p>', re.S), (r'<pre\b.*?</pre>', re.S), (r'<code\b.*?</code>', re.S), (r'``.+?``', 0), (r'`[^`\n]*(?:\n[^`\n]+)?`', 0),
                       (r'\]\([^)\s]*\)', 0), (r'https?://[^\s)>\]]+', 0), (r'<[^>\n]+>', 0), (r'\[#\]', 0), (r'&[a-z]+;|&#\d+;', 0)):
        for m in re.finditer(pat, outside, flags):
            blank(m.start(), m.end())
        outside = ''.join(chars)
    return outside


class Doc:
    def __init__(self, text):
        self.text = text
        self.masked = mask(text)
        secs = parts(text)
        self.sec_starts, pos = [], 0
        for s in secs:
            self.sec_starts.append(pos)
            pos += len(s)
        self.sections = secs
        self.line_starts = [0] + [m.end() for m in re.finditer('\n', text)]

    def where(self, pos):
        return dict(section=bisect.bisect_right(self.sec_starts, pos) - 1, line=bisect.bisect_right(self.line_starts, pos))

    def masked_section(self, i):
        a = self.sec_starts[i]
        return self.masked[a:a + len(self.sections[i])], a


def F(doc, check, level, pos, msg):
    return dict(check=check, level=level, msg=msg, **doc.where(pos))


# ---------------------------------------------------------------- footer
def check_footer(doc, meta, snapshot_date):
    out = []
    found = list(FOOTER.finditer(doc.text))
    if not found:
        line = next((m for m in re.finditer(r'^原文：.*$', doc.text, re.M)), None)
        if line:
            out.append(F(doc, 'footer.format', 'error', line.start(), '頁尾格式不符：' + line.group(0)[:80]))
        else:
            out.append(F(doc, 'footer.missing', 'error', len(doc.text) - 1, '缺少頁尾「原文：[PostgreSQL x Documentation](url)（原文版本：x；核對日期：YYYY-MM-DD）」'))
        return out
    m = found[-1]
    ver, url, ver2, date = m.groups()
    if ver != ver2:
        out.append(F(doc, 'footer.version', 'error', m.start(), f'頁尾兩處版本不一致：{ver} / {ver2}'))
    if meta:
        if meta.get('source_version') and meta['source_version'] not in (ver, ver2):
            out.append(F(doc, 'footer.version', 'error', m.start(), f'頁尾版本 {ver} 與 meta.source_version {meta["source_version"]} 不一致'))
        if meta.get('source_url') and meta['source_url'] != url:
            out.append(F(doc, 'footer.url', 'error', m.start(), f'頁尾網址與 meta.source_url 不一致：{url}'))
        if meta.get('retrieved') and meta['retrieved'][:10] != date:
            out.append(F(doc, 'footer.date', 'error', m.start(), f'核對日期 {date} 與 meta.retrieved {meta["retrieved"][:10]} 不一致'))
    if snapshot_date and snapshot_date[:10] != date:
        out.append(F(doc, 'footer.snapshot', 'warn', m.start(), f'核對日期 {date} 與審查端官方快照擷取日 {snapshot_date[:10]} 不同；送件須附出處，否則可能被退件'))
    return out


# ---------------------------------------------------------------- anchors
class _IDs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.append(a['id'])
    handle_startendtag = handle_starttag


def official_ids(html):
    from translation_packets import SourceIndex
    a, b = SourceIndex(html, ['x']).body
    p = _IDs()
    p.feed(html[a:b])
    return p.ids


def ids_with_pos(text):
    return {m.group(1): m.start() for m in re.finditer(r'\bid="([^"]+)"', text)}


def check_anchors(doc, baseline, html, page=None):
    out = []
    have = ids_with_pos(doc.text)
    own = re.escape(os.path.basename(page)) if page else None
    pat = r'\]\((?:' + own + r')?#([^)\s]+)\)' if own else r'\]\(#([^)\s]+)\)'
    for m in re.finditer(pat, doc.text):
        if m.group(1) not in have:
            out.append(F(doc, 'anchor.link', 'error', m.start(), f'頁內連結 #{m.group(1)} 沒有對應的 id="{m.group(1)}"'))
    # Heading self-link [#](#X): the target id must sit with the heading (same section, within 3 lines before it),
    # otherwise reviewers reading per-section packets see the section without its anchor.
    raw = doc.text.split('\n')
    for n, line in enumerate(raw):
        hm = re.match(r'#{1,6}[ \t]+.*\[#\]\(#([^)\s]+)\)', line)
        if hm and hm.group(1) in have:
            near = '\n'.join(raw[max(0, n - 3):n + 1])
            pos = have[hm.group(1)]
            if f'id="{hm.group(1)}"' not in near or doc.where(pos)['section'] != doc.where(doc.line_starts[n])['section']:
                out.append(F(doc, 'anchor.placement', 'error', doc.line_starts[n],
                             f'標題連結 #{hm.group(1)} 的 <a id> 不在標題正上方（位於第 {doc.where(pos)["line"]} 行）'))
    if baseline is not None:
        bdoc_secs = parts(baseline)
        bstarts, pos = [], 0
        for s in bdoc_secs:
            bstarts.append(pos); pos += len(s)
        for i, p in ids_with_pos(baseline).items():
            if i not in have:
                sec = bisect.bisect_right(bstarts, p) - 1
                pos = doc.sec_starts[min(sec, len(doc.sec_starts) - 1)]
                out.append(F(doc, 'anchor.baseline', 'error', pos, f'英文原稿的錨點 id="{i}" 在譯文中遺失'))
    if html:
        ids = official_ids(html)
        reported = {f['msg'].split('"')[1] for f in out if f['check'] == 'anchor.baseline'}
        for k, i in enumerate(ids):
            if i in have or i in reported:
                continue
            prev = next((have[j] for j in reversed(ids[:k]) if j in have), 0)
            nxt = next((have[j] for j in ids[k + 1:] if j in have), None)
            pos = prev if nxt is None or prev else nxt
            level, check = ('error', 'anchor.root') if k == 0 else ('error', 'anchor.official')
            out.append(F(doc, check, level, pos, f'官方頁面的錨點 id="{i}" 在譯文中沒有對應的 <a id="{i}"></a>'))
    return out


# ---------------------------------------------------------------- untranslated
WORD = re.compile(r"[A-Za-z][A-Za-z0-9_.'/-]*")


def plain_word(w):
    return re.fullmatch(r"[A-Za-z][a-z]*(?:'[a-z]+)?|[A-Za-z][a-z]+-[a-z]+", w) is not None


def check_untranslated(doc, baseline=None):
    out = []
    text = doc.text
    # English glosses （Table of Contents） and quoted messages 「does not exist」 are legitimate.
    masked = re.sub(r'（[^（）]{0,300}）', lambda m: re.sub(r'[A-Za-z]', FILL, m.group(0)), doc.masked)
    masked = re.sub(r'"[^"\n]*"|“[^”\n]*”',
                    lambda m: m.group(0) if re.search(f'[{CJK}]', m.group(0)[1:-1]) else FILL * len(m.group(0)), masked)
    masked = re.sub(r'「[^「」]{0,300}」', lambda m: re.sub(r'[A-Za-z]', FILL, m.group(0)), masked)
    masked = re.sub(SQL_PHRASES, lambda m: FILL * len(m.group(0)), masked, flags=re.I)
    en_heads = set()
    if baseline is not None:
        for h in re.findall(r'^#{1,6}[ \t]+(.*)$', baseline, re.M):
            en_heads.update(w for w in WORD.findall(h) if w.islower())
    for m in re.finditer(r'^(#{1,6})[ \t]+(.*)$', masked, re.M):
        body = m.group(2)
        bad = [w for w in WORD.findall(body) if plain_word(w) and not w.isupper() and w not in HEAD_ALLOW and w not in en_heads]
        if bad:
            out.append(F(doc, 'untranslated.heading', 'error', m.start(), '標題含未翻譯英文：' + ' '.join(dict.fromkeys(bad))))
    # link text such as [Section 17.7](...)
    for m in re.finditer(r'\[([^\]\n]+)\]\(', text):
        t = m.group(1).strip()
        if XREF.match(t) and not re.search(f'[{CJK}]', t):
            out.append(F(doc, 'untranslated.xref', 'error', m.start(), f'交互參照文字未翻譯：[{t}]'))
    for lm in re.finditer(r'^(?!#)(.*)$', masked, re.M):
        line = lm.group(1)
        if not line.strip() or line.lstrip().startswith(('原文：', '|---', '| ---')):
            continue
        errs, warns = [], []
        for wm in WORD.finditer(line):
            w = wm.group(0)
            if not plain_word(w) or w[0].isupper():
                continue
            lw = w.lower()
            if lw in PROSE_ERR:
                errs.append(w)
            elif len(w) >= 3 and lw not in PROSE_ALLOW and re.search(f'[{CJK}]', line):
                warns.append(w)
        if errs:
            out.append(F(doc, 'untranslated.prose', 'error', lm.start(), '正文含未翻譯英文：' + ' '.join(dict.fromkeys(errs)) + '｜' + text[lm.start():lm.end()].strip()[:60]))
        if warns:
            out.append(F(doc, 'untranslated.word', 'warn', lm.start(), '中文句中夾雜英文詞：' + ' '.join(dict.fromkeys(warns))))
    return out


# ---------------------------------------------------------------- terminology
def check_terms(doc, baseline):
    out = []
    en_secs = parts(baseline) if baseline is not None else None
    aligned = en_secs is not None and len(en_secs) == len(doc.sections)
    for i in range(len(doc.sections)):
        zh, base = doc.masked_section(i)
        en = en_secs[i] if aligned else (baseline or '')
        for r in RULES['terms']:
            if r['en'] and not (en and re.search(r['en'], en, re.I)):
                continue
            for f in [re.escape(x) for x in r.get('forbid', [])] + r.get('forbid_re', []):
                for m in re.finditer(f, zh):
                    out.append(F(doc, 'term.' + r['id'], 'error', base + m.start(), f'術語：「{m.group(0)}」應為「{r["prefer"]}」（{r["source"]}）'))
                    break
        for f in RULES['regional']['forbid']:
            m = re.search(re.escape(f) + ('(?!端)' if f == '用戶' else ''), zh)
            if m:
                out.append(F(doc, 'term.regional', 'error', base + m.start(), f'中國大陸用語「{f}」'))
    return out


# ---------------------------------------------------------------- typography
def check_typography(doc):
    out = []
    masked = doc.masked
    for lm in re.finditer(r'^.*$', masked, re.M):
        bad = [c for c in lm.group(0) if c in SIMPLIFIED]
        if bad:
            out.append(F(doc, 'simplified', 'error', lm.start(), '簡體字：' + ''.join(dict.fromkeys(bad)) + '｜' + doc.text[lm.start():lm.end()].strip()[:50]))
    for m in re.finditer(f'({DUP_WORDS})[，、 ]?\\1', masked):
        out.append(F(doc, 'dup', 'error', m.start(), f'重複字詞：「{m.group(0)}」'))
    for m in re.finditer(r'\b([A-Za-z]{2,}) \1\b', masked):
        out.append(F(doc, 'dup', 'error', m.start(), f'重複字詞：「{m.group(0)}」'))
    for m in re.finditer(f'[{CJK}][ \\t]+[{CJK}]', masked):
        out.append(F(doc, 'space', 'warn', m.start(), f'漢字之間有空白：「{m.group(0)}」'))
    return out


# ---------------------------------------------------------------- driver
def lint(text, meta=None, baseline=None, html=None, snapshot_date=None, page=None):
    doc = Doc(text)
    page = page or (meta or {}).get('page')
    findings = (check_footer(doc, meta, snapshot_date) + check_anchors(doc, baseline, html, page) +
                check_untranslated(doc, baseline) + check_terms(doc, baseline) + check_typography(doc))
    return sorted(findings, key=lambda f: (f['line'], f['check']))


def locate(page, root='.'):
    """Baseline, official HTML and snapshot date for a page from the pipeline runtime (latest manifest)."""
    best = None
    for f in glob.glob(str(translation_path(root, 'pipeline-runtime/pages/*/manifest.json'))):
        try:
            m = json.loads(read(f))
        except Exception:
            continue
        if m.get('page') == page and (best is None or os.path.getmtime(f) > best[0]):
            best = (os.path.getmtime(f), f, m)
    if not best:
        return None, None, None
    _, f, m = best
    src = os.path.join(os.path.dirname(f), 'draft', 'source.html')
    source = m.get('source')
    if isinstance(source, str):
        try:
            source = json.loads(source)
        except Exception:
            source = {}
    return m.get('baseline'), (read(src) if os.path.exists(src) else None), (source or {}).get('retrieved')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('file')
    ap.add_argument('--meta'); ap.add_argument('--baseline'); ap.add_argument('--source'); ap.add_argument('--snapshot-date')
    ap.add_argument('--page'); ap.add_argument('--auto', action='store_true'); ap.add_argument('--json', action='store_true')
    ap.add_argument('--errors-only', action='store_true')
    a = ap.parse_args()
    meta = json.loads(read(a.meta)) if a.meta else None
    baseline = read(a.baseline) if a.baseline else None
    html = read(a.source) if a.source else None
    snap = a.snapshot_date
    if a.auto:
        page = a.page or (meta or {}).get('page')
        b, h, s = locate(page) if page else (None, None, None)
        baseline, html, snap = baseline or b, html or h, snap or s
    findings = lint(read(a.file), meta, baseline, html, snap, a.page)
    if a.errors_only:
        findings = [f for f in findings if f['level'] == 'error']
    if a.json:
        print(json.dumps(dict(version=VERSION, rules=RULES['version'], findings=findings), ensure_ascii=False, indent=1))
    else:
        for f in findings:
            print(f"{f['level']:5} L{f['line']:<5} §{f['section']:<3} {f['check']:<22} {f['msg']}")
        n = sum(f['level'] == 'error' for f in findings)
        print(f'{VERSION}: {n} error(s), {len(findings) - n} warning(s)'
              + ('' if baseline is not None else '；未提供英文 baseline，術語／錨點比對範圍受限')
              + ('' if html else '；未提供官方 HTML，略過官方錨點比對'))
    sys.exit(1 if any(f['level'] == 'error' for f in findings) else 0)


if __name__ == '__main__':
    main()
