# Temporary Code Editor Implementation Plan

**Goal:** Implement the code editing and highlighting design approved in chat.
**Architecture:** Existing app.js creates transient textarea editors for starter panels and highlights code using escaped lexical tokens; style.css aligns the textarea and preview. The exercise generator labels editable groups. No dependencies or extra published assets.
**Spec:** docs/superpowers/specs/2026-10-26-code-editor-design.md

- [x] Add a browser regression test and observe missing-editor failure.
- [x] Add six-language/pseudocode highlighting, editor input/indentation/scroll/reset/copy behavior, and refresh reset.
- [x] Update generator, notes script loading, student instructions, README and AGENTS.md.
- [x] Rebuild and run structural QA, browser behavior tests and desktop/mobile visual QA; check file inventory and whitespace.

Review focus: HTML-like input remains text; drafts are isolated by language/problem; copy reads current input; Tab does not trap focus; browser-restored form values do not survive refresh. Keep code sources and harnesses unchanged. Do not commit or publish.

Validation: browser regression first failed with 0 editors, then all UI checks passed; structural QA reported 0 errors / 0 warnings. Desktop and 390px screenshots inspected. Solution/stub/harness sources were not changed by this feature.
