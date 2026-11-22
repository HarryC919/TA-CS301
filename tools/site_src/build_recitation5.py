#!/usr/bin/env python3
"""Build Recitation 5 HTML and practice notebooks from shared prose and the hash-table code."""
from pathlib import Path
from copy import deepcopy
import json
import re

from build_exercises import LANG_EXT, LANG_LABEL, BuildError, NOSCRIPT_STYLE, esc, render_tabs
from problems import LANGS
from build_notebooks import (KERNELS, Node, code_cell, collapse, md_cell, parse_fragment,
                             render_block, render_inline, render_section, SITE_URL, LANG_NAME)
from build_recitation4 import math_scripts, restore_math, strip_web_only
from site_layout import jump_bar, page

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).with_name('recitation5-content.html')
SOL = ROOT / 'material/week5/solutions'
CHECKS = ROOT / 'material/week5/checks'
TASKS = {
    'hashtable': {
        'section': 'exercise-2', 'marker': 'HASHTABLE', 'title': 'Hash table',
        'signatures': {
            'c': ('HashTable* htCreate(int m);\nbool htPut(HashTable* t, int key, int value);\n'
                  'int htGet(const HashTable* t, int key);\nbool htRemove(HashTable* t, int key);\n'
                  'int htSize(const HashTable* t);\nvoid htFree(HashTable* t);'),
            'cpp': ('class HashTable {\n    explicit HashTable(int m);\n    bool put(int key, int value);\n'
                    '    int get(int key) const;\n    bool remove(int key);\n    int size() const;\n};'),
            'cs': ('public class HashTable {\n    public HashTable(int m)\n    public bool Put(int key, int value)\n'
                   '    public int Get(int key)\n    public bool Remove(int key)\n    public int Size()\n}'),
            'java': ('public class HashTable {\n    public HashTable(int m)\n    public boolean put(int key, int value)\n'
                     '    public int get(int key)\n    public boolean remove(int key)\n    public int size()\n}'),
            'py': ('class HashTable:\n    def __init__(self, m: int)\n    def put(self, key: int, value: int) -> bool\n'
                   '    def get(self, key: int) -> int\n    def remove(self, key: int) -> bool\n    def size(self) -> int'),
            'js': ('class HashTable {\n    constructor(m)\n    put(key, value)   // returns a boolean\n'
                   '    get(key)          // returns the value or -1\n    remove(key)       // returns a boolean\n'
                   '    size()\n}'),
        },
        # Each language's operation names, so a stub or solution cannot drift from the interface.
        'names': {
            'c': ['htCreate', 'htPut', 'htGet', 'htRemove', 'htSize', 'htFree'],
            'cpp': ['HashTable(int m)', 'put(', 'get(', 'remove(', 'size()'],
            'cs': ['HashTable(int m)', 'Put(', 'Get(', 'Remove(', 'Size()'],
            'java': ['HashTable(int m)', 'put(', 'get(', 'remove(', 'size()'],
            'py': ['class HashTable', 'def put(', 'def get(', 'def remove(', 'def size('],
            'js': ['class HashTable', 'put(', 'get(', 'remove(', 'size()'],
        },
    },
}
# The exercise is to build the table, so reference code may not use library hash structures.
BANNED_HASH = [
    (r'\bdict\s*\(|\bset\s*\(|\{\s*\}|\bhash\s*\(', ('py',), 'Python dict/set/hash'),
    (r'\bnew\s+(?:Map|Set|WeakMap)\b|\{\s*\}', ('js',), 'JavaScript Map/Set/object map'),
    (r'HashMap|HashSet|Hashtable|TreeMap|hashCode', ('java',), 'Java hash collections'),
    (r'Dictionary<|HashSet<|Hashtable|GetHashCode', ('cs',), 'C# hash collections'),
    (r'unordered_map|unordered_set|std::map|std::set|std::hash', ('cpp',), 'C++ associative containers'),
]
TITLE = 'Hash Tables & Relational Algebra'
SECTION_IDS = ['overview', 'hash-review', 'ra-review', 'exercises', 'exercise-1', 'exercise-2',
               'optional-practice', 'discussion', 'extra', 'references']


WRITTEN_RESPONSES = {
    'exercise-1': """### Your answer — Exercise 1

1. **Read:** Tuples and attributes of Student × Takes and of Student ⋈ Takes; the result of the expression; the attributes each join matches on; whether Chen appears, and why.
2. **Write:** Your expression, and its result on this instance.
3. **Diagnose:** One student wrongly included, one wrongly left out, and why.
4. **Valid rewrite?**
   - 4a.
   - 4b.
   - 4c.
""",
    'exercise-2': """### Your answer — Exercise 2

**Part A · Trace**

| Key | h₁ | h₂ | Linear: slots tried | Double: slots tried |
|---|---|---|---|---|
| 22 | | | | |
| 1 | | | | |
| 13 | | | | |
| 11 | | | | |
| 24 | | | | |
| 33 | | | | |

- **Total probes and clustering:**
- **Searching for 33 after emptying 11's slot:**

**Part B · Explain your code**

- **DELETED, not EMPTY:**
- **Put keeps probing past the first DELETED slot:**
- **Cost:** Expected and worst-case probes per operation, and space.
- **Why m prime:**
- **After many insertions and removals:**
""",
    'optional-practice': """### Your answer — Optional practice (optional)

1. **Division with m = 16 and m = 17:**
2. **Quadratic probing slots:**
3. **Why random:**
4. **Self-join:**
5. **Every CS course:**
""",
    'discussion': """### Your reflection

**Linear vs double hashing:** Which needed fewer probes, and how does the gap change as the table fills?

**One slot vs the whole sequence:** Where else did a decision about one item need information about a whole set?

**Exit check:** How do a hash table and the "no CS course" query each decide that something is absent?
""",
    'extra': """### Your answer — Red-Black Tree (optional)

**Inserting 13:** The cases that apply, the tree afterwards, and your check of the black-heights.
""",
}


def read_code(task, kind, lang):
    path = SOL / task / f'{lang}.{kind}.{LANG_EXT[lang]}'
    text = path.read_text(encoding='utf-8')
    missing = [name for name in TASKS[task]['names'][lang] if name not in text]
    if not text.strip() or missing:
        raise BuildError(f'empty or mismatched {task} {kind} (missing {missing}): {path}')
    if kind == 'solution':
        for pattern, langs, label in BANNED_HASH:
            if lang in langs and re.search(pattern, text):
                raise BuildError(f'library hash structure ({label}) in {path}')
    return text


# Notebook Markdown has no subscripts outside math, so σ<sub>c</sub>(R) becomes σ[c](R),
# the same plain-text notation the page suggests for typing answers.
RA_SUBSCRIPT = re.compile(r'([σπρ⋈])<sub>(.*?)</sub>')


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
    intro = f'''# Recitation 5 — {TITLE} ({label})

Save this notebook in your `cs301-notebooks` project and open it in your IDE.
Use the {'project .venv Python / Python (CS301)' if lang == 'py' else 'Java (IJava)'} kernel.
See [Recitation 0]({SITE_URL}/recitation0.html) for setup.

Write your reasoning in the Markdown answer cells (double-click to edit, Shift+Enter to render).
Relational algebra subscripts are written in brackets here: σ[dept = 'CS'](Course) is σ with the subscript dept = 'CS'.
For Exercise 2, edit and run the starter definition, then run its self-check.
An untouched starter fails the check; that is expected. Keep the interface unchanged.
The Red-Black Tree section at the end is optional extra content.
Reference answers are not in this notebook; they are on the
[Recitation 5 page]({SITE_URL}/recitation5.html). Nothing is submitted or graded.
'''
    if lang == 'java':
        intro += '\nIJava accepts class definitions and statements directly, without a main method. The starter defines a class named `HashTable`: re-run the starter cell before the check cell. A check failure throws an exception; no JVM assertion flag is needed.\n'
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


def sections_of(source):
    root = parse_fragment(source)
    sections = {node.attrs.get('id'): node for node in root.find_all('section')}
    if list(sections) != SECTION_IDS:
        raise BuildError('Recitation 5 sections are missing, duplicated, or out of order')
    return sections


def build_recitation5():
    source = SOURCE.read_text(encoding='utf-8')
    sections_of(source)
    notebook_sections = sections_of(RA_SUBSCRIPT.sub(r'\1[\2]', source))
    # Notebook-only paragraphs stay in the notebook sections but not on the page.
    source = re.sub(r'<p data-notebook-only>.*?</p>\n?', '', source)
    for task, spec in TASKS.items():
        stubs = {lang: read_code(task, 'stub', lang) for lang, _, _ in LANGS}
        solutions = {lang: read_code(task, 'solution', lang) for lang, _, _ in LANGS}
        signature_rows = ''.join(f'<tr data-sig-lang="{lang}"><td>{LANG_LABEL[lang]}</td><td><code class="sig-block">{esc(sig)}</code></td></tr>'
                                 for lang, sig in spec['signatures'].items())
        replacements = {
            f'<!-- {spec["marker"]}_SIGNATURES -->': '<div class="table-wrap"><table class="data sig-table"><thead><tr><th>Language</th><th>Exact interface</th></tr></thead><tbody>' + signature_rows + '</tbody></table></div>',
            f'<!-- {spec["marker"]}_STARTER -->': render_tabs(f'r5-{task}-stub', f'{spec["title"]} starter template', stubs),
            f'<!-- {spec["marker"]}_SOLUTION -->': render_tabs(f'r5-{task}-solution', f'{spec["title"]} reference solution', solutions),
        }
        for marker, replacement in replacements.items():
            if source.count(marker) != 1:
                raise BuildError(f'expected exactly one {marker}')
            source = source.replace(marker, replacement)
    notebooks = ROOT / 'site/notebooks'
    notebooks.mkdir(exist_ok=True)
    for lang, name in [('py', 'python'), ('java', 'java')]:
        notebook = build_notebook(lang, notebook_sections)
        (notebooks / f'recitation5-{name}.ipynb').write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + '\n')
    hero = f'''<section class="page-hero" id="top"><div class="container">
<span class="eyebrow">Recitation 5 · Notes &amp; practice</span><h1>{esc(TITLE)}</h1>
<p class="subtitle">See why open addressing needs tombstones, build a double-hashing table from plain arrays, and read, write, and debug relational algebra.</p>
<div class="hero-actions"><a class="btn primary" href="#notes">Notes</a><a class="btn ghost" href="#exercises">Core practice</a><a class="btn ghost" href="#extra">Extra · Red-Black Trees</a><a class="btn ghost" href="#notebooks">Notebooks</a></div>
</div></section>'''
    downloads = '''<section class="section" id="notebooks"><div class="section-title"><h2>Practice notebooks</h2></div>
<p>Choose Python or Java. Each notebook contains these notes, written-response cells, and the Exercise 2 starter with runnable self-checks. The tree diagram appears on this page only; the notebooks describe the same trees in text. Reference answers stay on this page. Save the notebook in your course project and open it directly in your IDE with the matching kernel.</p>
<div class="hero-actions"><a class="btn primary" href="notebooks/recitation5-python.ipynb" download>Download Python notebook (.ipynb)</a><a class="btn ghost" href="notebooks/recitation5-java.ipynb" download>Download Java notebook (.ipynb)</a></div></section>'''
    # Notes anchor groups the review; exercise sections remain directly linkable.
    split = source.index('<section class="section" id="exercises">')
    jump = jump_bar([('overview', 'Overview'), ('hash-review', 'Hashing'), ('ra-review', 'Relational algebra'),
                     ('exercise-1', 'Ex 1'), ('exercise-2', 'Ex 2'), ('optional-practice', 'Optional'),
                     ('discussion', 'Discussion'), ('extra', 'Extra'), ('notebooks', 'Notebooks')])
    body = hero + '<div class="container">' + jump + '<div id="notes">' + source[:split] + '</div>' + source[split:] + downloads + '</div>'
    head = '<link rel="stylesheet" href="assets/notes.css"><noscript><style>' + NOSCRIPT_STYLE + '</style></noscript>'
    (ROOT / 'site/recitation5.html').write_text(page('recitation5.html', 'Recitation 5 · ' + TITLE, body, head))
    print('Built Recitation 5 notes, core exercises, Red-Black Tree extra, and Python/Java notebooks.')


if __name__ == '__main__':
    build_recitation5()
