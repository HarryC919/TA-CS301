# COMPSCI 301 modern academic redesign

## Intent

Make the complete recitation website feel polished, contemporary, and academically credible without changing its course content or established interactions. The current white-and-blue interface is functional but visually flat; the redesign should improve first impressions, information hierarchy, reading comfort, and mobile usability.

## Goals

- Apply a coherent modern-academic visual system to every published page.
- Give the home page a distinctive, composed hero and clearer recitation directory.
- Improve typography, spacing, card hierarchy, navigation, buttons, tables, code blocks, and exercise presentation.
- Preserve all existing text, links, anchors, local assets, notebook downloads, and code-editing behavior.
- Remain responsive, keyboard accessible, readable, and usable without JavaScript.

## Non-goals and anti-goals

- Do not rewrite course content, assign placeholder recitation topics, or add personal information.
- Do not introduce a framework, external fonts, a CDN, a theme dependency, or a publishing build step.
- Do not change the six language groups, temporary editor storage rules, or generated-notebook content.
- Do not turn the site into a dark, neon-heavy developer landing page or add decorative motion that distracts from reading.
- Do not directly edit generated recitation HTML or notebooks.

## Constraints and sources of truth

- Shared styling belongs in `site/assets/style.css`; notes-only additions remain in `site/assets/notes.css`.
- Shared header/footer changes belong in `tools/site_src/site_layout.py` and are synchronized by `build_site.py`.
- Home and Introduction are maintained directly in `site/index.html` and `site/intro.html`; `material/week1/Intro.md` must remain synchronized if Introduction content changes.
- Recitation 0 structure comes from `tools/site_src/recitation0-content.html`.
- Recitation 1 structure comes from its existing source files and builders.
- Keep internal links relative, exactly one active top-level navigation item, and all current local images.
- The publishable asset inventory must remain unchanged; decorative effects should use CSS and existing markup/assets.

## Approaches

1. **Shared-CSS-only refresh.** Lowest risk and smallest diff, but it cannot substantially improve the home hero or recitation directory composition.
2. **Design system plus key layout upgrades (selected).** Refresh shared styles and adjust the home hero/directory plus shared header markup. Leave long-form recitation content structure intact. This gives a visibly complete redesign while containing regression risk.

A full content-structure rewrite was rejected because it would add risk without improving the requested visual outcome.

## Visual direction

- Use deep navy as the primary brand color, cobalt blue for actions and active states, restrained teal accents, and cool off-white page backgrounds.
- Use native system sans-serif fonts throughout, with stronger display sizing and tighter heading spacing rather than external font downloads.
- Use generous but efficient whitespace, fine borders, small-to-medium radii, layered soft shadows, and subtle gradients/grid motifs.
- Use uppercase eyebrows and compact metadata for academic structure; avoid excessive badges or marketing copy.
- Motion is limited to short hover/focus transitions and must respect `prefers-reduced-motion`.

## Page and component decisions

### Shared shell

- Keep the sticky header, existing three navigation controls, and native Recitation details/summary dropdown.
- Add a compact CSS-styled `301` course mark beside the course title; keep the title link and accessible name intact.
- Increase header polish with a translucent surface, subtle border/shadow, pill-shaped navigation, and clearer active/hover states.
- Keep dropdown positioning usable when navigation wraps on small screens.

### Home

- Recompose the hero into a two-column desktop layout: existing headline, description, metadata, and actions on the left; a non-interactive course/recitation visual panel on the right.
- The visual panel should communicate `COMPSCI 301`, `Algorithms & Databases`, and the eight recitation slots using concise labels already supported by the site, not new course claims.
- On mobile, stack the panel below the primary content without pushing the main actions far down the screen.
- Turn recitation rows into a more ordered numbered directory using CSS counters or existing recitation numbers; available sessions receive a clear accent, while placeholders remain visibly quieter.
- Refresh the three content cards and session steps through shared styles; do not alter their meaning.

### Recitation and Introduction pages

- Use a consistent deep-navy hero treatment with readable light text and appropriately styled primary/secondary actions.
- Keep all existing page anchors and content order.
- Improve long-form reading with clearer section separation, restrained surfaces, better table/card treatment, and more refined code headers and language tabs.
- Preserve dark code-editor contrast, textarea alignment, syntax colors, copy/reset controls, and no-JavaScript fallback.

### Footer and responsive behavior

- Make the footer visually connected to the new shell with a dark or navy-toned surface and readable muted text.
- Verify desktop, tablet, and narrow mobile layouts, including long titles, dropdown overflow, recitation rows, tables, code blocks, and hero actions.
- Retain visible keyboard focus and sufficient color contrast.

## Builder latitude

The builder may tune exact color values, spacing, gradients, decorative CSS geometry, and small responsive breakpoints to achieve the direction. The builder may add structural classes to the home and shared header, but should not change course copy or add JavaScript solely for visual effects.

## Verification

- Rebuild generated pages with `python3 tools/site_src/build_site.py`.
- Run `python3 tools/site_src/check_site.py --strict-links` and require zero errors/warnings.
- Run `node tools/site_src/test_code_ui.cjs` and require all code UI checks to pass.
- Run `bash tools/verify_notebooks.sh` because the full site builder regenerates notebooks; require all notebook checks to pass.
- Capture and inspect home, Introduction, Recitation 0, and Recitation 1 in headless Chrome at desktop and mobile sizes. Recapture after any layout correction.
- Confirm no build/scratch artifacts were added under `site/`, and report exact verification results.
