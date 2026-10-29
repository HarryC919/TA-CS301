#!/usr/bin/env python3
"""Build Recitation 2 HTML and practice notebooks from shared prose and merge code."""
from pathlib import Path
from copy import deepcopy
import json
import re

from build_exercises import (LANG_EXT, LANG_LABEL, BANNED_IN_SOLUTIONS,
                             BuildError, NOSCRIPT_STYLE, esc, function_name, render_tabs)
from problems import LANGS
from build_notebooks import (KERNELS, Node, code_cell, md_cell, parse_fragment,
                             render_block, render_section, SITE_URL, LANG_NAME)
from site_layout import page

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).with_name('recitation2-content.html')
SOL = ROOT / 'material/week2/solutions/p3'
CHECKS = ROOT / 'material/week2/checks'
SIGNATURES = {
    'c': 'int* mergeSorted(const int* left, int leftSize, const int* right, int rightSize, int* returnSize)',
    'cpp': 'std::vector<int> mergeSorted(const std::vector<int>& left, const std::vector<int>& right)',
    'cs': 'public static int[] MergeSorted(int[] left, int[] right)',
    'java': 'public static int[] mergeSorted(int[] left, int[] right)',
    'py': 'def merge_sorted(left: list[int], right: list[int]) -> list[int]',
    'js': 'function mergeSorted(left, right)',
}
TITLE = 'Asymptotic Notation & Divide and Conquer'
SECTION_IDS = ['overview', 'notation', 'divide-conquer', 'exercises', 'exercise-1',
               'exercise-2', 'exercise-3', 'optional-practice', 'discussion', 'references']


WRITTEN_RESPONSES = {
    'exercise-1': """### Your answer — Exercise 1

1. **Validity and tightness of the three bounds:** Write your reasoning here.
2. **Constants and threshold for the first claim:** Give c, n₀, and the inequality.
3. **Bound notation versus case analysis:** Correct the classmate's statement.
""",
    'exercise-2': """### Your answer — Exercise 2

1. **Recurrence and base case:** Write your answer here.
2. **Tree for n = 8:** List call count, size per call, and local work at each depth.
3. **General total:** Give the level/leaf counts, exact total, and tight bound.
""",
    'exercise-3': """### Your explanation — Exercise 3

- **Correctness:** Explain why choosing the smaller head is safe and why every occurrence appears once.
- **Edge cases:** Explain what happens when either input is empty.
- **Complexity:** State time, output storage, and working space excluding the output.
""",
    'optional-practice': """### Your answer — Optional practice

**A. Loop growth:** Give each iteration count and tight bound, with reasoning.

**B. Quicksort shapes (after lecture coverage):** Compare the recursion shapes and total work.
""",
    'discussion': """### Your reflection

**Merge shortcut:** Explain the bug and how to repair it.

**Exit check:** Explain why halving alone does not imply logarithmic running time.
""",
}


def read_code(kind, lang):
    path = SOL / f'{lang}.{kind}.{LANG_EXT[lang]}'
    text = path.read_text(encoding='utf-8')
    if not text.strip() or function_name(SIGNATURES[lang]) not in text:
        raise BuildError(f'empty or mismatched merge {kind}: {path}')
    if kind == 'solution':
        for pattern, label in BANNED_IN_SOLUTIONS:
            if re.search(pattern, text):
                raise BuildError(f'library sort ({label}) in {path}')
        if re.search(r'\b(?:std::merge|heapq\.merge)\s*\(', text):
            raise BuildError(f'library merge in {path}')
    return text


def notebook_section(section, lang):
    section = deepcopy(section)
    # Notebook heading anchors differ from webpage ids. Preserve labels as text.
    for link in section.find_all('a'):
        if link.attrs.get('href', '').startswith('#'):
            link.tag = 'span'
            link.attrs = {}
    # The existing converter omits all details blocks, so answers never enter
    # notebooks. Add only explicitly marked hint blocks back as collapsible hints.
    result = render_section(section)
    for detail in section.find_all('details'):
        if detail.attrs.get('data-kind') != 'hint':
            continue
        summary = detail.find_all('summary')[0].text()
        blocks = []
        for child in detail.children:
            if isinstance(child, Node) and child.tag != 'summary':
                blocks.extend(render_block(child))
        result += f'\n\n<details><summary>{summary}</summary>\n\n' + '\n\n'.join(blocks) + '\n\n</details>'
    if section.attrs.get('id') == 'exercise-3':
        result = result.replace('### Function interfaces',
                                f"### Function interface ({LANG_LABEL[lang]})\n\n```{LANG_NAME[lang]}\n{SIGNATURES[lang]}\n```")
        result = result.replace('### Starter template · edit or copy', '')
        result = re.sub(r'In C, write the result length.*?Keep the selected interface unchanged\.',
                        'Return a new list/array and keep the interface unchanged.', result)
        result += '\n\nEdit and run the starter definition in the next cell, then run its self-check.'
    # Notebook links must resolve independently of the download directory.
    result = re.sub(r'\]\((recitation\d+\.html(?:#[^)]+)?)\)',
                    lambda m: f']({SITE_URL}/{m[1]})', result)
    return result


def build_notebook(lang, sections):
    label = LANG_LABEL[lang]
    intro = f'''# Recitation 2 — {TITLE} ({label})

Save this notebook in your `cs301-notebooks` project and open it in your IDE.
Use the {'project .venv Python / Python (CS301)' if lang == 'py' else 'Java (IJava)'} kernel.
See [Recitation 0]({SITE_URL}/recitation0.html) for setup.

Write your reasoning in the Markdown answer cells (double-click to edit, Shift+Enter to render). For Exercise 3, edit
and run the starter definition, then run its self-check. An untouched starter
fails the check; that is expected. Keep the signature unchanged and use no library
sort or merge routine. The notebook does not contain reference answers; they are
on the [Recitation 2 page]({SITE_URL}/recitation2.html). Nothing is submitted or graded.
'''
    if lang == 'java':
        intro += '\nIJava accepts class definitions and statements directly, without a main method. Re-run the Solution cell after editing it, then re-run the check cell. A check failure throws an exception; no JVM assertion flag is needed.\n'
    cells = [md_cell('intro', intro)]
    for section_id in SECTION_IDS:
        cells.append(md_cell(section_id, notebook_section(sections[section_id], lang)))
        if section_id == 'exercise-3':
            cells.extend([code_cell('p3-stub', read_code('stub', lang)),
                          code_cell('p3-check', (CHECKS / f'{lang}.check.{LANG_EXT[lang]}').read_text())])
        if section_id in WRITTEN_RESPONSES:
            cells.append(md_cell(f'{section_id}-response', WRITTEN_RESPONSES[section_id]))
    return {'cells': cells, 'metadata': KERNELS[lang], 'nbformat': 4, 'nbformat_minor': 5}


def build_recitation2():
    source = SOURCE.read_text(encoding='utf-8')
    root = parse_fragment(source)
    sections = {node.attrs.get('id'): node for node in root.find_all('section')}
    if list(sections) != SECTION_IDS:
        raise BuildError('Recitation 2 sections are missing, duplicated, or out of order')
    stubs = {lang: read_code('stub', lang) for lang, _, _ in LANGS}
    solutions = {lang: read_code('solution', lang) for lang, _, _ in LANGS}
    signature_rows = ''.join(f'<tr><td>{LANG_LABEL[lang]}</td><td><code>{esc(sig)}</code></td></tr>'
                             for lang, sig in SIGNATURES.items())
    replacements = {
        '<!-- MERGE_SIGNATURES -->': '<div class="table-wrap"><table class="data"><thead><tr><th>Language</th><th>Exact interface</th></tr></thead><tbody>' + signature_rows + '</tbody></table></div>',
        '<!-- MERGE_STARTER -->': render_tabs('r2-p3-stub', 'Merge starter template', stubs),
        '<!-- MERGE_SOLUTION -->': render_tabs('r2-p3-solution', 'Merge reference solution', solutions),
    }
    for marker, replacement in replacements.items():
        if source.count(marker) != 1:
            raise BuildError(f'expected exactly one {marker}')
        source = source.replace(marker, replacement)
    notebooks = ROOT / 'site/notebooks'
    notebooks.mkdir(exist_ok=True)
    for lang, name in [('py', 'python'), ('java', 'java')]:
        notebook = build_notebook(lang, sections)
        (notebooks / f'recitation2-{name}.ipynb').write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + '\n')
    hero = f'''<section class="page-hero" id="top"><div class="container">
<span class="eyebrow">Recitation 2 · Notes &amp; practice</span><h1>{esc(TITLE)}</h1>
<p class="subtitle">From growth bounds to recursive work: explain the analysis, then implement the merge step.</p>
<div class="hero-actions"><a class="btn primary" href="#notes">Notes</a><a class="btn ghost" href="#exercises">Core practice</a><a class="btn ghost" href="#optional-practice">Optional practice</a><a class="btn ghost" href="#notebooks">Notebooks</a></div>
</div></section>'''
    downloads = '''<section class="section" id="notebooks"><div class="section-title"><h2>Practice notebooks</h2></div>
<p>Choose Python or Java. Each notebook contains these notes, written-response cells, the merge starter, and runnable merge self-checks. Reference answers stay on this page. Save the notebook in your course project and open it directly in your IDE with the matching kernel.</p>
<div class="hero-actions"><a class="btn primary" href="notebooks/recitation2-python.ipynb" download>Download Python notebook (.ipynb)</a><a class="btn ghost" href="notebooks/recitation2-java.ipynb" download>Download Java notebook (.ipynb)</a></div></section>'''
    # Notes anchor groups the review; exercise sections remain directly linkable.
    split = source.index('<section class="section" id="exercises">')
    body = hero + '<div class="container"><div id="notes">' + source[:split] + '</div>' + source[split:] + downloads + '</div>'
    head = '<link rel="stylesheet" href="assets/notes.css"><noscript><style>' + NOSCRIPT_STYLE + '</style></noscript>'
    (ROOT / 'site/recitation2.html').write_text(page('recitation2.html', 'Recitation 2 · ' + TITLE, body, head))
    print('Built Recitation 2 notes, core/optional exercises, and Python/Java notebooks.')


if __name__ == '__main__':
    build_recitation2()
