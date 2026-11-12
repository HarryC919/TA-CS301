# Run this cell after implementing and running the floyd_warshall cell.
# These checks fail while the starter is still unchanged.
I = 1_000_000_000  # INF
cases = [
    (4, [[0, 1, 3], [0, 3, 7], [1, 0, 8], [1, 2, 2], [2, 0, 5], [2, 3, 1], [3, 0, 2]],
     [[0, 3, 5, 6], [5, 0, 2, 3], [3, 6, 0, 1], [2, 5, 7, 0]], "worked example"),
    (1, [], [[0]], "one vertex"),
    (3, [[0, 1, 4], [0, 2, 5], [2, 1, -3]], [[0, 2, 5], [I, 0, I], [I, -3, 0]], "negative edge"),
    (3, [[0, 1, 1]], [[0, 1, I], [I, 0, I], [I, I, 0]], "unreachable pairs"),
    (3, [[1, 2, -5]], [[0, I, I], [I, 0, -5], [I, I, 0]], "never add to INF"),
    (2, [[0, 1, 5], [0, 1, 2], [1, 0, 4]], [[0, 2], [4, 0]], "parallel edges"),
]
for n, edges, expected, label in cases:
    before = [list(e) for e in edges]
    result = floyd_warshall(n, edges)
    assert result == expected, f"{label}: expected {expected}, got {result!r}"
    assert edges == before, f"{label}: edges were modified"

n = 200
large = [[i, (i + 1) % n, 1] for i in range(n)] + [[i, (i * 7 + 3) % n, n + i % 5] for i in range(n) if (i * 7 + 3) % n != i]
assert floyd_warshall(n, large) == [[(j - i) % n for j in range(n)] for i in range(n)], "Check the 200-vertex case"
print("Floyd-Warshall checks passed (6 cases + 200 vertices).")
