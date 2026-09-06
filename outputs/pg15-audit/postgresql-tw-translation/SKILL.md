---
name: postgresql-tw-translation
description: Translate and review PostgreSQL manuals in Traditional Chinese for the pgsql-tw GitBook project. Use for manual chapter translation, version alignment, terminology, or GitBook chapter maintenance; not for general SQL advice.
---

Translate against the PostgreSQL major version named by the working branch. Confirm the branch and repository before applying project-specific paths. The observed baseline is branch `15` of `C:/Workspaces/gitbook-docs`, commit `9e1029c`, examined on 2026-09-06; do not assume later branches have identical contents.

Read [references/style.md](references/style.md) when translating or reviewing prose. It distinguishes observed conventions from editorial recommendations and records source files.

- Use the official `/docs/<major>/` manual as the technical authority. Record the minor-version baseline and retrieval date in the work report. A page copied from `/current/` or an older manual is not evidence of target-version correctness.
- Preserve the source's conditions, exceptions, warnings, tables, syntax, examples, and cross-references. Existing fluent Chinese may still describe obsolete behavior. Check version-sensitive claims before reusing them.
- Prefer existing local relative Markdown links for translated targets; use version-pinned official links for untranslated targets. Preserve existing paths unless restructuring is requested. Update `SUMMARY.md`, the page heading, and affected cross-references together when adding or renumbering sections.
- Preserve GitBook frontmatter, hint blocks, HTML tables, images, anchor IDs, and code fences. Inspect adjacent pages for their actual markup conventions; do not flatten these structures while polishing prose.
- Keep SQL keywords, API identifiers, parameter names, object names, and executable examples exact. Explain them in Chinese prose without translating identifiers.
- An English heading, a Markdown file, or a Chinese introduction does not establish translation completion. Distinguish missing pages, title-only leaf pages, navigation containers, untranslated prose, mixed translation, and translated content requiring version review. A missing SUMMARY entry may be existing content that needs relocation rather than a new translation.
- For this project, PostgreSQL 15 checks must use PostgreSQL 15 if runtime verification is needed. A locally available PostgreSQL 18 instance cannot establish PostgreSQL 15 semantics. Documentation-only work does not require database mutations.
- For completion review, compare the touched sections with their matching official sections; verify numbering, examples, relative links, and preserved GitBook structures. Report exactly what remains untranslated or unverified.
