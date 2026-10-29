---
name: prepare-recitation
description: Use when preparing the next CS301 recitation in this repository, drafting or approving its weekly layout, developing its course page and notebooks, or finalizing the resulting materials for a Git commit.
---

# Prepare a CS301 Recitation

Turn the agreed lecture coverage into a reviewed layout, complete practice
materials, a generated static page and notebooks, validation evidence, and an
authorized local commit. Run commands from the repository root. This is a local
course-material workflow, not a general website builder or publishing workflow.

## Read the current contracts

Read these live files before selecting content or editing generators:

- [AGENTS.md](../../../AGENTS.md): source maps, static-site rules, privacy, and checks.
- [DesignPrincipal.md](../../../material/DesignPrincipal.md): teaching and timing principles.
- [WeeklyContent.md](../../../material/WeeklyContent.md): fixed syllabus and separate Extra Content.
- The target `material/weekN/` and the most recent completed recitation's source,
  builder, notebooks, and code contracts. Recitation 2 is the current mixed
  written/coding example; use it as a reference rather than copying its three-question
  count or merge-specific requirements into every session.

Check Git status first. Preserve existing user edits, saved notebook work, and
unrelated files. Read only course-relevant material; `application/` is private.

## 1. Establish coverage and draft the layout

Use the topics explicitly requested by the user. Tuesday recitation normally
covers the previous week's latter half plus the current week's lectures delivered
before the session. Follow actual lecture progress; do not assume everything
listed under the current syllabus week has already been taught. Week 1–7 lecture
content in `WeeklyContent.md` is fixed; preparing a recitation does not authorize
rewriting it. Extra Content is TA-provided, optional, and not examined.

Write an English `material/weekN/Layout.md` with:

- Scope, prerequisites, and a few observable learning goals.
- Proposed page order and a short concept review.
- Core exercises: format, purpose, expected reasoning, and estimated minutes.
  Target approximately 30 minutes for the core practice path, excluding review,
  discussion, and questions. Choose the mix of written/application/coding work by
  learning goals, not by equal counts or a universal LeetCode difficulty quota.
- Clearly separated optional practice, feedback/discussion, and an exit check.
- What will be created after approval, including the intended notebook delivery.

When the request is layout-first, deliver this file and wait for its review before
writing full problems or changing the website. Existing approval in the conversation
satisfies this boundary: “没问题，继续” starts development without another permission
round. Respect explicit requests to skip layout review.

## 2. Develop the approved materials

Expand the approved scope into concise notes and complete exercises: statements,
examples, constraints, interfaces, staged hints, reference explanations, and code
where relevant. Explain correctness and cost under stated assumptions; re-derive
traces, sums, recurrences, and expected outputs before publishing them.

Use a shared maintained prose source to keep webpage and notebook prompts aligned.
Follow the repository's source/build pipeline; do not hand-edit generated HTML or
notebooks. Keep source code and contracts under `material/weekN/solutions/` and
reusable notebook checks alongside the week's material. Reuse the existing design
system and code-tab/editor helpers instead of rebuilding them.

For coding exercises, retain the site's six supported languages unless the user
sets a different scope. Provide matching stubs, references, and harnesses. Derive
edge cases from each contract: empty/minimal inputs, duplicates, boundaries,
input preservation, and large inputs where complexity matters. Distinguish
working space from output storage. Written questions need explanations, not six
translations or artificial coding requirements.

## 3. Generate notebooks and integrate the page

- Generate Python and Java notebooks from the same notes/prompts and their stubs.
  Keep reference answers on the webpage, initially collapsed; do not embed them in
  practice notebooks. Include runnable self-checks for coding tasks.
- Use **Markdown cells** for written responses, including coding explanations and
  reflection prompts. Provide short answer scaffolds without code fences; do not
  make students convert comment-only code cells to Markdown themselves.
- Every opening Markdown code fence declares its language. Use `python`, `java`,
  etc.; use `text`/`plaintext` for untyped material and exactly `pseudocode` for
  pseudocode. Closing fences remain bare. Preserve these labels in the shared
  HTML-to-Markdown converter, including blocks that only have a visible language label.
- Preserve internal-link labels during notebook conversion; webpage fragment ids
  may not work as notebook anchors. Check rendered prompts, not just valid JSON.
- Keep executable cells only for executable work; assign the correct kernel and
  initialize new code cells without saved outputs. Preserve existing user work in
  unrelated notebooks. Normalize string/list `source` representations when comparing
  notebook content so serialization changes do not erase user edits or results.
- Add notebook download links only after the artifacts exist. The website displays
  and copies code; it does not execute or grade it. Retain temporary draft behavior.
- Update the page builder, `site_layout.py`, and Home's directory. Check **Home's top
  `.hero-slots` badges as well**: all available recitations must be highlighted there,
  not just in the directory or navigation. The current Home hero is hand-authored in
  `site/index.html`; `build_site.py` replaces only its header and directory. Update
  that maintained badge markup (or its source if the pipeline later changes).
  Keep unassigned sessions as placeholders.
- Update README's material inventory and AGENTS' source map/checks when affected;
  synchronize Introduction HTML/Markdown if their information changes. Keep developer
  commands out of README. Update validation assumptions that hard-code old notebook,
  page, tab, or problem counts when introducing another recitation.

## 4. Verify the actual deliverables

Rebuild affected artifacts. Use current commands from AGENTS; extend existing
checks to the new session rather than validating only an older recitation:

- `python3 tools/site_src/build_site.py` — full site/notebook generation.
- `python3 tools/site_src/check_site.py --strict-links` — require zero errors/warnings.
- `python3 tools/site_src/test_notebook_format.py` — language-tagged fences and
  Markdown answer cells; update its expected inventory for new notebook artifacts.
- `bash tools/verify_notebooks.sh` — verify shipped notebook checks with references;
  untouched stubs must fail as expected, not pass vacuous checks. State whether Java
  was checked by compilation or in a live IJava kernel; do not conflate them.
- The relevant solution harnesses (`verify_all.sh` for Week 1 and `verify_week2.sh`
  for Week 2 currently); add the new week's equivalent when needed.
- `node tools/site_src/test_code_ui.cjs` — cover the new page's drafts, copy/reset,
  synchronized language selection, collapsed answers, navigation, and no-JS access.

Inspect desktop/mobile screenshots of changed pages, including Home availability,
and render the final notebooks to inspect prose, hints, answer cells, and code
labels. Store previews only in `.tmp/`. Remove compiled artifacts from source/site
folders, check C# source copies, and verify the final inventory against real files.

If a builder overwrites unrelated saved notebook work, preserve that work and
verify the final artifact's relevant cell sources; do not silently replace it with
a clean generated copy. Record exact commands/results and limits: automated checks
are not student-machine installation tests or empirical timing calibration.

## 5. Review and commit within authorization

Present the local page/notebook links and validation results for user review.
Apply requested corrections through the sources, then rebuild and recheck affected
outputs. This review stage is still part of producing the materials.

A request to prepare or approve materials alone does **not** authorize Git changes.
When the user authorizes committing (including earlier in the current task), inspect
`git status`, stage only related materials/sources/generated outputs/docs, and run
`git diff --cached --check`. Exclude private files, `.tmp/`, and build artifacts.
Create a descriptive local commit, then verify its hash and working-tree status.

If the user asks to include a correction in the same commit, verify HEAD is the
intended task commit and amend it with `git commit --amend --no-edit`; preserve
unrelated changes. Report the new hash because amendment changes it. Do not amend
another task's commit or rewrite shared history without authorization.

Commit authorization does not imply push or deployment authorization. Push only
when explicitly requested; Pages then publishes only `site/`. Finish with the
artifact links, actual checks/results, commit hash when applicable, and whether
anything remains uncommitted or unpushed. Do not auto-commit the skill itself.
