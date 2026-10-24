---
name: postgresql-tw-translation
description: Translate and review PostgreSQL manuals in Traditional Chinese for the pgsql-tw documentation project. Use for manual chapter translation, version alignment, terminology, or publication-format and navigation maintenance; not for general SQL advice.
---

Translate against the PostgreSQL major version named by the working branch. Confirm the branch and repository before applying project-specific paths. The observed baseline is branch `15` of `C:/Workspaces/gitbook-docs`, commit `9e1029c`, examined on 2026-09-06; do not assume later branches have identical contents.

Read [references/style.md](references/style.md) when translating or reviewing prose. It distinguishes observed conventions from editorial recommendations and records source files.
Before new translation, semantic review, or investigating a suspected official erratum, read [references/source-validation.md](references/source-validation.md) to distinguish authoritative source text from conversion artifacts. Purely mechanical maintenance need not load it unless the repair raises a source-content question.

## Select the working mode

Choose the mode from the user's requested outcome; do not turn maintenance into a new translation or a full semantic re-review without authorization.

- **New translation:** Confirm the target version and source, agree on the batch's prose style, and review the complete translated scope. Before each new translation batch, present concise Traditional Chinese style options using the same representative source excerpt, wait for the user's choice, then record and apply it. This style-choice gate applies to new translation, not mechanical maintenance or a revision that retains the approved style.
- **Revision re-review:** Compare the revised submission with its prior version, all same-page rejection reasons, applicable user rulings, and valid prior review coverage. Read [references/review-workflow.md](references/review-workflow.md) before reviewing or resubmitting revisions. Retain the approved style unless the user requests a style change.
- **Formatting/navigation maintenance:** Preserve technical prose and protected content; scope changes to markup, structure, links, or navigation. Check content preservation and actual public rendering when applicable. Do not ask for a fresh prose-style choice or claim a new semantic approval merely because maintenance checks pass. If a technical-content choice becomes necessary, separate it from the mechanical repair and obtain direction where required.

Read the repository's collaboration protocol and applicable user decisions before translation, review, or publication. In this project's PostgreSQL 18 checkout, the protocol is `outputs/pg18-translation/agents/PROTOCOL.md`; verify that path in the current repository rather than assuming it exists in every checkout. The skill does not grant permission to submit externally, publish, commit, or push.

## Work page by page with chapter context

Translate and review one page at a time; reading the whole manual first is not required. The manual is reference material whose pages are largely self-contained, and most review findings concern sentence-level precision against the official text. Cross-page problems come from terminology drift, repeated sentence patterns, navigation titles, and repeated passages; handle them with the two steps below instead of a full-manual pre-read.

- **Before starting a new chapter or page family:** read the chapter's README/overview and two or three already published neighboring pages. Note the terms, title forms, and recurring sentence patterns they use. For repetitive page families (catalog, view, and information-schema column tables; reference command and client-application pages; release notes; contrib modules), settle a representative pattern from published pages before translating the rest, and record it in the batch's working notes. The manual's own guides, such as the documentation style guide and the error-message style guide in the appendices, explain the source authors' intent for terms such as *should*/*must* and for callouts; consult them when a wording choice depends on that intent.
- **After finishing a batch:** sweep the batch and its neighboring published pages for consistency. Search for different renderings of the same concept, for repeated sentences or descriptions that were revised in one place only, and for page TOCs, chapter READMEs, and navigation entries whose titles no longer match their target headings. Align new pages with the established neighboring usage. Report conflicts that affect published pages or would require a site-wide change for a decision under the project protocol; do not batch-replace terminology across the site.

## Select the publishing target

Determine the publishing target from the user's request and repository guidance/configuration, independently of the working mode. The current project target is GitBook, as recorded in `AGENTS.md`; this is a project setting, not a permanent restriction of this skill.

- **GitBook:** For output formatting, navigation repair, or publication acceptance, read [references/gitbook-maintenance.md](references/gitbook-maintenance.md). Apply its renderer-specific guidance only to GitBook output.
- **Other targets:** Do not assume GitBook's anchor, hierarchy, path, or rendering behavior applies. Establish that target's build/navigation/acceptance requirements; add a focused target reference only when a concrete target is introduced. Do not create speculative target implementations. If the target is unclear and materially affects the work, clarify it before target-specific edits.

## Shared translation and preservation rules

- Use the official `/docs/<major>/` manual as the technical authority. Record the minor-version baseline and retrieval date in the work report. A page copied from `/current/` or an older manual is not evidence of target-version correctness.
- Preserve the source's conditions, exceptions, warnings, tables, syntax, examples, and cross-references. Existing fluent Chinese may still describe obsolete behavior. Check version-sensitive claims before reusing them.
- Prefer existing local relative Markdown links for translated targets; use version-pinned official links for untranslated targets. Preserve existing paths unless restructuring is requested. Update the publishing target's navigation manifests, page headings, and affected cross-references together when adding or renumbering sections.
- Preserve frontmatter, structured callouts, HTML tables, images, anchor IDs, and code fences according to the selected publishing target. Inspect adjacent pages for their actual markup conventions; do not flatten these structures while polishing prose.
- Keep SQL keywords, API identifiers, parameter names, object names, and executable examples exact. Explain them in Chinese prose without translating identifiers.
- Preserve original code verbatim, including apparent source errors. Explain a verified source defect in a Traditional Chinese translator's note outside the code block; do not silently repair protected code or describe an unverified suspicion as a confirmed erratum. Follow the project's applicable rulings when review requirements conflict with this preservation rule.
- An English heading, a Markdown file, or a Chinese introduction does not establish translation completion. Distinguish missing pages, title-only leaf pages, navigation containers, untranslated prose, mixed translation, and translated content requiring version review. A missing SUMMARY entry may be existing content that needs relocation rather than a new translation.
- Runtime verification must use the target major version; a locally available version cannot establish another major version's semantics. Documentation-only work does not require database mutations.
- Run the project's applicable deterministic checks before submission. Investigate failures against actual content and accepted exceptions rather than declaring every lint finding a rejection or forcing blanket zero counts. A tool pass proves only the checks performed, not semantic approval; see the source-validation reference for counter limitations.
- For completion review, compare the touched sections with their matching official sections; verify numbering, examples, relative links, and preserved target-specific structures. Report exactly what remains untranslated or unverified.
