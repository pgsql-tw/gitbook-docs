"""Single-page pilot: durable progress, bounded CLI retries and review-gated commit.

No scheduler is installed. The existing heartbeat must not write during a run.
Runtime state is deliberately outside the set of files this program commits.
"""
import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

PAGE = 'appendixes/contrib/ltree.md'
TRACKERS = ['SUMMARY.md', 'outputs/pg18-translation/pending-pages.md',
            'outputs/pg18-translation/continuation-state.md']
RUNTIME = 'outputs/pg18-translation/controller-runtime'


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def read(path):
    return Path(path).read_text(encoding='utf-8-sig')


def atomic(path, value):
    path = Path(path)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(temp, path)


@contextmanager
def exclusive(path):
    """OS releases the lock on crash; an old lock file is not a stale lock."""
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


def invariants(text):
    fences = re.findall(r'^\s*```[^\n]*\n(.*?)^\s*```\s*$', text, re.M | re.S)
    # ltree's first three fences are syntax + explanatory prose, not executable SQL.
    for i in range(min(3, len(fences))):
        fences[i] = '\n'.join(line.strip().split()[0] for line in fences[i].splitlines() if line.strip())
    return {
        'fences': fences,
        'markdown_code': Counter(re.findall(r'`([^`\n]+)`', re.sub(r'^\s*```[^\n]*\n.*?^\s*```\s*$', '', text, flags=re.M | re.S))),
        'inline_code': re.findall(r'<code\b[^>]*>.*?</code>', text, re.S),
        'anchors': re.findall(r'\bid="([^"]+)"', text),
        'tags': [re.sub(r'\s+summary="[^"]*"', '', tag) for tag in
                 re.findall(r'</?(?:table|thead|tbody|tr|td|th)\b[^>]*>', text)],
        'links': re.findall(r'\]\(([^)]+)\)', text),
    }


def structural_errors(baseline, current):
    before, after = invariants(baseline), invariants(current)
    errors = []
    for key in before:
        # Adding the missing page-level anchor is permitted; removing anchors is not.
        if key == 'anchors':
            if any(a not in after[key] for a in before[key]):
                errors.append('removed anchor')
        elif before[key] != after[key]:
            errors.append('changed protected ' + key)
    if '英文原文，待翻譯' in current:
        errors.append('untranslated marker remains')
    for anchor in re.findall(r'\]\((?:ltree.md)?#([^)]+)\)', current):
        if anchor not in after['anchors']:
            errors.append('missing local anchor: ' + anchor)
    return errors


class Controller:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.runtime = self.root / RUNTIME
        self.runtime.mkdir(parents=True, exist_ok=True)
        self.statefile = self.runtime / 'state.json'

    def git(self, *args):
        p = subprocess.run(['git', '-C', str(self.root), *args], capture_output=True,
                           encoding='utf-8', errors='replace')
        if p.returncode:
            raise RuntimeError(p.stderr.strip() or p.stdout.strip())
        return p.stdout.strip()

    def emit(self, event, **fields):
        record = dict(time=datetime.now(timezone.utc).isoformat(), event=event, page=PAGE, **fields)
        try:
            with (self.runtime / 'events.jsonl').open('a', encoding='utf-8') as f:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        except OSError as error:
            # Reporting an access error must not itself crash on the same access error.
            record['event_log_error'] = str(error)
        print(json.dumps(record, ensure_ascii=False), flush=True)

    def state(self):
        return json.loads(read(self.statefile))

    def save(self, state):
        atomic(self.statefile, state)

    def fail(self, reason):
        state = self.state()
        state.update(phase=reason, last_error=reason)
        self.save(state)
        self.emit(reason)

    def init(self):
        if self.statefile.exists():
            return self.state()
        text = read(self.root / PAGE)
        state = dict(page=PAGE, phase='translating', initial=text, last_hash=digest(text),
                     initial_hash=digest(text), no_progress=0, approval=None,
                     start_head=self.git('rev-parse', 'HEAD'))
        self.save(state)
        self.emit('started', sha256=state['last_hash'])
        return state

    def observe(self):
        state = self.state()
        current = digest(read(self.root / PAGE))
        changed = current != state['last_hash']
        if changed:
            state.update(last_hash=current, no_progress=0, approval=None, phase='translating')
        else:
            state['no_progress'] += 1
            if state['no_progress'] >= 2:
                state['phase'] = 'failed_no_progress'
        self.save(state)
        self.emit('candidate_change' if changed else 'no_progress', sha256=current,
                  consecutive=state['no_progress'])
        return changed

    def approve(self, expected_hash, note):
        state = self.state()
        current = read(self.root / PAGE)
        if digest(current) != expected_hash:
            raise RuntimeError('review hash is stale')
        errors = structural_errors(state['initial'], current)
        if errors:
            raise RuntimeError('; '.join(errors))
        if digest(current) == state['initial_hash']:
            raise RuntimeError('no translation change since initialization')
        if not note.strip():
            raise RuntimeError('semantic review evidence required')
        self.git('diff', '--check', '--', PAGE)
        state.update(phase='reviewed', approval={'sha256': expected_hash, 'note': note})
        self.save(state)
        self.emit('reviewed', sha256=expected_hash, note=note)

    def finalize(self):
        state = self.state()
        approval = state.get('approval')
        if not approval:
            raise RuntimeError('full-page semantic review required before commit')
        text = read(self.root / PAGE)
        if digest(text) != approval['sha256']:
            raise RuntimeError('file changed after review')
        marker = 'Translation-Page-SHA256: ' + approval['sha256']
        previous = self.git('log', '--format=%H', '--fixed-strings', '--grep=' + marker,
                            state['start_head'] + '..HEAD')
        if previous:
            commit = previous.splitlines()[0]
            committed = subprocess.run(['git', '-C', str(self.root), 'show', commit + ':' + PAGE],
                                       capture_output=True, encoding='utf-8', check=True).stdout
            if digest(committed) != approval['sha256']:
                raise RuntimeError('commit trailer does not match committed page')
            state.update(phase='completed', commit=commit)
            self.save(state)
            self.emit('reconciled', commit=commit)
            return commit
        if self.git('diff', '--cached', '--name-only'):
            raise RuntimeError('index is not empty; preserve existing staged work')
        pending = read(self.root / TRACKERS[1])
        if f'- [x] `{PAGE}`' not in pending:
            raise RuntimeError('pending list has not been marked complete')
        remaining = len(re.findall(r'^- \[ \]', pending, re.M))
        if f'待譯頁面：{remaining} 頁。' not in pending:
            raise RuntimeError('pending count is inconsistent')
        errors = structural_errors(state['initial'], text)
        if errors:
            raise RuntimeError('; '.join(errors))
        paths = [PAGE, *TRACKERS]
        self.git('diff', '--check', '--', *paths)
        state['phase'] = 'committing'
        self.save(state)
        self.git('add', '--', *paths)
        staged = set(self.git('diff', '--cached', '--name-only').splitlines())
        if not staged.issubset(set(paths)) or PAGE not in staged:
            raise RuntimeError('unexpected staged paths; inspect index before retry')
        self.git('commit', '-m', '文件(pg18)：翻譯 ltree', '-m', marker)
        commit = self.git('rev-parse', 'HEAD')
        state.update(phase='completed', commit=commit)
        self.save(state)
        self.emit('completed', commit=commit, remaining=remaining)
        return commit

    def run_cli(self, attempts=2, timeout=900):
        """Translation-only subprocess. Never lets model self-approve or commit."""
        if self.state()['phase'] in ('reviewed', 'completed', 'committing'):
            raise RuntimeError('page is already reviewed or committed; do not run translator again')
        exe = shutil.which('codex')
        if not exe:
            raise RuntimeError('codex executable unavailable')
        auth = subprocess.run([exe, 'login', 'status'], capture_output=True, timeout=30)
        if auth.returncode:
            # This is contextual: a sandbox may not see the desktop/CLI credential store.
            # Do not diagnose the user's account as logged out from this result alone.
            self.fail('failed_auth')
            return False
        schema = Path(__file__).with_name('translation-result.schema.json')
        prompt = (
            f'Translate only {PAGE} completely into Traditional Chinese. Preserve existing work. '
            'Read C:/Users/ycku/.codex/skills/postgresql-tw-translation/SKILL.md and references/style.md. '
            'User explicitly chose existing 技術直述 style, do not ask style questions. '
            'Verify against https://www.postgresql.org/docs/18/ltree.html. '
            'Preserve SQL, examples, HTML tables, anchors, links and identifiers. Translate explanatory '
            'prose in syntax examples too. Ensure every local # anchor link resolves; add missing '
            'page-level LTREE anchor if necessary. Use apply_patch. Do not edit any other file, commit, '
            'spawn workers or change automations. Return remaining sections honestly. '
            'You are translation-only; completion will be reviewed separately.'
        )
        for attempt in range(attempts):
            tag = str(time.time_ns())
            events = self.runtime / (tag + '.jsonl')
            result = self.runtime / (tag + '.result.json')
            self.emit('worker_started', attempt=attempt + 1, events=str(events))
            with events.open('w', encoding='utf-8') as output:
                p = subprocess.Popen([exe, 'exec', '--sandbox', 'workspace-write', '--json',
                    '--output-schema', str(schema), '-o', str(result), '-C', str(self.root), '-'],
                    stdin=subprocess.PIPE, stdout=output, stderr=subprocess.STDOUT,
                    text=True, encoding='utf-8')
                try:
                    p.communicate(prompt, timeout=timeout)
                except subprocess.TimeoutExpired:
                    if os.name == 'nt':
                        subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True)
                    else:
                        p.kill()
                    p.wait()
                    self.fail('worker_timeout')
                    return False
            changed = self.observe()
            if p.returncode:
                self.fail('worker_failed')
                return False
            try:
                response = json.loads(read(result))
                if (response['status'] not in ('partial', 'candidate_complete', 'blocked')
                        or not isinstance(response['remaining'], list)
                        or not all(isinstance(x, str) for x in response['remaining'])
                        or not isinstance(response['summary'], str)):
                    raise ValueError('invalid structured result')
            except (OSError, ValueError, KeyError, TypeError):
                self.fail('invalid_worker_result')
                return False
            if response['status'] == 'blocked':
                self.fail('worker_blocked')
                return False
            if changed:
                if response['status'] == 'candidate_complete' and not response['remaining']:
                    errors = structural_errors(self.state()['initial'], read(self.root / PAGE))
                    if errors:
                        self.emit('validation_rejected', errors=errors)
                        prompt += '\nPrevious candidate failed mechanical checks. Repair these: ' + '; '.join(errors)
                        continue
                    state = self.state()
                    state['phase'] = 'awaiting_review'
                    self.save(state)
                    self.emit('review_required', result=str(result))
                    return True
                self.emit('continue_immediately', remaining=response['remaining'])
            if self.state()['no_progress'] >= 2:
                self.emit('failed_no_progress')
                return False
        self.fail('attempt_budget_exhausted')
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['init', 'observe', 'status', 'check', 'run', 'approve', 'finalize'])
    parser.add_argument('--root', default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument('--sha256')
    parser.add_argument('--note', default='')
    args = parser.parse_args()
    controller = Controller(args.root)
    try:
        if args.action in ('status', 'check'):
            state = controller.state()
            if args.action == 'check':
                errors = structural_errors(state['initial'], read(controller.root / PAGE))
                print(json.dumps({'errors': errors}, ensure_ascii=False))
                return 1 if errors else 0
            state.pop('initial', None)
            print(json.dumps(state, ensure_ascii=False, indent=2))
            return 0
        with exclusive(controller.runtime / 'writer.lock'):
            if args.action == 'init':
                controller.init()
            elif args.action == 'observe':
                controller.observe()
            elif args.action == 'run':
                controller.init()
                return 0 if controller.run_cli() else 2
            elif args.action == 'approve':
                controller.approve(args.sha256, args.note)
            else:
                controller.finalize()
    except Exception as e:
        controller.emit('failed', reason=str(e))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
