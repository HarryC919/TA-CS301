# Recitation Navigation Implementation Plan

**Goal:** Implement the requested fixed Recitation 0–7 site organization.
**Spec:** docs/superpowers/specs/2026-10-27-recitation-navigation-design.md
**Architecture:** Shared Python layout functions and build_site.py produce static pages; build_exercises.py combines a preserved notes fragment with existing exercises. Native dropdown needs no JS. Existing temporary editors are retained; shared assets also support menu dismissal, shell highlighting, and standalone command copying.

- [x] Add structural expectations for Home/Introduction/Recitation 0–7 and see old site fail.
- [x] Extract notes without changing algorithm content; generate unified Recitation 1 and compatibility pages.
- [x] Add sourced Recitation 0 setup and reserved Recitation 2–7 pages; update Home/Intro/navigation/styles/docs.
- [x] Run build, structural and browser checks, legacy hashes and no-JS dropdown checks; inspect desktop/mobile screenshots and file inventory.

Do not assign database topics, create notebook exercise files, change solution contracts, commit or push without a new request. Preserve drafts while navigating Notes/Exercises within Recitation 1. Verify setup documentation separately from actual kernel installation; do not claim installations were tested.

Validation: 12-page structural QA has 0 errors/0 warnings; browser suite passes for all ten primary pages at 1440/390px, legacy deep links, editors, no-JS code and native dropdowns. Four algorithm sections/comparison table and all 72 exercise code blocks match their prior source verbatim. Build is idempotent; 26 publishable files only (12 HTML pages and 14 assets, including the two local Home icons). Setup guide was checked against official documentation, not installed or executed on student operating systems.
