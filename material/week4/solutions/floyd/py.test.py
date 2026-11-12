import importlib.util
from pathlib import Path
import copy
import random

spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("py.solution.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
INF = 1_000_000_000
assert module.INF == INF

def bellman_ford_all(n, edges):
    # Oracle: Bellman-Ford from every source.
    rows = []
    for s in range(n):
        d = [INF] * n
        d[s] = 0
        for _ in range(n - 1):
            for u, v, w in edges:
                if d[u] != INF and d[u] + w < d[v]:
                    d[v] = d[u] + w
        rows.append(d)
    return rows

def check(n, edges, expected=None):
    before = copy.deepcopy(edges)
    result = module.floyd_warshall(n, edges)
    expected = bellman_ford_all(n, edges) if expected is None else expected
    assert result == expected, (n, edges, result, expected)
    assert edges == before, "edges were modified"

example = [[0, 1, 3], [0, 3, 7], [1, 0, 8], [1, 2, 2], [2, 0, 5], [2, 3, 1], [3, 0, 2]]
check(4, example, [[0, 3, 5, 6], [5, 0, 2, 3], [3, 6, 0, 1], [2, 5, 7, 0]])
check(1, [], [[0]])
check(3, [[0, 1, 4], [0, 2, 5], [2, 1, -3]], [[0, 2, 5], [INF, 0, INF], [INF, -3, 0]])
check(3, [[0, 1, 1]], [[0, 1, INF], [INF, 0, INF], [INF, INF, 0]])
check(3, [[1, 2, -5]], [[0, INF, INF], [INF, 0, -5], [INF, INF, 0]])
check(2, [[0, 1, 5], [0, 1, 2], [1, 0, 4]], [[0, 2], [4, 0]])
rng = random.Random(301)
for _ in range(100):
    n = rng.randint(1, 8)
    # w = base + p[u] - p[v] with base >= 0: some edges are negative, no cycle is.
    p = [rng.randint(0, 20) for _ in range(n)]
    edges = [[u, v, rng.randint(0, 20) + p[u] - p[v]] for u, v in
             ((rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 20))) if u != v]
    check(n, edges)
# Large: a directed cycle of weight-1 edges plus heavier chords, so D[i][j] = (j - i) mod n.
n = 200
edges = [[i, (i + 1) % n, 1] for i in range(n)]
edges += [[i, (i * 7 + 3) % n, n + i % 5] for i in range(n) if (i * 7 + 3) % n != i]
check(n, edges, [[(j - i) % n for j in range(n)] for i in range(n)])
print("ALL WEEK 4 FLOYD PYTHON TESTS PASSED (108 cases)")
