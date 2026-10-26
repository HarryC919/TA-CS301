#!/usr/bin/env python3
"""Print the document Y offset of every element id on a site page.

Headless Chrome can neither scroll nor measure elements from the command line,
so this helper injects a tiny script that records every id's position into the
DOM, runs `--dump-dom`, and parses the result. Use the offsets to crop the tall
full-page screenshots taken by `shot_page.py` / the shell one-liners.

Usage:
    python3 tools/site_src/page_offsets.py PAGE [--prefix problem-] [--json OUT]
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SITE = ROOT / "site"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP_PAGE = SITE / ".qa-tmp.html"
PROFILE = ROOT / ".tmp" / "chrome-profile"

SCRIPT = """<script>
window.addEventListener("load", function () {
  var out = {};
  var nodes = document.querySelectorAll("[id]");
  for (var i = 0; i < nodes.length; i++) {
    out[nodes[i].id] = Math.round(nodes[i].getBoundingClientRect().top + window.scrollY);
  }
  var pre = document.createElement("pre");
  pre.id = "qa-offsets";
  pre.textContent = JSON.stringify(out);
  document.body.appendChild(pre);
});
</script>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", help="page file name under site/")
    parser.add_argument("--prefix", default="", help="only print ids starting with this")
    parser.add_argument("--json", help="also write the full offset map to this path")
    args = parser.parse_args()

    page = SITE / args.page
    if not page.is_file():
        print(f"missing page {page}")
        return 1
    src = page.read_text(encoding="utf-8")
    TMP_PAGE.write_text(src.replace("</body>", SCRIPT + "</body>"), encoding="utf-8")
    PROFILE.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            [
                CHROME,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-gpu-sandbox",
                f"--user-data-dir={PROFILE}",
                "--window-size=1440,2000",
                "--virtual-time-budget=5000",
                "--dump-dom",
                f"file://{TMP_PAGE}",
            ],
            capture_output=True,
            text=True,
            timeout=90,
        )
    finally:
        TMP_PAGE.unlink(missing_ok=True)

    match = re.search(r'<pre id="qa-offsets">(.*?)</pre>', result.stdout, re.DOTALL)
    if not match:
        print("could not read offsets from the rendered DOM")
        return 1
    offsets = json.loads(html.unescape(match.group(1)))
    if args.json:
        Path(args.json).write_text(json.dumps(offsets, indent=0), encoding="utf-8")
    for name, position in offsets.items():
        if name.startswith(args.prefix):
            print(f"{position:>7}  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
