#!/usr/bin/env python3
"""Verify the shipped Recitation 2 notebook checks with references and stubs."""
import json
from pathlib import Path
import subprocess
import sys

from build_recitation2 import ROOT, SOL

WORK = ROOT / '.tmp/week2-notebooks'
WORK.mkdir(parents=True, exist_ok=True)


def source(cell):
    value = cell['source']
    return ''.join(value) if isinstance(value, list) else value


def main():
    for lang, label, ext in [('py', 'python', 'py'), ('java', 'java', 'java')]:
        notebook = json.loads((ROOT / f'site/notebooks/recitation2-{label}.ipynb').read_text())
        cells = {cell['id']: cell for cell in notebook['cells']}
        assert len(cells) == len(notebook['cells']), 'duplicate cell ids'
        assert notebook['nbformat'] == 4 and notebook['nbformat_minor'] == 5
        for name in ['notation', 'divide-conquer', 'exercise-1', 'exercise-2', 'exercise-3',
                     'exercise-1-response', 'exercise-2-response', 'optional-practice', 'p3-stub', 'p3-check']:
            assert name in cells, name
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                assert cell['execution_count'] is None and cell['outputs'] == []
            assert 'Reference explanation' not in source(cell), 'reference answer leaked'
            assert 'The shortcut returns only' not in source(cell), 'discussion answer leaked'
        for expected_label in ['Exercise 1 · classify and justify bounds',
                      'Exercise 2 · account for recursive work',
                      'Exercise 3 · implement the merge step']:
            assert expected_label in source(cells['exercises']), 'core-path label lost: ' + expected_label
        check = source(cells['p3-check'])
        assert source(cells['p3-stub']) == (SOL / f'{lang}.stub.{ext}').read_text()
        for kind in ['stub', 'solution']:
            code = source(cells['p3-stub']) if kind == 'stub' else (SOL / f'{lang}.solution.{ext}').read_text()
            if lang == 'py':
                try:
                    exec(compile(code + '\n' + check, f'notebook-{kind}.py', 'exec'), {})
                except AssertionError:
                    if kind != 'stub':
                        raise
                else:
                    assert kind == 'solution', 'untouched Python stub passed self-check'
            else:
                folder = WORK / kind
                folder.mkdir(exist_ok=True)
                imports = '\n'.join(line for line in check.splitlines() if line.startswith('import '))
                body = '\n'.join(line for line in check.splitlines() if not line.startswith('import '))
                (folder / 'Solution.java').write_text(code)
                (folder / 'Main.java').write_text(imports + '\npublic class Main { public static void main(String[] args) {\n' + body + '\n}}\n')
                subprocess.run(['javac', 'Solution.java', 'Main.java'], cwd=folder, check=True)
                run = subprocess.run(['java', 'Main'], cwd=folder, capture_output=True, text=True)
                if kind == 'stub':
                    assert run.returncode != 0 and 'UnsupportedOperationException' in run.stderr, run.stderr
                else:
                    assert run.returncode == 0, run.stderr
                    assert 'Exercise 3 checks passed' in run.stdout, run.stdout
            print(f'PASS Recitation 2 {label}: {kind} ' + ('fails as expected' if kind == 'stub' else 'passes shipped checks'))
    print('ALL RECITATION 2 NOTEBOOK CHECKS PASSED')


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, subprocess.CalledProcessError) as error:
        print(f'FAILED: {error}', file=sys.stderr)
        sys.exit(1)
