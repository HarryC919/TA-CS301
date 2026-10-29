"""Shared static page layout and fixed recitation navigation."""
from html import escape

RECITATIONS = [('Environment & kernels', 'Setup guide'), ('Sorting algorithms', 'Available')] + [('Asymptotic notation & divide and conquer', 'Available')] + [('Content to be announced', 'Coming soon')] * 5
PAGES = ['index.html', 'intro.html'] + [f'recitation{n}.html' for n in range(8)]


def header(current: str) -> str:
    def link(href, label):
        active = ' class="active" aria-current="page"' if current == href else ''
        return f'<a href="{href}"{active}>{label}</a>'
    items = '\n'.join(link(f'recitation{n}.html', f'Recitation {n} — {title}') for n, (title, _) in enumerate(RECITATIONS))
    selected = current.startswith('recitation')
    label = 'Recitation ' + current.removeprefix('recitation').removesuffix('.html') if selected else 'Recitation'
    return f'''<header class="site-header">
  <div class="container header-inner">
    <a class="site-title" href="index.html"><span class="course-mark" aria-hidden="true">301</span><span class="site-title-copy"><span class="site-title-course">COMPSCI 301</span><span class="site-title-sub">Algorithms &amp; Databases</span></span></a>
    <nav class="site-nav" aria-label="Site">
      {link('index.html', 'Home')}
      {link('intro.html', 'Introduction')}
      <details class="recitation-menu">
        <summary class="{'active' if selected else 'menu-label'}">{label}</summary>
        <div class="recitation-options">{items}</div>
      </details>
    </nav>
  </div>
</header>'''


FOOTER = '''<footer class="site-footer"><div class="container">
<p>COMPSCI 301 · course materials for the recitation sessions.</p>
<p class="muted small">The official course site is temporarily unavailable. If you spot a mistake, tell the TA.</p>
</div></footer>'''


def page(current, title, body, extra_head=''):
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · COMPSCI 301</title>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/style.css">
<script src="assets/app.js" defer></script>{extra_head}</head><body>
{header(current)}<main id="main">{body}</main>{FOOTER}</body></html>'''
