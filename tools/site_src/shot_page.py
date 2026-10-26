#!/usr/bin/env python3
"""Render one section of a site page to a PNG with headless Chrome.

Chrome's --screenshot always captures from the top of the document, so this
helper writes a throwaway copy of the page inside `site/` with a tiny script
that scrolls to the requested element, screenshots it, then removes the copy.

Usage:
    python3 tools/site_src/shot_page.py PAGE ANCHOR OUT [--height 2600] [--width 1440] [--offset 0]
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SITE = ROOT / "site"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP_PAGE = SITE / ".qa-tmp.html"
PROFILE = ROOT / ".tmp" / "chrome-profile"


SCRIPT = """<script>
window.addEventListener("load", function () {{
  var el = document.getElementById("{anchor}");
  if (el) {{
    el.scrollIntoView({{ behavior: "auto", block: "start" }});
    window.scrollBy(0, {offset});
  }}
}});
</script>
<style>html {{ scroll-padding-top: 80px; }}</style>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", help="page file name under site/, e.g. week1-exercises.html")
    parser.add_argument("anchor", help="element id to scroll to")
    parser.add_argument("out", help="output PNG path")
    parser.add_argument("--height", type=int, default=2600)
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--offset", type=int, default=0)
    args = parser.parse_args()

    page = SITE / args.page
    if not page.is_file():
        print(f"missing page {page}")
        return 1
    html = page.read_text(encoding="utf-8")
    injected = SCRIPT.format(anchor=args.anchor, offset=args.offset)
    if "</body>" not in html:
        print(f"{page} has no </body>")
        return 1
    TMP_PAGE.write_text(html.replace("</body>", injected + "</body>"), encoding="utf-8")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    PROFILE.mkdir(parents=True, exist_ok=True)
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-gpu-sandbox",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        f"--user-data-dir={PROFILE}",
        f"--window-size={args.width},{args.height}",
        "--virtual-time-budget=5000",
        f"--screenshot={out}",
        f"file://{TMP_PAGE}",
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=60)
    finally:
        TMP_PAGE.unlink(missing_ok=True)
    if not out.is_file() or out.stat().st_size == 0:
        print(f"screenshot failed for {args.page}#{args.anchor}")
        return 1
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
