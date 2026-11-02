#!/usr/bin/env python3
"""Build the fixed Recitation 0–7 static site and practice notebooks."""
from pathlib import Path
import re
from html import escape
from build_exercises import build
from build_notebooks import build_notebooks
from build_recitation2 import build_recitation2
from site_layout import header, page, RECITATIONS

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'
SOURCE = Path(__file__).resolve().parent


def directory():
    rows, reserved = [], []
    for n, (title, status) in enumerate(RECITATIONS):
        if status == 'Coming soon':
            reserved.append(n)
            continue
        rows.append(f'''<div class="week-row available"><div>
<div class="week-name">Recitation {n} — {title} <span class="pill blue">{status}</span></div>
<div class="week-topics">{'Environment setup and language kernels' if n == 0 else 'Notes and six practice problems on one page' if n == 1 else 'Growth bounds, recursive work, and a linear merge exercise'}</div></div>
<div class="week-links"><a class="btn primary" href="recitation{n}.html">Open</a></div></div>''')
    if reserved:
        first, last = reserved[0], reserved[-1]
        rows.append(f'''<div class="week-row reserved" data-range="{first:02d}–{last:02d}"><div>
<div class="week-name">Recitations {first}–{last} <span class="pill gray">Coming soon</span></div>
<div class="week-topics">Topics follow lecture progress; materials are posted here before each session.</div></div></div>''')
    return '<section class="section" id="recitations"><div class="section-title"><h2>Recitations</h2></div><div class="week-list">' + ''.join(rows) + '</div></section>'


def hero_slots():
    slots = []
    for n, (title, status) in enumerate(RECITATIONS):
        if status == 'Coming soon':
            slots.append(f'<span aria-hidden="true">{n:02d}</span>')
        else:
            slots.append(f'<a href="recitation{n}.html" aria-label="Recitation {n}: {escape(title)}">{n:02d}</a>')
    return '<div class="hero-slots">' + ''.join(slots) + '</div>'


def main():
    build_notebooks()
    (SITE / 'recitation1.html').write_text(build(False), encoding='utf-8')
    body = (SOURCE / 'recitation0-content.html').read_text(encoding='utf-8')
    (SITE / 'recitation0.html').write_text(page('recitation0.html', 'Recitation 0 · Environment & kernels', body), encoding='utf-8')
    build_recitation2()
    for n in range(3, 8):
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
            text = re.sub(r'<div class="hero-slots">.*?</div>', lambda _: hero_slots(), text, count=1, flags=re.S)
        p.write_text(text, encoding='utf-8')
    print('Built Home/Introduction navigation, Recitations 0–7, and the Recitation 1–2 notebooks.')


if __name__ == '__main__':
    main()
