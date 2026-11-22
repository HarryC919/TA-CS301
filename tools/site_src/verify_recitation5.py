#!/usr/bin/env python3
"""Verify the shipped Recitation 5 notebook checks with references and stubs."""
import json
import shutil
import subprocess
import sys

from build_recitation5 import ROOT, SOL, TASKS

WORK = ROOT / '.tmp/week5-notebooks'
PASS_TEXT = {'hashtable': 'Exercise 2 checks passed'}


def source(cell):
    value = cell['source']
    return ''.join(value) if isinstance(value, list) else value


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    for lang, label, ext in [('py', 'python', 'py'), ('java', 'java', 'java')]:
        notebook = json.loads((ROOT / f'site/notebooks/recitation5-{label}.ipynb').read_text())
        cells = {cell['id']: cell for cell in notebook['cells']}
        assert len(cells) == len(notebook['cells']), 'duplicate cell ids'
        assert notebook['nbformat'] == 4 and notebook['nbformat_minor'] == 5
        for name in ['hash-review', 'ra-review', 'exercise-1', 'exercise-2', 'exercise-1-response',
                     'exercise-2-response', 'optional-practice', 'optional-practice-response',
                     'discussion-response', 'extra', 'extra-response', 'hashtable-stub', 'hashtable-check']:
            assert name in cells, name
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                assert cell['execution_count'] is None and cell['outputs'] == []
            text = source(cell)
            assert 'Reference explanation' not in text, 'reference answer leaked'
            assert 'Optional practice answers' not in text and 'Discussion notes' not in text, 'answer leaked'
            assert 'Red-Black Tree answer' not in text and '20B(13B' not in text, 'Extra answer leaked'
            assert 'Chen, Dana, Eli' not in text, 'Exercise 1 answer leaked'
            assert '1 + 1 + 1 + 4 + 3 + 6' not in text, 'Exercise 2 Part A answer leaked'
            assert 'In C, the table is a struct' not in text, 'web-only C note leaked'
            assert '<svg' not in text, 'web-only figure leaked'
            assert '<sub>' not in text and '<sup>' not in text, 'raw sub/superscript left in notebook'
        markdown = '\n'.join(source(cell) for cell in notebook['cells'] if cell['cell_type'] == 'markdown')
        assert '$h_{1}$' in markdown and '$\\log_{2}$' in markdown, 'scripts must render as KaTeX math'
        assert "σ[dept = 'CS'](Course)" in markdown and 'π[sname]' in markdown, 'relational algebra must use bracket subscripts'
        assert '\\_' not in markdown and '$$' not in markdown, 'escaped or empty math left in notebook'
        assert '| sid | sname | major |' in markdown, 'relation tables need their column headers'
        for expected_label in ['Exercise 1 · relational algebra: read, write, diagnose',
                               'Exercise 2 · build an open-addressing hash table']:
            assert expected_label in source(cells['exercises']), 'core-path label lost: ' + expected_label
        for task in TASKS:
            check = source(cells[f'{task}-check'])
            stub = source(cells[f'{task}-stub'])
            assert stub == (SOL / task / f'{lang}.stub.{ext}').read_text()
            for kind in ['stub', 'solution']:
                code = stub if kind == 'stub' else (SOL / task / f'{lang}.solution.{ext}').read_text()
                if lang == 'py':
                    try:
                        exec(compile(code + '\n' + check, f'notebook-{task}-{kind}.py', 'exec'), {})
                    except AssertionError:
                        if kind != 'stub':
                            raise
                    else:
                        assert kind == 'solution', f'untouched Python {task} stub passed self-check'
                else:
                    folder = WORK / task / kind
                    folder.mkdir(parents=True, exist_ok=True)
                    imports = '\n'.join(line for line in check.splitlines() if line.startswith('import '))
                    body = '\n'.join(line for line in check.splitlines() if not line.startswith('import '))
                    (folder / 'HashTable.java').write_text(code)
                    (folder / 'Main.java').write_text(imports + '\npublic class Main { public static void main(String[] args) {\n' + body + '\n}}\n')
                    subprocess.run(['javac', 'HashTable.java', 'Main.java'], cwd=folder, check=True)
                    run = subprocess.run(['java', 'Main'], cwd=folder, capture_output=True, text=True)
                    if kind == 'stub':
                        assert run.returncode != 0 and 'UnsupportedOperationException' in run.stderr, run.stderr
                    else:
                        assert run.returncode == 0, run.stderr
                        assert PASS_TEXT[task] in run.stdout, run.stdout
                print(f'PASS Recitation 5 {label} {task}: {kind} ' + ('fails as expected' if kind == 'stub' else 'passes shipped checks'))
    print('ALL RECITATION 5 NOTEBOOK CHECKS PASSED')


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, subprocess.CalledProcessError) as error:
        print(f'FAILED: {error}', file=sys.stderr)
        sys.exit(1)
