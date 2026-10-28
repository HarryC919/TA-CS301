# AGENTS.md — working notes for AI agents

Course-materials repository for **COMPSCI 301: Algorithms & Databases** (Duke Kunshan
University). The official course website is temporarily unavailable, so the Week 1 material
is mirrored as a static site in `site/` that is published on GitHub Pages. The recitation is
optional (~5–15 students, mostly Data Science sophomores/juniors who know Python and Java).
**All student-facing content is in English.**

## Layout

```text
site/                       publishable static site (publish this folder, not the root)
  index.html                home page + fixed Recitation 0–7 directory
  intro.html                TA introduction: contact, office hours, session format, AI policy
  recitation0.html          GENERATED — environment and Python/Java kernel guide
  recitation1.html          GENERATED — merged notes and exercises
  recitation2.html … recitation7.html  GENERATED — placeholders
  week1-notes.html / week1-exercises.html  legacy deep-link redirects
  assets/style.css          shared design system
  assets/notes.css          notes-page-only additions
  assets/app.js             local highlighting, temporary editors, synced language tabs, copy/reset
  assets/icons/             local Java/Python icons used on Home
  assets/favicon.svg
  assets/logos/             AI-tool brand marks used on intro.html (local files, no CDN)
material/week1/Intro.md               source text behind site/intro.html (keep the two in sync)
material/week1/solutions/             CONTRACTS.md + p1 … p6, exactly 20 files each
  pN/<lang>.solution.*                6 solutions (c, cpp, cs, java, py, js)
  pN/<lang>.stub.*                    6 starter templates (canonical TODO format)
  pN/c.test.c, cpp.test.cpp, Main.java, py.test.py, js.test.js, csproj/   6 harnesses
tools/verify_all.sh                   runs all 36 harnesses (6 problems × 6 languages)
tools/site_src/problems.py            single source of truth: statements, examples, hints, signatures
tools/site_src/build_exercises.py     renders site/recitation1.html
tools/site_src/build_site.py          builds all pages and shared navigation
tools/site_src/site_layout.py         single source of shared navigation
tools/site_src/recitation1-notes.html  hand-authored notes source fragment
tools/site_src/recitation0-content.html setup guide source
tools/site_src/check_site.py          structural QA for every site/*.html page
tools/site_src/shot_page.py           section screenshots (QA helper)
tools/site_src/page_offsets.py        element offsets for cropping screenshots (QA helper)
.github/workflows/pages.yml           publishes only site/ to GitHub Pages (GitHub Actions)
README.md                   user-facing docs: structure, publishing, rebuild commands
application/                PRIVATE — CV, statement of purpose, transcript, grades. NEVER publish.
.tmp/                       scratch (screenshots, logs). Ignored. Leave `.tmp/ta_ps` alone.
CLAUDE.md                   just `@ AGENTS.md` so Claude-style agents load this file
```

The workspace root is a git repository on `main` with remote `origin` at
`https://github.com/HarryC919/TA-CS301.git`. Its
`.gitignore` excludes `application/` and `.tmp/`, and `.github/workflows/pages.yml` publishes
only the `site/` folder through GitHub Actions. Alternatively `site/` can be initialized as its
own repository (`cd site && git init -b main`) and published from its root. Never commit
`application/` or `.tmp/` anywhere, never copy private files into `site/`, and never use the
repository root as a "Deploy from a branch" Pages source.

## Commands

```bash
python3 tools/site_src/build_site.py           # rebuild all recitation pages and navigation
python3 tools/site_src/build_exercises.py      # rebuild only Recitation 1
python3 tools/site_src/check_site.py --strict-links   # structural QA; expect 0 errors, 0 warnings
node tools/site_src/test_code_ui.cjs           # Chrome behavior checks; expect ALL CODE UI CHECKS PASSED
bash tools/verify_all.sh                       # 36 harnesses; expect "ALL 36 HARNESSES PASSED"
cd site && python3 -m http.server 8000         # local preview (file:// also works)
```

Toolchain used for verification: Apple clang 21 (C11/C++17), .NET SDK 10 (`net10.0`),
OpenJDK 21, Python 3.13, Node 24. Chrome is at
`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` for visual QA.

## Exercise page pipeline (important)

`site/recitation1.html` is generated from `tools/site_src/recitation1-notes.html`,
`tools/site_src/problems.py` plus the code files
in `material/week1/solutions/pN/`. Editing the generated HTML directly will be overwritten.

- To change concept notes, edit `tools/site_src/recitation1-notes.html`; for setup edit
  `tools/site_src/recitation0-content.html`. Rebuild with `python3 tools/site_src/build_site.py`.
- To change exercise wording, examples, constraints, hints or signatures: edit `problems.py`, then rebuild.
- To change code: edit `material/week1/solutions/pN/` (solution **and** stub), then rebuild.
- The builder is strict. It fails if a solution/stub is missing or empty, if a solution calls a
  library sort (`Arrays.sort`, `std::sort`, `qsort`, `sorted(`, `.sort(`, …), or if the function
  name parsed from the signature does not appear in both the solution and the stub. Keep exactly
  six languages: c, cpp, cs, java, py, js.
- Signatures in `problems.py` must match `material/week1/solutions/CONTRACTS.md` and the code
  files character-for-character. Harnesses call those exact signatures.
- The page defaults every tab group to **java** (CS201 language) and `app.js` keeps one language
  selection synced across all 12 tab groups, persisted as `localStorage["cs301-week1-lang"]`.
  Without JS, a `<noscript>` style reveals all panels.
- Starter groups have `data-editable`. `app.js` adds textarea editors with a matching
  highlighted preview. Original code stays in the HTML for no-JS fallback. Only the
  language choice may use localStorage; never persist code drafts in storage or send
  them to a server. Reset restores the current template; page load/pageshow restores
  all templates. Copy must read the textarea value for starters.
- Setup code blocks use `.code-block[data-language]` with an explicit Bash/Zsh/PowerShell
  or notebook language label and a copy button. Copy/highlighting must work on pages
  without exercise tabs, such as Recitation 0. Keep command comments as literal code.
- `app.js` also highlights the notes' read-only pseudocode. Always escape source text
  before inserting highlight spans. This is lexical highlighting, not syntax validation.
- For editor changes, run `node tools/site_src/test_code_ui.cjs`; it checks real typing,
  draft isolation, copy/reset/reload, scroll synchronization, keyboard exit, 390px
  layout, notes highlighting, and no-JS fallback. Screenshots go only in `.tmp/`.

## Code and harness conventions

- Teaching code: beginner-readable, a short header comment with complexity, comments only at
  algorithm steps. No library sort in a solution (harnesses may use library sorts as oracles).
- Canonical stub format: C/C++ TODO + placeholder return; C# `throw new NotImplementedException()`;
  Java `throw new UnsupportedOperationException()`; Python `pass`; JS empty body + `module.exports`.
- Harness commands (each run from its own `pN/` directory):
  - C: `gcc -std=c11 -Wall c.solution.c c.test.c -o ctest && ./ctest`
  - C++: `g++ -std=c++17 -Wall cpp.solution.cpp cpp.test.cpp -o cpptest && ./cpptest`
  - C#: `dotnet run --project csproj` — `csproj/Solution.cs` must stay a byte-identical copy of
    `cs.solution.cs`, because the console project compiles every `.cs` file in `csproj/`.
  - Java: `cp java.solution.java Solution.java && javac Solution.java Main.java && java Main`
    (files declare `public class Solution`), then remove `Solution.java` and `.class` files.
  - Python: `python3 py.test.py` (uses an `importlib` shim because the file is named `py.solution.py`).
  - JS: `node js.test.js`.
- After running tests, remove build artifacts: `ctest`, `cpptest`, `*.class`, `Solution.java`,
  `csproj/bin`, `csproj/obj`, `__pycache__`. Each `pN/` must contain exactly 20 source files.
- Every solution must handle the contract's edge cases and performance limits (e.g. 100k-element
  inputs, duplicates, empty input where the contract allows it, input-not-mutated assertions).

## Site conventions

- Pure static HTML/CSS/JS; no frameworks, no CDN, no external fonts. Publishing is a plain file
  copy, with no build step at publish time.
- Every page needs: `lang="en"`, a `<title>`, `assets/style.css`, the shared `.site-header`
  (with nav), the shared `.site-footer`, and a `<main>`.
- Navigation is defined in `tools/site_src/site_layout.py`: Home → Introduction → a native
  details/summary Recitation dropdown containing Recitations 0–7. Build with `build_site.py`
  to synchronize every page, including compatibility redirects. Mark exactly one link active.
- Recitations 2–7 stay unassigned placeholders. Do not assign database topics, tools or
  environments until the owner decides. Notebook downloads must not be advertised as
  available before the files exist. Recitation 1 keeps its current exercises for now.
- Links inside the site must stay relative (`index.html`, `recitation1.html#bubble-sort`, …) so
  the site works from `file://` and from any GitHub Pages subpath. External `http(s)` and
  `mailto:` links are allowed but are not fetched by QA; `javascript:` links are rejected.
- Reuse classes from `assets/style.css` (`page-hero`, `section`, `section-title`, `lead`,
  `card-grid`/`card`, `callout` (`info`/`tip`/`warn`), `pill`, `table-wrap` + `table.data`,
  `steps`, `note`, `more-link`, `btn`/`primary`/`ghost`, `site-header`/`site-nav` …). Put new
  shared styles in `style.css`; notes-page-only styles in `notes.css`. Check the class-coverage
  warnings printed by `check_site.py`.
- The AI-tools section of `site/intro.html` lists models in two equal card groups ("US models",
  "Chinese models"), each a `.tool-list` of `.tool-item` rows with a `.tool-logo` slot (26 px
  icon, no chip background) and the model name. Keep the two groups visually equal through
  identical markup and styling — do not add comparisons, rankings or qualitative claims about
  either group. Logos are the official colored SVG brand marks, kept locally in `assets/logos/`
  (one file per tool: `openai.svg`, `claude.svg`, `gemini.svg`, `grok.svg`, `deepseek.svg`,
  `kimi.svg`, `zai.svg`, `qwen.svg`). Never hotlink a CDN. `check_site.py` fails on missing
  local `<img>` files.
- Notes page accuracy matters: the bubble/insertion/merge traces and the Lomuto quick-sort trace
  are hand-checked; do not "fix" them without re-deriving the states, and keep the pseudocode and
  the trace consistent with each other. `#comparison` complexity columns are `white-space: nowrap`.
- `site/intro.html` publishes the TA's real contact information (name, DKU email, NetID, planned
  office hours) with the owner's approval. Keep it in sync with `material/week1/Intro.md`; do not
  add further personal data without asking. The "official course site is temporarily unavailable"
  notices exist on purpose — keep them.
- Screenshots: headless Chrome needs `--user-data-dir=<tmp dir>` **and** `--disable-gpu-sandbox`
  (`--disable-gpu` alone is not enough). Fragment scrolling does not work in headless screenshots;
  use `page_offsets.py` to measure section offsets, then crop a tall capture with Pillow.

## Verification discipline

Before claiming work is complete:

1. `python3 tools/site_src/build_exercises.py` (if any problem data or code changed).
2. `python3 tools/site_src/check_site.py --strict-links` → must print `OK: 0 errors, 0 warning(s)`.
3. `bash tools/verify_all.sh` (if any solution/stub/harness changed) → `ALL 36 HARNESSES PASSED`.
4. Visual check of changed pages via headless Chrome; if layout changed, recapture.
5. Confirm `site/` contains only Home, Introduction, Recitations 0–7, the two legacy
   Week 1 redirects, and the existing assets (style.css, notes.css, app.js, favicon.svg,
   eight logo SVGs, and two local Home language icons): 12 HTML pages + 14 assets. No build artifacts or scratch files.

Report exact commands run and their results; do not claim a check passed without running it.

## Current status

- Site: Home/Introduction, Recitations 0–7, and two legacy Week 1 redirects.
- Recitation 0 documents uv-managed Python/project environments and Java/IJava setup;
  Windows uses PowerShell, existing JDK >=17 is accepted, and mise is the optional JDK manager.
  Kernel specs belong in the project environment (`--sys-prefix`), not global user storage;
  documentation verification does not establish installation success on student machines.
- Recitation 1 combines preserved concept notes and six exercises in six languages, with
  temporary code editors. Notes/Exercises anchors stay within one page and preserve drafts.
- Recitations 2–7 are placeholders. Database planning and notebook exercise migration remain open.
- Keep README, sources, generated pages and validation tooling consistent.
