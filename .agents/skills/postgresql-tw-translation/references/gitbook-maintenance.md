# GitBook formatting, navigation, and publication acceptance

Read this reference only when the publishing target is GitBook and the task concerns output formatting, navigation, or publication acceptance. These are project-tested observations and verification practices, not universal Markdown rules or guarantees about every GitBook version. Technical semantics and user rulings remain governed by the shared skill and project protocol.

## Diagnose the actual output before broad repairs

- A valid local Markdown parse, an existing source ID, or an HTTP 200 does not establish that the published page renders correctly. Classify the suspect target: page root, section heading, function/parameter entry, caption, table note, or cross-page reference.
- Confirm a representative defect in the actual published output before extending a repair pattern. Preserve the source/commit baseline, observed public URL, relevant rendered content, and interaction evidence. Discover public routes from actual navigation or verified responses; source file layout alone does not establish the published path.
- GitBook has rendered indented definition-list continuations as code, including literal fences, Chinese prose, and raw Markdown links. Check container boundaries and continuation indentation, not merely balanced backtick counts. Nested callouts, multiple examples, lists, and following paragraphs can be swallowed into the same block.
- The current project has successfully used lowercase custom aliases attached to source H2/H3 headings while retaining original uppercase IDs. Deeper source headings and standalone/nonheading IDs have not behaved equivalently. Verify the selected pattern on the actual target; do not assume an ID exists because the hash changes or an alias works elsewhere.
- Distinguish preserved source anchors from renderer-compatible aliases. Keep an original heading anchor associated with its heading and avoid inserting an unrelated note between them; do not move a working inline alias above the heading to satisfy a blanket placement rule. Separate adjacent anchors or `<br>` markup only when the applicable parser or rendered evidence justifies it, preserving IDs and target association.
- Definition-list continuation indentation is context-dependent. Neither "four spaces always works" nor "eight spaces always fails" is a safe GitBook rule. Check list nesting, container boundaries, fences, and actual output; place translator's notes outside protected examples and verify that they render as prose.
- A source heading level is not necessarily the rendered DOM heading level. Inspect actual IDs and structure rather than inferring behavior from heading tag names alone. An official section without an ID must not acquire a guessed "required official" anchor.

## Preserve hierarchy and navigation when repairing

- Do not promote every function or parameter to the same level as its parent merely to obtain a working anchor. When a verified shallow-heading pattern cannot preserve the hierarchy, split at the existing semantic section boundary within the authorized restructuring scope.
- For a split, keep a meaningful entry in the original page, add a return path, preserve section numbering and original IDs, and update `SUMMARY.md`, relevant chapter README navigation, and affected local references together. Check nested order and depth, not just whether the new file appears in the menu.
- For aliases or moved targets, inventory and update references by exact destination file plus fragment outside protected code. Preserve the original IDs, but do not claim that retaining them creates a working redirect for old public URLs. Test legacy URLs separately when compatibility is required.
- Preserve frontmatter, hints, tables, captions, footnotes, and source/version notes. A formatting repair must not silently become a terminology rewrite or a new semantic translation.
- If a converted page lost an official figure, visually compare the intended figure with available project assets (including `.gitbook/assets/`) before reuse. Choose Markdown or HTML figure markup for correct target rendering and semantics, not to bypass a protected-link counter. Record the asset provenance, intended structural delta, alt text/caption, and public rendering check; do not invent empty captions or assume an asset with a similar name is the same figure.
- Change table-break markup only when official structure or a demonstrated rendering defect warrants it; do not mechanically replace every `<br>` with `<br class="table-break" />`. Row-per-line table formatting is optional: verify unchanged tags, attributes, cell content, order, and rendered output where affected, not just tag counts.

## Protect the source before committing

- Compare fenced code contents byte-for-byte within the project's agreed newline/encoding convention, including comments, indentation, and ordering. When content moves across files, reconstruct each original source family in original order; per-file block counts alone cannot prove preservation.
- Check inline-code multiplicities, HTML tables, IDs, and prose order. Account explicitly for permitted navigation additions and markup changes. Where practical, reverse the exact allowed transformations and compare with the baseline instead of applying broad whitespace or punctuation normalization.
- Validate local link destinations and fragments, unique IDs, navigation membership/order, and parser boundaries. Ensure genuine fences are recognized as code and surrounding prose is not parsed as indented code. Do not alter protected examples to make a renderer or a test pass.
- Keep exact change scope and distinguish original source pages, added child pages, and supporting reference/navigation files. A full-site static scan and source-preservation tests are separate from published rendering acceptance; report their limitations separately.

## Verify the published result

- Establish which commit reached the repository's publication branch, then separately verify that the public page contains the expected changed content. A remote commit or a "synced" indicator alone is not page-level rendering evidence.
- Exercise repaired targets at desktop and narrow widths. For actual clicks, check the chosen link, destination URL/fragment, target existence and uniqueness, and target position in the viewport. For direct fragment loads, record arrival position before any diagnostic scrolling. Changing the hash without finding the element is a failure.
- Test entry/return paths and representative cross-page references affected by the repair. Distinguish exhaustive target testing from sampled reference testing; report the actual coverage rather than extrapolating it to all links.
- Compare rendered code contents and sequence, table rows/cells, and relevant lists with their expected contents. GitBook DOM text can add blank lines: any normalization must be explicit and narrow, preserving nonempty lines, indentation, identifiers, and order. Do not call a normalized DOM comparison byte-for-byte source equality.
- Inspect representative screenshots, particularly long code/table pages and narrow layouts. DOM checks do not replace visual inspection, and screenshots obscured by cookie dialogs do not prove that hidden content is correct. Distinguish intentional block-level horizontal scrolling from whole-page overflow.
- Include regression checks for adjacent or previously repaired structures that the change could affect. Do not infer full chapter or site acceptance from a repaired subset.

## Handle inconsistent loads and report honestly

- If a public load shows older content, preserve the original evidence and perform a bounded normal reload/recheck. Record which observation is used for the final result; do not overwrite failed evidence or repeatedly retry without a stopping condition. Do not assert a CDN/cache cause without supporting diagnostics or alter GitBook sync/settings merely to resolve an unexplained observation.
- Compare unexpected rendering with the saved pre-change public output and source diff to distinguish a newly introduced regression from a pre-existing defect. Normalize only the exact permitted differences when making that comparison, not arbitrary text or code changes.
- Report source preservation, static validation, published navigation, rendered content, visual checks, and outstanding defects as distinct results. An anchor pass with a code-layout or menu failure is partial acceptance, not "all passed."
- Keep failed assertions visible. If a test selected the wrong source link or misread parser behavior, correct the test against evidence and disclose that correction; do not relax checks merely to obtain green results.
- State the reviewed commit, scope, evidence location, untested areas, and whether any new commit exists. If no new commit was made, do not ask the user to push again. Verification does not grant permission to push, merge a change request, or change publication settings.
