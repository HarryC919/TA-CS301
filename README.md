# COMPSCI 301 — TA materials

Teaching materials for **COMPSCI 301: Algorithms & Databases**. The official course
site is temporarily unavailable, so the Week 1 material is mirrored here as a static
site that can be published on GitHub Pages.

## What is in this folder

```
site/                            static site (the only folder that should be published)
  index.html                     home page + fixed Recitation 0–7 directory
  intro.html                     TA introduction: office hours, session format, AI policy
  recitation0.html              environment and Python/Java kernel setup
  recitation1.html              GENERATED: sorting notes + six exercises
  recitation2.html … recitation7.html  reserved session placeholders
  week1-notes.html / week1-exercises.html  compatibility redirects
  assets/style.css               shared design system
  assets/notes.css               notes-page additions only
  assets/app.js                  local highlighting, temporary editors, synced tabs, copy/reset
  assets/icons/                 local Java/Python language icons on Home
  assets/favicon.svg
  assets/logos/                  brand marks for the AI tools shown on the introduction page
material/week1/Intro.md           source text for site/intro.html (keep both in sync)
material/week1/solutions/        reference material behind the exercise page
  CONTRACTS.md                   the spec every implementation follows
  p1 … p6/                       per problem: 6 solutions, 6 stubs, 6 test harnesses
tools/
  verify_all.sh                  compiles/runs all 36 harnesses (6 problems x 6 languages)
  site_src/build_site.py         builds all recitation pages and shared navigation
  site_src/recitation1-notes.html hand-authored concept source fragment
  site_src/recitation0-content.html environment guide source
  site_src/site_layout.py        shared header, page shell and session labels
  site_src/problems.py           problem statements, examples, hints, signatures
  site_src/build_exercises.py    renders site/recitation1.html from notes + problems + solutions
  site_src/check_site.py         structural QA: nesting, ids, links, furniture, nav consistency
  site_src/shot_page.py          section screenshots via headless Chrome (QA helper)
  site_src/page_offsets.py       element offsets for cropping screenshots (QA helper)
application/                     PRIVATE — TA application documents, never publish
AGENTS.md                        instructions for AI agents working in this repo
CLAUDE.md                        points Claude-style agents at AGENTS.md
.github/workflows/pages.yml      GitHub Actions: publish site/ to GitHub Pages
.tmp/                            local scratch (screenshots, logs); safe to delete
```

## Recitation structure

Recitation 0 uses uv to install managed Python, create a project-local virtual
environment, add notebook dependencies and register kernels. Windows examples use
PowerShell. Setup command blocks show shell labels, highlighting, copy buttons and
inline explanations; creating the working folder is a separate step. Existing CS201
JDKs at least 17 are accepted; mise is optional for
installing/managing a suitable JDK, with Jupyter launched through `mise exec`. Recitation 1 combines the existing
sorting notes and exercises. Recitations 2–7 are reserved placeholders; later topics
and the database environment remain undecided. No notebook exercise downloads have
been published yet. Legacy Week 1 links redirect to Recitation 1 and retain hashes
when JavaScript is enabled.

## The Recitation 1 material

- **Introduction** (`site/intro.html`): who runs the recitation, contact details and
  office hours, who the session is for, what happens in a session, and the AI policy
  (AI tools allowed during the recitation, but you must be able to explain your solution).
  The recommended models are listed with their logos, stored locally in `assets/logos/`
  so the page needs no network access.
- **Notes** (`site/recitation1.html#notes`): a quick concept pass. Five key takeaways,
  learning goals, the Ω(n log n) decision-tree argument, one section per algorithm
  (idea → steps → worked trace → pseudocode → complexity → pitfall), stability /
  in-place / adaptive vocabulary, a side-by-side table, when to use which, and a
  optional order-statistics preview.
- **Exercises** (`site/recitation1.html#exercises`): six problems, each with a description,
  worked examples with input/output, constraints, the exact function signature, a
  starter template with a `TODO`, hints, and a collapsible reference solution in
  **C, C++, C#, Java, Python and JavaScript**. A single language choice is remembered
  across every code block in the page. Starter templates are editable in the browser with
  lexical syntax highlighting. Drafts stay isolated by problem and language, survive
  language switches, and reset on refresh. **Reset code** restores the current template;
  **Copy code** copies the current draft. Tab indents, Shift+Tab removes current-line
  indentation, and Escape then Tab leaves the editor. Code is never saved or run by
  the website. Reference answers and notes pseudocode remain read-only and highlighted.
  Highlighting is a lightweight lexical aid, not a compiler or error checker.

| # | Problem | Difficulty | Target |
|---|---------|------------|--------|
| 1 | Bubble Sort with Early Exit | Easy | loop bounds, `swapped`, O(n) best case |
| 2 | Insertion Sort: Count the Shifts | Easy | insert step, inversions |
| 3 | Stable Sort by Word Length | Easy–Medium | stability by sort choice |
| 4 | Count Inversions | Medium | merge sort's merge routine, 64-bit answers |
| 5 | Quick Sort: Random Pivot, 3-Way Partition | Medium | partition, duplicates, worst case |
| 6 | Kth Largest Element (Quickselect) | Medium+ | optional exploration, iterative 3-way partition |

The exercises are optional, ungraded practice for an optional session with roughly
5–15 students. Problem 6 is independent exploration and is not covered in class.
The session uses 5–10 minutes for introductions, 10–15 for concepts, 30 for practice,
15 for discussing approaches (not a line-by-line code walkthrough), and the remaining
time for questions. Java is the default language because it is the CS201 language.

## Publish the site

For the existing `origin` repository, rebuild and verify first, then commit and push
to `main` when authorized. The existing GitHub Actions workflow publishes only `site/`.
The alternatives below describe setting up a new repository.

The site is plain static HTML/CSS/JS with **no build step**. It works from any
subdirectory (all links are relative).

**Option A — publish only `site/` (simplest).** `site/` is not a git repository yet.
Initialize one inside it and push it to a new empty GitHub repository:

```bash
cd site
git init -b main
git add .
git commit -m "Publish COMPSCI 301 Week 1 site"
git remote add origin git@github.com:<your-user>/<repo-name>.git
git push -u origin main
```

Then open **Settings → Pages** and choose **Deploy from a branch → `main` →
`/ (root)`**. The site appears at `https://<your-user>.github.io/<repo-name>/`, and
only the contents of `site/` are public.

**Option B — publish from this folder's repository.** The workspace root already has a
Git repository on `main`, with `origin` pointing to `https://github.com/HarryC919/TA-CS301.git`. Its `.gitignore` keeps
`application/` and `.tmp/` out, and `.github/workflows/pages.yml` publishes only the
`site/` folder through GitHub Actions:

```bash
git add .
git commit -m "COMPSCI 301 Week 1 materials"
git remote add origin git@github.com:<your-user>/<repo-name>.git
git push -u origin main
```

Then open **Settings → Pages** and set **Source: GitHub Actions**. The workflow runs on
every push to `main`.

**Do not publish the repository root with "Deploy from a branch"**: Pages can only serve
the repo root or a `/docs` folder from a branch, so the root would expose the README,
`AGENTS.md` and the tooling instead of the site. `application/` contains private TA
application documents (CV, statement of purpose, transcript, grades) and is gitignored —
but check `git status` before making any repository public.

## Preview locally

Open `site/index.html` in a browser — `file://` works, including the language tabs
and copy buttons. For a local server:

```bash
cd site && python3 -m http.server 8000
# then open http://localhost:8000
```

## Rebuild and verify

Recitation 1 is generated. Edit `tools/site_src/recitation1-notes.html` for concepts,
`recitation0-content.html` for setup instructions, and `problems.py` or the solution
files for exercises. Edit `site_layout.py` for navigation, then rebuild the whole site:

```bash
# 1. edit statements/examples/hints
$EDITOR tools/site_src/problems.py
# 2. edit the reference solutions and stubs
$EDITOR material/week1/solutions/p4/py.solution.py
# 3. regenerate the page
python3 tools/site_src/build_site.py
# 4. structural QA (fails on broken links or malformed HTML)
python3 tools/site_src/check_site.py --strict-links
# browser checks for editing, highlighting, refresh reset, copy, and no-JS fallback
node tools/site_src/test_code_ui.cjs
# 5. compile and run every reference answer
bash tools/verify_all.sh
```

The generator refuses to build if a solution or stub is missing or empty, if a
solution calls a library sort, or if the signature in `problems.py` does not appear in
the code. Every harness runs from its own problem directory; `verify_all.sh` cleans
build artifacts afterwards.

Verified with: Apple clang 21 (C/C++), .NET SDK 10 (`net10.0`), OpenJDK 21,
Python 3.13, Node 24. Two implementation details worth remembering:

- Java files declare `public class Solution`, so the harnesses copy
  `java.solution.java` to `Solution.java` before compiling.
- The C# console harness compiles every `.cs` file in `csproj/`, so
  `csproj/Solution.cs` must stay a byte-identical copy of `cs.solution.cs`.

## Notes for the teaching team

- Answers deliberately do not use library sorts; harnesses may use them as oracles.
- The notes page traces were verified by hand and (for quick sort) by re-running the
  page's own pseudocode; keep them exact if the page is edited.
- Recitations 2–7 are unassigned placeholders. The database portion is still to be decided.
