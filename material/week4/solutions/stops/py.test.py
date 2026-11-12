import importlib.util
from pathlib import Path
import copy
import random

spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("py.solution.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def enumerate_routes(n, flights, src, dst, k):
    # Exhaustive oracle: try every route of at most k + 1 flights.
    best = 0 if src == dst else None
    def walk(city, used, cost):
        nonlocal best
        if used == k + 1:
            return
        for u, v, price in flights:
            if u == city:
                if v == dst and (best is None or cost + price < best):
                    best = cost + price
                walk(v, used + 1, cost + price)
    walk(src, 0, 0)
    return -1 if best is None else best

def layered(n, flights, src, dst, k):
    # Separate oracle: best[t][v] over exactly t flights, minimum over t <= k + 1.
    INF = float("inf")
    best = [INF] * n
    best[src] = 0
    answer = 0 if src == dst else INF
    for _ in range(k + 1):
        nxt = [INF] * n
        for u, v, price in flights:
            nxt[v] = min(nxt[v], best[u] + price)
        best = nxt
        answer = min(answer, best[dst])
    return -1 if answer == INF else answer

def check(n, flights, src, dst, k, expected):
    before = copy.deepcopy(flights)
    result = module.cheapest_route(n, flights, src, dst, k)
    assert result == expected, (n, flights, src, dst, k, result, expected)
    assert flights == before, "flights were modified"

sample = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
trap = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
cases = [
    (4, sample, 0, 3, 1, 700), (4, sample, 0, 3, 2, 400), (4, sample, 0, 0, 0, 0),
    (3, trap, 0, 2, 0, 500), (3, trap, 0, 2, 1, 200),
    (3, [[0, 1, 5]], 0, 2, 2, -1), (4, [[0, 1, 1], [1, 2, 1], [2, 3, 1]], 0, 3, 1, -1),
    (4, [[0, 1, 1], [1, 2, 1], [2, 3, 1]], 0, 3, 2, 3), (2, [[0, 1, 7], [0, 1, 3]], 0, 1, 0, 3),
    (3, [[0, 1, 1], [1, 0, 1], [1, 2, 10]], 0, 2, 2, 11), (3, [[0, 1, 0], [1, 2, 0]], 0, 2, 1, 0),
    (1, [], 0, 0, 0, 0), (3, [[1, 2, 4]], 0, 2, 2, -1),
]
for case in cases:
    check(*case)
rng = random.Random(301)
for _ in range(200):
    n = rng.randint(1, 6)
    flights = [[u, v, rng.randint(0, 20)] for u, v in
               ((rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 12))) if u != v]
    src, dst, k = rng.randrange(n), rng.randrange(n), rng.randrange(min(n, 4))
    expected = enumerate_routes(n, flights, src, dst, k)
    assert expected == layered(n, flights, src, dst, k)
    check(n, flights, src, dst, k, expected)
n = 100
flights = [[u, v, (u * 37 + v * 91) % 10_001] for u in range(n) for v in range(n) if u != v]
for src, dst, k in [(0, 99, 99), (5, 42, 0), (17, 3, 2)]:
    check(n, flights, src, dst, k, layered(n, flights, src, dst, k))
print("ALL WEEK 4 STOPS PYTHON TESTS PASSED (216 cases)")
