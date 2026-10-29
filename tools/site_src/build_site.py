#!/usr/bin/env python3
"""Build the fixed Recitation 0–7 static site, including legacy Week 1 redirects."""
from pathlib import Path
import re
from build_exercises import build
from build_notebooks import build_notebooks
from site_layout import header, page, RECITATIONS

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'
SOURCE = Path(__file__).resolve().parent


def directory():
    rows = []
    for n, (title, status) in enumerate(RECITATIONS):
        rows.append(f'''<div class="week-row{' available' if n < 2 else ''}"><div>
<div class="week-name">Recitation {n} — {title} <span class="pill {'blue' if n < 2 else 'gray'}">{status}</span></div>
<div class="week-topics">{'Environment setup and language kernels' if n == 0 else 'Notes and six practice problems on one page' if n == 1 else 'Reserved session; details will be posted here.'}</div></div>
<div class="week-links"><a class="btn{' primary' if n < 2 else ''}" href="recitation{n}.html">{'Open' if n < 2 else 'View placeholder'}</a></div></div>''')
    return '<section class="section" id="recitations"><div class="section-title"><h2>Recitations 0–7</h2></div><p>Eight fixed slots: environment setup, Recitation 1, and six reserved sessions. Topics for the reserved sessions will be announced later.</p><div class="week-list">' + ''.join(rows) + '</div></section>'


def main():
    build_notebooks()
    (SITE / 'recitation1.html').write_text(build(False), encoding='utf-8')
    body = (SOURCE / 'recitation0-content.html').read_text(encoding='utf-8')
    (SITE / 'recitation0.html').write_text(page('recitation0.html', 'Recitation 0 · Environment & kernels', body), encoding='utf-8')
    for n in range(2, 8):
        body = f'''<section class="page-hero"><div class="container"><span class="eyebrow">Recitation {n} · Coming soon</span>
<h1>Recitation {n}</h1><p class="subtitle">This session is reserved. Topics and materials will be announced here.</p></div></section>
<div class="container"><section class="section"><div class="callout info"><span class="callout-title">Materials to follow</span>
<p>No notes, exercises, or notebook downloads have been published for this session yet.</p></div>
<div class="hero-actions"><a class="btn" href="recitation{n-1}.html">Previous recitation</a>{f'<a class="btn" href="recitation{n+1}.html">Next recitation</a>' if n < 7 else ''}<a class="btn ghost" href="index.html#recitations">All recitations</a></div></section></div>'''
        (SITE / f'recitation{n}.html').write_text(page(f'recitation{n}.html', f'Recitation {n}', body), encoding='utf-8')
    for name in ['index.html', 'intro.html']:
        p = SITE / name
        text = p.read_text(encoding='utf-8')
        text = re.sub(r'<header class="site-header">.*?</header>', lambda _: header(name), text, count=1, flags=re.S)
        if name == 'index.html':
            if '<!-- RECITATION_DIRECTORY -->' in text:
                text = text.replace('<!-- RECITATION_DIRECTORY -->', directory())
            else:
                text = re.sub(r'<section class="section" id="recitations">.*?</section>', lambda _: directory(), text, flags=re.S)
        p.write_text(text, encoding='utf-8')
    for name, anchor in [('week1-notes.html', 'notes'), ('week1-exercises.html', 'exercises')]:
        body = f'''<section class="page-hero"><div class="container"><h1>Materials moved to Recitation 1</h1><p>The notes and exercises now share one page.</p>
<a class="btn primary" href="recitation1.html#{anchor}">Open Recitation 1 — {anchor}</a></div></section>'''
        # Preserve deep links when JS is available; the visible link works without JS.
        script = f'''<script>location.replace("recitation1.html" + (location.hash || "#{anchor}"));</script>'''
        (SITE / name).write_text(page('recitation1.html', 'Moved to Recitation 1', body, script), encoding='utf-8')
    print('Built Home/Introduction navigation, Recitations 0–7, two legacy redirects, and the Recitation 1 notebooks.')


if __name__ == '__main__':
    main()
