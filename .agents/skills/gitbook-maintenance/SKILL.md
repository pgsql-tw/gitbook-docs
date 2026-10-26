---
name: gitbook-maintenance
description: Maintain this project's GitBook formatting, navigation, links, and publication rendering. Use for GitBook page and structure changes or rendering verification; this project is not a translation workflow.
---

# GitBook maintenance

Read [references/gitbook-maintenance.md](references/gitbook-maintenance.md) for formatting, anchors, navigation, content preservation, and published rendering acceptance.

## Project context

- Repository: `https://github.com/pgsql-tw/gitbook-docs.git`, branch `master`. Verify the current checkout before changes.
- `book.json` sets the content root to `./tw`. Inspect the actual navigation and adjacent pages before choosing paths or markup.
- This is a GitBook website maintenance project, not a manual translation project. Do not import translation style selection, PostgreSQL 18 collaboration protocols, worker claims, or translation review gates from the source project.
- The reference was copied from `docs.pgsql.18` (`C:/Workspaces/gitbook-docs/.agents/skills/postgresql-tw-translation/references/gitbook-maintenance.md`) on 2026-10-26. Its renderer observations are candidates to verify here, not proof of this site's behavior.
- Translation, official-manual comparison, and new-manual pilot passages in the reference apply only if a future task explicitly introduces that scope. For ordinary website maintenance, preserve the existing content and use the relevant formatting/navigation checks.
- Confirm publication URLs and setup from repository evidence or the user before public verification. Local validation does not establish published rendering success.
- This skill does not authorize pushing, publishing, or changing GitBook settings.
