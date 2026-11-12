# Recitation 4 — Graph Algorithms

Status: approved layout. Implemented in `../../tools/site_src/recitation4-content.html`
and `../../site/recitation4.html`, with cheapest-route and Floyd–Warshall code under
`solutions/` and generated Python/Java notebooks under `../../site/notebooks/`. The practice content was agreed in conversation:
graph search gets a review table only (no exercise), the coding task is
Bellman-Ford with a limited number of rounds, union-find was not taught (so there
is no Kruskal coding task), and the extended ~40-minute core pace from
Recitation 3 is kept.

## 1. Scope and learning goals

Lectures are ahead of schedule, so this Tuesday session covers the latter half of
Week 3 (BFS, DFS, UCS, IDDFS) and all of Week 4 (Prim, Kruskal, Dijkstra,
Bellman-Ford). Graph search is CS201 review and gets a short summary only. All-pairs
shortest paths (Floyd–Warshall) appears only in the separate, optional Extra section.

Students should be able to:

- Compare BFS, DFS, UCS, and IDDFS by the structure holding waiting nodes, what
  each guarantees, and memory use; recognize UCS as Dijkstra that stops at the goal.
- State the cut property and explain Prim and Kruskal as two ways of applying it.
- Trace Prim and Kruskal, and decide with a justification or counterexample whether
  a given edge must, may, or cannot be in an MST.
- Explain which assumption Dijkstra relies on, and find the step where it fails on
  a graph with a negative edge.
- Explain the Bellman-Ford invariant ("after round i, every shortest path with at
  most i edges is correct"), why V − 1 rounds suffice, and how one extra round
  detects a negative cycle.
- Implement Bellman-Ford with a limited number of rounds, and explain why each
  round must read from the previous round's distances.

Prerequisites: graph representations (adjacency list/matrix), BFS/DFS from CS201,
priority queues as used in lecture, and the greedy/exchange reasoning from
Recitation 3.

## 2. Proposed page order

1. **Overview:** scope, goals, prerequisites, suggested session path.
2. **Review A — Graph search in one table.**
3. **Review B — Minimum spanning trees.**
4. **Review C — Single-source shortest paths.**
5. **Core practice:** three exercises, about 40 minutes in total.
6. **Optional practice** (written).
7. **Discussion and exit check.**
8. **Extra · Floyd–Warshall** (optional, not examined; separated as in Recitation 3).

One page with direct anchors, following Recitations 1–3.

## 3. Concept review — approximately 12 minutes

### A. Graph search in one table (about 3 minutes)

| Algorithm | Waiting nodes kept in | Guarantee | Memory |
| --- | --- | --- | --- |
| BFS | FIFO queue | fewest-edges path | O(V) frontier (whole level) |
| DFS | stack / recursion | none for path length | O(depth) |
| UCS | priority queue by path cost | cheapest path (non-negative costs) | O(V) |
| IDDFS | repeated depth-limited DFS | fewest-edges path, like BFS | O(depth), like DFS |

Two takeaways: UCS is Dijkstra that stops once the goal is removed from the
priority queue; IDDFS repeats shallow levels but this costs only a constant factor
when the branching factor is at least 2. Time costs are O(V + E) for BFS/DFS on an
explicit graph. No exercise.

### B. Minimum spanning trees (about 4 minutes)

- Problem: connected, undirected, weighted graph; find a spanning tree of minimum
  total weight.
- **Cut property:** for any cut (S, V − S), a lightest edge crossing it belongs to
  some MST (to every MST when weights are distinct). Proof idea: exchange argument,
  the same idea as Recitation 3.
- **Prim:** grow one tree; the cut is (tree, rest); add the lightest crossing edge.
  O(E log V) with a binary-heap priority queue.
- **Kruskal:** scan edges by increasing weight; add an edge if it joins two different
  components (the cut is one component versus everything else). Sorting costs
  O(E log E); the component check is described abstractly (union-find was not taught,
  so the page states the total cost as the lecture gave it and does not derive the
  union-find part).

### C. Single-source shortest paths (about 5 minutes)

- **Relaxation:** `if d[u] + w(u, v) < d[v] then d[v] = d[u] + w(u, v)`, the shared
  step of both algorithms.
- **Dijkstra:** remove the vertex with the smallest tentative distance and finalize
  it. Correct when all weights are non-negative, because any other path to it would
  have to pass through a vertex that already has a distance at least as large.
  O((V + E) log V) with a binary heap.
- **Bellman-Ford:** relax every edge, V − 1 rounds. Invariant: after round i, `d[v]`
  is at most the cheapest cost of any path to v using at most i edges. A shortest
  path without a negative cycle has at most V − 1 edges, so V − 1 rounds suffice;
  if a V-th round still improves something, a reachable negative cycle exists.
  O(VE).

## 4. Core practice — approximately 40 minutes

### Exercise 1. MST: trace and true/false — 12 minutes (written)

Graph (undirected, distinct weights): A–B 4, A–C 1, B–C 3, B–D 2, C–D 5, C–E 8,
D–E 6, D–F 9. (Corrected during development: the draft also had E–F 7, which made
D–F 9 the heaviest edge on the cycle D–E–F and therefore *not* in the MST.)

1. Trace Kruskal: list the edges in the order they are accepted, and name the first
   edge rejected and the cycle it would close.
   *Reference:* accepts A–C 1, B–D 2, B–C 3; rejects A–B 4 (cycle A–C–B) and
   C–D 5; accepts D–E 6; rejects C–E 8; accepts D–F 9. Total 21.
2. Trace Prim from A, writing the crossing edge chosen at each step.
   *Reference:* A–C 1, C–B 3, B–D 2, D–E 6, D–F 9. Same tree, different order,
   total 21. Why the same tree: distinct weights ⇒ the MST is unique.
3. True or false, with a justification or counterexample:
   - "The heaviest edge of a graph is never in an MST." *False:* D–F 9 is the
     heaviest edge in this graph and it is in the MST, because it is the only edge
     reaching F.
   - "The lightest edge is in every MST." *True with distinct weights* (cut property
     on the cut around one of its endpoints). Discussion: with ties, it is in
     *some* MST but not necessarily every one.
   - "An MST contains a shortest path between every pair of vertices." *False:*
     triangle X–Y 1, Y–Z 1, X–Z 1.5. The MST is {X–Y, Y–Z} (cost 2), but the
     shortest X–Z path is the direct edge, 1.5. Leads into Exercise 2.
- Staged hints: for statement 1, look for an edge that is the only way to reach a
  vertex; for statement 3, try three vertices.

### Exercise 2. Dijkstra vs Bellman-Ford — 10 minutes (written)

Directed graph: S→A 2, S→B 5, B→A −4, A→T 1. Source S.

1. Trace the lecture's Dijkstra (finalize on removal, never update a finalized
   vertex). Report the order vertices are finalized and the final distances.
   *Reference:* finalizes S (0), A (2), T (3), B (5); then B→A would give 1, but A
   is already final. Result A = 2, T = 3; true distances are A = 1 (S→B→A),
   T = 2.
2. Which step went wrong, and which assumption failed? *Reference:* finalizing A at
   distance 2 assumed no later path could be cheaper, which needs non-negative
   weights; the path through B gets cheaper after the −4 edge.
3. Explain why Bellman-Ford's V − 1 rounds find the correct distances here and in
   general, and how to detect a negative cycle with one more round.
- Staged hints: write the tentative distances after each removal; for part 3, how
  many edges can a shortest path have without repeating a vertex?
- Note in the answer: some heap implementations reinsert improved vertices and
  happen to fix this example, but then the "each vertex is finalized once" bound is
  lost; the exercise refers to the lecture's version.

### Exercise 3. Cheapest route with at most k stops — 18 minutes (coding)

- Task: `n` cities `0..n−1`; a list of directed flights `(u, v, price)` with
  non-negative integer prices; `src`, `dst`, `k`. Return the cheapest price from
  `src` to `dst` using at most `k` intermediate stops (at most k + 1 flights), or
  −1 if there is no such route.
- Method: Bellman-Ford with k + 1 rounds instead of V − 1, which uses the round
  invariant from Review C directly.
- Key point to diagnose: updating `d` in place lets one round chain several flights.
  Example: flights 0→1 100, 1→2 100, 0→2 500, `src = 0`, `dst = 2`, `k = 0`.
  Correct answer 500; in-place updates (edges in the given order) return 200. Each
  round must read from a copy of the previous round's distances. Students explain
  this in a written cell, as well as fixing the code.
- Starter: signature, distance array initialization, and the round loop skeleton;
  students write the copy and the relaxation step.
- Checks: `src == dst` (0), unreachable destination (−1), `k = 0`, cheapest route
  overall needs too many stops (the example above), parallel flights between the
  same cities, cycles in the flight graph, input list not modified, and a large
  input (e.g., n = 100, ~5,000 flights, k = 99) for O(k·E) time and O(n) extra space.
- Expected evidence: working code plus an explanation of O(k · E) time and O(n)
  working space (two distance arrays), and why the copy is needed.
- Six languages (c, cpp, cs, java, py, js). No priority queue is needed, so no
  helper code.

## 5. Optional practice (written)

Union-find was not taught, so there is no Kruskal coding task. Two short written
questions instead, with collapsed answers:

1. "To handle negative edges, add a constant to every weight so all are
   non-negative, then run Dijkstra." Give a counterexample. (Paths with more edges
   are penalized more, so the shortest path can change.)
2. Show that in an MST, the path between two vertices minimizes the largest edge
   weight on the path (minimum bottleneck path), even though it need not minimize
   the total weight (Exercise 1's triangle).

## 6. Discussion, feedback, and exit check

About 10–15 minutes: compare the counterexamples students found, connect "Prim is
fine with negative weights, Dijkstra is not" to which property each proof uses, and
review the in-place update bug from Exercise 3. Staged hints, self-checks, and
collapsed reference explanations provide the feedback path.

Exit check: "Your friend runs Prim on a graph with negative edge weights, and
Dijkstra on the same graph. Which result can you trust, and why?" (Prim: the cut
property only compares weights crossing a cut and does not care about signs;
Dijkstra's finalize step needs non-negative weights.)

## 7. Extra · Floyd–Warshall (optional, not examined)

- **Why:** distances between all pairs. Running Dijkstra from every vertex fails
  with negative edges; running Bellman-Ford from every vertex costs O(V²E).
- **How, as a DP** (the five-step path from Recitation 3):
  - Subproblem: `D_k(i, j)` = cheapest i → j path whose intermediate vertices are
    all in `{1..k}`.
  - Recurrence: `D_k(i, j) = min(D_{k−1}(i, j), D_{k−1}(i, k) + D_{k−1}(k, j))`.
  - Base: `D_0(i, j) = w(i, j)`, 0 on the diagonal, ∞ if there is no edge.
  - Order: k outermost; a single 2-D table can be updated in place (row and
    column k do not change during round k).
  - Cost: Θ(V³) time, Θ(V²) space. A negative diagonal entry means a negative cycle.
- Small worked example (4 vertices) with the table after each k.
- **Build it:** input `n` and a directed edge list (negative weights allowed, no
  negative cycles); return the distance matrix with a sentinel for unreachable
  pairs. Checks: unreachable pairs, a negative edge, parallel edges, self-distance
  0. Six languages.

## 8. Next stage after approval

- Write `tools/site_src/recitation4-content.html` (shared notes/prompts/hints/
  answers) and `tools/site_src/build_recitation4.py`, reusing Recitation 3's tabs,
  table styles, and Markdown conversion. Simple inline SVG figures for the
  Exercise 1 and Exercise 2 graphs.
- Solutions and contracts for Exercise 3 and Floyd–Warshall under
  `material/week4/solutions/`; notebook checks under `material/week4/checks/`.
- Python/Java notebooks with Exercise 3 and the Floyd–Warshall task at the end under
  an "Extra (optional)" heading; written answers in Markdown cells.
- Update `site_layout.py`, Home directory and `.hero-slots` badges, README
  inventory, AGENTS source map and counts, `test_notebook_format.py`,
  `verify_notebooks.sh`, `test_code_ui.cjs`, and add `tools/verify_week4.sh`.
- Rebuild and run all checks listed in AGENTS, plus desktop/mobile screenshots.
  No commit without your authorization.
