"""Isolated regression probe; no model calls or production repository writes."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
import agent_handoff as h
from test_agent_handoff import Tests, TARGET, PAGE
from translation_pipeline import Queue

fixture = Tests()
fixture.setUp()
try:
    # Negate the instruction without changing any protected markup.
    candidate = TARGET.replace('請先設定', '請勿設定')
    fixture.submit(candidate)
    queue = Queue(fixture.root)
    try:
        queue.init()
        result = h.publish(fixture.root, publisher='publish-inbox-structural',
                           reviewer=lambda root, meta, candidate: [])
        queue.sync_collaborators()
        row = queue.db.execute('SELECT phase FROM pages WHERE path=?', (PAGE,)).fetchone()
        print(json.dumps(dict(outcome=result[0]['outcome'], pending=h.pending_state(fixture.root, PAGE),
                              queue_phase=row['phase'], model_calls=0,
                              semantic_error='Set PGHOST first translated as do not set PGHOST'),
                         ensure_ascii=False))
        assert row['phase'] == 'review_required', 'Unreviewed legacy publication must not be complete'
    finally:
        queue.db.close()
finally:
    fixture.doCleanups()
    fixture.tearDown()
