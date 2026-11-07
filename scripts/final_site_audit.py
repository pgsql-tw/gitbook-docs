"""Read-only site scan; writes evidence only under the requested report directory.

No network requests, publisher actions or document edits. Lint/fragment findings
are candidates, not semantic rejection decisions or GitBook rendering results.
"""
import argparse
import hashlib
import json
import posixpath
import re
import subprocess
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
import agent_handoff
import zh_lint
from pg_project import translation_path
from pg_maintenance import InputSnapshot, atomic_json


def git(*args, root=None):
    return subprocess.check_output(['git', *args], cwd=root).decode('utf-8-sig')


def read(p):
    return p.read_text(encoding='utf-8-sig').replace('\r\n', '\n')


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def local_target(page, url):
    dest = unquote(urlsplit(url).path)
    return (posixpath.normpath(posixpath.join(posixpath.dirname(page), dest))
            if dest and not dest.startswith('/') else dest.lstrip('/') or page)


class HTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('id', 'name'):
            if attrs.get(key):
                self.ids.append(attrs[key])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])


def inspect(text):
    # Existing helper understands definition-list code fences as well.
    masked = list(text)
    frontmatter = re.match(r'\A---\n.*?\n---(?:\n|$)', text, re.S)
    if frontmatter:
        masked[:frontmatter.end()] = ['\n' if c == '\n' else ' ' for c in frontmatter[0]]
    for start, end, _ in agent_handoff.code_fences(text):
        masked[start:end] = ['\n' if c == '\n' else ' ' for c in text[start:end]]
    masked_text = ''.join(masked)
    tokens = MarkdownIt('commonmark', {'html': True}).parse(masked_text)
    ids, links, headings = [], [], []
    # GitBook definition-list parameters contain indented HTML anchors. CommonMark
    # labels them code blocks, but that is not proof those IDs are absent in the
    # source. Inventory explicit markup independently; do not claim live rendering.
    html_text = re.sub(r'(`+)(.*?)\1', lambda m: ' ' * len(m[0]), masked_text, flags=re.S)
    h = HTML()
    h.feed(html_text)
    ids.extend(h.ids)
    links.extend((x, None) for x in h.links)
    def visit(items):
        for token in items:
            if token.type == 'link_open':
                links.append((token.attrGet('href'), None))
            if token.type == 'image':
                links.append((token.attrGet('src'), None))
            if token.children:
                visit(token.children)
    visit(tokens)
    for i, token in enumerate(tokens):
        if token.type == 'heading_open' and i + 1 < len(tokens):
            headings.append(tokens[i + 1].content)
    return dict(ids=ids, links=links, headings=headings)


def scan(root, out):
    root, out = Path(root).resolve(), Path(out).resolve()
    if not out.is_relative_to(root / 'outputs'):
        raise ValueError('Report directory must be below workspace outputs')
    snapshot = InputSnapshot(root)
    head = git('rev-parse', 'HEAD', root=root).strip()
    read = snapshot.text
    def local_files(pattern):
        return sorted(p.relative_to(root).as_posix() for p in translation_path(root).glob(pattern))
    tracked = snapshot.inventory('tracked_files', lambda: git('ls-files', '-z', root=root).split('\0'))
    def summary_and_pages():
        summary_text = (root / 'SUMMARY.md').read_text(encoding='utf-8-sig')
        names = re.findall(r'^\s*\* \[[^\n]+\]\(([^)]+)\)', summary_text, re.M)
        declared = [unquote(urlsplit(x).path) for x in names]
        roots = {p.split('/')[0] for p in declared if '/' in p}
        tracked_now = git('ls-files', '-z', root=root).split('\0')
        return sorted({p for p in tracked_now if p.endswith('.md') and (p in declared or p.split('/')[0] in roots)} |
                      {p for p in declared if p.endswith('.md') and (root / p).is_file()})
    pages = snapshot.inventory('site_pages', summary_and_pages)
    manifest_names = snapshot.inventory('manifests', lambda: local_files('pipeline-runtime/pages/*/manifest.json'))
    snapshot.inventory('manifest_selection_times', lambda: [
        (name, (root / name).stat().st_mtime_ns)
        for name in local_files('pipeline-runtime/pages/*/manifest.json')])
    manifest_times = {name: (root / name).stat().st_mtime_ns for name in manifest_names}
    archive_names = snapshot.inventory('published_archives', lambda: local_files('agents/inbox/*/_published/*/result.json'))
    inboxes = snapshot.inventory('inbox', lambda: [
        name for name in local_files('agents/inbox/*/*/meta.json')
        if not Path(name).parent.name.startswith('_')])
    claims = snapshot.inventory('claims', lambda: local_files('agents/claims/*.json'))
    inputs = ['SUMMARY.md', *pages, *manifest_names, *archive_names, *inboxes,
              translation_path(root, 'pending-pages.md')]
    for name in manifest_names:
        inputs.append(root / name.replace('/manifest.json', '/draft/source.html'))
    for name in archive_names:
        inputs.extend([root / name.replace('/result.json', '/meta.json'),
                       root / name.replace('/result.json', '/page.md')])
    snapshot.capture(inputs)
    summary = read(root / 'SUMMARY.md')
    entries = re.findall(r'^\s*\* \[([^\n]+)\]\(([^)]+)\)', summary, re.M)
    targets = [unquote(urlsplit(url).path) for _, url in entries]
    texts = {p: read(root / p) for p in pages}
    docs = {p: inspect(t) for p, t in texts.items()}
    linked = {local_target(p, url) for p, doc in docs.items() for url, _ in doc['links']
              if not urlsplit(url).scheme and not urlsplit(url).netloc}
    # Link existence and directory-to-README resolution are inputs too; retain
    # their initial state instead of mixing live filesystem checks into the scan.
    directories = snapshot.inventory('linked_directories', lambda: [p for p in linked if (root / p).is_dir()])
    snapshot.capture([root / p for p in linked] + [root / p / 'README.md' for p in directories])
    findings, evidence = [], []
    def finding(kind, page, **details):
        findings.append(dict(kind=kind, page=page, **details))
    for p in targets:
        if not (root / p).is_file():
            finding('summary_missing_target', 'SUMMARY.md', target=p)
    for p, n in Counter(targets).items():
        if n > 1:
            finding('summary_duplicate_target', 'SUMMARY.md', target=p, count=n)
    for p in sorted(set(pages) - set(targets)):
        finding('unlisted_page', p)
    def title_key(title):
        title = re.sub(r'\[#\]\(#[^)]*\)', '', title)
        return ''.join(c.lower() for c in title if c.isalnum())
    for label, target in entries:
        if target in docs and docs[target]['headings']:
            heading = docs[target]['headings'][0]
            if title_key(label) != title_key(heading):
                finding('summary_title_candidate', target, label=label, heading=heading)
    manifests = {}
    for name in manifest_names:
        f = root / name
        m = json.loads(read(f))
        p = m.get('page')
        if p not in manifests or manifest_times[name] > manifest_times[manifests[p][0].relative_to(root).as_posix()]:
            manifests[p] = f, m
    trailers = {}
    all_proofs = set()
    for block in git('log', '--format=%H%x1e%B%x1f', root=root).split('\x1f'):
        if '\x1e' not in block:
            continue
        commit, body = block.strip().split('\x1e', 1)
        p = re.search(r'^Translation-Page: (.+)$', body, re.M)
        h = re.search(r'^Translation-Page-SHA256: (\w+)$', body, re.M)
        if p and h:
            trailers.setdefault(p[1].strip(), (commit, h[1]))
            all_proofs.add((commit, p[1].strip(), h[1]))
    archives = []
    for name in archive_names:
        f = root / name
        result = json.loads(read(f))
        meta = json.loads(read(f.parent / 'meta.json'))
        digest = sha(read(f.parent / 'page.md'))
        record = dict(archive=str(f.parent.relative_to(root)).replace('\\', '/'),
                      page=result.get('page'), commit=result.get('commit'), sha256=digest,
                      meta_hash_matches=meta.get('page_sha256') == digest,
                      trailer_matches=(result.get('commit'), result.get('page'), digest) in all_proofs)
        archives.append(record)
        if not record['meta_hash_matches'] or not record['trailer_matches']:
            finding('archive_evidence_mismatch', result.get('page'), evidence=record)
    external = Counter()
    for p, text in texts.items():
        proof = trailers.get(p)
        evidence.append(dict(page=p, sha256=sha(text), trailer=proof,
                             hash_matches_latest_trailer=bool(proof and proof[1] == sha(text)),
                             baseline_available=p in manifests))
        if proof and proof[1] != sha(text):
            finding('current_hash_differs_from_latest_translation', p, commit=proof[0])
        doc = docs[p]
        for ident, n in Counter(doc['ids']).items():
            if n > 1:
                finding('duplicate_explicit_anchor', p, anchor=ident, count=n)
        for url, _ in doc['links']:
            u = urlsplit(url)
            if u.scheme or u.netloc:
                external[u.netloc or u.scheme] += 1
                continue
            target = local_target(p, url)
            path = root / target
            if target in directories:
                target = posixpath.join(target, 'README.md')
                path = root / target
            if snapshot.data[snapshot.key(path)] is None:
                finding('missing_local_target', p, url=url, target=target)
            elif u.fragment and target in docs:
                fragment = unquote(u.fragment)
                if fragment not in docs[target]['ids']:
                    finding('fragment_needs_resolution', p, url=url, target=target,
                            fragment=fragment,
                            reason='No matching explicit ID; generated GitBook anchors not verified')
        f, m = manifests.get(p, (None, {}))
        src = f.parent / 'draft/source.html' if f else None
        html = read(src) if src and snapshot.data.get(snapshot.key(src)) is not None else None
        meta = m.get('submission')
        for item in zh_lint.lint(text, meta=meta, baseline=m.get('baseline'), html=html, page=p):
            finding('lint_candidate', p, **item)
        if m.get('baseline'):
            for error in agent_handoff.structural_errors(m['baseline'], text, p):
                finding('baseline_structure_candidate', p, detail=error)
        if '英文原文，待翻譯' in text:
            finding('pending_translation_marker', p)
    pending_text = read(translation_path(root, 'pending-pages.md'))
    pending = re.findall(r'^\s*- \[ \].*$', pending_text, re.M)
    end_head = git('rev-parse', 'HEAD', root=root).strip()
    consistency = snapshot.verify()
    consistency['head_changed'] = head != end_head
    consistency['valid'] = consistency['valid'] and head == end_head
    result = dict(head=head, end_head=end_head, scan_valid=consistency['valid'], input_consistency=consistency,
                  tracked_site_pages=sum(p in tracked for p in pages), site_pages=len(pages),
                  untracked_summary_pages=sorted(set(pages)-set(tracked)), summary_entries=len(entries),
                  pending_count=len(pending), inbox=inboxes,
                  claims=len(claims),
                  evidence_counts=dict(Counter('matching_trailer' if e['hash_matches_latest_trailer']
                                              else 'different_trailer' if e['trailer'] else 'no_trailer'
                                              for e in evidence)),
                  archive_counts=dict(total=len(archives),
                                      meta_hash_matches=sum(x['meta_hash_matches'] for x in archives),
                                      trailer_matches=sum(x['trailer_matches'] for x in archives)),
                  finding_counts=dict(Counter(f['kind'] for f in findings)),
                  external_links_not_requested=dict(external),
                  limitations=['Static audit only; not whole-site semantic re-review',
                               'No actual GitBook rendering or external URL availability check',
                               'Lint, baseline and fragment findings require triage against approved exceptions'],
                  dirty_status=git('status', '--short', root=root),
                  pages=evidence, archives=archives, findings=findings)
    out.mkdir(parents=True, exist_ok=True)
    atomic_json(out / 'scan.json', result)
    return result

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    result = scan(Path.cwd(), args.out)
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ('pages', 'archives', 'findings', 'dirty_status',
                      'external_links_not_requested', 'input_consistency')},
                     ensure_ascii=False, indent=2))
    return 0 if result['scan_valid'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
