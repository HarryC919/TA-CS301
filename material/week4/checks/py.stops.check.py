# Run this cell after implementing and running the cheapest_route cell.
# These checks fail while the starter is still unchanged.
sample = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
trap = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
chain = [[0, 1, 1], [1, 2, 1], [2, 3, 1]]
cases = [
    (4, sample, 0, 3, 1, 700, "sample, k = 1"),
    (4, sample, 0, 3, 2, 400, "sample, k = 2"),
    (4, sample, 0, 0, 0, 0, "src == dst"),
    (3, trap, 0, 2, 0, 500, "in-place trap: one round must not chain two flights"),
    (3, trap, 0, 2, 1, 200, "trap, k = 1"),
    (3, [[0, 1, 5]], 0, 2, 2, -1, "unreachable destination"),
    (4, chain, 0, 3, 1, -1, "route needs too many stops"),
    (4, chain, 0, 3, 2, 3, "chain, k = 2"),
    (2, [[0, 1, 7], [0, 1, 3]], 0, 1, 0, 3, "parallel flights"),
    (3, [[0, 1, 1], [1, 0, 1], [1, 2, 10]], 0, 2, 2, 11, "cycle"),
    (3, [[0, 1, 0], [1, 2, 0]], 0, 2, 1, 0, "zero prices"),
]
for n, flights, src, dst, k, expected, label in cases:
    before = [list(f) for f in flights]
    result = cheapest_route(n, flights, src, dst, k)
    assert result == expected, f"{label}: expected {expected}, got {result!r}"
    assert flights == before, f"{label}: flights were modified"

n = 100
large = [[u, v, (u * 37 + v * 91) % 10_001] for u in range(n) for v in range(n) if u != v]
assert cheapest_route(n, large, 0, 99, 99) == 2464, "Check the 100-city, 9,900-flight case"
print("Exercise 3 checks passed (11 cases + 100 cities, 9,900 flights, k = 99).")
