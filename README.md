# COMPSCI 301 — TA Materials

Teaching materials for **COMPSCI 301: Algorithms & Databases** at Duke Kunshan
University. The optional recitation usually has 5–15 students, mostly Data Science
sophomores and juniors who know Python and Java. Student-facing content is in English.

## Repository contents

```text
site/                            static course website
  index.html                     home page and Recitation 0–7 directory
  intro.html                     TA, session, IDE, office-hour, and AI-policy information
  recitation0.html               environment and Python/Java kernel guide
  recitation1.html               sorting notes and six exercises, plus notebook downloads
  recitation2.html … recitation7.html  reserved session placeholders
  week1-notes.html / week1-exercises.html  legacy Week 1 redirects
  notebooks/                     generated Recitation 1 Python and Java notebooks
  assets/                       local CSS, JavaScript, icons, and brand marks
material/week1/
  Intro.md                       source text for site/intro.html
  solutions/
    CONTRACTS.md                 function contracts and edge-case requirements
    p1 … p6/                    solutions, starter templates, and tests in six languages
tools/
  verify_all.sh                  runner for all 36 solution harnesses
  verify_notebooks.sh            rebuilds the notebooks and re-runs their self-check cells
  site_src/                     site sources, generators, and structural/browser QA helpers
docs/
  planning/                      course-material planning documents
  superpowers/                   design and implementation records
.github/workflows/pages.yml      site deployment workflow
application/                     PRIVATE TA application documents; not course material
.tmp/                            ignored local screenshots, logs, and previews
AGENTS.md                        editing, verification, preview, and publishing instructions
CLAUDE.md                        loads AGENTS.md for Claude-style agents
```

## Recitation materials

Recitation materials are generally prepared as **Jupyter Notebooks** and distributed
through Canvas. Recitation 1 additionally ships generated Python and Java exercise
notebooks in `site/notebooks/`, offered as downloads on the Recitation 1 page; the
website mirrors the same notes and exercises in the browser.

- **Recitation 0** covers uv-managed Python and project-local environments, notebook
  dependencies, Python and Java/IJava kernels, and JDK setup. Windows examples use
  PowerShell. Existing JDK 17 or newer installations are accepted, and mise is an
  optional JDK manager.
- **Recitation 1** combines sorting concept notes with six practice problems in C,
  C++, C#, Java, Python, and JavaScript, plus Python and Java Jupyter notebooks.
- **Recitations 2–7** are reserved placeholders. Later topics and the database
  environment have not been assigned to a session. The SQL notebook document under
  `docs/planning/` is a recommendation, not published course material.
- The two legacy Week 1 pages redirect to the corresponding Recitation 1 sections.

## Recitation 1 content

### Introduction

`site/intro.html` describes the TA, intended audience, session format, recommended
IDEs, office hours, and AI policy. AI tools are allowed during recitation practice,
but students must understand and be able to explain their solutions. Assignment and
exam rules remain under the instructor's control.

### Notes

`site/recitation1.html#notes` contains learning goals, five key takeaways, the
Ω(n log n) comparison-sorting lower bound, algorithm traces and pseudocode,
complexity analysis, stability/in-place/adaptive terminology, a comparison table,
selection guidance, and an optional order-statistics preview.

### Exercises

`site/recitation1.html#exercises` provides six optional, ungraded problems. Each
problem includes a statement, examples, constraints, exact function signatures,
starter templates, hints, and collapsible reference solutions in all six languages.

| # | Problem | Difficulty | Main topic |
|---|---------|------------|------------|
| 1 | Bubble Sort with Early Exit | Easy | Loop bounds, `swapped`, O(n) best case |
| 2 | Insertion Sort: Count the Shifts | Easy | Insertion steps and inversions |
| 3 | Stable Sort by Word Length | Easy–Medium | Stability and sort choice |
| 4 | Count Inversions | Medium | Merge-sort merging and 64-bit answers |
| 5 | Quick Sort: Random Pivot, 3-Way Partition | Medium | Partitioning and duplicates |
| 6 | Kth Largest Element (Quickselect) | Medium+ | Optional iterative 3-way partition exploration |

Problem 6 is independent exploration and is not covered in class. Java is the default
displayed language because it is the CS201 language. The browser editors support
temporary drafts, language switching, copy/reset, keyboard indentation, and lexical
highlighting; they do not save or execute code. Reference solutions and notes
pseudocode are read-only.

### Notebooks

`site/notebooks/` holds generated Jupyter versions of Recitation 1, one per language:
`recitation1-python.ipynb` (Python (CS301) kernel) and `recitation1-java.ipynb`
(Java/IJava kernel). Both are downloadable from the Recitation 1 page and carry the
concept notes, the six problem briefs with hidden hints, the language's starter
template, and one runnable self-check cell per problem. Reference solutions are not
embedded — they stay on the website. The notebooks are generated from the same
sources as the page, so statements, templates, and examples cannot drift apart.

The current session outline reserves 15–20 minutes for concept review, 25–30 minutes
for practice, 15 minutes for discussing approaches, and the remaining time for
questions. The recitation and exercises are optional and ungraded.
