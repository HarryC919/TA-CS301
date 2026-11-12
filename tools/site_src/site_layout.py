"""Shared static page layout and fixed recitation navigation."""
from html import escape

RECITATIONS = [('Environment & kernels', 'Setup guide'), ('Sorting algorithms', 'Available')] + [('Asymptotic notation & divide and conquer', 'Available'), ('Dynamic programming & greedy algorithms', 'Available'), ('Graph algorithms', 'Available')] + [('Content to be announced', 'Coming soon')] * 3
PAGES = ['index.html', 'intro.html'] + [f'recitation{n}.html' for n in range(8)]


# Runs before first paint so a saved theme never flashes the other one.
THEME_BOOT = ('<script>try{var t=localStorage.getItem("cs301-theme");'
              'if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t)}catch(e){}</script>')

# Shown by app.js; cycles follow system → light → dark.
THEME_TOGGLE = (
    '<button class="theme-toggle" type="button" hidden aria-label="Color theme">'
    '<svg class="icon-auto" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 3.5a8.5 8.5 0 0 1 0 17z" fill="currentColor"/></svg>'
    '<svg class="icon-light" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
    '<svg class="icon-dark" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
    '</button>'
)


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
    {THEME_TOGGLE}
  </div>
</header>'''


def jump_bar(items) -> str:
    """Sticky in-page section links; items are (anchor id, label) in page order."""
    links = ''.join(f'<a href="#{anchor}">{label}</a>' for anchor, label in items)
    return f'<nav class="page-jump" aria-label="On this page"><div class="page-jump-inner">{links}</div></nav>'


FOOTER = '''<footer class="site-footer"><div class="container footer-inner">
<p>COMPSCI 301 recitation materials · Instructor announcements remain authoritative.</p>
<p class="muted">If you spot a mistake, tell the TA.</p>
</div></footer>'''


def page(current, title, body, extra_head=''):
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · COMPSCI 301</title>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/style.css">
{THEME_BOOT}
<script src="assets/app.js" defer></script>{extra_head}</head><body>
{header(current)}<main id="main">{body}</main>{FOOTER}</body></html>'''
