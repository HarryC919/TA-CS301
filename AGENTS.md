# AGENTS.md — working notes for AI agents

Operational guide for the **COMPSCI 301: Algorithms & Databases** course-materials
repository at Duke Kunshan University. All student-facing content is in English.

## Document responsibilities

- `README.md` describes only the repository's contents and course materials. Keep
  development, preview, verification, and publishing instructions out of it.
- This file contains the editing rules, source-of-truth map, validation workflow,
  local preview instructions, and GitHub Pages publishing instructions.
- Update both files when a change affects the information they own.

## Repository map

```text
site/                       publishable static site; never publish the repository root
  index.html                home page + fixed Recitation 0–7 directory
  intro.html                TA introduction, session, IDEs, office hours, AI policy
  recitation0.html          GENERATED — environment and Python/Java kernel guide
  recitation1.html          GENERATED — merged notes and exercises
  recitation2.html … recitation7.html  GENERATED — placeholders
  notebooks/                GENERATED — recitation1-python.ipynb, recitation1-java.ipynb
  week1-notes.html / week1-exercises.html  legacy deep-link redirects
  assets/style.css          shared design system
  assets/notes.css          notes-page-only additions
  assets/app.js             highlighting, temporary editors, tabs, copy/reset
  assets/icons/             local language, IDE, and code-action icons
  assets/logos/             local AI-tool brand marks used on Introduction
  assets/favicon.svg
material/week1/Intro.md     source text behind site/intro.html; keep the two in sync
material/week1/solutions/
  CONTRACTS.md              signatures, edge cases, and performance requirements
  pN/                       exactly 20 files: 6 solutions, 6 stubs, 6 harnesses
tools/verify_all.sh         runs all 36 harnesses
tools/verify_notebooks.sh   rebuilds the notebooks and re-runs their self-check cells
tools/site_src/             site sources, builders, and QA helpers
docs/                       planning, design, and implementation records
.github/workflows/pages.yml publishes only site/ through GitHub Actions
README.md                   repository-contents and course-material overview
application/                PRIVATE — CV, statement, transcript, grades; never publish
.tmp/                       ignored scratch; leave .tmp/ta_ps alone
CLAUDE.md                   loads this file for Claude-style agents
```

The root git repository is on `main`, with `origin` at
`https://github.com/HarryC919/TA-CS301.git`. `.gitignore` excludes `application/`,
`.tmp/`, build artifacts, and OS noise.

## Current content status

- Recitation materials are generally prepared as Jupyter Notebooks and distributed
  through Canvas. Recitation 1's Python and Java notebooks are generated into
  `site/notebooks/` and offered as downloads on the Recitation 1 page. Notebook
  downloads must not be advertised as available before the files exist.
- Recitation 0 documents uv-managed Python/project environments and Java/IJava setup.
  Kernel specs belong in the project environment (`--sys-prefix`), not global user
  storage. Documentation verification does not prove installation on student machines.
- Recitation 1 combines preserved concept notes and six exercises in six languages,
  with temporary browser editors, plus generated Python/Java notebook downloads.
  Notes/Exercises anchors stay on one page and keep drafts intact.
- Recitations 2–7 are unassigned placeholders. Do not assign database topics, tools,
  or environments until the owner decides. `docs/planning/sql-notebook-recommendation.md`
  is planning material only.

## Editing rules and sources of truth

### Introduction, setup, and navigation

- Edit `site/intro.html` directly for Introduction changes and keep
  `material/week1/Intro.md` in sync. The build script updates its navigation only.
- Edit `tools/site_src/recitation0-content.html` for the Recitation 0 setup guide.
- Navigation is defined in `tools/site_src/site_layout.py`: Home → Introduction →
  a native details/summary Recitation dropdown containing Recitations 0–7. Run
  `build_site.py` after changing navigation to synchronize every page and redirect.
- `site/intro.html` publishes approved contact information. Do not add further
  personal data without asking.

### Recitation 1 pipeline

`site/recitation1.html` is generated from `tools/site_src/recitation1-notes.html`,
`tools/site_src/problems.py`, and `material/week1/solutions/pN/`. Never edit the
generated page directly.

- Concept notes: edit `recitation1-notes.html`.
- Statements, examples, constraints, hints, and signatures: edit `problems.py`.
- Code: edit both the solution and stub under the appropriate `pN/` directory.
- Rebuild with `python3 tools/site_src/build_site.py`, or use
  `python3 tools/site_src/build_exercises.py` for Recitation 1 only.
- Keep exactly six languages: `c`, `cpp`, `cs`, `java`, `py`, `js`.
- Signatures in `problems.py`, `CONTRACTS.md`, solutions, stubs, and harnesses must
  match exactly.

The builder fails if a solution or stub is missing or empty, if a solution calls a
library sort (`Arrays.sort`, `std::sort`, `qsort`, `sorted(`, `.sort(`, …), or if the
function name parsed from the signature is absent from either code file.

### Recitation 1 notebooks

`site/notebooks/recitation1-python.ipynb` and `recitation1-java.ipynb` are generated
by `tools/site_src/build_notebooks.py` from the same sources as the page
(`problems.py`, the `py`/`java` stubs, `recitation1-notes.html` converted to
markdown). Never edit the generated `.ipynb` files. Notebook-specific prose — the
per-language intro, self-check cells, and closing — lives in that script, so edit it
and rebuild. `build_site.py` regenerates the notebooks before the pages; reference
solutions are deliberately not embedded. The self-check cells are re-verified
against the reference solutions by `tools/verify_notebooks.sh`.

## Site conventions

- Use plain static HTML/CSS/JS: no frameworks, CDN, external fonts, or publish-time
  build step. Publishing is a plain file copy.
- Every page needs `lang="en"`, a `<title>`, `assets/style.css`, the shared
  `.site-header` and `.site-footer`, and a `<main>`. Mark exactly one navigation link
  active.
- Keep internal links relative so the site works from `file://` and any GitHub Pages
  subpath. External `http(s)` and `mailto:` links are allowed; `javascript:` links are
  rejected.
- Reuse the existing design-system classes in `assets/style.css`. Put shared styles
  in `style.css` and notes-only styles in `notes.css`. Resolve class-coverage warnings
  from `check_site.py`.
- Code drafts are temporary. Only the language choice may use
  `localStorage["cs301-week1-lang"]`; never store code drafts or send them to a server.
  Page load/pageshow restores all templates, reset restores the current template, and
  copy reads the current starter textarea.
- The page defaults to Java and synchronizes one language selection across all 12 tab
  groups. Without JavaScript, the `<noscript>` style reveals all panels.
- Setup blocks use `.code-block[data-language]` with an explicit shell or notebook
  language label and a copy button. Command comments remain literal code. Copy and
  highlighting must also work on pages without exercise tabs.
- All source text must be escaped before highlight spans are inserted. Highlighting
  is lexical, not syntax validation.
- The AI-tools section has two visually equal groups, "US models" and "Chinese
  models". Do not add comparisons, rankings, or qualitative claims about either group.
  Keep their eight official colored SVG marks local in `assets/logos/`.
- Keep Java/Python and VS Code/PyCharm icons local in `assets/icons/`. Never hotlink
  brand assets; `check_site.py` fails on missing local images.
- The bubble/insertion/merge traces and Lomuto quick-sort trace are hand-checked. Do
  not change them without re-deriving the states and checking the pseudocode against
  the trace. `#comparison` complexity columns use `white-space: nowrap`.
- Headless Chrome screenshots require `--user-data-dir=<tmp dir>` and
  `--disable-gpu-sandbox`. Store screenshots only in `.tmp/`. If fragment scrolling
  fails, use `page_offsets.py` and crop a tall capture with Pillow.

## Code and harness conventions

- Teaching code should be beginner-readable, with a short complexity header and
  comments only at algorithm steps. Solutions must not use library sorts; harnesses
  may use them as oracles.
- Canonical stubs: C/C++ TODO plus placeholder return; C#
  `throw new NotImplementedException()`; Java
  `throw new UnsupportedOperationException()`; Python `pass`; JS empty body plus
  `module.exports`.
- Every solution must handle its contract's edge cases and performance limits,
  including large inputs, duplicates, allowed empty inputs, and input-not-mutated
  assertions.

Run each harness from its own `pN/` directory:

- C: `gcc -std=c11 -Wall c.solution.c c.test.c -o ctest && ./ctest`
- C++: `g++ -std=c++17 -Wall cpp.solution.cpp cpp.test.cpp -o cpptest && ./cpptest`
- C#: `dotnet run --project csproj`. `csproj/Solution.cs` must remain a byte-identical
  copy of `cs.solution.cs` because the project compiles every `.cs` file in `csproj/`.
- Java: `cp java.solution.java Solution.java && javac Solution.java Main.java && java Main`.
  Remove `Solution.java` and `.class` files afterward.
- Python: `python3 py.test.py`, which uses an importlib shim for `py.solution.py`.
- JS: `node js.test.js`.

After testing, remove `ctest`, `cpptest`, `*.class`, `Solution.java`, `csproj/bin`,
`csproj/obj`, and `__pycache__`. Each `pN/` must retain exactly 20 source files.

## Commands and verification

```bash
python3 tools/site_src/build_site.py           # rebuild notebooks, recitation pages, and navigation
python3 tools/site_src/build_exercises.py      # rebuild Recitation 1 page only
python3 tools/site_src/build_notebooks.py      # rebuild the Recitation 1 notebooks only
python3 tools/site_src/check_site.py --strict-links
node tools/site_src/test_code_ui.cjs
bash tools/verify_all.sh
bash tools/verify_notebooks.sh
```

Verification toolchain: Apple clang 21 (C11/C++17), .NET SDK 10 (`net10.0`), OpenJDK
21, Python 3.13, Node 24. Chrome is at
`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.

Before claiming work is complete:

1. Rebuild affected generated pages.
2. Run `python3 tools/site_src/check_site.py --strict-links`; expect
   `OK: 0 errors, 0 warning(s)`.
3. For editor changes, run `node tools/site_src/test_code_ui.cjs`; expect
   `ALL CODE UI CHECKS PASSED`.
4. For solution, stub, or harness changes, run `bash tools/verify_all.sh`; expect
   `ALL 36 HARNESSES PASSED`.
5. For notebook-affecting changes (problems, stubs, notes, notebook prose), run
   `bash tools/verify_notebooks.sh`; expect `ALL NOTEBOOK CHECKS PASSED`.
6. Visually inspect changed pages in headless Chrome and recapture after layout changes.
7. Confirm `site/` contains only the 12 HTML pages, the two generated notebooks under
   `site/notebooks/`, and 22 expected assets: style.css, notes.css, app.js, favicon.svg,
   eight logo SVGs, and ten language/IDE/code-action icons. Leave no build artifacts or scratch
   files there.
8. Report the exact commands and results. Never claim an unrun check passed.

## GitHub Pages publishing

### Existing repository

The published site is `https://harryc919.github.io/TA-CS301/`. The existing workflow
runs on pushes to `main` and manual workflow dispatch, uploads only `site/`, and deploys
it with GitHub Actions. Repository **Settings → Pages → Source** must be **GitHub
Actions**.

Rebuild and verify first, then commit and push only when authorized. There is no
site-generation step in the publishing workflow, so generated pages must already be
up to date before pushing.

### Publishing safety

- Never publish the workspace root with **Deploy from a branch**. It would expose
  repository documentation and tooling instead of only the site.
- Never commit `application/` or `.tmp/`, copy private files into `site/`, or include
  them in a standalone site repository.
- Check `git status` before making any repository public. `application/` contains
  private CV, statement, transcript, and grade documents even though it is gitignored.
