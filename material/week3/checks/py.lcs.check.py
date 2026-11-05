# Run this cell after implementing and running the longest_common_subsequence cell.
# These checks fail while the starter is still unchanged.
def is_subsequence(s, t):
    it = iter(t)
    return all(c in it for c in s)

cases = [
    ("", "", 0), ("", "ABC", 0), ("ABC", "DEF", 0), ("a", "A", 0),
    ("ABCB", "BDCAB", 3), ("ABCBDAB", "BDCABA", 4), ("AGGTAB", "GXTXAYB", 4),
    ("ABC", "ABC", 3), ("ACE", "ABCDE", 3), ("AAAA", "AA", 2),
]
for a, b, length in cases:
    result = longest_common_subsequence(a, b)
    assert isinstance(result, str), f"Return a string, got {result!r}"
    assert len(result) == length, (a, b, result, f"expected length {length}")
    assert is_subsequence(result, a) and is_subsequence(result, b), (a, b, result, "not a common subsequence")

large = longest_common_subsequence("AB" * 500, "BA" * 500)
assert isinstance(large, str) and len(large) == 999, "Check the 1,000 x 1,000 case"
assert is_subsequence(large, "AB" * 500) and is_subsequence(large, "BA" * 500)
print("Exercise 2 checks passed (10 cases + 1,000 x 1,000 input).")
