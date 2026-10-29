# Modern Academic Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give every COMPSCI 301 page a polished modern-academic visual system and a more distinctive home page while preserving all content and interactions.

**Architecture:** Keep the static HTML/CSS/JS architecture and existing generators. Centralize the redesign in `site/assets/style.css`, add only structural classes/markup to the shared header and direct home page, then regenerate all derived pages.

**Tech Stack:** Static HTML, plain CSS, existing Python site builders, existing Node UI checks, headless Chrome.

**Spec:** `docs/superpowers/specs/2026-10-29-modern-academic-redesign-design.md`

## Global Constraints

- No frameworks, external fonts, CDNs, new theme dependencies, or publish-time build step.
- Preserve all course copy, links, anchors, local assets, notebook downloads, and editor behavior.
- Never edit generated recitation HTML directly; shared shell changes belong in `tools/site_src/site_layout.py`.
- Decorative effects use CSS and existing markup/assets; the publishable asset inventory stays unchanged.
- Keep keyboard focus, no-JavaScript behavior, responsive layouts, and reduced-motion support.
- Do not commit or push unless separately authorized.

## Review Focus

- Narrow mobile header and open Recitation dropdown: all controls remain visible and the dropdown stays within the viewport; cover with Task 3 mobile screenshots.
- Long Recitation 1 code editors: visual changes must not alter textarea/preview metrics or tab behavior; cover with Task 3 code UI checks and desktop screenshot.
- Hero actions on navy backgrounds: primary, ghost, focus, and hover text remain legible; cover with Task 1 style rules and Task 3 screenshots.
- Placeholder versus available recitations: available sessions stand out without making placeholders look disabled or broken; cover with Task 2 home screenshot.
- Motion and printing: reduced-motion users get no decorative animation and print output remains readable; cover with Task 1 media rules and Task 3 static checks.

---

### Task 1: Shared visual system and site shell

**Files:**
- Modify: `site/assets/style.css`
- Modify: `tools/site_src/site_layout.py`

**Interfaces:**
- Consumes: existing `.site-header`, `.header-inner`, `.site-title`, `.site-nav`, `.page-hero`, `.card`, `.problem`, `.algo`, `.tabs`, and `.site-footer` markup.
- Produces: a `.course-mark` span inside the existing title link and shared visual rules consumed by every page; no new JavaScript interface.

- [ ] **Step 1: Establish baseline checks**

Run: `python3 tools/site_src/check_site.py --strict-links && node tools/site_src/test_code_ui.cjs`
Expected: `OK: 0 errors, 0 warning(s)` and `ALL CODE UI CHECKS PASSED` before editing; record any pre-existing failure rather than treating it as a redesign regression.

- [ ] **Step 2: Implement the shared visual system**

Update the CSS custom properties and existing component rules to use deep navy, cobalt, restrained teal, cool off-white surfaces, refined type scale, radii, borders, and soft shadows. Restyle the sticky navigation, dark hero, buttons, cards, section headings, tables, callouts, code blocks, exercise panels, tabs, and footer without changing editor font size, line height, padding, or positioning.

Add `prefers-reduced-motion` handling that disables nonessential transitions and smooth scrolling. Preserve the existing print and forced-colors rules.

- [ ] **Step 3: Add the course mark to the shared title**

In `site_layout.py`, insert `<span class="course-mark" aria-hidden="true">301</span>` inside `.site-title` before the existing `COMPSCI 301` text, wrapping the remaining title text only if needed for layout. Keep the link destination and accessible course title intact.

- [ ] **Step 4: Regenerate and run static checks**

Run: `python3 tools/site_src/build_site.py && python3 tools/site_src/check_site.py --strict-links`
Expected: all generated pages include the same course mark; `OK: 0 errors, 0 warning(s)`.

### Task 2: Home hero and recitation directory

**Files:**
- Modify: `site/index.html`
- Modify: `site/assets/style.css`

**Interfaces:**
- Consumes: the shared visual system and `.page-hero` treatment from Task 1.
- Produces: home-only `.home-hero`, `.home-hero-grid`, `.hero-copy`, `.hero-panel`, and recitation-directory styling; no new behavior or external asset.

- [ ] **Step 1: Recompose the existing home hero**

Wrap the current home hero copy in `.hero-copy` and use `.home-hero-grid` for a desktop two-column layout. Add an `aria-hidden="true"` `.hero-panel` with the existing course identity, `Algorithms & Databases`, and `Recitations 00–07` represented through concise CSS-styled labels and eight slot indicators. Keep the existing headline, description, metadata, and action URLs unchanged.

- [ ] **Step 2: Style the home composition and directory**

Add home-scoped CSS for the hero panel, subtle grid/accent decoration, stacked mobile layout, and numbered recitation rows using `.week-list` counters. Distinguish `.week-row.available` with an accent edge and slightly elevated surface while retaining readable placeholder rows.

- [ ] **Step 3: Validate links and asset inventory**

Run: `python3 tools/site_src/check_site.py --strict-links`
Expected: `OK: 0 errors, 0 warning(s)`; no new file is added under `site/assets/`.

### Task 3: End-to-end interaction and visual verification

**Files:**
- Verify: `site/index.html`, `site/intro.html`, `site/recitation0.html`, `site/recitation1.html`
- Create only under ignored scratch: `.tmp/` screenshots

**Interfaces:**
- Consumes: the completed static site from Tasks 1–2.
- Produces: verification evidence only; no product-code interface.

- [ ] **Step 1: Verify generated pages and code interactions**

Run: `python3 tools/site_src/build_site.py && python3 tools/site_src/check_site.py --strict-links && node tools/site_src/test_code_ui.cjs`
Expected: successful build, `OK: 0 errors, 0 warning(s)`, and `ALL CODE UI CHECKS PASSED`.

- [ ] **Step 2: Verify regenerated notebooks**

Run: `bash tools/verify_notebooks.sh`
Expected: `ALL NOTEBOOK CHECKS PASSED`.

- [ ] **Step 3: Inspect desktop and mobile pages**

Use the existing `tools/site_src/shot_page.py` helper or headless Chrome with a temporary user-data directory and `--disable-gpu-sandbox`. Capture home, Introduction, Recitation 0, and Recitation 1 at a desktop viewport and at 390px width; save screenshots only in `.tmp/`. Inspect hero actions, navigation/dropdown, cards, recitation rows, tables, long-form sections, code editors, and footer. Correct and recapture any clipping, overflow, contrast, or spacing defect.

- [ ] **Step 4: Check final workspace and deliverable**

Run: `git status --short` and inspect the publishable file inventory.
Expected: only intended source/generated/design/plan files are modified; no screenshots, logs, binaries, caches, or other verification artifacts appear under `site/`. Report exact commands and results without committing or pushing.
