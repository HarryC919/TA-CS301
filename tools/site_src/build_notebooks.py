#!/usr/bin/env python3
"""Build the Recitation 1 Jupyter notebooks (Python + Java) for site download.

Inputs (the same sources behind `site/recitation1.html`):
  - `tools/site_src/problems.py`                    statements, examples, hints, signatures
  - `material/week1/solutions/pN/{py,java}.stub.*`  starter templates, verbatim
  - `tools/site_src/recitation1-notes.html`         concept notes, converted to markdown

Outputs:
  - `site/notebooks/recitation1-python.ipynb`
  - `site/notebooks/recitation1-java.ipynb`

The .ipynb files are generated artifacts: never edit them directly. Edit the
sources above, or the notebook-specific prose in this file (intro, self-check
cells, closing), then re-run:

    python3 tools/site_src/build_notebooks.py

Reference solutions are deliberately NOT embedded: the notebook ships starter
templates and self-check cells, while worked solutions stay on the website.
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

from build_exercises import function_name, read_code  # noqa: E402
from problems import PROBLEMS, SIGNATURES  # noqa: E402

SOL = ROOT / "material" / "week1" / "solutions"
NOTES_HTML = HERE / "recitation1-notes.html"
OUT_DIR = ROOT / "site" / "notebooks"

SITE_URL = "https://harryc919.github.io/TA-CS301"
LANG_KEYS = ("py", "java")
LANG_LABEL = {"py": "Python", "java": "Java"}
OUT_NAME = {"py": "recitation1-python.ipynb", "java": "recitation1-java.ipynb"}
KERNELS = {
    "py": {
        "kernelspec": {"display_name": "Python (CS301)", "language": "python", "name": "cs301-python"},
        "language_info": {"name": "python"},
    },
    "java": {
        "kernelspec": {"display_name": "Java", "language": "java", "name": "java"},
        "language_info": {"name": "java"},
    },
}
LANG_NAME = {"py": "python", "java": "java"}

FENCE = "`" * 3

# Note sections that become notebook markdown cells, in document order.
REQUIRED_SECTIONS = [
    "takeaways", "goals", "big-picture", "bubble-sort", "insertion-sort",
    "merge-sort", "quick-sort", "stability", "comparison", "when-to-use",
    "order-statistics", "before-exercises",
]


class BuildError(RuntimeError):
    pass


# ---------------------------------------------------------------------------
# Minimal HTML tree for the notes fragment and exercise prose
# ---------------------------------------------------------------------------

VOID_ELEMENTS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                 "link", "meta", "param", "source", "track", "wbr"}


class Node:
    def __init__(self, tag: str, attrs: dict[str, str]) -> None:
        self.tag = tag
        self.attrs = attrs
        self.classes = set(attrs.get("class", "").split())
        self.children: list["Node | str"] = []

    def text(self) -> str:
        return "".join(child if isinstance(child, str) else child.text()
                       for child in self.children)

    def find_all(self, tag: str, cls: str | None = None) -> list["Node"]:
        found = []
        for child in self.children:
            if isinstance(child, Node):
                if child.tag == tag and (cls is None or cls in child.classes):
                    found.append(child)
                found.extend(child.find_all(tag, cls))
        return found


class TreeBuilder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("root", {})
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in VOID_ELEMENTS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, dict(attrs)))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def parse_fragment(html_text: str) -> Node:
    builder = TreeBuilder()
    builder.feed(html_text)
    builder.close()
    return builder.root


# ---------------------------------------------------------------------------
# HTML -> markdown rendering
# ---------------------------------------------------------------------------

SUPERSCRIPTS = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
SUBSCRIPTS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def escape_md(text: str) -> str:
    text = text.replace("\xa0", " ")
    return re.sub(r"([*_`])", r"\\\1", text)


def render_inline(node: Node | str) -> str:
    if isinstance(node, str):
        return escape_md(node)
    children = node.children
    if node.tag == "code":
        return "`" + "".join(child.text() if isinstance(child, Node) else child
                             for child in children).replace("\xa0", " ").strip() + "`"
    if node.tag == "a":
        href = node.attrs.get("href", "")
        if href.startswith("#"):
            return ""  # in-notebook anchors do not exist; drop the link entirely
        label = "".join(render_inline(child) for child in children).strip()
        return f"[{label}]({href})"
    if node.tag == "sub":
        return "".join(child for child in children if isinstance(child, str)).translate(SUBSCRIPTS)
    if node.tag == "sup":
        return "".join(child for child in children if isinstance(child, str)).translate(SUPERSCRIPTS)
    if node.tag == "br":
        return " "
    if node.tag in ("strong", "em"):
        return render_sequence(children, markers(node.tag))
    return render_sequence(children)


def markers(tag: str) -> str:
    return "**" if tag == "strong" else "*"


def _first_char(child: Node | str) -> str:
    text = child if isinstance(child, str) else child.text()
    return text.lstrip()[:1]


def render_sequence(children: list[Node | str], marker: str = "") -> str:
    """Render inline children; pad emphasis markers only where the words on
    either side are alphanumeric, so punctuation never gets pushed away."""
    parts: list[str] = []
    last = ""
    for index, child in enumerate(children):
        if isinstance(child, Node) and child.tag in ("strong", "em"):
            inner = collapse(render_sequence(child.children)).strip()
            if not inner:
                continue
            child_marker = markers(child.tag)
            prefix = " " if last.isalnum() else ""
            following = ""
            for later in children[index + 1:]:
                following = _first_char(later)
                if following:
                    break
            suffix = " " if following.isalnum() else ""
            piece = f"{prefix}{child_marker}{inner}{child_marker}{suffix}"
            parts.append(piece)
            last = piece[-1]
            continue
        piece = render_inline(child)
        if not piece:
            continue
        if piece[0] == " " and (last == "" or last == " "):
            piece = piece.lstrip()
        parts.append(piece)
        last = piece[-1] if piece else last
    if marker:
        text = collapse("".join(parts)).strip()
        return f"{marker}{text}{marker}" if text else ""
    return "".join(parts)


def collapse(text: str) -> str:
    return re.sub(r"[ \t\n]+", " ", text).strip()


def render_table(node: Node) -> str:
    blocks = []
    captions = node.find_all("caption")
    if captions:
        blocks.append(f"*{collapse(render_inline(captions[0]))}*")
    head_rows = [row for thead in node.find_all("thead")
                 for row in thead.find_all("tr")]
    body_rows = [row for tbody in node.find_all("tbody")
                 for row in tbody.find_all("tr")]

    def cells(row: Node) -> list[str]:
        return [collapse(render_inline(cell)).replace("|", "\\|")
                for cell in row.children
                if isinstance(cell, Node) and cell.tag in ("th", "td")]

    if not head_rows:
        raise BuildError("table without a header row in the notes fragment")
    header = cells(head_rows[0])
    lines = ["| " + " | ".join(header) + " |",
             "| " + " | ".join("---" for _ in header) + " |"]
    for row in body_rows:
        lines.append("| " + " | ".join(cells(row)) + " |")
    blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def render_code_block(node: Node) -> str:
    titles = node.find_all("span", "code-title")
    tags = node.find_all("span", "lang-tag")
    pres = node.find_all("pre")
    if not pres:
        raise BuildError("code-block without <pre> in the notes fragment")
    code = pres[0].text().strip("\n")
    label = collapse(tags[0].text()) if tags else ""
    parts = []
    if titles:
        parts.append(f"**{collapse(titles[0].text())}**"
                     + (f" ({label})" if label else ""))
    parts.append(f"{FENCE}\n{code}\n{FENCE}")
    return "\n\n".join(parts)


def render_list(node: Node) -> str:
    ordered = node.tag == "ol"
    lines = []
    index = 0
    for child in node.children:
        if not (isinstance(child, Node) and child.tag == "li"):
            continue
        index += 1
        marker = f"{index}. " if ordered else "- "
        lines.append(marker + collapse(render_inline(child)))
    return "\n".join(lines)


def render_definition_list(node: Node) -> str:
    lines = []
    term = None
    for child in node.children:
        if not isinstance(child, Node):
            continue
        if child.tag == "dt":
            term = collapse(render_inline(child))
        elif child.tag == "dd" and term is not None:
            lines.append(f"- **{term}** — {collapse(render_inline(child))}")
            term = None
    return "\n".join(lines)


def render_callout(node: Node) -> str:
    titles = node.find_all("span", "callout-title")
    title = collapse(titles[0].text()) if titles else "Note"
    body_blocks = []
    for child in node.children:
        if isinstance(child, Node) and child.tag == "p":
            body_blocks.append(collapse(render_inline(child)))
    body = "\n> ".join(body_blocks)
    return f"> **{title}.** {body}" if body else f"> **{title}.**"


def is_button_link_only(node: Node) -> bool:
    """True for paragraphs that hold nothing but a button-style link."""
    meaningful = [child for child in node.children
                  if not (isinstance(child, str) and not child.strip())]
    return bool(meaningful) and all(
        isinstance(child, Node) and child.tag == "a" and "btn" in child.classes
        for child in meaningful
    )


def render_block(node: Node) -> list[str]:
    """Render one child element of a section into markdown blocks."""
    if isinstance(node, str):
        text = collapse(node)
        return [text] if text else []
    if node.tag in ("h2", "h3"):
        return [f"{'##' if node.tag == 'h2' else '###'} {collapse(render_inline(node))}"]
    if node.tag == "p":
        if is_button_link_only(node):
            return []
        text = collapse(render_inline(node))
        if "note" in node.classes:
            return [f"> {text}"]
        return [text] if text else []
    if node.tag in ("ul", "ol"):
        return [render_list(node)]
    if node.tag == "dl":
        return [render_definition_list(node)]
    if node.tag == "table":
        return [render_table(node)]
    if node.tag == "div":
        if "code-block" in node.classes:
            return [render_code_block(node)]
        if "pill-row" in node.classes:
            pills = [collapse(render_inline(pill)) for pill in node.find_all("span", "pill")]
            return ["*" + " · ".join(pills) + "*"] if pills else []
        if "card-grid" in node.classes:
            blocks = []
            for card in node.find_all("div", "card"):
                heads = card.find_all("h3")
                if heads:
                    blocks.append(f"### {collapse(heads[0].text())}")
                for paragraph in card.find_all("p"):
                    blocks.append(collapse(render_inline(paragraph)))
            return blocks
        blocks = []
        for child in node.children:
            blocks.extend(render_block(child))
        return blocks
    if node.tag == "aside":
        return [render_callout(node)]
    if node.tag in ("section", "nav"):
        return []  # handled at the section level or skipped (toc)
    return []


def render_section(section: Node) -> str:
    blocks = []
    for child in section.children:
        if isinstance(child, Node) and "section-title" in child.classes:
            heads = child.find_all("h2")
            if heads:
                blocks.append(f"## {collapse(heads[0].text())}")
            continue
        if isinstance(child, Node) and "algo-head" in child.classes:
            nums = child.find_all("span", "algo-num")
            heads = child.find_all("h2")
            number = collapse(nums[0].text()) if nums else ""
            title = collapse(heads[0].text()) if heads else ""
            blocks.append(f"## {number}. {title}".replace(" . ", " . "))
            continue
        blocks.extend(render_block(child))
    return "\n\n".join(block for block in blocks if block.strip())


def render_signature(problem: dict, lang: str) -> str:
    name = function_name(SIGNATURES[problem["number"]][lang])
    return (f"{FENCE}{LANG_NAME[lang]}\n"
            f"{SIGNATURES[problem['number']][lang]}\n{FENCE}"), name


# ---------------------------------------------------------------------------
# Notebook-specific prose (authored here; the site pages do not carry it)
# ---------------------------------------------------------------------------

NOTEBOOK_TITLES = {
    "py": "Recitation 1 — Sorting Algorithms (Python)",
    "java": "Recitation 1 — Sorting Algorithms (Java)",
}

INTRO_MD = {
    "py": """## How to use this notebook

- This notebook mirrors the [Recitation 1 page](https://harryc919.github.io/TA-CS301/recitation1.html): the same concept notes and the same six problems. Reference solutions in all six languages stay on the website — try each problem before reading them.
- **Setup:** follow [Recitation 0](https://harryc919.github.io/TA-CS301/recitation0.html) once to create your `cs301-notebooks` uv project. Save this notebook into that folder and open it with the **Python (CS301)** kernel.
- **Work top to bottom.** Read the notes, then for each problem: read the brief, complete the starter-template cell, and run the self-check cell below it with Shift+Enter.
- A self-check cell fails with an `AssertionError` while the function is still the untouched stub. That is expected — implement, re-run the template cell, then re-run the check.
- Keep the function signature unchanged, sort manually (no `sorted(...)` or `list.sort(...)` in your implementation), and mind the "must not modify the input" requirements where stated.
- Nothing here is submitted or graded. Bring your attempt, or the exact line that breaks, to the recitation session.""",
    "java": """## How to use this notebook

- This notebook mirrors the [Recitation 1 page](https://harryc919.github.io/TA-CS301/recitation1.html): the same concept notes and the same six problems. Reference solutions in all six languages stay on the website — try each problem before reading them.
- **Setup:** follow [Recitation 0](https://harryc919.github.io/TA-CS301/recitation0.html) once to create your `cs301-notebooks` uv project and install the **Java** (IJava) kernel. Save this notebook into that folder and open it.
- **Work top to bottom.** Read the notes, then for each problem: read the brief, complete the `Solution` template cell, and run the check cell below it with Shift+Enter.
- IJava is JShell-style: cells contain plain statements and class definitions, no `main` wrapper. Each problem defines its own `public class Solution`, and running a definition cell (again) replaces the class — so edit → Shift+Enter → re-run that problem's check.
- Right after its own template cell, an untouched stub's check fails with `UnsupportedOperationException` — expected. If you see `cannot find symbol` instead, a later problem's `Solution` has replaced this one: re-run this problem's template cell, then the check. Implemented solutions print `OK ...` or `FAIL ...` lines; compare them with the expected values in the comments.
- Keep the signature unchanged, sort manually (no `Arrays.sort` in your implementation), and mind the "must not modify the input" requirements where stated.
- Nothing here is submitted or graded. Bring your attempt, or the exact line that breaks, to the recitation session.""",
}

EXERCISES_INTRO_MD = """## Exercises

Six problems mapped to the four sorts above. Each problem has a brief (statement,
examples, constraints, signature, hidden hints), a starter-template cell, and a
self-check cell. Keep the signature unchanged and implement the algorithms
yourself — built-in sorts are off limits. Problem 6 is optional exploration and
is not covered in class."""

CLOSING_MD = """## Where to go next

- [Recitation 1 page](https://harryc919.github.io/TA-CS301/recitation1.html) — full notes and reference solutions in six languages.
- [Recitation 0](https://harryc919.github.io/TA-CS301/recitation0.html) — environment setup and troubleshooting.
- [Introduction](https://harryc919.github.io/TA-CS301/intro.html) — office hours and course policies.

If a check cell reports a failure you believe is wrong, tell the TA."""


# Self-check cells per (lang, problem number). Expected values mirror the
# published examples and edge cases in problems.py; they are verified at build
# time against the reference solutions by tools/verify_notebooks.sh.
CHECKS: dict[tuple[str, int], str] = {
    ("py", 1): '''# Self-check — fails while bubble_sort is still the untouched stub.
nums = [5, 2, 4, 1, 3]
bubble_sort(nums)
assert nums == [1, 2, 3, 4, 5], f"expected [1, 2, 3, 4, 5], got {nums}"

nums = [1, 2, 3, 4]
bubble_sort(nums)
assert nums == [1, 2, 3, 4], f"expected no changes, got {nums}"

print("Problem 1 checks passed.")''',
    ("py", 2): '''# Self-check — fails while insertion_sort is still the untouched stub.
nums = [5, 2, 4, 1]
shifts = insertion_sort(nums)
assert shifts == 5, f"expected 5 shifts, got {shifts}"
assert nums == [1, 2, 4, 5], f"expected [1, 2, 4, 5], got {nums}"

assert insertion_sort([1, 2, 3]) == 0

nums = [2, 2, 2]
assert insertion_sort(nums) == 0, "equal keys must not shift (use >, not >=)"

print("Problem 2 checks passed.")''',
    ("py", 3): '''# Self-check — fails while sort_by_length is still the untouched stub.
words = ["pear", "kiwi", "apple", "fig", "banana"]
result = sort_by_length(words)
assert result == ["fig", "pear", "kiwi", "apple", "banana"], f"got {result}"

assert sort_by_length(["bb", "aa", "cc"]) == ["bb", "aa", "cc"], (
    "equal lengths must keep their original order")

assert sort_by_length(["ccc", "a", "bb", "ab", "ba"]) == ["a", "bb", "ab", "ba", "ccc"], (
    "the three length-2 words must keep their original order")

print("Problem 3 checks passed.")''',
    ("py", 4): '''# Self-check — fails while count_inversions is still the untouched stub.
nums = [8, 4, 2, 1]
result = count_inversions(nums)
assert result == 6, f"expected 6, got {result}"
assert nums == [8, 4, 2, 1], "the input array must not be modified"

assert count_inversions([1, 20, 6, 4, 5]) == 5
assert count_inversions([2, 2, 2]) == 0, "equal values are not inversions (strict >)"

# Requires the O(n log n) merge-sort approach; also proves the 64-bit range.
assert count_inversions(list(range(100_000, 0, -1))) == 4_999_950_000

print("Problem 4 checks passed.")''',
    ("py", 5): '''# Self-check — fails while quick_sort is still the untouched stub.
original = [5, 2, 4, 1, 3]
result = quick_sort(original)
assert result == [1, 2, 3, 4, 5], f"got {result}"
assert original == [5, 2, 4, 1, 3], "the input array must not be modified"

assert quick_sort([3, 1, 3, 3, 2, 3]) == [1, 2, 3, 3, 3, 3]
assert quick_sort([]) == [], "an empty array must be handled"

# All-equal input must stay fast: the 3-way partition skips it in one pass.
assert quick_sort([7] * 100_000) == [7] * 100_000

print("Problem 5 checks passed.")''',
    ("py", 6): '''# Self-check — fails while find_kth_largest is still the untouched stub.
assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
assert find_kth_largest([3, 3, 3], 2) == 3, "duplicates: [3, 3, 3] with k = 2 must return 3"

nums = [2, 1]
assert find_kth_largest(nums, 1) == 2
assert find_kth_largest(nums, 2) == 1

print("Problem 6 checks passed.")''',
    ("java", 1): '''import java.util.Arrays;

int[] nums = {5, 2, 4, 1, 3};
Solution.bubbleSort(nums);
System.out.println(Arrays.equals(nums, new int[]{1, 2, 3, 4, 5})
        ? "OK: [5, 2, 4, 1, 3] -> [1, 2, 3, 4, 5]"
        : "FAIL: got " + Arrays.toString(nums));

int[] alreadySorted = {1, 2, 3, 4};
Solution.bubbleSort(alreadySorted);
System.out.println(Arrays.equals(alreadySorted, new int[]{1, 2, 3, 4})
        ? "OK: already-sorted input stays unchanged"
        : "FAIL: got " + Arrays.toString(alreadySorted));''',
    ("java", 2): '''import java.util.Arrays;

int[] nums = {5, 2, 4, 1};
int shifts = Solution.insertionSort(nums);
System.out.println(shifts == 5 && Arrays.equals(nums, new int[]{1, 2, 4, 5})
        ? "OK: 5 shifts, nums = [1, 2, 4, 5]"
        : "FAIL: shifts = " + shifts + ", nums = " + Arrays.toString(nums));

System.out.println(Solution.insertionSort(new int[]{2, 2, 2}) == 0
        ? "OK: [2, 2, 2] performs 0 shifts"
        : "FAIL: equal keys must not shift (compare with >, not >=)");''',
    ("java", 3): '''import java.util.Arrays;

String[] words = {"pear", "kiwi", "apple", "fig", "banana"};
String[] result = Solution.sortByLength(words);
System.out.println(Arrays.equals(result, new String[]{"fig", "pear", "kiwi", "apple", "banana"})
        ? "OK: " + Arrays.toString(result)
        : "FAIL: got " + Arrays.toString(result));

String[] ties = {"ccc", "a", "bb", "ab", "ba"};
String[] tiesSorted = Solution.sortByLength(ties);
System.out.println(Arrays.equals(tiesSorted, new String[]{"a", "bb", "ab", "ba", "ccc"})
        ? "OK: the three length-2 words kept their original order"
        : "FAIL: got " + Arrays.toString(tiesSorted));''',
    ("java", 4): '''int[] nums = {8, 4, 2, 1};
long count = Solution.countInversions(nums);
System.out.println(count == 6
        ? "OK: [8, 4, 2, 1] has 6 inversions"
        : "FAIL: got " + count);

System.out.println(Solution.countInversions(new int[]{1, 20, 6, 4, 5}) == 5
        ? "OK: [1, 20, 6, 4, 5] has 5 inversions"
        : "FAIL: expected 5");

System.out.println(Solution.countInversions(new int[]{2, 2, 2}) == 0
        ? "OK: equal values are not inversions"
        : "FAIL: use a strict > comparison");

// Requires the O(n log n) merge-sort approach and the long return type.
int[] big = new int[100_000];
for (int i = 0; i < big.length; i++) {
    big[i] = big.length - i;
}
long expected = 100_000L * (big.length - 1) / 2;
System.out.println(Solution.countInversions(big) == expected
        ? "OK: 4,999,950,000 counted exactly with long"
        : "FAIL: expected " + expected);''',
    ("java", 5): '''import java.util.Arrays;

int[] original = {5, 2, 4, 1, 3};
int[] result = Solution.quickSort(original);
System.out.println(Arrays.equals(result, new int[]{1, 2, 3, 4, 5})
                        && Arrays.equals(original, new int[]{5, 2, 4, 1, 3})
        ? "OK: sorted copy returned, input unchanged"
        : "FAIL: got " + Arrays.toString(result) + ", input " + Arrays.toString(original));

System.out.println(Arrays.equals(Solution.quickSort(new int[]{}), new int[]{})
        ? "OK: empty array handled"
        : "FAIL: empty array must return an empty array");

// All-equal input must stay fast: the 3-way partition skips it in one pass.
int[] equal = new int[100_000];
Arrays.fill(equal, 7);
System.out.println(Arrays.equals(Solution.quickSort(equal), equal)
        ? "OK: 100,000 equal values sorted quickly"
        : "FAIL: all-equal input must stay fast (3-way partition)");''',
    ("java", 6): '''System.out.println(Solution.findKthLargest(new int[]{3, 2, 1, 5, 6, 4}, 2) == 5
        ? "OK: second largest of [3, 2, 1, 5, 6, 4] is 5"
        : "FAIL: expected 5");

System.out.println(Solution.findKthLargest(new int[]{3, 2, 3, 1, 2, 4, 5, 5, 6}, 4) == 4
        ? "OK: k = 4 returns 4"
        : "FAIL: expected 4");

System.out.println(Solution.findKthLargest(new int[]{3, 3, 3}, 2) == 3
        ? "OK: duplicates handled ([3, 3, 3], k = 2 -> 3)"
        : "FAIL: expected 3");''',
}


# ---------------------------------------------------------------------------
# Exercise brief (markdown) from problems.py
# ---------------------------------------------------------------------------

def problem_markdown(problem: dict, lang: str) -> str:
    number = problem["number"]
    blocks = [
        f"## Problem {number} — {problem['title']}",
        f"**Difficulty:** {problem['difficulty']} · **Topics:** "
        + " · ".join(problem["topics"]),
    ]
    blocks.extend(collapse(render_inline(parse_fragment(p))) for p in problem["statement"])

    example_blocks = ["### Examples"]
    for example in problem["examples"]:
        lines = [f"**{example['label']}**",
                 f"- Input: `{example['input']}`",
                 f"- Output: `{example['output']}`"]
        if example.get("explanation"):
            lines.append(f"- Explanation: {example['explanation']}")
        example_blocks.append("\n".join(lines))
    blocks.append("\n\n".join(example_blocks))

    constraints = "\n".join(f"- {collapse(render_inline(parse_fragment(item)))}"
                            for item in problem["constraints"])
    blocks.append("### Constraints\n\n" + constraints)

    signature_md, name = render_signature(problem, lang)
    signature_block = (f"### Function signature ({LANG_LABEL[lang]})\n\n{signature_md}")
    if problem["sig_note"]:
        signature_block += "\n\n" + collapse(render_inline(parse_fragment(problem["sig_note"])))
    blocks.append(signature_block)

    hint_items = "\n".join(f"<li>{hint}</li>" for hint in problem["hints"])
    blocks.append(
        "### Hints\n\n"
        "<details><summary>Show hints (open only if you are stuck)</summary>\n"
        f"<ol>\n{hint_items}\n</ol>\n</details>"
    )
    return "\n\n".join(blocks)


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

def md_cell(cell_id: str, source: str) -> dict:
    return {"cell_type": "markdown", "id": cell_id,
            "metadata": {}, "source": source}


def code_cell(cell_id: str, source: str) -> dict:
    return {"cell_type": "code", "id": cell_id, "metadata": {},
            "execution_count": None, "outputs": [], "source": source}


def build_notebook(lang: str, notes_root: Node) -> dict:
    cells = [md_cell("title", f"# {NOTEBOOK_TITLES[lang]}\n\n"
                     "COMPSCI 301 · Algorithms & Databases — Duke Kunshan University\n\n"
                     f"Practice notebook for [Recitation 1]({SITE_URL}/recitation1.html)."),
             md_cell("how-to", INTRO_MD[lang])]

    sections = notes_root.find_all("section")
    by_id = {}
    for section in sections:
        section_id = section.attrs.get("id")
        if section_id:
            by_id[section_id] = section
    for section_id in REQUIRED_SECTIONS:
        if section_id not in by_id:
            raise BuildError(f"notes fragment is missing section #{section_id}")
        cells.append(md_cell(f"notes-{section_id}", render_section(by_id[section_id])))

    cells.append(md_cell("exercises-intro", EXERCISES_INTRO_MD))

    for problem in PROBLEMS:
        number = problem["number"]
        stub = read_code(number, "stub", lang, allow_missing=False)
        name = function_name(SIGNATURES[number][lang])
        if name not in stub:
            raise BuildError(f"p{number} {lang} stub does not define {name!r}")
        check = CHECKS[(lang, number)]
        if name not in check:
            raise BuildError(f"self-check for p{number} ({lang}) never calls {name!r}")
        cells.append(md_cell(f"p{number}-brief", problem_markdown(problem, lang)))
        cells.append(code_cell(f"p{number}-stub", stub))
        cells.append(code_cell(f"p{number}-check", check))

    cells.append(md_cell("closing", CLOSING_MD))

    ids = [cell["id"] for cell in cells]
    if len(ids) != len(set(ids)):
        raise BuildError("duplicate notebook cell ids")

    return {
        "cells": cells,
        "metadata": {"kernelspec": KERNELS[lang]["kernelspec"],
                     "language_info": KERNELS[lang]["language_info"]},
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def build_notebooks() -> list[Path]:
    notes_root = parse_fragment(NOTES_HTML.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for lang in LANG_KEYS:
        notebook = build_notebook(lang, notes_root)
        payload = json.dumps(notebook, indent=1, ensure_ascii=False) + "\n"
        json.loads(payload)  # the written file must always parse back
        out = OUT_DIR / OUT_NAME[lang]
        out.write_text(payload, encoding="utf-8")
        written.append(out)
        print(f"wrote {out.relative_to(ROOT)}: {len(payload):,} bytes, "
              f"{len(notebook['cells'])} cells")
    return written


def main() -> int:
    try:
        build_notebooks()
    except BuildError as error:
        print(f"BUILD FAILED: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
