import importlib.util
from pathlib import Path
import random

spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("py.solution.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def lcs_length(a, b):
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if x == y else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]

def is_subsequence(s, t):
    it = iter(t)
    return all(c in it for c in s)

def check(a, b, expected=None):
    result = module.longest_common_subsequence(a, b)
    assert isinstance(result, str), (a, b, result)
    length = lcs_length(a, b) if expected is None else expected
    assert len(result) == length, (a, b, result, length)
    assert is_subsequence(result, a) and is_subsequence(result, b), (a, b, result)

cases = [("", "", 0), ("", "ABC", 0), ("ABC", "", 0), ("ABC", "DEF", 0), ("a", "A", 0),
         ("ABCB", "BDCAB", 3), ("ABCBDAB", "BDCABA", 4), ("AGGTAB", "GXTXAYB", 4),
         ("ABC", "ABC", 3), ("ACE", "ABCDE", 3), ("AAAA", "AA", 2), ("XMJYAUZ", "MZJAWXU", 4)]
for a, b, expected in cases:
    check(a, b, expected)
assert module.longest_common_subsequence("ABCB", "BDCAB") == "BCB"
rng = random.Random(301)
for _ in range(100):
    check("".join(rng.choice("ABC") for _ in range(rng.randrange(25))),
          "".join(rng.choice("ABC") for _ in range(rng.randrange(25))))
check("AB" * 500, "BA" * 500, 999)
print("ALL WEEK 3 LCS PYTHON TESTS PASSED (113 cases)")
