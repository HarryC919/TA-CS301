# AGENTS.md — COMPSCI 301 working rules

Course-materials repository for Duke Kunshan University. Student-facing content
must be in English. Preserve existing user edits and unrelated content.

## Scope and safety

- `README.md` describes repository contents and course materials only. Keep editing,
  verification, and publishing instructions here; update each document when its scope changes.
- Publish only `site/`. Never commit `application/` (private records) or `.tmp/`,
  copy private files into `site/`, or publish the repository root. Leave `.tmp/ta_ps` alone.
- Introduction contact information is approved; ask before adding other personal data.
- Commit and push only when explicitly authorized, after rebuilding and verification.

## Sources of truth

Never hand-edit generated HTML or notebooks. Paths below are relative to the root;
site builders live in `tools/site_src/`.

- **Introduction:** edit `site/intro.html` and keep `material/week1/Intro.md` in sync.
  The builder updates its navigation only.
- **Recitation 0:** edit `tools/site_src/recitation0-content.html`. Keep uv-managed
  project environments, project-local kernels (`--sys-prefix`), IDE-first notebook
  usage, and a separate optional JupyterLab section. Documentation checks do not
  establish successful installation on student machines.
- **Recitation 1:** edit `tools/site_src/recitation1-notes.html` for concepts,
  `tools/site_src/problems.py` for statements/examples/hints/signatures, and
  `material/week1/solutions/pN/` for solutions and stubs. These generate
  `site/recitation1.html`; preserve the combined Notes/Exercises anchors and drafts.
- **Notebooks:** `tools/site_src/build_notebooks.py` generates the Python/Java files
  under `site/notebooks/` from the same notes, problems, and stubs. Edit notebook-only
  prose and self-check cells in that script. Do not embed reference solutions or
  advertise downloads before the files exist. Notebooks are also distributed via Canvas.
- **Navigation:** edit `tools/site_src/site_layout.py`, then run `build_site.py`.
  Keep Home → Introduction → native details/summary Recitation 0–7 dropdown
  and the Home directory.
- **Recitations 2–7:** unassigned placeholders. Do not assign topics, database tools,
  or environments without the owner's decision. `docs/planning/` is not course content.

## Site behavior

- Plain static HTML/CSS/JS; no frameworks, CDN, external fonts, or publish-time build.
  Use relative internal links (support `file://` and GitHub Pages subpaths);
  external HTTP(S)/mailto links are allowed, `javascript:` links are not.
- Every page needs `lang="en"`, a title, `assets/style.css`, shared header/footer,
  `<main>`, and exactly one active navigation link. Reuse the design system:
  shared styles in `style.css`, notes-only styles in `notes.css`; resolve QA warnings.
- Drafts stay temporary: never persist or transmit code. Only language choice may
  use `localStorage["cs301-week1-lang"]`. Load/pageshow restores templates; reset
  restores the current template; copy reads the current starter textarea.
- Default to Java; synchronize language across all 12 tab groups. Without JavaScript,
  reveal all panels. Keep highlighting/copy functional on pages without exercise tabs.
- Setup blocks use `.code-block[data-language]`, an explicit shell/notebook language
  label, and a copy button. Preserve literal command comments; escape all source text
  before adding highlight spans. Highlighting is lexical, not syntax validation.
- Keep all brand icons/logos local. The AI-tools section has visually equal
  “US models” and “Chinese models” groups with eight official colored SVG marks;
  do not add rankings, comparisons, or qualitative claims.
- Re-derive sorting trace states and check pseudocode before changing them.
  Keep `#comparison` complexity columns at `white-space: nowrap`.

## Solutions and harnesses

- Keep six languages: `c`, `cpp`, `cs`, `java`, `py`, `js`. Signatures must match
  `problems.py`, `CONTRACTS.md`, solutions, stubs, and harnesses exactly.
- Code changes must keep solutions and stubs aligned. Use beginner-readable code,
  short complexity headers, and algorithm-step comments. No library sorts in solutions;
  harnesses may use them as oracles. Honor all contract edge cases, performance limits,
  duplicates, allowed empty inputs, and input-not-mutated checks.
- Stubs: C/C++ TODO plus placeholder return; C# `NotImplementedException`;
  Java `UnsupportedOperationException`; Python `pass`; JS empty body plus `module.exports`.
- Keep `csproj/Solution.cs` byte-identical to `cs.solution.cs`. Each `pN/` retains
  exactly 20 source files. `tools/verify_all.sh` contains individual harness commands
  and cleans binaries, Java copies/classes, .NET build directories, and Python caches;
  clean these artifacts after manual runs too.

## Verification

Run checks appropriate to the changed files; report exact commands and results.
Never claim an unrun check passed. Repository-doc edits alone need no site rebuild.

- Generated content/navigation: `python3 tools/site_src/build_site.py` rebuilds all
  pages and notebooks. For Recitation 1 only, use `build_exercises.py`; for notebooks
  only, use `build_notebooks.py` (both under `tools/site_src/`).
- Site changes: `python3 tools/site_src/check_site.py --strict-links`
  → `OK: 0 errors, 0 warning(s)`.
- Editor changes: `node tools/site_src/test_code_ui.cjs`
  → `ALL CODE UI CHECKS PASSED`.
- Solutions/stubs/harnesses: `bash tools/verify_all.sh`
  → `ALL 36 HARNESSES PASSED`.
- Notebook inputs (problems, stubs, notes, notebook prose):
  `bash tools/verify_notebooks.sh` → `ALL NOTEBOOK CHECKS PASSED`.
- Visually inspect changed pages in headless Chrome, including mobile; recapture after
  layout changes. Use `--user-data-dir=<tmp dir>` and `--disable-gpu-sandbox`.
  Store screenshots only in `.tmp/`; helpers: `shot_page.py` and `page_offsets.py`.
- Keep `site/` free of scratch/build artifacts: currently 10 HTML pages, two generated
  notebooks, and 22 assets (two CSS, one JS, favicon, eight logos, ten icons).

## Publishing

`https://harryc919.github.io/TA-CS301/` is deployed by `.github/workflows/pages.yml`
from `site/` on pushes to `main` or manual dispatch. Pages Source must be **GitHub
Actions**. The workflow does not generate files: rebuild and verify before publishing.
Check `git status` before publishing or changing repository visibility; never use
**Deploy from a branch** to expose the workspace root.
