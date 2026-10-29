# Recitation 2 Implementation Plan

> **For agentic workers:** Implement inline with superpowers:executing-plans.

**Goal:** Deliver the approved Recitation 2 notes, exercises, six-language merge
references, Python/Java practice notebooks, and generated static page.
**Architecture:** Author prose in `tools/site_src/recitation2-content.html`, reuse
existing code tabs and HTML-to-notebook markdown helpers, and keep merge code in
`material/week2/solutions/p3/`. One builder generates the page and notebooks.
**Tech Stack:** Static HTML/CSS/JS; standard-library Python builders and tests;
existing C/C++/.NET/Java/Python/Node toolchains.
**Spec:** `material/week2/Layout.md`, approved in chat; use `material/DesignPrincipal.md`.

## Constraints and review focus

- Core path is 6 + 8 + 16 minutes; optional work is separate; no DP or new exam claims.
- Explain valid versus tight bounds, case versus notation, and recurrence assumptions.
- Empty arrays, duplicates, unequal lengths, leftover tails, and input preservation
  must work in all six languages; large interleaved inputs exercise the linear path.
- Browsers only display/edit code; no execution or draft persistence. Keep no-JS access.
- Notebooks contain prompts/stubs/self-checks but no reference answers; run actual
  shipped checks with reference code and verify untouched stubs fail.
- Keep Recitations 3–7 unassigned, existing user edits intact, and publishing authorized
  separately. No commits or pushes in this task.

## Tasks

- [x] 1. Write merge contracts and six-language harnesses; observe stub failure;
  implement merge references and scaffolds. Verify with `bash tools/verify_week2.sh`.
- [x] 2. Author complete notes, three core exercises, two optional exercises, staged
  hints, worked explanations, and discussion/exit check. Build HTML and notebooks
  from shared prose using `tools/site_src/build_recitation2.py`.
- [x] 3. Integrate site navigation, directory, structural/browser checks, documentation,
  and notebook verification. Rebuild and run strict site QA, the existing 36 harnesses,
  week2 harnesses, notebook checks, and browser UI regression; inspect captures.
- [x] 4. Independently review instructional correctness and integration, resolve material
  findings, and report validation accurately. Do not equate runtime checks with timing
  calibration on students.

## Validation record

- Six new merge harnesses: passed (110 cases each, including a 200,000-element merge).
- Existing Week 1 harnesses: all 36 passed.
- Shipped notebook self-checks pass with references and fail with untouched stubs.
- Strict site QA and the expanded Chrome UI suite pass; mobile/desktop captures inspected.
- Independent read-only review found lost core-path labels in notebook conversion.
  Added a regression assertion, observed failure, preserved fragment-link labels as
  plain text, and verified the check passes. No material instructional/code findings.
- The original Recitation 1 Python notebook is preserved after validation; its
  saved user content differs from a fresh generator build. No source change to it
  is part of this task. Student timing remains an estimate rather than a tested claim.
