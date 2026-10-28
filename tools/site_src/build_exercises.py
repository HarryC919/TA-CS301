#!/usr/bin/env python3
"""Build `site/recitation1.html` from the exercise content + reference files.

Inputs:
  - `tools/site_src/problems.py`      statements, examples, hints, signatures
  - `material/week1/solutions/p<N>/<lang>.solution.*` reference solutions (rendered verbatim)
  - `material/week1/solutions/p<N>/<lang>.stub.*`    starter templates  (rendered verbatim)

The generated page is a plain static HTML file: the published site has no build
step. Re-run this script after editing problems.py or any reference file:

    python3 tools/site_src/build_exercises.py

The build is strict: a missing or suspicious file fails loudly instead of
publishing a broken page (`--allow-missing` exists only for local previews).
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

from problems import DEFAULT_LANG, LANGS, PROBLEMS, SIGNATURES  # noqa: E402
from site_layout import header

SOL = ROOT / "material" / "week1" / "solutions"
SITE = ROOT / "site"
DEFAULT_OUT = SITE / "recitation1.html"

LANG_EXT = {key: ext for key, _label, ext in LANGS}
LANG_LABEL = {key: label for key, label, _ext in LANGS}

# Calls to a library sort inside a *solution* defeat the exercise.
BANNED_IN_SOLUTIONS = [
    (r"\bArrays\.sort\s*\(", "Java: Arrays.sort"),
    (r"\bCollections\.sort\s*\(", "Java: Collections.sort"),
    (r"\bstd::sort\s*\(", "C++: std::sort"),
    (r"\bstd::stable_sort\s*\(", "C++: std::stable_sort"),
    (r"\bqsort\s*\(", "C: qsort"),
    (r"\bArray\.Sort\s*\(", "C#: Array.Sort"),
    (r"\bList<[^>]*>\s*\.\s*Sort\s*\(", "C#: List.Sort"),
    (r"\.OrderBy\s*\(", "C#: LINQ OrderBy"),
    (r"\bsorted\s*\(", "Python: sorted"),
    (r"\.sort\s*\(", "in-place sort method"),
]

NOSCRIPT_STYLE = """
    .tab-btn, .copy-btn { display: none !important; }
    .tab-panel[hidden] { display: block !important; }
    .tab-panel { border-top: 1px solid rgba(255, 255, 255, 0.08); }
    .tab-panel:first-child { border-top: 0; }
"""


class BuildError(RuntimeError):
    pass


def read_code(problem_number: int, kind: str, lang: str, allow_missing: bool) -> str:
    path = SOL / f"p{problem_number}" / f"{lang}.{kind}.{LANG_EXT[lang]}"
    if not path.is_file():
        if allow_missing:
            return f"// MISSING FILE: {path.relative_to(ROOT)}\n"
        raise BuildError(f"missing {kind} file: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    text = "\n".join(line.rstrip() for line in text.split("\n")).strip("\n")
    if not text.strip():
        raise BuildError(f"empty file: {path.relative_to(ROOT)}")
    return text + "\n"


def function_name(signature: str) -> str:
    match = re.search(r"([A-Za-z_]\w*)\s*\(", signature)
    if not match:
        raise BuildError(f"cannot find a function name in signature: {signature!r}")
    return match.group(1)


def check_solution(problem: dict, lang: str, kind: str, text: str, allow_missing: bool) -> None:
    if allow_missing and text.startswith("// MISSING FILE:"):
        return
    number = problem["number"]
    name = function_name(SIGNATURES[number][lang])
    if name not in text:
        raise BuildError(
            f"p{number}/{lang}.{kind}: expected function name {name!r} "
            f"(from the contract signature) but it does not appear in the file"
        )
    if kind != "solution":
        return
    for pattern, description in BANNED_IN_SOLUTIONS:
        if re.search(pattern, text):
            raise BuildError(
                f"p{number}/{lang}.solution: uses a library sort ({description}); "
                f"the contract requires implementing the algorithm manually"
            )


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def render_io_row(key: str, value: str, plain: bool = False) -> str:
    css = "io-value plain" if plain else "io-value"
    return (
        f'<div class="io-row"><span class="io-key">{key}</span>'
        f'<div class="{css}">{value}</div></div>'
    )


def render_tabs(group_id: str, title: str, codes: dict[str, str]) -> str:
    buttons = []
    panels = []
    for key, label, _ext in LANGS:
        panel_id = f"{group_id}-{key}"
        button_id = f"{panel_id}-tab"
        selected = key == DEFAULT_LANG
        buttons.append(
            f'<button class="tab-btn" type="button" role="tab" id="{button_id}" '
            f'data-lang="{key}" aria-controls="{panel_id}" '
            f'aria-selected="{"true" if selected else "false"}" '
            f'tabindex="{0 if selected else -1}">{label}</button>'
        )
        panels.append(
            f'<div class="tab-panel" role="tabpanel" id="{panel_id}" '
            f'aria-labelledby="{button_id}" data-lang="{key}"'
            f'{" hidden" if not selected else ""}>'
            f'<div class="code-head"><span class="code-title">{title}</span>'
            f'<span class="lang-tag">{label}</span></div>'
            f"<pre><code>{esc(codes[key])}</code></pre></div>"
        )
    return (
        f'<div class="tabs" data-tabs{" data-editable" if group_id.endswith("-stub") else ""}>\n'
        '  <div class="tab-bar">\n'
        '    <div class="tab-btns" role="tablist" aria-label="Choose a language">\n'
        f"      {'\n      '.join(buttons)}\n"
        "    </div>\n"
        '    <button class="copy-btn" type="button">Copy code</button>\n'
        "  </div>\n"
        '  <div class="tab-panels">\n'
        f"    {'\n    '.join(panels)}\n"
        "  </div>\n"
        "</div>"
    )


def render_signature_table(problem: dict) -> str:
    sigs = SIGNATURES[problem["number"]]
    rows = "\n".join(
        f"        <tr><td>{LANG_LABEL[key]}</td><td><code>{esc(sigs[key])}</code></td></tr>"
        for key, _label, _ext in LANGS
    )
    return (
        '<div class="table-wrap">\n'
        '  <table class="data">\n'
        "    <thead><tr><th>Language</th><th>Exact signature (the tests call this)</th></tr></thead>\n"
        f"    <tbody>\n{rows}\n    </tbody>\n"
        "  </table>\n"
        "</div>"
    )


def render_problem(problem: dict, allow_missing: bool) -> str:
    number = problem["number"]
    solutions = {}
    stubs = {}
    for key, _label, _ext in LANGS:
        stubs[key] = read_code(number, "stub", key, allow_missing)
        solutions[key] = read_code(number, "solution", key, allow_missing)
        check_solution(problem, key, "stub", stubs[key], allow_missing)
        check_solution(problem, key, "solution", solutions[key], allow_missing)

    statements = "\n".join(f"      <p>{paragraph}</p>" for paragraph in problem["statement"])

    examples = []
    for example in problem["examples"]:
        rows = [
            render_io_row("Input", example["input"]),
            render_io_row("Output", example["output"]),
        ]
        if example.get("explanation"):
            rows.append(render_io_row("Explanation", example["explanation"], plain=True))
        examples.append(
            f'      <div class="example">\n'
            f'        <div class="example-label">{example["label"]}</div>\n'
            f"        {chr(10).join(rows)}\n"
            f"      </div>"
        )

    constraints = "\n".join(
        f"        <li>{item}</li>" for item in problem["constraints"]
    )

    topics = "".join(
        f'<span class="pill gray">{topic}</span>' for topic in problem["topics"]
    )

    hints = "\n".join(f"        <li>{hint}</li>" for hint in problem["hints"])

    notes_link = (
        f'<a href="#{problem["notes_anchor"]}">{problem["notes_label"]}</a>'
    )

    return f"""
    <section class="problem" id="{problem["slug"]}">
      <div class="problem-index">Problem {number}</div>
      <div class="problem-head">
        <h2 class="problem-title">{problem["title"]}</h2>
        <span class="pill difficulty {problem["difficulty_class"]}">{problem["difficulty"]}</span>
      </div>
      <div class="problem-meta">{topics}</div>

{statements}

      <h3>Examples</h3>
{chr(10).join(examples)}

      <h3>Constraints</h3>
      <div class="constraints">
        <ul>
{constraints}
        </ul>
      </div>

      <h3>Function signature</h3>
{render_signature_table(problem)}
      <p class="sig-note">{problem["sig_note"]}</p>

      <h3>Starter template</h3>
      <p class="solution-note">Edit the TODO below, or copy the template into your editor. Changes here are temporary and clear on refresh. Keep the function signature unchanged.</p>
{render_tabs(f"p{number}-stub", "Starter template", stubs)}

      <h3>Hints</h3>
      <details>
        <summary>Show hints (open only if you are stuck)</summary>
        <ol class="hint-list">
{hints}
        </ol>
      </details>

      <h3>Reference solution</h3>
      <p class="solution-note">Try the problem yourself first. Reading a solution you have not attempted teaches very little.</p>
      <details>
        <summary>Show the reference solution</summary>
{render_tabs(f"p{number}-solution", "Reference solution", solutions)}
      </details>

      <div class="problem-links">
        Related notes: {notes_link} &nbsp;&middot;&nbsp; <a href="#problem-index">Back to the problem index</a>
      </div>
    </section>
"""


def build_problem_index() -> str:
    rows = []
    for problem in PROBLEMS:
        topics = " &middot; ".join(problem["topics"])
        rows.append(
            f"        <tr>\n"
            f'          <td>{problem["number"]}</td>\n'
            f'          <td><a href="#{problem["slug"]}">{problem["title"]}</a></td>\n'
            f'          <td><span class="pill difficulty {problem["difficulty_class"]}">{problem["difficulty"]}</span></td>\n'
            f"          <td>{topics}</td>\n"
            f"        </tr>"
        )
    return (
        '<div class="table-wrap">\n'
        '  <table class="data">\n'
        "    <thead><tr><th>#</th><th>Problem</th><th>Difficulty</th><th>Topics</th></tr></thead>\n"
        f"    <tbody>\n{chr(10).join(rows)}\n    </tbody>\n"
        "  </table>\n"
        "</div>"
    )


HEAD = (
    """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Recitation 1 · Sorting Algorithms — COMPSCI 301</title>
  <meta name="description" content="Six LeetCode-style sorting exercises for COMPSCI 301 Recitation 1: bubble sort, insertion sort, stable sorting, counting inversions, quick sort, and quickselect. Starter templates and verified reference solutions in C, C++, C#, Java, Python and JavaScript.">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/style.css">
  <link rel="stylesheet" href="assets/notes.css">
  <noscript><style>"""
    + NOSCRIPT_STYLE
    + """  </style></noscript>
  <script src="assets/app.js" defer></script>
</head>
<body>
"""
)

HEADER = header("recitation1.html")

HERO = """<section class="page-hero" id="top"><div class="container">
<span class="eyebrow">Recitation 1 · Available</span><h1>Sorting Algorithms</h1>
<p class="subtitle">Concept notes and six practice problems in one place: bubble, insertion, merge and quick sort.</p>
<p class="hero-meta">Read the notes, try the exercises, and use Problem 6 for independent exploration.</p>
<div class="hero-actions"><a class="btn primary" href="#notes">Notes</a><a class="btn ghost" href="#exercises">Exercises</a></div>
<div class="callout info"><span class="callout-title">Course materials</span><p>The official course site is temporarily unavailable. These materials support the recitation; instructor announcements remain authoritative.</p></div>
</div></section>"""

INTRO = """    <section class="section" id="how-to-use">
      <div class="section-title"><h2>How these exercises work</h2></div>
      <div class="practice-intro">
        <ol class="steps">
          <li><strong>Pick your language.</strong> Choose C, C++, C#, Java, Python or JavaScript in
            any code block &mdash; your choice is remembered and applied to every problem on this
            page. Java is selected by default because it is the CS201 language.</li>
          <li><strong>Fill in the TODO.</strong> Each problem prints the exact function signature the
            tests use, plus a starter template. Keep the signature unchanged.</li>
          <li><strong>Implement the algorithm yourself.</strong> Built-in sorting calls are off limits
            in these exercises; the point is to write the loops and the recursion yourself.</li>
          <li><strong>Examples, then hints, then solutions.</strong> Check the worked examples, open the
            hints if you are stuck, and read the reference solution only after a serious attempt.</li>
          <li><strong>Choose your level.</strong> Use the 30-minute practice time for problems that
            help you. You do not need to finish all six. Problem 6 is optional exploration and will
            not be covered in class.</li>
          <li><strong>Ask questions.</strong> Bring your attempt to the session. There is no submission
            and no autograder &mdash; the goal is understanding, not a score.</li>
        </ol>
      </div>
      <p class="note" id="editor-help">Temporary editor: Tab inserts four spaces; Shift+Tab removes
        leading indentation on the current line. Press Escape, then Tab to move focus out.
        Switch languages without losing drafts on this page. Reset code restores the current template;
        refreshing restores all templates. Code is not saved or run by this website.</p>
      <div class="callout tip">
        <span class="callout-title">Pick once, copy anywhere</span>
        <p>Language tabs are synchronized across all six problems, and every code block has a
          <strong>Copy code</strong> button. Starter templates can be edited here with syntax highlighting;
          Copy code copies your current draft. To run it, paste it into an environment with the compiler or interpreter for your language already available.
          These are function templates, not complete runnable programs: add a test call, and a
          <code>main</code> method or function where your language requires one. This page displays
          code; it does not execute or grade it.</p>
      </div>
    </section>
"""

PROBLEM_INDEX_HEAD = """    <section class="section" id="problem-index">
      <div class="section-title"><h2>Problem index</h2></div>
"""

PROBLEM_INDEX_TAIL = """      <p class="note">
        Difficulty labels: <span class="pill difficulty easy">Easy</span>
        <span class="pill difficulty medium">Medium</span>
        &mdash; they refer to the algorithm, not to how long the code is.
      </p>
    </section>
"""

FINISHED_EARLY = """    <section class="section" id="finished-early">
      <div class="section-title"><h2>Finished early?</h2></div>
      <div class="card-grid">
        <div class="card">
          <span class="pill blue">Challenge</span>
          <h3>Make quickselect fast</h3>
          <p>Problem 6 is the hardest exercise here. If you finish early, implement it without
            looking at the 3-way partition hint, then prove to yourself why the expected runtime
            is O(n) rather than O(n log n).</p>
          <a class="more-link" href="#problem-6">Open Problem 6</a>
        </div>
        <div class="card">
          <span class="pill green">Experiment</span>
          <h3>Count the shifts</h3>
          <p>On a reversed array of length n, insertion sort performs exactly n(n&minus;1)/2 shifts.
            Verify that with your Problem 2 solution for n = 5, 10 and 100, then explain where the
            formula comes from.</p>
          <a class="more-link" href="#problem-2">Open Problem 2</a>
        </div>
        <div class="card">
          <span class="pill orange">Read ahead</span>
          <h3>Explore order statistics</h3>
          <p>Quickselect is your first taste of order statistics. Selection and binary
            search are related topics to explore; the notes page ends with a short preview so you can start thinking about it.</p>
          <a class="more-link" href="#notes">Revisit the Recitation 1 notes</a>
        </div>
      </div>
      <div class="callout info">
        <span class="callout-title">Optional and ungraded</span>
        <p>These problems are practice material for the Recitation 1 session. They are not part of your
          grade, there is nothing to upload, and you are welcome to work on them before, during or
          after the session. If a reference answer looks wrong, tell the TA.</p>
      </div>
    </section>
"""

FOOTER = """  <footer class="site-footer">
    <div class="container">
      <p>COMPSCI 301 · course materials for the recitation sessions.</p>
      <p class="muted small">The official course site is temporarily unavailable. If you spot a mistake, tell the TA.</p>
    </div>
  </footer>

</body>
</html>
"""


def build(allow_missing: bool) -> str:
    notes = (ROOT / "tools/site_src/recitation1-notes.html").read_text(encoding="utf-8")
    parts = [HEAD, HEADER, '<main id="main">', HERO, '<div class="container">',
             '<section class="section" id="notes"><div class="section-title"><h2>Notes</h2></div>',
             notes, '</section>',
             '<section class="section" id="exercises"><div class="section-title"><h2>Exercises</h2></div>',
             INTRO, PROBLEM_INDEX_HEAD]
    parts.append(build_problem_index())
    parts.append(PROBLEM_INDEX_TAIL)
    for problem in PROBLEMS:
        parts.append(render_problem(problem, allow_missing))
    parts.append(FINISHED_EARLY)
    parts.append("</section></div></main>\n")
    parts.append(FOOTER)
    return "".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"output file (default: {DEFAULT_OUT.relative_to(ROOT)})",
    )
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="render placeholders instead of failing on missing files (local preview only)",
    )
    args = parser.parse_args()

    try:
        page = build(args.allow_missing)
    except BuildError as error:
        print(f"BUILD FAILED: {error}", file=sys.stderr)
        return 1

    out = args.out if args.out.is_absolute() else (ROOT / args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    code_blocks = len(PROBLEMS) * len(LANGS) * 2
    print(
        f"wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}: {len(page):,} bytes, "
        f"{len(PROBLEMS)} problems, {code_blocks} code panels ({len(LANGS)} languages x solutions + stubs)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
