#!/usr/bin/env python3
"""Build Recitation 3 HTML and practice notebooks from shared prose, LCS, and Huffman code."""
from pathlib import Path
from copy import deepcopy
import json
import re

from build_exercises import (LANG_EXT, LANG_LABEL, BANNED_IN_SOLUTIONS,
                             BuildError, NOSCRIPT_STYLE, esc, function_name, render_tabs)
from problems import LANGS
from build_notebooks import (KERNELS, Node, code_cell, collapse, md_cell, parse_fragment,
                             render_block, render_inline, render_section, SITE_URL, LANG_NAME)
from site_layout import jump_bar, page

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).with_name('recitation3-content.html')
SOL = ROOT / 'material/week3/solutions'
CHECKS = ROOT / 'material/week3/checks'
TASKS = {
    'lcs': {
        'section': 'exercise-2-code', 'marker': 'LCS', 'title': 'LCS',
        'signatures': {
            'c': 'char* longestCommonSubsequence(const char* a, const char* b)',
            'cpp': 'std::string longestCommonSubsequence(const std::string& a, const std::string& b)',
            'cs': 'public static string LongestCommonSubsequence(string a, string b)',
            'java': 'public static String longestCommonSubsequence(String a, String b)',
            'py': 'def longest_common_subsequence(a: str, b: str) -> str',
            'js': 'function longestCommonSubsequence(a, b)',
        },
    },
    'huffman': {
        'section': 'extra-build', 'marker': 'HUFFMAN', 'title': 'Huffman',
        'signatures': {
            'c': 'char** huffmanCodes(const int* freq, int n)',
            'cpp': 'std::vector<std::string> huffmanCodes(const std::vector<int>& freq)',
            'cs': 'public static string[] HuffmanCodes(int[] freq)',
            'java': 'public static String[] huffmanCodes(int[] freq)',
            'py': 'def huffman_codes(freq: list[int]) -> list[str]',
            'js': 'function huffmanCodes(freq)',
        },
    },
}
TITLE = 'Dynamic Programming & Greedy Algorithms'
SECTION_IDS = ['overview', 'dp-review', 'greedy-review', 'exercises', 'exercise-1',
               'exercise-2', 'exercise-2-code', 'discussion', 'extra', 'extra-build', 'references']


WRITTEN_RESPONSES = {
    'greedy-review': """### Your answer — Greedy review (optional)

**Try it, 1–2–5 system:** List your exchange rules, then show the smaller coins add up to less than each coin.

**Quick check, {1, 7, 10}:** Compute q and r, apply the test, and give a counterexample if greedy fails.
""",
    'exercise-1': """### Your answer — Exercise 1

1. **Trace:** EDD order, completion times, lateness, and $L_{\\max}$; then $L_{\\max}$ for SPT.
2. **Complexity:** Time and space, and the step that dominates.
3. **Correctness:**
   - 3.1 Why a non-EDD schedule has an adjacent inversion:
   - 3.2 Lateness of i and j before and after the swap:
   - 3.3 How to reach an EDD schedule without increasing $L_{\\max}$:
""",
    'exercise-2': """### Your answer — Exercise 2, Part A

1. **Meaning of L(i, j) and where the answer is:** Write your answer here.
2. **Case $x_i = y_j$:** L(i, j) = … and why matching is safe.
3. **Case $x_i \\neq y_j$:** L(i, j) = …
4. **Base cases and fill order:** Write your answer here.
5. **Table for "ABCB" / "BDCAB":** Fill the table below, then give the LCS length and one LCS.

| | "" | B | D | C | A | B |
|---|---|---|---|---|---|---|
| "" | | | | | | |
| A | | | | | | |
| B | | | | | | |
| C | | | | | | |
| B | | | | | | |

6. **Cost:** Number of cells, work per cell, time and space.
""",
    'exercise-2-code': """### Your explanation — Exercise 2, Part B

- **Traceback correctness:** Why is the returned string a common subsequence of maximum length?
- **Complexity:** Time and space of the fill and the traceback.
- **Two rows:** Why is a two-row table enough for the length but not for the string?
""",
    'discussion': """### Your reflection

**LCS indexing bug:** What goes wrong with `a[i] == b[j]`, and how do you fix it?

**Exit check:** What does the EDD proof rely on that has no counterpart for coins {1, 3, 4}?
""",
}


def read_code(task, kind, lang):
    path = SOL / task / f'{lang}.{kind}.{LANG_EXT[lang]}'
    text = path.read_text(encoding='utf-8')
    if not text.strip() or function_name(TASKS[task]['signatures'][lang]) not in text:
        raise BuildError(f'empty or mismatched {task} {kind}: {path}')
    if kind == 'solution':
        for pattern, label in BANNED_IN_SOLUTIONS:
            if re.search(pattern, text):
                raise BuildError(f'library sort ({label}) in {path}')
    return text


def strip_web_only(node):
    node.children = [child for child in node.children
                     if not (isinstance(child, Node) and 'data-web-only' in child.attrs)]
    for child in node.children:
        if isinstance(child, Node):
            strip_web_only(child)


MATH_OPEN, MATH_CLOSE = '\ue000', '\ue001'
MATH_RUN = re.compile(f'(?:{MATH_OPEN}\\d+{MATH_CLOSE})+')
NAMED = {'log': '\\log', 'max': '\\max', 'min': '\\min'}


def latex_atom(text):
    text = text.replace('−', '-').replace('′', "'")
    return NAMED.get(text, '\\mathrm{' + text + '}' if len(text) > 1 and text.isalpha() else text)


def math_scripts(node, formulas):
    """Replace base<sub>s</sub> and base<sup>s</sup> with placeholders for $base_{s}$."""
    for index, child in enumerate(node.children):
        if not isinstance(child, Node):
            continue
        if child.tag not in ('sub', 'sup'):
            math_scripts(child, formulas)
            continue
        base = ''
        previous = node.children[index - 1] if index else None
        if isinstance(previous, str):
            match = re.search(r'(log|max|min|[A-Za-z0-9]′?)$', previous)
            if match:
                base = match[1]
                node.children[index - 1] = previous[:match.start()]
        mark = '_' if child.tag == 'sub' else '^'
        formulas.append(latex_atom(base) + mark + '{' + latex_atom(child.text()) + '}')
        node.children[index] = f'{MATH_OPEN}{len(formulas) - 1}{MATH_CLOSE}'


def restore_math(text, formulas):
    # Adjacent scripts such as x<sub>i</sub>c<sub>i</sub> share one $...$ span.
    return MATH_RUN.sub(lambda run: '$' + ''.join(formulas[int(n)] for n in re.findall(r'\d+', run[0])) + '$', text)


def notebook_section(section, lang):
    section = deepcopy(section)
    strip_web_only(section)
    formulas = []
    math_scripts(section, formulas)
    # Notebook heading anchors differ from webpage ids. Preserve labels as text.
    for link in section.find_all('a'):
        if link.attrs.get('href', '').startswith('#'):
            link.tag = 'span'
            link.attrs = {}
    # The converter omits all details blocks, so answers never enter notebooks.
    # Add only explicitly marked hint blocks back as collapsible hints.
    result = render_section(section)
    for detail in section.find_all('details'):
        if detail.attrs.get('data-kind') != 'hint':
            continue
        summary = collapse(render_inline(detail.find_all('summary')[0]))
        blocks = []
        for child in detail.children:
            if isinstance(child, Node) and child.tag != 'summary':
                blocks.extend(render_block(child))
        result += f'\n\n<details><summary>{summary}</summary>\n\n' + '\n\n'.join(blocks) + '\n\n</details>'
    for task in TASKS.values():
        if section.attrs.get('id') == task['section']:
            result = result.replace('### Function interfaces',
                                    f"### Function interface ({LANG_LABEL[lang]})\n\n```{LANG_NAME[lang]}\n{task['signatures'][lang]}\n```")
            result = result.replace('### Starter template · edit or copy\n\n', '')
            result += '\n\nEdit and run the starter definition in the next cell, then run its self-check.'
    result = restore_math(result, formulas)
    # Notebook links must resolve independently of the download directory.
    result = re.sub(r'\]\((recitation\d+\.html(?:#[^)]+)?)\)',
                    lambda m: f']({SITE_URL}/{m[1]})', result)
    return result


def build_notebook(lang, sections):
    label = LANG_LABEL[lang]
    intro = f'''# Recitation 3 — {TITLE} ({label})

Save this notebook in your `cs301-notebooks` project and open it in your IDE.
Use the {'project .venv Python / Python (CS301)' if lang == 'py' else 'Java (IJava)'} kernel.
See [Recitation 0]({SITE_URL}/recitation0.html) for setup.

Write your reasoning in the Markdown answer cells (double-click to edit, Shift+Enter to render).
For Exercise 2, Part B, edit and run the starter definition, then run its self-check.
An untouched starter fails the check; that is expected. Keep the signature unchanged.
The Huffman coding section at the end is optional extra content and has its own starter and check.
Reference answers are not in this notebook; they are on the
[Recitation 3 page]({SITE_URL}/recitation3.html). Nothing is submitted or graded.
'''
    if lang == 'java':
        intro += '\nIJava accepts class definitions and statements directly, without a main method. Each starter defines a class named `Solution`: re-run the matching starter cell before its check cell. A check failure throws an exception; no JVM assertion flag is needed.\n'
    cells = [md_cell('intro', intro)]
    for section_id in SECTION_IDS:
        cells.append(md_cell(section_id, notebook_section(sections[section_id], lang)))
        for task, spec in TASKS.items():
            if section_id == spec['section']:
                cells.extend([code_cell(f'{task}-stub', read_code(task, 'stub', lang)),
                              code_cell(f'{task}-check', (CHECKS / f'{lang}.{task}.check.{LANG_EXT[lang]}').read_text())])
        if section_id in WRITTEN_RESPONSES:
            cells.append(md_cell(f'{section_id}-response', WRITTEN_RESPONSES[section_id]))
    return {'cells': cells, 'metadata': KERNELS[lang], 'nbformat': 4, 'nbformat_minor': 5}


def build_recitation3():
    source = SOURCE.read_text(encoding='utf-8')
    root = parse_fragment(source)
    sections = {node.attrs.get('id'): node for node in root.find_all('section')}
    if list(sections) != SECTION_IDS:
        raise BuildError('Recitation 3 sections are missing, duplicated, or out of order')
    for task, spec in TASKS.items():
        stubs = {lang: read_code(task, 'stub', lang) for lang, _, _ in LANGS}
        solutions = {lang: read_code(task, 'solution', lang) for lang, _, _ in LANGS}
        signature_rows = ''.join(f'<tr data-sig-lang="{lang}"><td>{LANG_LABEL[lang]}</td><td><code>{esc(sig)}</code></td></tr>'
                                 for lang, sig in spec['signatures'].items())
        replacements = {
            f'<!-- {spec["marker"]}_SIGNATURES -->': '<div class="table-wrap"><table class="data sig-table"><thead><tr><th>Language</th><th>Exact interface</th></tr></thead><tbody>' + signature_rows + '</tbody></table></div>',
            f'<!-- {spec["marker"]}_STARTER -->': render_tabs(f'r3-{task}-stub', f'{spec["title"]} starter template', stubs),
            f'<!-- {spec["marker"]}_SOLUTION -->': render_tabs(f'r3-{task}-solution', f'{spec["title"]} reference solution', solutions),
        }
        for marker, replacement in replacements.items():
            if source.count(marker) != 1:
                raise BuildError(f'expected exactly one {marker}')
            source = source.replace(marker, replacement)
    notebooks = ROOT / 'site/notebooks'
    notebooks.mkdir(exist_ok=True)
    for lang, name in [('py', 'python'), ('java', 'java')]:
        notebook = build_notebook(lang, sections)
        (notebooks / f'recitation3-{name}.ipynb').write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + '\n')
    hero = f'''<section class="page-hero" id="top"><div class="container">
<span class="eyebrow">Recitation 3 · Notes &amp; practice</span><h1>{esc(TITLE)}</h1>
<p class="subtitle">Set up the key math function, prove when greedy is right, and build an LCS from its table.</p>
<div class="hero-actions"><a class="btn primary" href="#notes">Notes</a><a class="btn ghost" href="#exercises">Core practice</a><a class="btn ghost" href="#extra">Extra · Huffman</a><a class="btn ghost" href="#notebooks">Notebooks</a></div>
</div></section>'''
    downloads = '''<section class="section" id="notebooks"><div class="section-title"><h2>Practice notebooks</h2></div>
<p>Choose Python or Java. Each notebook contains these notes, written-response cells, the LCS starter with runnable self-checks, and the optional Huffman starter and checks. Reference answers stay on this page. Save the notebook in your course project and open it directly in your IDE with the matching kernel.</p>
<div class="hero-actions"><a class="btn primary" href="notebooks/recitation3-python.ipynb" download>Download Python notebook (.ipynb)</a><a class="btn ghost" href="notebooks/recitation3-java.ipynb" download>Download Java notebook (.ipynb)</a></div></section>'''
    # Notes anchor groups the review; exercise sections remain directly linkable.
    split = source.index('<section class="section" id="exercises">')
    jump = jump_bar([('overview', 'Overview'), ('dp-review', 'DP path'), ('greedy-review', 'Greedy'),
                     ('exercise-1', 'Ex 1'), ('exercise-2', 'Ex 2A'), ('exercise-2-code', 'Ex 2B'),
                     ('discussion', 'Discussion'), ('extra', 'Extra'), ('notebooks', 'Notebooks')])
    body = hero + '<div class="container">' + jump + '<div id="notes">' + source[:split] + '</div>' + source[split:] + downloads + '</div>'
    head = '<link rel="stylesheet" href="assets/notes.css"><noscript><style>' + NOSCRIPT_STYLE + '</style></noscript>'
    (ROOT / 'site/recitation3.html').write_text(page('recitation3.html', 'Recitation 3 · ' + TITLE, body, head))
    print('Built Recitation 3 notes, core exercises, Huffman extra, and Python/Java notebooks.')


if __name__ == '__main__':
    build_recitation3()
