"""Preview and apply exact local-link edits; never commit, push or alter examples."""
import argparse
import html
import json
import os
from pathlib import Path
import posixpath
import re
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from markdown_it import MarkdownIt
from agent_handoff import code_fences
from pg_maintenance import atomic_json, atomic_write, digest


def safe_path(root, name):
    if not isinstance(name, str) or not name or '\\' in name:
        raise ValueError('Use a relative POSIX workspace path')
    p = (Path(root).resolve() / name).resolve()
    if (Path(name).is_absolute() or not p.is_relative_to(Path(root).resolve()) or '.git' in p.parts or
            p.relative_to(Path(root).resolve()).as_posix() != name):
        raise ValueError('Path outside editable workspace: ' + name)
    return p


def protected_ranges(text):
    ranges = [(a, b) for a, b, _ in code_fences(text)]
    offsets = [0]
    for line in text.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))
    for token in MarkdownIt('commonmark', {'html': True}).parse(text):
        if token.type in ('fence', 'code_block') and token.map:
            ranges.append((offsets[token.map[0]], offsets[token.map[1]]))
    ranges += [m.span() for m in re.finditer(r'<(pre|code|script|style|textarea)\b[^>]*>.*?</\1\s*>', text, re.I | re.S)]
    ranges += [m.span() for m in re.finditer(r'<!--.*?-->', text, re.S)]
    # Match complete inline backtick runs; protect their contents as well.
    for m in re.finditer(r'(?<!`)(`+)(?!`)', text):
        if any(a <= m.start() < b for a, b in ranges):
            continue
        end = re.search(r'(?<!`)' + re.escape(m[1]) + r'(?!`)', text[m.end():])
        if end:
            ranges.append((m.start(), m.end() + end.end()))
    return ranges


def url_spans(text):
    """Source offsets for inline destinations, reference definitions and HTML hrefs.

    Preserve titles, attributes, whitespace, BOM and newlines. Read-only public
    inventory uses a Markdown parser separately, so reference *uses* count twice
    when appropriate while a reference definition is rewritten only once.
    """
    protected = protected_ranges(text)
    free = lambda start: not any(a <= start < b for a, b in protected)
    found = []
    starts = [m.end() for m in re.finditer(r'\]\(\s*', text) if free(m.start())]
    starts += [m.end() for m in re.finditer(r'^ {0,3}\[[^\]\n]+\]:[ \t]*', text, re.M) if free(m.start())]
    for start in starts:
        if start >= len(text):
            continue
        if text[start] == '<':
            end = text.find('>', start + 1)
            if end < 0:
                continue
            found.append((start + 1, end, 'markdown'))
            continue
        pos, depth = start, 0
        while pos < len(text):
            char = text[pos]
            if char == '\\' and pos + 1 < len(text):
                pos += 2
                continue
            if char.isspace() or (char == ')' and depth == 0):
                break
            depth += (char == '(') - (char == ')')
            pos += 1
        if pos > start:
            found.append((start, pos, 'markdown'))
    for tag in re.finditer(r'''<[A-Za-z](?:"[^"]*"|'[^']*'|[^'">])*?>''', text, re.S):
        if not free(tag.start()):
            continue
        for attr in re.finditer(r'''([^\s=<>/]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))''', tag[0], re.S):
            if attr[1].lower() != 'href':
                continue
            a, b = attr.span(next(i for i in (2, 3, 4) if attr[i] is not None))
            found.append((tag.start() + a, tag.start() + b, 'html'))
    return sorted(set((a, b, kind) for a, b, kind in found if free(a)))


def rewrite_links(text, source, destination, targets):
    """Rebase only when moving content; in-place edits require an exact mapping."""
    mapping = {}
    for item in targets:
        key = (item['from']['page'], item['from']['fragment'])
        if key in mapping:
            raise ValueError('Duplicate link target mapping')
        mapping[key] = item['to']
    edits = []
    for a, b, kind in url_spans(text):
        raw = text[a:b]
        value = html.unescape(raw) if kind == 'html' else re.sub(r'\\([()<> ])', r'\1', raw)
        url = urlsplit(value)
        if url.scheme or url.netloc or value.startswith('/') or not value:
            continue
        old_page = posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(url.path))) if url.path else source
        target = mapping.get((old_page, unquote(url.fragment)))
        if source == destination and not target:
            continue
        page = target['page'] if target else old_page
        fragment = target['fragment'] if target else url.fragment
        rel = '' if page == destination else posixpath.relpath(page, posixpath.dirname(destination))
        rel = quote(rel, safe="/-._~!$&'()*+,;=@")
        if target:
            fragment = quote(fragment, safe="/-._~!$&'()*+,;=:@?")
        updated = urlunsplit(('', '', rel, url.query, fragment))
        if kind == 'html':
            updated = html.escape(updated, quote=True)
        else:
            updated = updated.replace(' ', '%20').replace('(', '\\(').replace(')', '\\)')
        if raw != updated:
            edits.append(dict(start=a, end=b, before=raw, after=updated))
    changed = text
    for e in reversed(edits):
        changed = changed[:e['start']] + e['after'] + changed[e['end']:]
    return changed, edits


def build_plan(root, spec):
    root = Path(root).resolve()
    files = spec['files']
    if not files or len(files) != len(set(files)):
        raise ValueError('Specify unique candidate files')
    for t in spec['targets']:
        for side in ('from', 'to'):
            safe_path(root, t[side]['page'])
            if not isinstance(t[side]['fragment'], str):
                raise ValueError('Fragment must be a string')
    plans, counts = [], {}
    for name in files:
        path = safe_path(root, name)
        before = path.read_bytes()
        after, edits = rewrite_links(before.decode('utf-8'), name, name, spec['targets'])
        if edits:
            plans.append(dict(path=name, before_sha256=digest(before), after_sha256=digest(after.encode('utf-8')),
                              edits=edits))
            counts[name] = len(edits)
    expected = spec.get('expected_changes')
    return dict(schema=1, root=str(root), targets=spec['targets'], files=plans,
                candidate_sha256={f: digest(safe_path(root, f).read_bytes()) for f in files},
                expected_changes=expected, actual_changes=counts,
                ready_for_apply=expected is not None and expected == counts)


def apply_plan(root, plan, report):
    root = Path(root).resolve()
    if plan.get('schema') != 1 or Path(plan['root']).resolve() != root:
        raise ValueError('Plan belongs to another workspace or schema')
    if not plan.get('ready_for_apply') or plan['actual_changes'] != plan['expected_changes']:
        raise ValueError('Review the preview and provide matching expected_changes before applying')
    for target in plan['targets']:
        for side in ('from', 'to'):
            safe_path(root, target[side]['page'])
    lock = root / 'outputs/pg-maintenance/rewrite.lock'
    lock.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    applied, originals = [], {}
    result = dict(status='failed', applied=[], rollback_conflicts=[])
    try:
        os.close(fd)
        # Preflight every candidate before the first source write.
        for name, expected in plan['candidate_sha256'].items():
            raw = safe_path(root, name).read_bytes()
            if digest(raw) != expected:
                raise ValueError('Stale candidate: ' + name)
            originals[name] = raw
        generated = {}
        for item in plan['files']:
            name = item['path']
            if name in generated or name not in originals:
                raise ValueError('Invalid or duplicate planned file: ' + name)
            after, edits = rewrite_links(originals[name].decode('utf-8'), name, name, plan['targets'])
            data = after.encode('utf-8')
            if (edits != item['edits'] or digest(originals[name]) != item['before_sha256'] or
                    digest(data) != item['after_sha256'] or len(edits) != plan['actual_changes'].get(name)):
                raise ValueError('Plan edits failed verification: ' + name)
            generated[name] = data
        if set(generated) != set(plan['actual_changes']):
            raise ValueError('Changed-file scope differs from the preview')
        for name, data in generated.items():
            path = safe_path(root, name)
            if path.read_bytes() != originals[name]:
                raise ValueError('Candidate changed before write: ' + name)
            atomic_write(path, data)
            applied.append(name)
        result.update(status='complete', applied=applied)
        return result
    except Exception as error:
        for name in reversed(applied):
            path = safe_path(root, name)
            expected = next(f['after_sha256'] for f in plan['files'] if f['path'] == name)
            try:
                if digest(path.read_bytes()) != expected:
                    result['rollback_conflicts'].append(name)
                    continue
                atomic_write(path, originals[name])
            except OSError:
                result['rollback_conflicts'].append(name)
        result.update(error=str(error), applied=applied)
        raise
    finally:
        try:
            atomic_json(report, result)
        finally:
            lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default='.')
    sub = parser.add_subparsers(dest='command', required=True)
    preview = sub.add_parser('plan')
    preview.add_argument('--spec', required=True)
    preview.add_argument('--out', required=True)
    apply = sub.add_parser('apply')
    apply.add_argument('--plan', required=True)
    apply.add_argument('--report', required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    output = Path(args.out if args.command == 'plan' else args.report).resolve()
    if not output.is_relative_to(root / 'outputs'):
        parser.error('Evidence must be below workspace outputs')
    if output.exists():
        parser.error('Use a new evidence path; retain previous plan/result')
    if args.command == 'plan':
        result = build_plan(root, json.loads(Path(args.spec).read_text(encoding='utf-8-sig')))
        atomic_json(output, result)
        print(json.dumps(dict(actual_changes=result['actual_changes'], ready_for_apply=result['ready_for_apply'])))
    else:
        print(json.dumps(apply_plan(root, json.loads(Path(args.plan).read_text(encoding='utf-8-sig')), output)))


if __name__ == '__main__':
    main()
