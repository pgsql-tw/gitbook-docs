"""Replay the saved pre-translation ltree in an isolated disposable repository.

Keeps the evidence directory for inspection. Does not commit a second translation
in the real repository or modify its completed page.
"""
import json
from pathlib import Path
import tempfile

from translation_controller import Controller, PAGE, TRACKERS, RUNTIME, exclusive, read


def main():
    root = Path(__file__).resolve().parents[1]
    state = json.loads(read(root / RUNTIME / 'state.json'))
    probe = Path(tempfile.mkdtemp(prefix='live-ltree-', dir=root / RUNTIME))
    page = probe / PAGE
    page.parent.mkdir(parents=True)
    page.write_text(state['initial'], encoding='utf-8')
    for path in TRACKERS:
        target = probe / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(read(root / path), encoding='utf-8')
    controller = Controller(probe)
    controller.git('init')
    controller.git('config', 'user.name', 'Translation Probe')
    controller.git('config', 'user.email', 'translation-probe@example.invalid')
    controller.git('add', '--', PAGE, *TRACKERS)
    controller.git('commit', '-m', 'ltree incomplete snapshot for live probe')
    print('LIVE_PROBE_ROOT=' + str(probe), flush=True)
    with exclusive(controller.runtime / 'writer.lock'):
        controller.init()
        return 0 if controller.run_cli() else 2


if __name__ == '__main__':
    raise SystemExit(main())
