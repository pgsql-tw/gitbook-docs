"""Version-neutral public-result comparisons; no browser, network or automatic retry."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import posixpath
import re
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
from pg_link_rewrite import protected_ranges
from pg_maintenance import atomic_json, digest, read_json


def plain(value):
    return re.sub(r'\s+', ' ', value).strip()


def paragraphs(values, ignore_last_updated=False):
    result = []
    for value in values:
        value = plain(value)
        if not value:
            continue
        if ignore_last_updated and re.fullmatch(
                r'Last updated (?:\d+ (?:second|minute|hour|day|week|month|year)s? ago|just now)', value):
            continue
        result.append(value)
    return result


def authored_links(text):
    """Count parsed reference uses/autolinks and HTML hrefs, excluding examples."""
    masked = list(text)
    for a, b in protected_ranges(text):
        masked[a:b] = ['\n' if c == '\n' else ' ' for c in text[a:b]]
    source = ''.join(masked)
    result = []
    def visit(tokens):
        for token in tokens:
            if token.type == 'link_open':
                result.append(token.attrGet('href'))
            if token.children:
                visit(token.children)
    visit(MarkdownIt('commonmark', {'html': True}).parse(source))
    class Links(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag.lower() == 'a':
                attrs = dict(attrs)
                if 'href' in attrs:
                    result.append(attrs['href'])
    Links().feed(source)
    return result


def public_url(source, url, *, origin, major, routes):
    u = urlsplit(url)
    if u.scheme or u.netloc:
        return url
    if u.path.startswith('/'):
        return origin.rstrip('/') + url
    dest = posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(u.path))) if u.path else source
    if dest not in routes:
        raise ValueError('Provide an observed or explicitly planned public route: ' + dest)
    path = routes[dest]
    if path != '/' + str(major) and not path.startswith('/' + str(major) + '/'):
        raise ValueError('Route differs from configured manual major: ' + path)
    return origin.rstrip('/') + path + ('?' + u.query if u.query else '') + ('#' + u.fragment if u.fragment else '')


def expected_links(source, text, *, origin, major, routes, interface_links=()):
    """Interface links are explicit per-page evidence, never parent leftovers."""
    result = Counter(public_url(source, u, origin=origin, major=major, routes=routes)
                     for u in authored_links(text))
    result.update(interface_links)
    return dict(result)


def arrival_ok(value, *, count='count', top='top', height='viewportHeight'):
    return (value.get(count) == 1 and isinstance(value.get(top), (int, float)) and
            isinstance(value.get(height), (int, float)) and 0 <= value[top] < value[height])


def compare_case(case, record, *, origin):
    if not record:
        return ['missing']
    bad = []
    if record.get('url') != origin.rstrip('/') + case['path']:
        bad.append('route')
    if record.get('documentWidth', 1) > record.get('viewportWidth', 0):
        bad.append('overflow')
    expected = case.get('expected', {})
    supported = {'allCodeTexts', 'tableRows', 'listBlocks', 'headingIds', 'rootParagraphs',
                 'outsideCodeParagraphs', 'link_counts', 'ignore_last_updated'}
    if set(expected) - supported:
        raise ValueError('Unknown expected fields: ' + ', '.join(sorted(set(expected) - supported)))
    for field in ['allCodeTexts', 'tableRows', 'listBlocks', 'headingIds']:
        if field in expected and record.get(field) != expected[field]:
            bad.append(field)
    for field in ['rootParagraphs', 'outsideCodeParagraphs']:
        if field in expected and paragraphs(record.get(field, []), expected.get('ignore_last_updated', False)) != expected[field]:
            bad.append(field)
    if 'link_counts' in expected and Counter(x['href'] for x in record.get('mainLinks', [])) != Counter(expected['link_counts']):
        bad.append('links')
    if case.get('anchor') and (not record.get('idExists') or not arrival_ok(record, count='anchorCount', top='anchorTop')):
        bad.append('direct')
    wanted = [x['anchor'] for x in case.get('batchTargets', [])] or case.get('batchAnchors', [])
    jumps = record.get('batchJumps', [])
    if [j.get('anchor') for j in jumps] != wanted:
        bad.append('click_coverage')
    for index, jump in enumerate(jumps):
        if not jump.get('clicked') or jump.get('hash') != '#' + jump['anchor'] or not arrival_ok(jump, count='idCount', top='targetTop'):
            bad.append('click')
        if case.get('batchTargets') and index < len(case['batchTargets']):
            target = case['batchTargets'][index]
            if target['kind'] == 'heading' and not jump.get('inHeading'):
                bad.append('heading_click')
            if target['kind'] in ('body', 'table', 'compatibility') and jump.get('inHeading', True):
                bad.append('body_click')
            if target['kind'] == 'table' and not jump.get('inTable'):
                bad.append('table_click')
            if target.get('paragraphPrefix') and not jump.get('paragraphText', '').startswith(target['paragraphPrefix']):
                bad.append('compatibility_click')
    if case.get('travel'):
        travel, arrival, target = record.get('travel', {}), record.get('travelArrival', {}), case['travel']
        url = origin.rstrip('/') + target['path'] + '#' + target['anchor']
        if (not travel.get('clicked') or not travel.get('text', '').strip() or travel.get('text', '').strip() == '#' or
                arrival.get('url') != url or not arrival_ok(arrival)):
            bad.append('travel')
        if (target.get('kind') == 'table' or target.get('tableOnly')) and not travel.get('inTable'):
            bad.append('table_click')
        prefix = target.get('paragraphPrefix')
        if prefix and 'paragraphText' in travel and not travel['paragraphText'].startswith(prefix):
            bad.append('compatibility_click')
    if case.get('focusParagraph'):
        p = record.get('focusedParent', {})
        if not p.get('exists') or p.get('insideList') or plain(p.get('text', '')) != case['focusParagraph']:
            bad.append('placeholder')
    if case.get('targetOutline'):
        outline = record.get('targetOutline', [])
        if ([v.get('id') for v in outline] != case['targetOutline'] or
                any(v.get('count') != 1 or not re.fullmatch(r'H[1-6]', v.get('tag') or '') for v in outline)):
            bad.append('hierarchy')
        elif any(int(v['tag'][1:]) != int(outline[0]['tag'][1:]) + 1 for v in outline[1:]):
            bad.append('hierarchy')
    if case.get('navTargets'):
        links = [x for x in record.get('sidebarProbe', []) if x.get('visible') and x.get('x', 9999) < 320]
        a, b = ([x for x in links if x['path'] == path] for path in case['navTargets'])
        if len(a) != 1 or len(b) != 1 or a[0].get('textX') is None or b[0].get('textX') is None or b[0]['textX'] <= a[0]['textX']:
            bad.append('sidebar')
    return sorted(set(bad))


def check_results(bundle, runs, bundle_sha):
    if not re.fullmatch(r'[1-9][0-9]*', str(bundle['major'])) or not isinstance(bundle['source_commit'], str) or not bundle['source_commit'].strip():
        raise ValueError('Supply a manual major and reviewed source_commit string')
    cases = {c['name']: c for c in bundle['cases']}
    if not cases or len(cases) != len(bundle['cases']):
        raise ValueError('Specify nonempty unique cases')
    records, issues = {}, []
    for run in runs:
        if (run.get('status') != 'complete' or run.get('bundle_sha256') != bundle_sha or
                str(run.get('major')) != str(bundle['major']) or run.get('source_commit') != bundle['source_commit'] or
                run.get('origin') != bundle['origin']):
            issues.append('Incomplete run or mismatched bundle/source provenance')
        names = run.get('cases_requested', [])
        actual = [r.get('screenshot', '').removesuffix('.png') for r in run.get('results', [])]
        if len(names) != len(set(names)) or len(actual) != len(set(actual)) or set(actual) != set(names):
            issues.append('Run result coverage differs from requested cases')
        for name, record in zip(actual, run.get('results', [])):
            if name not in cases or name in records:
                issues.append('Unexpected or duplicate result: ' + name)
            records[name] = record
    failures = {name: compare_case(case, records.get(name), origin=bundle['origin']) for name, case in cases.items()}
    failures = {name: why for name, why in failures.items() if why}
    return dict(status='complete', origin=bundle['origin'], major=str(bundle['major']),
                source_commit=bundle['source_commit'], bundle_sha256=bundle_sha,
                passed=not issues and not failures, cases=len(cases), collected=len(records),
                provenance_errors=issues, failures=failures,
                declared_content_fields={name: sorted(c.get('expected', {})) for name, c in cases.items()})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', required=True)
    parser.add_argument('--results', nargs='+', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--root', default='.')
    args = parser.parse_args()
    raw = Path(args.bundle).read_bytes()
    bundle = json.loads(raw.decode('utf-8-sig'))
    if not Path(args.out).resolve().is_relative_to(Path(args.root).resolve() / 'outputs'):
        parser.error('Evidence must be below workspace outputs')
    if Path(args.out).exists():
        parser.error('Use a new report path; retain previous evidence')
    try:
        report = check_results(bundle, [read_json(p) for p in args.results], digest(raw))
    except Exception as error:
        atomic_json(args.out, dict(status='failed', passed=False, source_commit=bundle.get('source_commit'),
                                   bundle_sha256=digest(raw), error=str(error)))
        raise
    atomic_json(args.out, report)
    print(json.dumps({k: v for k, v in report.items() if k != 'declared_content_fields'}, ensure_ascii=False))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
