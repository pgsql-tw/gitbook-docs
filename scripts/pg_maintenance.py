"""Small IO and input-consistency primitives for read-only audits and planned edits."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import time
from contextlib import contextmanager
from collections import deque
import threading


def digest(data):
    return hashlib.sha256(data).hexdigest()


def atomic_write(path, data):
    """Readers see the old complete file or the new complete file, never truncation."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.' + path.name + '.', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if path.exists():
            os.chmod(temporary, path.stat().st_mode)
        for attempt in range(6):
            try:
                os.replace(temporary, path)
                break
            except PermissionError:
                if attempt == 5:
                    raise
                time.sleep(0.02)  # Bounded Windows reader-sharing contention, not a task retry.
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


_io_condition = threading.Condition()
_io_queues = {}


@contextmanager
def json_io_lock(path):
    key, ticket = os.path.normcase(str(Path(path).resolve())), object()
    with _io_condition:
        queue = _io_queues.setdefault(key, deque())
        queue.append(ticket)
        _io_condition.wait_for(lambda: queue[0] is ticket)
    try:
        with _json_file_lock(path):
            yield
    finally:
        with _io_condition:
            queue.popleft()
            if not queue:
                del _io_queues[key]
            _io_condition.notify_all()


@contextmanager
def _json_file_lock(path):
    """Coordinate our readers/writers; external busy handles still fail boundedly."""
    lock = Path(str(path) + '.io.lock')
    for attempt in range(10):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            break
        except FileExistsError:
            if attempt == 9:
                raise TimeoutError('JSON IO lock busy: ' + str(lock))
            time.sleep(0.02)
    try:
        yield
    finally:
        os.close(fd)
        lock.unlink()


def atomic_json(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with json_io_lock(path):
        atomic_write(path, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def read_json(path):
    """Bounded sharing-error tolerance on Windows; malformed JSON is never hidden."""
    for attempt in range(6):
        try:
            with json_io_lock(path):
                return json.loads(Path(path).read_text(encoding='utf-8-sig'))
        except (PermissionError, FileNotFoundError):
            if attempt == 5:
                raise
            time.sleep(0.02)


class InputSnapshot:
    """Cache the bytes actually read and detect changed/missing inputs at completion.

    Inventory suppliers cover additions/removals, including files not yet in Git.
    They must be read-only and return workspace-relative names.
    """
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.data = {}
        self.inventories = {}

    def key(self, path):
        path = Path(path)
        path = (self.root / path).resolve() if not path.is_absolute() else path.resolve()
        if not path.is_relative_to(self.root):
            raise ValueError('Audit input escapes workspace: ' + str(path))
        return path.relative_to(self.root).as_posix()

    def capture(self, paths):
        for path in paths:
            key = self.key(path)
            if key not in self.data:
                p = self.root / key
                self.data[key] = p.read_bytes() if p.is_file() else None

    def text(self, path):
        key = self.key(path)
        self.capture([path])
        data = self.data[key]
        if data is None:
            raise FileNotFoundError(self.root / key)
        return data.decode('utf-8-sig').replace('\r\n', '\n')

    def inventory(self, name, supplier):
        values = sorted(set(supplier()))
        self.inventories[name] = (values, supplier)
        return values

    def verify(self):
        changed = []
        hashes = {}
        for key, before in sorted(self.data.items()):
            path = self.root / key
            after = path.read_bytes() if path.is_file() else None
            hashes[key] = digest(before) if before is not None else None
            if after != before:
                changed.append(dict(path=key, before=hashes[key],
                                    after=digest(after) if after is not None else None))
        inventories = []
        for name, (before, supplier) in self.inventories.items():
            after = sorted(set(supplier()))
            if before != after:
                inventories.append(dict(name=name, added=sorted(set(after) - set(before)),
                                        removed=sorted(set(before) - set(after))))
        return dict(valid=not changed and not inventories, input_sha256=hashes,
                    changed_inputs=changed, inventory_changes=inventories)
