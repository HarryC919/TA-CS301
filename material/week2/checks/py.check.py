# Run this cell after implementing and running the merge_sorted starter cell.
# These checks fail while the starter is still unchanged.
cases = [
    ([], [], []),
    ([], [-2, 5], [-2, 5]),
    ([1, 2], [], [1, 2]),
    ([1, 4, 9], [2, 2, 3, 10], [1, 2, 2, 3, 4, 9, 10]),
    ([2, 2], [2], [2, 2, 2]),
    ([-10**9, 0], [0, 10**9], [-10**9, 0, 0, 10**9]),
]
for left, right, expected in cases:
    before_left, before_right = left[:], right[:]
    result = merge_sorted(left, right)
    assert result == expected, (left, right, result, expected)
    assert left == before_left and right == before_right, "Inputs must not change"
    assert result is not left and result is not right, "Return a new list"
    if result:
        result[0] = 123456789
        assert left == before_left and right == before_right, "Result must be independent"

large = merge_sorted(list(range(0, 200000, 2)), list(range(1, 200000, 2)))
assert large == list(range(200000)), "Check the long interleaved merge"
print("Exercise 3 checks passed (6 edge cases + 200,000-element merge).")
