#!/usr/bin/env python3
"""Verify the shipped Recitation 3 notebook checks with references and stubs."""
import json
import shutil
import subprocess
import sys

from build_recitation3 import ROOT, SOL, TASKS

WORK = ROOT / '.tmp/week3-notebooks'
PASS_TEXT = {'lcs': 'Exercise 2 checks passed', 'huffman': 'Huffman checks passed'}


def source(cell):
    value = cell['source']
    return ''.join(value) if isinstance(value, list) else value


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    for lang, label, ext in [('py', 'python', 'py'), ('java', 'java', 'java')]:
        notebook = json.loads((ROOT / f'site/notebooks/recitation3-{label}.ipynb').read_text())
        cells = {cell['id']: cell for cell in notebook['cells']}
        assert len(cells) == len(notebook['cells']), 'duplicate cell ids'
        assert notebook['nbformat'] == 4 and notebook['nbformat_minor'] == 5
        for name in ['dp-review', 'greedy-review', 'greedy-review-response', 'exercise-1', 'exercise-2', 'exercise-2-code',
                     'exercise-1-response', 'exercise-2-response', 'exercise-2-code-response',
                     'discussion-response', 'extra', 'extra-build',
                     'lcs-stub', 'lcs-check', 'huffman-stub', 'huffman-check']:
            assert name in cells, name
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                assert cell['execution_count'] is None and cell['outputs'] == []
            text = source(cell)
            assert 'Reference explanation' not in text, 'reference answer leaked'
            assert 'Quick check answer' not in text and 'Try-it answer' not in text and 'Discussion notes' not in text, 'answer leaked'
            assert 'L(4, 5) = 3' not in text, 'Part A answer leaked'
            assert 'In C, return' not in text, 'web-only C note leaked'
        markdown = '\n'.join(source(cell) for cell in notebook['cells'] if cell['cell_type'] == 'markdown')
        assert '$L_{j}$' in markdown and '$L_{\\max}$' in markdown, 'scripts must render as KaTeX math'
        assert '\\_' not in markdown and '$$' not in markdown, 'escaped or empty math left in notebook'
        for expected_label in ['Exercise 1 · greedy scheduling, 1 || Lmax',
                               'Exercise 2 · LCS, Part A: the key math function',
                               'Exercise 2 · LCS, Part B: return the LCS']:
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
                    (folder / 'Solution.java').write_text(code)
                    (folder / 'Main.java').write_text(imports + '\npublic class Main { public static void main(String[] args) {\n' + body + '\n}}\n')
                    subprocess.run(['javac', 'Solution.java', 'Main.java'], cwd=folder, check=True)
                    run = subprocess.run(['java', 'Main'], cwd=folder, capture_output=True, text=True)
                    if kind == 'stub':
                        assert run.returncode != 0 and 'UnsupportedOperationException' in run.stderr, run.stderr
                    else:
                        assert run.returncode == 0, run.stderr
                        assert PASS_TEXT[task] in run.stdout, run.stdout
                print(f'PASS Recitation 3 {label} {task}: {kind} ' + ('fails as expected' if kind == 'stub' else 'passes shipped checks'))
    print('ALL RECITATION 3 NOTEBOOK CHECKS PASSED')


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, subprocess.CalledProcessError) as error:
        print(f'FAILED: {error}', file=sys.stderr)
        sys.exit(1)
