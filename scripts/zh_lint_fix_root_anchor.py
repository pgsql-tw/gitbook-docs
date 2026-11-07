"""Dry-run (no tracked file is modified): add the official root anchor to pages that lack it (user ruling 2026-10-11: follow the official manual).

Reads the CURRENT repo file of each page, inserts <a id="ROOT"></a> as the first line, and writes the
patched copy + meta.json under outputs/zh-lint/root-anchor-fix/<slug>/ and one combined git patch
(root-anchor-fix.patch). Published pages are not 'todo', so agent_handoff inbox cannot take these;
apply with `git apply` after review.
Never edits tracked pages. Verifies: only one line added; zh_lint anchor.root resolved; structural_errors
against the original unchanged apart from anchors.
"""
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import zh_lint
from zh_lint_eval import manifests, read
from translation_pipeline import structural_errors

OUT = Path('outputs/zh-lint/root-anchor-fix')


def main():
    idx = manifests()
    rows = []
    for page, info in sorted(idx.items()):
        p = Path(page)
        if not p.exists():
            continue
        raw_bytes = p.read_bytes()
        bom = raw_bytes.startswith(b'\xef\xbb\xbf')
        raw = raw_bytes.decode('utf-8-sig')
        eol = '\r\n' if '\r\n' in raw else '\n'
        text = raw.replace('\r\n', '\n')
        if '原文：[PostgreSQL' not in text or '英文原文，待翻譯' in text:   # untranslated / partial: not in scope
            continue
        ids = zh_lint.official_ids(read(info['source']))
        if not ids or f'id="{ids[0]}"' in text:
            continue
        root = ids[0]
        patched = f'<a id="{root}"></a>\n' + text
        before = {f['check'] for f in zh_lint.lint(text, html=read(info['source']), page=page) if f['level'] == 'error'}
        after = {f['check'] for f in zh_lint.lint(patched, html=read(info['source']), page=page) if f['level'] == 'error'}
        assert 'anchor.root' in before and 'anchor.root' not in after, page
        assert set(structural_errors(text, patched, page)) <= set(structural_errors(text, text, page)), page
        slug = page.replace('/', '__')
        d = OUT / slug
        d.mkdir(parents=True, exist_ok=True)
        out_bytes = (('\ufeff' if bom else '') + patched.replace('\n', eol)).encode('utf-8')
        expect = (('\ufeff' if bom else '') + f'<a id="{root}"></a>' + eol).encode('utf-8') + raw_bytes[3 if bom else 0:]
        assert out_bytes == expect, page   # byte-exact: one line added, BOM and line endings preserved
        (d / 'page.md').write_bytes(out_bytes)
        (d / 'meta.json').write_text(json.dumps(dict(
            page=page, agent='claude', kind='anchor-only', root=root,
            base_sha256=hashlib.sha256(raw_bytes).hexdigest(),
            page_sha256=hashlib.sha256(out_bytes).hexdigest(),
            change=f'只在第一行加入官方根節點錨點 <a id="{root}"></a>；其餘內容不變（使用者裁決 2026-10-11：錨點比照官方手冊）',
        ), ensure_ascii=False, indent=2), encoding='utf-8')
        rows.append(dict(page=page, root=root, other_errors=sorted(after)))
    import subprocess
    chunks = []
    for r in rows:
        slug = r['page'].replace('/', '__')
        diff = subprocess.run(['git', 'diff', '--no-index', '--', r['page'], str(OUT / slug / 'page.md')],
                              capture_output=True).stdout.decode('utf-8')
        diff = diff.replace('b/' + str(OUT / slug / 'page.md'), 'b/' + r['page'])
        chunks.append(diff)
    (OUT / 'root-anchor-fix.patch').write_bytes(''.join(chunks).encode('utf-8'))
    (OUT / 'SUMMARY.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    print(len(rows), 'pages prepared')


if __name__ == '__main__':
    main()
