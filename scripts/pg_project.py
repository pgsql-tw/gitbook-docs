"""Shared PostgreSQL project paths and version selection; no data migration."""
import argparse
import json
from pathlib import Path
import re
import subprocess

BASE = 'outputs/pg-translation'


def translation_root(root):
    root = Path(root).resolve()
    preferred = root / BASE
    # Existing evidence can contain nested Git repositories and absolute paths.
    # Discover it without renaming or copying it into a second publisher queue.
    legacy = [p for p in (root / 'outputs').glob('pg*-translation')
              if re.fullmatch(r'pg[0-9]+-translation', p.name)
              and ((p / 'agents/PROTOCOL.md').is_file() or (p / 'pending-pages.md').is_file())]
    candidates = ([preferred] if preferred.exists() else []) + legacy
    if len(candidates) > 1:
        raise ValueError('Multiple translation roots; reconcile them before running a publisher')
    selected = (candidates[0] if candidates else preferred).resolve()
    if not selected.is_relative_to(root):
        raise ValueError('Translation root must remain inside the project')
    return selected


def translation_path(root, suffix=''):
    return translation_root(root) / suffix


def translation_relative(root, suffix=''):
    return translation_path(root, suffix).relative_to(Path(root).resolve()).as_posix()


def major_version(root):
    root = Path(root)
    config = root / 'pg-project.json'
    configured = str(json.loads(config.read_text(encoding='utf-8-sig'))['major']) if config.exists() else None
    result = subprocess.run(['git', '-C', str(root), 'branch', '--show-current'],
                            capture_output=True, text=True, encoding='utf-8')
    branch = (result.stdout or '').strip() if result.returncode == 0 else ''
    numeric = branch if re.fullmatch(r'[1-9][0-9]*', branch) else None
    if configured and not re.fullmatch(r'[1-9][0-9]*', configured):
        raise ValueError('pg-project.json major must be a positive PostgreSQL major version')
    if configured and numeric and configured != numeric:
        raise ValueError('Configured PostgreSQL major differs from the version branch')
    if configured or numeric:
        return configured or numeric
    raise ValueError('Use a numeric version branch or set major in pg-project.json')


def source_prefix(root):
    return 'https://www.postgresql.org/docs/' + major_version(root) + '/'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument('--relative', action='store_true', help='Print only the selected relative storage path')
    args = parser.parse_args()
    if args.relative:
        print(translation_relative(args.root))
    else:
        print(json.dumps(dict(major=major_version(args.root),
                              translation_root=translation_relative(args.root),
                              default_translation_root=BASE), ensure_ascii=False))
