#!/usr/bin/env python3
"""Build Recitation 4 HTML and practice notebooks from shared prose, cheapest-route, and Floyd–Warshall code."""
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
SOURCE = Path(__file__).with_name('recitation4-content.html')
SOL = ROOT / 'material/week4/solutions'
CHECKS = ROOT / 'material/week4/checks'
TASKS = {
    'stops': {
        'section': 'exercise-3', 'marker': 'STOPS', 'title': 'Cheapest route',
        'signatures': {
            'c': 'int cheapestRoute(int n, const int* flights, int m, int src, int dst, int k)',
            'cpp': 'int cheapestRoute(int n, const std::vector<std::vector<int>>& flights, int src, int dst, int k)',
            'cs': 'public static int CheapestRoute(int n, int[][] flights, int src, int dst, int k)',
            'java': 'public static int cheapestRoute(int n, int[][] flights, int src, int dst, int k)',
            'py': 'def cheapest_route(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int',
            'js': 'function cheapestRoute(n, flights, src, dst, k)',
        },
    },
    'floyd': {
        'section': 'extra-build', 'marker': 'FLOYD', 'title': 'Floyd–Warshall',
        'signatures': {
            'c': 'int* floydWarshall(int n, const int* edges, int m)',
            'cpp': 'std::vector<std::vector<int>> floydWarshall(int n, const std::vector<std::vector<int>>& edges)',
            'cs': 'public static int[][] FloydWarshall(int n, int[][] edges)',
            'java': 'public static int[][] floydWarshall(int n, int[][] edges)',
            'py': 'def floyd_warshall(n: int, edges: list[list[int]]) -> list[list[int]]',
            'js': 'function floydWarshall(n, edges)',
        },
    },
}
TITLE = 'Graph Algorithms'
SECTION_IDS = ['overview', 'search-review', 'mst-review', 'sp-review', 'exercises', 'exercise-1',
               'exercise-2', 'exercise-3', 'optional-practice', 'discussion', 'extra', 'extra-build', 'references']


WRITTEN_RESPONSES = {
    'exercise-1': """### Your answer — Exercise 1

1. **Kruskal:** Accepted edges in order, the first rejected edge and its cycle, and the total weight.
2. **Prim from A:** The edge chosen at each step. Same tree? Same order? Why must the trees agree?
3. **True or false:**
   - 3a. Heaviest edge never in an MST:
   - 3b. Lightest edge in every MST (distinct weights):
   - 3c. MST contains shortest paths:
""",
    'exercise-2': """### Your answer — Exercise 2

1. **Dijkstra trace:** Order of finalized vertices, final d values, and the true distances.

| Removed (final) | d[S] | d[A] | d[B] | d[T] |
|---|---|---|---|---|
| Start | 0 | ∞ | ∞ | ∞ |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

2. **Diagnosis:** The wrong step and the failed assumption.
3. **Bellman-Ford:** Your run on this graph; why V − 1 rounds suffice; how the extra check detects a negative cycle.
""",
    'exercise-3': """### Your explanation — Exercise 3

- **The copy:** Why does reading from a copy mean round t adds exactly one more flight?
- **Rounds:** Why are k + 1 rounds the right number?
- **Cost:** Time and extra space.
- **Plain Dijkstra:** Why does it fail on the trap example with k = 0?
""",
    'optional-practice': """### Your answer — Optional practice (optional)

1. **Shifted weights:** Your counterexample, and what goes wrong in general.
2. **Bottleneck paths:** Your argument.
""",
    'discussion': """### Your reflection

**Prim vs Dijkstra:** What is each key, and why does only Dijkstra care about negative weights?

**In-place rounds:** Why is writing in place a bug in Exercise 3 but harmless in standard Bellman-Ford?

**Exit check:** Which result can you trust, Prim's or Dijkstra's, on a graph with negative edges, and why?
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
    intro = f'''# Recitation 4 — {TITLE} ({label})

Save this notebook in your `cs301-notebooks` project and open it in your IDE.
Use the {'project .venv Python / Python (CS301)' if lang == 'py' else 'Java (IJava)'} kernel.
See [Recitation 0]({SITE_URL}/recitation0.html) for setup.

Write your reasoning in the Markdown answer cells (double-click to edit, Shift+Enter to render).
For Exercise 3, edit and run the starter definition, then run its self-check.
An untouched starter fails the check; that is expected. Keep the signature unchanged.
The Floyd–Warshall section at the end is optional extra content and has its own starter and check.
Reference answers are not in this notebook; they are on the
[Recitation 4 page]({SITE_URL}/recitation4.html). Nothing is submitted or graded.
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


def build_recitation4():
    source = SOURCE.read_text(encoding='utf-8')
    root = parse_fragment(source)
    sections = {node.attrs.get('id'): node for node in root.find_all('section')}
    if list(sections) != SECTION_IDS:
        raise BuildError('Recitation 4 sections are missing, duplicated, or out of order')
    for task, spec in TASKS.items():
        stubs = {lang: read_code(task, 'stub', lang) for lang, _, _ in LANGS}
        solutions = {lang: read_code(task, 'solution', lang) for lang, _, _ in LANGS}
        signature_rows = ''.join(f'<tr data-sig-lang="{lang}"><td>{LANG_LABEL[lang]}</td><td><code>{esc(sig)}</code></td></tr>'
                                 for lang, sig in spec['signatures'].items())
        replacements = {
            f'<!-- {spec["marker"]}_SIGNATURES -->': '<div class="table-wrap"><table class="data sig-table"><thead><tr><th>Language</th><th>Exact interface</th></tr></thead><tbody>' + signature_rows + '</tbody></table></div>',
            f'<!-- {spec["marker"]}_STARTER -->': render_tabs(f'r4-{task}-stub', f'{spec["title"]} starter template', stubs),
            f'<!-- {spec["marker"]}_SOLUTION -->': render_tabs(f'r4-{task}-solution', f'{spec["title"]} reference solution', solutions),
        }
        for marker, replacement in replacements.items():
            if source.count(marker) != 1:
                raise BuildError(f'expected exactly one {marker}')
            source = source.replace(marker, replacement)
    notebooks = ROOT / 'site/notebooks'
    notebooks.mkdir(exist_ok=True)
    for lang, name in [('py', 'python'), ('java', 'java')]:
        notebook = build_notebook(lang, sections)
        (notebooks / f'recitation4-{name}.ipynb').write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + '\n')
    hero = f'''<section class="page-hero" id="top"><div class="container">
<span class="eyebrow">Recitation 4 · Notes &amp; practice</span><h1>{esc(TITLE)}</h1>
<p class="subtitle">Review graph search, reason about which edges an MST needs, see why Dijkstra needs non-negative weights, and put Bellman-Ford's rounds to work.</p>
<div class="hero-actions"><a class="btn primary" href="#notes">Notes</a><a class="btn ghost" href="#exercises">Core practice</a><a class="btn ghost" href="#extra">Extra · Floyd–Warshall</a><a class="btn ghost" href="#notebooks">Notebooks</a></div>
</div></section>'''
    downloads = '''<section class="section" id="notebooks"><div class="section-title"><h2>Practice notebooks</h2></div>
<p>Choose Python or Java. Each notebook contains these notes, written-response cells, the Exercise 3 starter with runnable self-checks, and the optional Floyd–Warshall starter and checks. Graph diagrams appear on this page only; the notebooks list the same edges in the text. Reference answers stay on this page. Save the notebook in your course project and open it directly in your IDE with the matching kernel.</p>
<div class="hero-actions"><a class="btn primary" href="notebooks/recitation4-python.ipynb" download>Download Python notebook (.ipynb)</a><a class="btn ghost" href="notebooks/recitation4-java.ipynb" download>Download Java notebook (.ipynb)</a></div></section>'''
    # Notes anchor groups the review; exercise sections remain directly linkable.
    split = source.index('<section class="section" id="exercises">')
    jump = jump_bar([('overview', 'Overview'), ('search-review', 'Search'), ('mst-review', 'MST'),
                     ('sp-review', 'Shortest paths'), ('exercise-1', 'Ex 1'), ('exercise-2', 'Ex 2'),
                     ('exercise-3', 'Ex 3'), ('optional-practice', 'Optional'), ('discussion', 'Discussion'),
                     ('extra', 'Extra'), ('notebooks', 'Notebooks')])
    body = hero + '<div class="container">' + jump + '<div id="notes">' + source[:split] + '</div>' + source[split:] + downloads + '</div>'
    head = '<link rel="stylesheet" href="assets/notes.css"><noscript><style>' + NOSCRIPT_STYLE + '</style></noscript>'
    (ROOT / 'site/recitation4.html').write_text(page('recitation4.html', 'Recitation 4 · ' + TITLE, body, head))
    print('Built Recitation 4 notes, core exercises, Floyd–Warshall extra, and Python/Java notebooks.')


if __name__ == '__main__':
    build_recitation4()
