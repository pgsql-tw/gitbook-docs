---
name: postgresql-tw-translation
description: Translate and review PostgreSQL manuals in Traditional Chinese for the pgsql-tw GitBook project. Use for manual chapter translation, version alignment, terminology, or GitBook chapter maintenance; not for general SQL advice.
---

Translate against the PostgreSQL major version named by the working branch. Confirm the branch and repository before applying project-specific paths. The observed baseline is branch `15` of `C:/Workspaces/gitbook-docs`, commit `9e1029c`, examined on 2026-09-06; do not assume later branches have identical contents.

Read [references/style.md](references/style.md) when translating or reviewing prose. It distinguishes observed conventions from editorial recommendations and records source files.

## Select the working mode

Choose the mode from the user's requested outcome; do not turn maintenance into a new translation or a full semantic re-review without authorization.

- **New translation:** Confirm the target version and source, agree on the batch's prose style, and review the complete translated scope. Before each new translation batch, present concise Traditional Chinese style options using the same representative source excerpt, wait for the user's choice, then record and apply it. This style-choice gate applies to new translation, not mechanical maintenance or a revision that retains the approved style.
- **Revision re-review:** Compare the revised submission with its prior version, all same-page rejection reasons, applicable user rulings, and valid prior review coverage. Read [references/review-workflow.md](references/review-workflow.md) before reviewing or resubmitting revisions. Retain the approved style unless the user requests a style change.
- **Formatting/navigation maintenance:** Preserve technical prose and protected content; scope changes to markup, structure, links, or navigation. Check content preservation and actual public rendering when applicable. Do not ask for a fresh prose-style choice or claim a new semantic approval merely because maintenance checks pass. If a technical-content choice becomes necessary, separate it from the mechanical repair and obtain direction where required.

Read the repository's collaboration protocol and applicable user decisions before translation, review, or publication. In this project's PostgreSQL 18 checkout, the protocol is `outputs/pg18-translation/agents/PROTOCOL.md`; verify that path in the current repository rather than assuming it exists in every checkout. The skill does not grant permission to submit externally, publish, commit, or push.

## Shared translation and preservation rules

- Use the official `/docs/<major>/` manual as the technical authority. Record the minor-version baseline and retrieval date in the work report. A page copied from `/current/` or an older manual is not evidence of target-version correctness.
- Preserve the source's conditions, exceptions, warnings, tables, syntax, examples, and cross-references. Existing fluent Chinese may still describe obsolete behavior. Check version-sensitive claims before reusing them.
- Prefer existing local relative Markdown links for translated targets; use version-pinned official links for untranslated targets. Preserve existing paths unless restructuring is requested. Update `SUMMARY.md`, the page heading, and affected cross-references together when adding or renumbering sections.
- Preserve GitBook frontmatter, hint blocks, HTML tables, images, anchor IDs, and code fences. Inspect adjacent pages for their actual markup conventions; do not flatten these structures while polishing prose.
- Keep SQL keywords, API identifiers, parameter names, object names, and executable examples exact. Explain them in Chinese prose without translating identifiers.
- Preserve original code verbatim, including apparent source errors. Explain a verified source defect in a Traditional Chinese translator's note outside the code block; do not silently repair protected code or describe an unverified suspicion as a confirmed erratum. Follow the project's applicable rulings when review requirements conflict with this preservation rule.
- An English heading, a Markdown file, or a Chinese introduction does not establish translation completion. Distinguish missing pages, title-only leaf pages, navigation containers, untranslated prose, mixed translation, and translated content requiring version review. A missing SUMMARY entry may be existing content that needs relocation rather than a new translation.
- For this project, PostgreSQL 15 checks must use PostgreSQL 15 if runtime verification is needed. A locally available PostgreSQL 18 instance cannot establish PostgreSQL 15 semantics. Documentation-only work does not require database mutations.
- For completion review, compare the touched sections with their matching official sections; verify numbering, examples, relative links, and preserved GitBook structures. Report exactly what remains untranslated or unverified.
