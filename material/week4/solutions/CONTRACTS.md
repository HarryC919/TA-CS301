# Recitation 4 — code contracts

## Exercise 3: Cheapest route with at most k stops (`stops/`)

Cities are numbered `0..n−1`, 1 ≤ n ≤ 100. `flights` lists directed flights
`(from, to, price)`: 0 ≤ m ≤ 10,000 flights, `from ≠ to`, 0 ≤ price ≤ 10,000, and
parallel flights between the same pair are allowed. `src` and `dst` are valid
cities and 0 ≤ k ≤ n − 1. Return the minimum total price of a route from `src` to
`dst` that uses at most k intermediate stops (at most k + 1 flights), or −1 if no
such route exists. `src == dst` costs 0. Every answer is at most
100 · 10,000 = 1,000,000, so 32-bit integers suffice. Do not modify `flights`.

Method: Bellman-Ford with k + 1 rounds. Each round relaxes every flight while
reading the distances of the previous round (a copy), so round t extends routes by
exactly one more flight. Time: O(k · m). Working space: O(n) for two distance
arrays.

- C: `int cheapestRoute(int n, const int* flights, int m, int src, int dst, int k)`
  `flights` holds m flights as consecutive triples: flight i is
  `flights[3*i]`, `flights[3*i + 1]`, `flights[3*i + 2]` (from, to, price).
  Returns −1 on allocation failure as well (the harness never triggers it).
- C++: `int cheapestRoute(int n, const std::vector<std::vector<int>>& flights, int src, int dst, int k)`
- C#: `public static int CheapestRoute(int n, int[][] flights, int src, int dst, int k)` in `Solution`.
- Java: `public static int cheapestRoute(int n, int[][] flights, int src, int dst, int k)` in `Solution`.
- Python: `def cheapest_route(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int`
- JavaScript: `function cheapestRoute(n, flights, src, dst, k)`; export via `module.exports = { cheapestRoute };`.

Harnesses cover `src == dst`, an unreachable destination, k = 0, the in-place
update trap (`0→1 100, 1→2 100, 0→2 500`, k = 0 → 500, k = 1 → 200), a chain
that needs more stops than allowed, parallel flights, cycles, zero prices, a city
with no flights, input preservation, 200 deterministic random cases checked against
an exhaustive enumeration of all routes with at most k + 1 flights, and a complete
graph with n = 100 (9,900 flights) and k = 99 checked against a separate layered
DP oracle.

## Extra: Floyd–Warshall (`floyd/`)

Vertices are numbered `0..n−1`, 1 ≤ n ≤ 200. `edges` lists directed edges
`(from, to, weight)`: 0 ≤ m ≤ 10,000, `from ≠ to`, −10,000 ≤ weight ≤ 10,000,
parallel edges allowed (the lightest one counts). The graph has no negative cycle.
Return the n × n matrix `D` where `D[i][j]` is the shortest-path distance from i
to j, `D[i][i] = 0`, and `D[i][j] = INF = 1,000,000,000` when j is unreachable
from i. Finite distances lie in ±(n − 1) · 10,000, so 32-bit integers suffice, and
the code must never add to an `INF` entry (that could turn "unreachable" into a
finite value when a negative edge follows). Do not modify `edges`.

Time: Θ(n³) plus O(m) to load the edges. Space: Θ(n²) for the returned matrix,
updated in place.

- C: `int* floydWarshall(int n, const int* edges, int m)`
  `edges` holds consecutive triples like `flights` above. Return a newly allocated
  row-major array of n · n ints (`D[i][j]` is element `i * n + j`); the caller frees
  it. Return NULL on allocation failure.
- C++: `std::vector<std::vector<int>> floydWarshall(int n, const std::vector<std::vector<int>>& edges)`
- C#: `public static int[][] FloydWarshall(int n, int[][] edges)` in `Solution`.
- Java: `public static int[][] floydWarshall(int n, int[][] edges)` in `Solution`.
- Python: `def floyd_warshall(n: int, edges: list[list[int]]) -> list[list[int]]`
- JavaScript: `function floydWarshall(n, edges)`; export via `module.exports = { floydWarshall, INF };`.

Every starter and reference defines `INF = 1,000,000,000` as a named constant.
Harnesses cover n = 1, the worked example, a negative edge, unreachable pairs, a
negative edge leaving an unreachable vertex (the `INF` guard), parallel edges,
input preservation, 100 deterministic random graphs with non-negative weights and
some negative edges arranged so no negative cycle exists, compared with
Bellman-Ford from every source, and n = 200 (a weight-1 cycle plus heavier chords,
so `D[i][j] = (j − i) mod n`) for the Θ(n³) loop.
