# Version-neutral project tools

Use `python scripts/pg_project.py` before interpreting project paths. It reports the target PostgreSQL major version and selected translation root; `--relative` prints just the relative root for shell wrappers. Resolve `<translation-root>` in the skill's evidence examples against this result.

- New projects use `outputs/pg-translation`. A single existing version-labelled translation directory is supported in place, preserving historical evidence, absolute paths inside archived drafts, and the shared publisher lock. If both the new root and an older root exist, or multiple older roots exist, stop and reconcile them; do not choose one silently or start a competing queue.
- The target major normally comes from a numeric Git branch such as `18` or `19`. For read-only tools on another branch, an explicit `pg-project.json` containing `{"major": 19}` identifies the target. A conflicting numeric branch/configuration is an error. Publishing still requires the numeric target-version branch; configuration does not authorize publishing from a feature branch.
- Use separate checkouts and translation state for separate manual versions. Do not reuse another major's source snapshot, queue approval, or rendered acceptance. The pipeline rejects a cached official source URL pinned to a different major.
- Submission URLs must use `https://www.postgresql.org/docs/<major>/`; redirects outside that prefix are rejected. A generic `pg` name does not remove version validation or turn historical evidence from one version into proof for another.
- Commit subjects use `文件(pg)：…`. Source provenance, major/minor labels, official URLs, historical commit messages, and manual-specific rulings retain their actual version information.
- The maintained skill lives in `.agents/skills/postgresql-tw-translation` inside the project. Do not depend on a collaborator's absolute home-directory skill path.

The naming change does not authorize moving or rewriting archived submissions, nested Git repositories, other agents' status files, public manual routes, or historical audit scripts. Those artifacts remain attached to their original source/version and can still be located through the selected translation root. New reusable code and newly generated state use the neutral naming convention.
