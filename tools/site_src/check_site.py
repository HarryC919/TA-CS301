#!/usr/bin/env python3
"""Structural QA for the generated COMPSCI 301 site.

Checks, for every page in `site/`:
  - well-formed HTML tags (explicit close tags only),
  - unique element ids,
  - internal links resolve to an existing file and an existing anchor,
  - local images referenced by <img> exist inside the site,
  - each page has the shared header/footer, stylesheet and a title,
  - every page's site navigation lists all pages in the same order and marks
    exactly the current page as active,
  - the exercises page has the expected 6 problems x 6 languages structure,
  - classes used in HTML are defined in the stylesheet (warnings only).

Usage:
    python3 tools/site_src/check_site.py [--site site] [--strict-links]

Exit code 1 if any error is reported. Pending pages (not yet generated) are
warnings; --strict-links turns them into errors for the final check.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

LANGS = ["c", "cpp", "cs", "java", "py", "js"]

# Every page must offer the same navigation, in this order, with the current
# page marked `class="active"` (the exercises page is generated from its own
# header template, so the check covers that template too).
NAV_ORDER = ["index.html", "intro.html"] + [f"recitation{n}.html" for n in range(8)]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.errors: list[str] = []
        self.ids: dict[str, int] = {}
        self.duplicate_ids: list[str] = []
        self.links: list[tuple[str, str]] = []  # (href, where)
        self.classes: set[str] = set()
        self.tags: dict[str, int] = defaultdict(int)
        self.attrs_by_tag: dict[str, list[dict[str, str]]] = defaultdict(list)

    def handle_starttag(self, tag: str, attrs) -> None:
        self.tags[tag] += 1
        amap = dict(attrs)
        self.attrs_by_tag[tag].append(amap)
        if "id" in amap:
            if amap["id"] in self.ids:
                self.duplicate_ids.append(amap["id"])
            self.ids[amap["id"]] = self.getpos()[0]
        if "class" in amap:
            for name in amap["class"].split():
                self.classes.add(name)
        if tag == "a" and "href" in amap:
            self.links.append((amap["href"], f"line {self.getpos()[0]}"))
        if tag not in VOID_ELEMENTS:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag: str, attrs) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID_ELEMENTS and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_ELEMENTS:
            self.errors.append(f"line {self.getpos()[0]}: closing void element </{tag}>")
            return
        if not self.stack:
            self.errors.append(f"line {self.getpos()[0]}: stray </{tag}>")
            return
        open_tag, line = self.stack.pop()
        if open_tag != tag:
            self.errors.append(
                f"line {self.getpos()[0]}: </{tag}> closes <{open_tag}> opened at line {line}"
            )

    def finish(self) -> None:
        for tag, line in self.stack:
            self.errors.append(f"line {line}: <{tag}> is never closed")


def check_page(path: Path, site: Path, strict_links: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    rel = path.relative_to(site)

    raw = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(raw)
    parser.close()
    parser.finish()
    errors.extend(f"{rel}: {message}" for message in parser.errors)

    for duplicate in parser.duplicate_ids:
        errors.append(f"{rel}: duplicate id {duplicate!r}")

    # Shared page furniture.
    if not re.search(r'<html[^>]*lang="en"', raw):
        errors.append(f"{rel}: <html lang=\"en\"> missing")
    if "<title>" not in raw:
        errors.append(f"{rel}: <title> missing")
    if 'href="assets/style.css"' not in raw:
        errors.append(f"{rel}: stylesheet link missing")
    if 'class="site-header"' not in raw:
        errors.append(f"{rel}: shared header missing")
    if 'class="site-footer"' not in raw:
        errors.append(f"{rel}: shared footer missing")
    if "<main" not in raw:
        errors.append(f"{rel}: <main> missing")

    # Navigation: same links and order everywhere, current page marked active.
    nav_match = re.search(r'<nav class="site-nav"[^>]*>(.*?)</nav>', raw, re.DOTALL)
    if not nav_match:
        errors.append(f"{rel}: site navigation <nav class=\"site-nav\"> missing")
    else:
        nav_links = re.findall(r"<a\b([^>]*)>(.*?)</a>", nav_match.group(1), re.DOTALL)
        nav_hrefs = []
        nav_active = []
        for attrs, _text in nav_links:
            href_match = re.search(r'href="([^"]+)"', attrs)
            if not href_match:
                errors.append(f"{rel}: navigation link without href")
                continue
            href = href_match.group(1)
            nav_hrefs.append(href)
            if re.search(r'class="[^"]*\bactive\b', attrs):
                nav_active.append(href)
        if nav_hrefs != NAV_ORDER:
            errors.append(f"{rel}: navigation should be {NAV_ORDER}, found {nav_hrefs}")
        if nav_active != [rel.name]:
            errors.append(
                f"{rel}: navigation should mark only {rel.name!r} as active, "
                f"found {nav_active}"
            )

    # Internal links.
    for href, where in parser.links:
        if href.startswith(("http://", "https://", "mailto:")):
            # External destinations are allowed but not fetched; the site must
            # still work offline, so only internal links get verified.
            continue
        if href.startswith("javascript:"):
            errors.append(f"{rel} ({where}): javascript: link not allowed: {href}")
            continue
        if href.startswith("#"):
            anchor = href[1:]
            if anchor and anchor not in parser.ids:
                errors.append(f"{rel} ({where}): anchor {href!r} does not exist on this page")
            continue
        target, _, anchor = href.partition("#")
        target_path = (site / target).resolve()
        if not target_path.is_file():
            message = f"{rel} ({where}): link to missing page {target!r}"
            if strict_links:
                errors.append(message)
            else:
                warnings.append(message)
            continue
        if anchor:
            target_ids = collect_ids(target_path)
            if anchor not in target_ids:
                errors.append(
                    f"{rel} ({where}): link {href!r} - anchor {anchor!r} "
                    f"not found in {target}"
                )

    # Local images (brand logos, ...) must exist next to the site.
    for amap in parser.attrs_by_tag.get("img", []):
        src = amap.get("src")
        if not src:
            errors.append(f"{rel}: <img> without src")
            continue
        if src.startswith(("http://", "https://", "data:")):
            errors.append(f"{rel}: image must be a local file (no CDN): {src!r}")
            continue
        image_path = (path.parent / src.split("#")[0].split("?")[0]).resolve()
        if not image_path.is_file():
            errors.append(f"{rel}: image {src!r} not found")

    # Exercises-specific structure.
    if rel.name == "recitation1.html":
        problems = re.findall(r'<section class="problem" id="(problem-\d+)"', raw)
        if problems != [f"problem-{n}" for n in range(1, 7)]:
            errors.append(f"{rel}: expected problem-1..problem-6 sections, found {problems}")
        tab_groups = re.findall(r'<div class="tabs" data-tabs(?: data-editable)?>', raw)
        if len(tab_groups) != 12:
            errors.append(f"{rel}: expected 12 tab groups (6 problems x stub+solution), found {len(tab_groups)}")
        panel_count = len(re.findall(r'class="tab-panel" role="tabpanel"', raw))
        if panel_count != 72:
            errors.append(f"{rel}: expected 72 code panels, found {panel_count}")
        selected_langs = []
        for button in re.findall(r"<button\b[^>]*>", raw):
            if 'aria-selected="true"' in button:
                match = re.search(r'data-lang="(\w+)"', button)
                if match:
                    selected_langs.append(match.group(1))
        if len(selected_langs) != 12 or set(selected_langs) != {"java"}:
            errors.append(
                f"{rel}: expected every group to select java by default, found {sorted(set(selected_langs))} "
                f"({len(selected_langs)} selections)"
            )
        hidden_panels = len(re.findall(r'class="tab-panel"[^>]* hidden>', raw))
        if hidden_panels != 60:
            errors.append(f"{rel}: expected 60 hidden panels (72 - 12 java), found {hidden_panels}")
        exercise_html = raw.split('id="exercises"', 1)[-1]
        signatures = len(re.findall(r"<td><code>", exercise_html))
        if signatures != 36:
            errors.append(f"{rel}: expected 36 signature rows, found {signatures}")
        for lang in LANGS:
            panels = len(re.findall(rf'data-lang="{lang}"', raw))
            # 12 tab buttons + 12 panels per language.
            if panels != 24:
                errors.append(f"{rel}: language {lang!r} should appear 24 times, found {panels}")
        if exercise_html.count("<details>") != 12:
            errors.append(f"{rel}: expected 12 <details> blocks (hints + solutions), found {raw.count('<details>')}")
        if "TODO" not in raw:
            errors.append(f"{rel}: no TODO text found in starter templates")

    if rel.name == "recitation2.html":
        required = {"overview", "notes", "notation", "divide-conquer", "exercises",
                    "exercise-1", "exercise-2", "exercise-3", "optional-practice",
                    "discussion", "references", "notebooks"}
        missing = required - parser.ids.keys()
        if missing:
            errors.append(f"{rel}: missing Recitation 2 sections: {sorted(missing)}")
        panels = [a for a in parser.attrs_by_tag["div"] if a.get("role") == "tabpanel"]
        if len(panels) != 12 or any(sum(a.get("data-lang") == lang for a in panels) != 2 for lang in LANGS):
            errors.append(f"{rel}: expected two six-language code groups")
        selected = [a for a in parser.attrs_by_tag["button"] if a.get("aria-selected") == "true"]
        if len(selected) != 2 or any(a.get("data-lang") != "java" for a in selected):
            errors.append(f"{rel}: both code groups must default to Java")
        for name in ("python", "java"):
            href = f"notebooks/recitation2-{name}.ipynb"
            if not any(a.get("href") == href and "download" in a for a in parser.attrs_by_tag["a"]):
                errors.append(f"{rel}: missing downloadable {name} notebook")
        if any("open" in a for a in parser.attrs_by_tag["details"] if a.get("data-kind") == "answer"):
            errors.append(f"{rel}: reference answers should start collapsed")

    # aria-controls / aria-labelledby integrity.
    ids = parser.ids
    for tag, attrs_list in parser.attrs_by_tag.items():
        for amap in attrs_list:
            for attr in ("aria-controls", "aria-labelledby"):
                target = amap.get(attr)
                if target and target not in ids:
                    errors.append(f"{rel}: <{tag} {attr}={target!r}> points at a missing id")

    return errors, warnings


def collect_ids(path: Path) -> set[str]:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return set(parser.ids)


def collect_css_classes(paths: list[Path]) -> set[str]:
    classes: set[str] = set()
    for path in paths:
        css = path.read_text(encoding="utf-8")
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
        classes |= set(re.findall(r"\.([A-Za-z][A-Za-z0-9_-]*)", css))
    return classes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=ROOT / "site")
    parser.add_argument("--strict-links", action="store_true")
    args = parser.parse_args()
    site: Path = args.site

    pages = sorted(site.glob("*.html"))
    if not pages:
        print(f"no HTML pages found in {site}")
        return 1

    errors: list[str] = []
    for required in NAV_ORDER:
        if not (site / required).is_file():
            errors.append(f"missing required page: {required}")
    warnings: list[str] = []
    for page in pages:
        page_errors, page_warnings = check_page(page, site, args.strict_links)
        errors.extend(page_errors)
        warnings.extend(page_warnings)

    css_paths = [site / "assets" / "style.css", site / "assets" / "notes.css"]
    if not css_paths[0].is_file():
        errors.append("site/assets/style.css is missing")
    else:
        css_classes = collect_css_classes([p for p in css_paths if p.is_file()])
        used: set[str] = set()
        for page in pages:
            page_parser = PageParser()
            page_parser.feed(page.read_text(encoding="utf-8"))
            page_parser.close()
            used |= page_parser.classes
        unknown = sorted(used - css_classes)
        # Utility/JS-only hooks and anything dynamic are fine; report all.
        for name in unknown:
            warnings.append(f"class {name!r} is used in HTML but not styled in style.css")

    for name in ("app.js", "favicon.svg"):
        if not (site / "assets" / name).is_file():
            errors.append(f"site/assets/{name} is missing")

    print(f"checked {len(pages)} page(s): {', '.join(p.name for p in pages)}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"\nOK: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
