"""Matched real reviewer A/B; isolated snapshots, no publication or translation."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import types

import translation_pipeline as new
from translation_controller import atomic, read, digest

ROOT = Path(__file__).resolve().parents[1]
PAGE = 'appendixes/contrib/passwordcheck.md'
SNAPSHOT = ROOT / new.RUNTIME / 'pages' / digest(PAGE)[:20]


def main():
    run = ROOT / 'outputs/pg18-translation/token-flow-review' / ('ab-' + str(time.time_ns()))
    run.mkdir(parents=True)
    code = subprocess.check_output(['git', '-C', str(ROOT), 'show',
                                    '9a2b72b5:scripts/translation_pipeline.py'], encoding='utf-8')
    old = types.ModuleType('benchmark_old_pipeline')
    old.__file__ = str(ROOT / 'scripts/translation_pipeline.py')
    exec(compile(code, old.__file__, 'exec'), old.__dict__)
    report = dict(page=PAGE, baseline_commit='9a2b72b5',
                  new_code_sha256=digest(read(ROOT / 'scripts/translation_pipeline.py')),
                  cli=subprocess.check_output(['codex', '--version'], encoding='utf-8').strip(),
                  settings='same existing CLI defaults; read-only; no model/reasoning override', runs={})
    for label, module in [('old', old), ('new', new)]:
        queue = module.Queue(run / label)
        folder = queue.workdir(PAGE)
        shutil.copytree(SNAPSHOT / 'draft', folder / 'draft')
        state = json.loads(read(SNAPSHOT / 'manifest.json'))
        state['reviews'] = []
        state.pop('review_context_hash', None)
        candidate = read(folder / 'draft' / PAGE)
        report['source'] = state['source']
        report['candidate_sha256'] = digest(candidate)
        report['policy_sha256'] = state['policy_hash']
        call = queue.call
        def recorded_call(page, role, prompt, schema):
            atomic(folder / ('prompt-' + str(time.time_ns()) + '.json'), dict(prompt=prompt, schema=schema))
            return call(page, role, prompt, schema)
        queue.call = recorded_call
        start = time.monotonic()
        error = None
        issues = None
        try:
            issues = queue.review(PAGE, state, candidate)
        except Exception as exc:
            error = repr(exc)
        finally:
            queue.db.close()
        calls = []
        for logfile in sorted(folder.glob('*-reviewer.jsonl')):
            events = []
            for line in read(logfile).splitlines():
                try:
                    events.append(json.loads(line))
                except ValueError:
                    pass
            usages = [e['usage'] for e in events if e.get('type') == 'turn.completed']
            calls.append(dict(log=str(logfile.relative_to(run)), usage=usages,
                              commands=sum(e.get('type') == 'item.completed' and
                                           e.get('item', {}).get('type') == 'command_execution' for e in events)))
        totals = {k: sum(u.get(k, 0) for c in calls for u in c['usage'])
                  for k in ['input_tokens', 'cached_input_tokens', 'output_tokens', 'reasoning_output_tokens']}
        totals['uncached_input_tokens'] = totals['input_tokens'] - totals['cached_input_tokens']
        report['runs'][label] = dict(seconds=round(time.monotonic()-start, 2), calls=calls,
                                     totals=totals, issues=issues, error=error,
                                     reviews=state['reviews'])
        atomic(run / 'report.json', report)
        print(json.dumps(dict(mode=label, totals=totals, issues=issues, error=error, report=str(run / 'report.json'))), flush=True)
        if error:
            raise RuntimeError(error)


if __name__ == '__main__':
    main()
