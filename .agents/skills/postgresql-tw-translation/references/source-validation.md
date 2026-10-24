# Source provenance and deterministic checks

Use this reference for new translation, semantic review, or a suspected source defect. It supplements the shared skill; it does not authorize a full retranslation during a formatting-only task.

## Establish which source is authoritative

- A repository page or extracted English baseline is a converted snapshot, not independent proof of the official text. Conversion can lose superscripts, escape characters, images, table structure, or fence boundaries. NBSP and line-ending differences alone do not establish a content error.
- Compare suspect material with the version-pinned official page. If that page cannot be accessed, use an official source-tree revision matched to the intended release where possible, recording the file, revision, and version limitations. A moving `REL_<major>_STABLE` branch is not proof of the same minor-release snapshot without a matching revision.
- Distinguish an official defect from a conversion artifact. Correct a conversion artifact within the authorized source/format-maintenance scope; do not label it as an official erratum. A confirmed official defect follows the project's code-preservation and external translator-note rules.
- For an older translated baseline, compare against the target-version official text rather than treating footer and terminology updates as a completed new translation. If a full retranslation would exceed the task, report that scope change instead of silently expanding the work.

## Write accurate translator's notes

- Check surrounding prose, related tables, and the target-version implementation or catalog definition where needed to substantiate a claim. Match the note's scope to that evidence; do not turn a conditional statement into an unconditional one.
- Keep notes outside protected code and tables. For ordinary prose, choose a clearly identified parenthetical or separate note that remains readable; do not mandate one placement across all contexts or publishing targets.
- On example-heavy pages, check examples against stated prerequisites such as declared variables, included headers, transaction state, and consistent identifiers or paths. Findings are candidates to substantiate, not permission to repair protected source code.
- When changing a repeated description or note, search the same page and relevant navigation for equivalent occurrences. Update only the confirmed affected scope, not unrelated terminology across the site.

## Use deterministic checks without mistaking them for authority

- Use the structural and lint tools applicable to the current repository and working mode. In the PostgreSQL 18 checkout, these include `scripts/agent_handoff.py`, pipeline structural checks, and `scripts/zh_lint.py`; inspect their current interfaces before use. Classify tool errors, legitimate findings, and accepted exceptions explicitly; do not disable checks or alter content merely to obtain zero findings.
- Check protected inline spans and HTML code as well as fenced blocks. Simple backtick regexes can misparse multi-backtick or multiline spans, normalize meaningful whitespace, or return incomplete coverage. Verify the current implementation and supplement it with exact extraction/parser checks where necessary; do not hard-code a historical limitation as permanent tool behavior.
- Protect multiplicities and relevant ordering. Record justified structural changes separately instead of hiding them in broad normalization or adding/removing formatting solely to satisfy a counter. A justified navigation addition may require an explicit expected delta.
- Preserve source-verification dates unless the source was actually rechecked. Submission timestamps and content hashes describe the new submission; they do not establish a new official-source retrieval date.
