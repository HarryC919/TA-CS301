#!/usr/bin/env python3
"""Regression checks for notebook Markdown fences and written-answer cells."""
import json
from pathlib import Path
import unittest

from build_notebooks import parse_fragment, render_code_block

ROOT = Path(__file__).resolve().parents[2]


class NotebookFormatTests(unittest.TestCase):
    def test_code_block_languages(self):
        for attrs, label, expected in [
            ('', 'pseudocode', 'pseudocode'),
            ('data-language="pseudo"', 'Pseudocode · fragments', 'pseudocode'),
            ('data-language="py"', 'Python', 'python'),
            ('', '', 'text'),
        ]:
            with self.subTest(expected=expected, attrs=attrs):
                root = parse_fragment(f'<div class="code-block" {attrs}><span class="lang-tag">{label}</span><pre><code>x &lt; y</code></pre></div>')
                result = render_code_block(root.find_all('div')[0])
                self.assertIn(f'```{expected}\nx < y\n```', result)

    def test_shipped_notebook_cells(self):
        paths = sorted((ROOT / 'site/notebooks').glob('*.ipynb'))
        self.assertEqual(len(paths), 4)
        for path in paths:
            nb = json.loads(path.read_text())
            for cell in nb['cells']:
                source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
                with self.subTest(notebook=path.name, cell=cell['id']):
                    if cell['id'].endswith('-response'):
                        self.assertEqual(cell['cell_type'], 'markdown')
                        self.assertNotIn('```', source)
                    if cell['cell_type'] != 'markdown':
                        continue
                    in_fence = False
                    for line in source.splitlines():
                        if not line.startswith('```'):
                            continue
                        if not in_fence:
                            language = line[3:].strip()
                            self.assertTrue(language, 'opening fence needs a language')
                            self.assertNotIn(language, ['pseudo', 'py'])
                        else:
                            self.assertEqual(line.strip(), '```')
                        in_fence = not in_fence
                    self.assertFalse(in_fence, 'unclosed fence')
                    if cell['id'] in ['notes-bubble-sort', 'notes-insertion-sort',
                                      'notes-merge-sort', 'notes-quick-sort', 'optional-practice']:
                        self.assertIn('```pseudocode\n', source)


if __name__ == '__main__':
    unittest.main()
