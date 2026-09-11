"""多代理交接：認領（claims）、送件（inbox）、單一發佈者提交（publish）。

PostgreSQL 18 翻譯由多個 AI 代理並行。只有 publisher 會修改真實 checkout 中的
受追蹤檔案並 commit；其他代理把譯稿放進 inbox，由本程式檢查後代為提交。
提交與 translation_pipeline.py 共用 pipeline-runtime/publish.lock，彼此序列化。

協定全文：outputs/pg18-translation/agents/PROTOCOL.md

  python scripts/agent_handoff.py status
  python scripts/agent_handoff.py claim --agent codex --page appendixes/contrib/ltree.md
  python scripts/agent_handoff.py claimed-by --page tutorial/tutorial-start/tutorial-install.md
  python scripts/agent_handoff.py validate            # 只檢查 inbox，不寫任何受追蹤檔
  python scripts/agent_handoff.py publish [--agent claude] [--limit N] [--dry-run]
  python scripts/agent_handoff.py message --from codex --to claude --subject 主旨 --body 內容

在 pipeline 中使用：
  from agent_handoff import is_claimed_by_other, claim, publish
"""
import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

BASE = 'outputs/pg18-translation'
AGENTS = BASE + '/agents'
PENDING = BASE + '/pending-pages.md'
SUMMARY = 'SUMMARY.md'
LOCK = BASE + '/pipeline-runtime/publish.lock'
MARKER = '英文原文，待翻譯'
SOURCE_PREFIX = 'https://www.postgresql.org/docs/18/'
TZ = timezone(timedelta(hours=8))
DEFAULT_TTL_HOURS = 12
IDENTITIES = {
    'claude': 'Claude <noreply@anthropic.com>',
    'codex': None,  # 沿用本機 git 設定（ycku）
}
AGENT_RE = re.compile(r'^[a-z][a-z0-9-]{1,30}$')
PAGE_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_./-]*\.md$')
TRAILER_RE = re.compile(r'^[A-Za-z][A-Za-z-]*: \S.*$')


# ---------- 基本工具 ----------

def now():
    return datetime.now(TZ)


def stamp(dt=None):
    return (dt or now()).isoformat(timespec='seconds')


def read(path):
    """與 translation_controller.read 相同：去除 BOM，換行正規化為 LF。"""
    return Path(path).read_text(encoding='utf-8-sig')


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def read_styled(path):
    """讀取並記住原檔的 BOM 與換行風格，寫回時保持一致以減少雜訊差異。"""
    raw = Path(path).read_bytes()
    bom = raw.startswith(b'\xef\xbb\xbf')
    crlf = b'\r\n' in raw
    return read(path), (bom, crlf)


def write_styled(path, text, style=(False, False)):
    bom, crlf = style
    if crlf:
        text = text.replace('\r\n', '\n').replace('\n', '\r\n')
    data = (b'\xef\xbb\xbf' if bom else b'') + text.encode('utf-8')
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_bytes(data)
    os.replace(temp, path)


def write_json(path, value):
    write_styled(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def check_page(page):
    if not PAGE_RE.match(page) or '..' in page.split('/') or page.startswith('outputs/'):
        raise ValueError('invalid page path: ' + page)
    return page


def check_agent(agent):
    if not AGENT_RE.match(agent or ''):
        raise ValueError('invalid agent name: %r' % agent)
    return agent


def slug(page):
    return check_page(page).replace('/', '__')


def git(root, *args, check=True):
    p = subprocess.run(['git', '-C', str(root), *args], capture_output=True,
                       encoding='utf-8', errors='replace')
    if check and p.returncode:
        raise RuntimeError('git %s: %s' % (args[0], (p.stderr or p.stdout).strip()))
    return p.stdout.strip()


@contextmanager
def exclusive(path):
    """與 translation_controller.exclusive 相同語意：OS 在崩潰時自動釋放。"""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from translation_controller import exclusive as shared
    except Exception:  # 控制器不存在時的後備實作
        shared = None
    if shared is not None:
        with shared(Path(path)):
            yield
        return
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as f:
        f.seek(0, 2)
        if f.tell() == 0:
            f.write(b'0')
            f.flush()
        f.seek(0)
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            f.seek(0)
            if os.name == 'nt':
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)


# ---------- 待譯清單 ----------

def pending_lines(text):
    return re.findall(r'^- \[([ x~])\] `([^`]+)`', text, re.M)


def pending_state(root, page):
    for mark, path in pending_lines(read(Path(root) / PENDING)):
        if path == page:
            return {' ': 'todo', 'x': 'done', '~': 'todo'}[mark]
    return None


def todo_pages(root):
    return [p for m, p in pending_lines(read(Path(root) / PENDING)) if m != 'x']


def page_title(text):
    heading = next(l for l in text.splitlines() if l.startswith('#'))
    return re.sub(r'\s*\[#\]\(#[^)]+\)', '', heading).lstrip('# ').strip()


def mark_done(pending, page, title):
    def repl(m):
        suffix = ' #' if m.group(1).rstrip().endswith(' #') else ''
        return f'- [x] `{page}` — {title}{suffix}'
    pending, count = re.subn(r'^- \[[ ~]\] `' + re.escape(page) + r'`(.*)$', repl, pending, flags=re.M)
    if count != 1:
        raise RuntimeError('pending list has no unique open line for ' + page)
    remaining = len(re.findall(r'^- \[[ ~]\]', pending, re.M))
    pending, n = re.subn(r'待譯頁面：\d+ 頁。', f'待譯頁面：{remaining} 頁。', pending)
    if n != 1:
        raise RuntimeError('pending count line not found')
    return pending, remaining


def retitle_summary(summary, page, title):
    def repl(m):
        suffix = ' #' if m.group(1).rstrip().endswith(' #') else ''
        return f'[{title}{suffix}]({page})'
    summary, count = re.subn(r'\[([^\n]*?)\]\(' + re.escape(page) + r'\)', repl, summary)
    if count < 1:
        raise RuntimeError('SUMMARY.md has no entry for ' + page)
    return summary


# ---------- 認領 ----------

def claims_dir(root):
    return Path(root) / AGENTS / 'claims'


def load_claim(root, page):
    path = claims_dir(root) / (slug(page) + '.json')
    if not path.exists():
        return None
    try:
        return json.loads(read(path))
    except (OSError, ValueError):
        return {'agent': '?', 'expires_at': stamp(now() + timedelta(hours=1)), 'broken': True}


def claim_owner(root, page, at=None):
    """回傳持有有效認領的代理名稱；無認領或已過期則回傳 None。"""
    item = load_claim(root, page)
    if not item or item.get('status') == 'released':
        return None
    try:
        expires = datetime.fromisoformat(item['expires_at'])
        if expires.tzinfo is None:
            return item.get('agent') or '?'
    except (KeyError, ValueError):
        return item.get('agent')
    return item.get('agent') if expires > (at or now()) else None


def is_claimed_by_other(root, page, me):
    owner = claim_owner(root, page)
    return owner is not None and owner != me


def claim(root, page, agent, ttl_hours=DEFAULT_TTL_HOURS, note=''):
    with exclusive(Path(root) / BASE / 'pipeline-runtime/claims.lock'):
        return _claim(root, page, agent, ttl_hours, note)


def _claim(root, page, agent, ttl_hours=DEFAULT_TTL_HOURS, note=''):
    """原子地建立認領；他人有效認領或頁面已完成時丟出 RuntimeError。"""
    check_agent(agent)
    state = pending_state(root, page)
    if state != 'todo':
        raise RuntimeError(f'{page} is not open in pending list ({state})')
    owner = claim_owner(root, page)
    if owner and owner != agent:
        raise RuntimeError(f'{page} already claimed by {owner}')
    folder = claims_dir(root)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (slug(page) + '.json')
    old = load_claim(root, page) or {}
    value = dict(page=page, agent=agent, status='active', claimed_at=old.get('claimed_at', stamp()) if owner == agent else stamp(),
                 expires_at=stamp(now() + timedelta(hours=ttl_hours)), note=note)
    if not path.exists():
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        except FileExistsError:
            raise RuntimeError(f'{page} was claimed concurrently; re-check')
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    else:
        write_json(path, value)  # 自己續期，或接手過期認領
    if old.get('agent') and old['agent'] != agent:
        message(root, agent, old['agent'], '接手過期認領', f'`{page}` 的認領已過期，由 {agent} 接續。')
    return value


def release(root, page, agent=None):
    with exclusive(Path(root) / BASE / 'pipeline-runtime/claims.lock'):
        return _release(root, page, agent)


def _release(root, page, agent=None):
    path = claims_dir(root) / (slug(page) + '.json')
    item = load_claim(root, page)
    if item and (agent is None or item.get('agent') == agent):
        path.unlink()


# ---------- 結構檢查（優先沿用 pipeline 的規則） ----------

def _fallback_structural_errors(baseline, current, page):
    def protected(text):
        fence = r'^([ \t]*)(`{3,}|~{3,})[^\n]*\n(.*?)^\1\2[ \t]*$'
        fences = re.findall(fence, text, re.M | re.S)
        outside = re.sub(fence, '', text, flags=re.M | re.S)
        tags = re.findall(r'</?(?:table|thead|tbody|tr|td|th|col|colgroup)\b[^>]*>', text)
        return dict(fences=[f[2] for f in fences],
                    inline=Counter(re.findall(r'`([^`\n]+)`', outside)),
                    html_code=re.findall(r'<code\b[^>]*>.*?</code>', text, re.S),
                    tags=[re.sub(r'\s+summary="[^"]*"', '', t) for t in tags],
                    links=Counter(re.findall(r'\]\(([^)]+)\)', text)),
                    anchors=Counter(re.findall(r'\bid="([^"]+)"', text)),
                    headings=len(re.findall(r'^#{2,6}\s', text, re.M)))
    a, b = protected(baseline), protected(current)
    errors = []
    for key in a:
        if key == 'anchors':
            if a[key] - b[key]:
                errors.append('missing original anchors')
        elif a[key] != b[key]:
            errors.append('changed protected ' + key)
    for link in b['links']:
        target, sep, anchor = link.partition('#')
        if sep and target in ('', Path(page).name) and anchor not in b['anchors']:
            errors.append('missing anchor ' + anchor)
    if MARKER in current:
        errors.append('untranslated marker remains')
    return errors


def inline_code_spans(text):
    """行內程式碼（容許跨單一換行，不跨空行），內部空白正規化後計數。

    pipeline 的檢查以 `[^`\n]+` 逐行配對，遇到跨行的行內程式碼（例如
    `pg_config\n--sharedir`）會把後續反引號配錯對，造成誤判。這裡依序配對
    反引號，只在兩者都一致時才撤銷該項誤判。
    """
    outside, last = [], 0
    for start, end, _ in code_fences(text):
        outside.append(text[last:start])
        last = end
    outside = ''.join(outside) + text[last:]
    spans = [m for m in re.findall(r'`([^`]*)`', outside)]
    if any('\n\n' in m for m in spans):
        return None
    return Counter(' '.join(m.split()) for m in spans if m.strip())


def code_fences(text):
    """正確解析圍欄程式碼區塊，包含開在定義清單行上的圍欄（`:   ```sql`）。

    回傳 (起點, 終點, 內容) 清單；起點位於反引號（不含前面的 `:   `），
    內容為開頭行之後到結束行之前的原文。pipeline 的正規表示式無法辨識
    定義清單行上的圍欄，會把之後的說明文字誤當成程式碼。
    """
    blocks, pos, open_ = [], 0, None
    for line in text.splitlines(keepends=True):
        body = line.rstrip('\n')
        if open_ is None:
            m = re.match(r'^([ \t]*(?::[ \t]+)?)(`{3,}|~{3,})', body)
            if m:
                open_ = (pos + len(m.group(1)), m.group(2), pos + len(line))
        else:
            m = re.match(r'^[ \t]*(`{3,}|~{3,})[ \t]*$', body)
            if m and m.group(1)[0] == open_[1][0] and len(m.group(1)) >= len(open_[1]):
                blocks.append((open_[0], pos + len(body), text[open_[2]:pos]))
                open_ = None
        pos += len(line)
    return blocks


def structural_errors(baseline, current, page):
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from translation_pipeline import structural_errors as shared
    except Exception:
        shared = None
    errors = shared(baseline, current, page) if shared else _fallback_structural_errors(baseline, current, page)
    errors = list(errors)
    if 'changed protected fences' in errors:
        if [b[2] for b in code_fences(baseline)] == [b[2] for b in code_fences(current)]:
            errors.remove('changed protected fences')
    if 'changed protected inline' in errors:
        a, b = inline_code_spans(baseline), inline_code_spans(current)
        if a is not None and a == b:
            errors.remove('changed protected inline')
    if MARKER in current and 'untranslated marker remains' not in errors:
        errors.append('untranslated marker remains')
    return errors


# ---------- inbox ----------

REQUIRED_META = ['page', 'agent', 'base_sha256', 'page_sha256', 'source_url', 'source_version',
                 'retrieved', 'submitted_at', 'self_review']


def inbox_dir(root, agent=None):
    base = Path(root) / AGENTS / 'inbox'
    return base / agent if agent else base


def inbox_items(root, agent=None):
    base = inbox_dir(root)
    if not base.exists():
        return []
    items = []
    for agent_dir in sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith(('_', '.'))):
        if agent and agent_dir.name != agent:
            continue
        for item in sorted(p for p in agent_dir.iterdir() if p.is_dir() and not p.name.startswith(('_', '.'))):
            if (item / 'meta.json').exists() and (item / 'page.md').exists():
                items.append(item)
    def order(item):
        try:
            return json.loads(read(item / 'meta.json')).get('submitted_at', '')
        except ValueError:
            return ''
    return sorted(items, key=order)


def validate(root, item):
    """回傳 (meta, candidate, errors)。不修改任何檔案。"""
    root = Path(root)
    errors = []
    try:
        meta = json.loads(read(item / 'meta.json'))
    except ValueError as e:
        return {}, '', ['meta.json is not valid JSON: %s' % e]
    missing = [k for k in REQUIRED_META if not meta.get(k)]
    if missing:
        errors.append('meta.json missing: ' + ', '.join(missing))
        return meta, '', errors
    try:
        page = check_page(meta['page'])
        check_agent(meta['agent'])
    except ValueError as e:
        return meta, '', [str(e)]
    if item.name != slug(page) or item.parent.name != meta['agent']:
        errors.append('inbox path does not match meta page/agent')
    candidate = read(item / 'page.md')
    if digest(candidate) != meta['page_sha256']:
        errors.append('page.md sha256 differs from meta.page_sha256')
    if not meta['source_url'].startswith(SOURCE_PREFIX):
        errors.append('source_url must be pinned to ' + SOURCE_PREFIX)
    for trailer in meta.get('trailers', []):
        if not TRAILER_RE.match(trailer) or '\n' in trailer:
            errors.append('invalid trailer: %r' % trailer)
    target = root / page
    if not target.is_file():
        errors.append('target page does not exist')
        return meta, candidate, errors
    state = pending_state(root, page)
    if state != 'todo':
        errors.append(f'page is not open in pending list ({state})')
    owner = claim_owner(root, page)
    if owner and owner != meta['agent']:
        errors.append('page is claimed by ' + owner)
    baseline = read(target)
    if digest(baseline) != meta['base_sha256']:
        errors.append('stale base: target page changed since the agent read it')
    errors += structural_errors(baseline, candidate, page)
    return meta, candidate, errors


def already_committed(root, sha):
    out = git(root, 'log', '-n', '400', '--format=%H', '--fixed-strings',
              '--grep=Translation-Page-SHA256: ' + sha)
    return out.splitlines()[0] if out else None


def move_item(item, bucket, extra):
    dest_root = item.parent / bucket
    dest_root.mkdir(parents=True, exist_ok=True)
    dest = dest_root / (item.name + '--' + now().strftime('%Y%m%dT%H%M%S'))
    shutil.move(str(item), str(dest))
    write_json(dest / 'result.json', extra)
    return dest


def message(root, sender, to, subject, body):
    check_agent(sender)
    if to != 'all':
        check_agent(to)
    folder = Path(root) / AGENTS / 'messages'
    folder.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r'[\\/:*?"<>|\s]+', '-', subject).strip('-')[:40] or 'note'
    name = f"{now().strftime('%Y%m%dT%H%M%S')}--{sender}--to-{to}--{safe}.md"
    text = (f'---\nfrom: {sender}\nto: {to}\ndate: {stamp()}\nsubject: {subject}\n---\n\n'
            f'{body.rstrip()}\n')
    write_styled(folder / name, text)
    return folder / name


def semantic_review(root, meta, candidate):
    from translation_pipeline import Queue
    queue = Queue(root)
    try:
        # Standalone publishers must use the same supervisor lock as the queue.
        with exclusive(queue.rt / 'supervisor.lock'):
            return queue.review_inbox(meta, candidate)
    finally:
        queue.db.close()


def publish(root, agent=None, dry_run=False, limit=None, publisher='codex', reviewer=None):
    """把 inbox 中通過檢查的譯稿逐頁提交；每頁一筆 commit。回傳結果清單。"""
    root = Path(root).resolve()
    results = []
    items = inbox_items(root, agent)
    if not items:
        return results
    lock = root / LOCK
    with exclusive(lock):
        if git(root, 'branch', '--show-current') != '18':
            raise RuntimeError('expected branch 18')
        if git(root, 'diff', '--cached', '--name-only'):
            raise RuntimeError('index is not empty; refusing to publish')
        for item in items[:limit] if limit else items:
            meta, candidate, errors = validate(root, item)
            page = meta.get('page', item.name)
            if meta.get('page_sha256') == digest(candidate) and PAGE_RE.fullmatch(page) and '..' not in page.split('/'):
                prior = already_committed(root, meta['page_sha256'])
                if prior and digest(git(root, 'show', prior + ':' + page) + '\n') == digest(candidate) and digest(read(root / page)) == digest(candidate):
                    if pending_state(root, page) != 'done':
                        raise RuntimeError('committed translation was reopened; reconcile list explicitly: ' + page)
                    results.append(dict(page=page, outcome='reconciled', commit=prior))
                    if not dry_run:
                        move_item(item, '_published', dict(page=page, commit=prior, at=stamp(), by=publisher,
                                                            outcome='reconciled'))
                        release(root, page)
                    continue
            if errors:
                results.append(dict(page=page, outcome='rejected', errors=errors))
                if not dry_run:
                    move_item(item, '_rejected', dict(page=page, errors=errors, at=stamp(), by=publisher))
                    if meta.get('agent') and PAGE_RE.fullmatch(page) and '..' not in page.split('/'):
                        release(root, page, meta['agent'])
                    if meta.get('agent'):
                        message(root, publisher, meta['agent'], f'退件 {Path(page).stem}',
                                f'`{page}` 未通過發佈檢查：\n\n' + '\n'.join('- ' + e for e in errors) +
                                '\n\n原件已移至 `inbox/%s/_rejected/`。' % meta['agent'])
                continue
            targets = [page, PENDING, SUMMARY]
            dirty = git(root, 'diff', '--name-only', '--', *targets)
            if dirty:
                raise RuntimeError('uncommitted changes in publish targets: ' + dirty.replace('\n', ', '))
            if dry_run:
                results.append(dict(page=page, outcome='would_publish'))
                continue
            review_errors = (reviewer or semantic_review)(root, meta, candidate)
            if review_errors:
                results.append(dict(page=page, outcome='review_rejected', errors=review_errors))
                move_item(item, '_rejected', dict(page=page, errors=review_errors, at=stamp(), by=publisher))
                release(root, page, meta['agent'])
                message(root, publisher, meta['agent'], '語意審查退件',
                        f'`{page}`：\n' + '\n'.join(review_errors))
                continue
            # Recheck after a potentially long review. A lock coordinates our
            # publishers, but cannot stop edits by an unrelated user/tool.
            latest_meta, latest_candidate, latest_errors = validate(root, item)
            if latest_errors or latest_meta != meta or latest_candidate != candidate:
                raise RuntimeError('inbox changed during semantic review; preserving item')
            if git(root, 'diff', '--cached', '--name-only') or git(root, 'diff', '--name-only', '--', *targets):
                raise RuntimeError('publish targets/index changed during review; preserving edits')
            title = page_title(candidate)
            pending, style_p = read_styled(root / PENDING)
            summary, style_s = read_styled(root / SUMMARY)
            _, style_page = read_styled(root / page)
            pending, remaining = mark_done(pending, page, title)
            summary = retitle_summary(summary, page, title)
            try:
                write_styled(root / page, candidate, style_page)
                write_styled(root / PENDING, pending, style_p)
                write_styled(root / SUMMARY, summary, style_s)
                git(root, 'diff', '--check', '--', *targets)
                git(root, 'add', '--', *targets)
                staged = set(git(root, 'diff', '--cached', '--name-only').splitlines())
                if not staged <= set(targets) or page not in staged:
                    raise RuntimeError('unexpected staged paths: %r' % sorted(staged))
                trailers = [f'Translation-Page: {page}',
                            f'Translation-Page-SHA256: {meta["page_sha256"]}',
                            f'Translated-By: {meta["agent"]}',
                            f'Source: {meta["source_url"]} ({meta["source_version"]}, {meta["retrieved"]})',
                            *meta.get('trailers', [])]
                args = ['commit', '-m', f'文件(pg18)：翻譯 {Path(page).stem}', '-m', '\n'.join(trailers)]
                author = meta.get('author') or IDENTITIES.get(meta['agent'])
                if author:
                    args.insert(1, '--author=' + author)
                git(root, *args)
            except Exception as error:
                # Preserve the exact working tree/index on failure. Never discard
                # user edits, including edits concurrent with the publisher.
                write_json(item / 'publish-failure.json', dict(page=page, targets=targets,
                           error=str(error), at=stamp(), page_sha256=meta['page_sha256']))
                raise
            commit = git(root, 'rev-parse', 'HEAD')
            move_item(item, '_published', dict(page=page, commit=commit, remaining=remaining,
                                                at=stamp(), by=publisher, outcome='published'))
            release(root, page)
            results.append(dict(page=page, outcome='published', commit=commit, remaining=remaining))
    return results


def status(root):
    root = Path(root)
    todo = todo_pages(root)
    claims = []
    if claims_dir(root).exists():
        for path in sorted(claims_dir(root).glob('*.json')):
            item = json.loads(read(path))
            item['valid'] = claim_owner(root, item['page']) == item.get('agent')
            claims.append(item)
    inbox = Counter(p.parent.name for p in inbox_items(root))
    buckets = {}
    base = inbox_dir(root)
    if base.exists():
        for agent_dir in base.iterdir():
            for bucket in ('_published', '_rejected'):
                d = agent_dir / bucket
                if d.exists():
                    buckets[f'{agent_dir.name}{bucket}'] = sum(1 for _ in d.iterdir())
    msgs = Counter()
    mdir = root / AGENTS / 'messages'
    if mdir.exists():
        for p in mdir.glob('*.md'):
            m = re.match(r'^\d{8}T\d{6}--[^-]+(?:-[^-]+)*?--to-([a-z0-9-]+)--', p.name)
            if m:
                msgs[m.group(1)] += 1
    return dict(remaining=len(todo), top=todo[:3], bottom=todo[-3:][::-1], claims=claims,
                inbox=dict(inbox), history=buckets, messages_by_recipient=dict(msgs))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('action', choices=['status', 'claim', 'release', 'claimed-by', 'validate',
                                           'publish', 'message'])
    parser.add_argument('--root', default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument('--agent')
    parser.add_argument('--page')
    parser.add_argument('--ttl-hours', type=float, default=DEFAULT_TTL_HOURS)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--publisher', default='codex')
    parser.add_argument('--from', dest='sender')
    parser.add_argument('--to')
    parser.add_argument('--subject', default='')
    parser.add_argument('--body', default='')
    args = parser.parse_args()
    root = Path(args.root)
    try:
        if args.action == 'status':
            out = status(root)
        elif args.action == 'claim':
            out = claim(root, check_page(args.page), args.agent, args.ttl_hours)
        elif args.action == 'release':
            release(root, check_page(args.page), args.agent)
            out = dict(released=args.page)
        elif args.action == 'claimed-by':
            out = dict(page=args.page, owner=claim_owner(root, check_page(args.page)),
                       pending=pending_state(root, args.page))
        elif args.action == 'validate':
            out = []
            for item in inbox_items(root, args.agent):
                meta, _, errors = validate(root, item)
                out.append(dict(item=str(item.relative_to(root)), page=meta.get('page'), errors=errors))
        elif args.action == 'publish':
            out = publish(root, args.agent, args.dry_run, args.limit, args.publisher)
        else:
            out = dict(file=str(message(root, args.sender, args.to, args.subject, args.body)))
    except Exception as error:
        print(json.dumps(dict(error=str(error)), ensure_ascii=False))
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if args.action == 'publish' and any(r['outcome'] == 'rejected' for r in out):
        return 3
    return 0


if __name__ == '__main__':
    sys.exit(main())
