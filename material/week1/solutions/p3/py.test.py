"""Test harness for P3 (sort words by length, stably). Not shipped to students."""
import importlib.util
import random
import sys
from pathlib import Path

# The solution file is named py.solution.py, so load it by path and register it
# under the module name "py.solution"; then the contracted import line works.
_spec = importlib.util.spec_from_file_location(
    "py.solution", Path(__file__).parent / "py.solution.py")
_module = importlib.util.module_from_spec(_spec)
sys.modules["py.solution"] = _module
_spec.loader.exec_module(_module)

from py.solution import sort_by_length

failures = 0


def check(input_words, expected, name):
    """Runs one case and records a failure instead of raising."""
    global failures
    original = list(input_words)
    got = sort_by_length(input_words)

    if input_words != original:
        print("FAIL " + name + ": input list was modified")
        failures += 1
        return
    if got != expected:
        print("FAIL " + name)
        print("  got  " + repr(got))
        print("  want " + repr(expected))
        failures += 1
        return
    print("PASS " + name)


def make_random_words(count, max_length, seed):
    """Builds seeded random lowercase words so every run is reproducible."""
    rng = random.Random(seed)
    letters = "abcdefghijklmnopqrstuvwxyz"
    words = []
    for _ in range(count):
        length = rng.randint(1, max_length)
        words.append("".join(rng.choice(letters) for _ in range(length)))
    return words


def check_random(count, max_length, seed, name):
    """Cross-checks against a library stable sort. The HARNESS may use it as
    the oracle; the solution itself may not."""
    words = make_random_words(count, max_length, seed)
    expected = sorted(words, key=len)
    check(words, expected, name)


# Fixed cases from the contract.
check(["pear", "kiwi", "apple", "fig", "banana"],
      ["fig", "pear", "kiwi", "apple", "banana"],
      "case pear/kiwi/apple/fig/banana")
check(["a"], ["a"], "case single word [a]")
check(["bb", "aa", "cc"], ["bb", "aa", "cc"],
      "case all equal length (order preserved)")
check(["ccc", "a", "bb", "ab", "ba"], ["a", "bb", "ab", "ba", "ccc"],
      "case ties keep original order")
check(["abcd", "a", "abc", "ab"], ["a", "ab", "abc", "abcd"],
      "case ascending lengths")
check(["a", "q" * 100, "bb"], ["a", "bb", "q" * 100],
      "case word of 100 characters")
check(["b", "a"], ["b", "a"], "case two equal-length words")

# Seeded random cross-checks against the library stable-sort oracle.
check_random(1000, 100, 12345, "random n=1000, lengths 1..100 (seed 12345)")
check_random(1000, 6, 999, "random n=1000, many ties (lengths 1..6, seed 999)")

if failures == 0:
    print("ALL TESTS PASSED")
    sys.exit(0)
print(str(failures) + " TEST(S) FAILED")
sys.exit(1)
