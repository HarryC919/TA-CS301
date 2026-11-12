const assert = require('node:assert/strict');
const {floydWarshall, INF} = require('./js.solution.js');
assert.equal(INF, 1_000_000_000);
function bellmanFordAll(n, edges) {
  return Array.from({length: n}, (_, s) => {
    const d = new Array(n).fill(INF); d[s] = 0;
    for (let r = 0; r < n - 1; r++) for (const [u, v, w] of edges) if (d[u] !== INF && d[u] + w < d[v]) d[v] = d[u] + w;
    return d;
  });
}
function check(n, edges, expected = bellmanFordAll(n, edges)) {
  const before = JSON.stringify(edges);
  assert.deepEqual(floydWarshall(n, edges), expected, `n=${n} ${JSON.stringify(edges)}`);
  assert.equal(JSON.stringify(edges), before, 'edges were modified');
}
const I = INF;
check(4, [[0,1,3],[0,3,7],[1,0,8],[1,2,2],[2,0,5],[2,3,1],[3,0,2]], [[0,3,5,6],[5,0,2,3],[3,6,0,1],[2,5,7,0]]);
check(1, [], [[0]]);
check(3, [[0,1,4],[0,2,5],[2,1,-3]], [[0,2,5],[I,0,I],[I,-3,0]]);
check(3, [[0,1,1]], [[0,1,I],[I,0,I],[I,I,0]]);
check(3, [[1,2,-5]], [[0,I,I],[I,0,-5],[I,I,0]]);
check(2, [[0,1,5],[0,1,2],[1,0,4]], [[0,2],[4,0]]);
let seed = 301;
function next() { seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0; return seed; }
for (let t = 0; t < 100; t++) {
  const n = 1 + next() % 8, tries = next() % 21, p = Array.from({length: n}, () => next() % 21), edges = [];
  // w = base + p[u] - p[v] with base >= 0: some edges are negative, no cycle is.
  for (let i = 0; i < tries; i++) { const u = next() % n, v = next() % n; if (u !== v) edges.push([u, v, next() % 21 + p[u] - p[v]]); }
  check(n, edges);
}
// Large: a weight-1 cycle plus heavier chords, so D[i][j] = (j - i) mod n.
const N = 200, large = [];
for (let i = 0; i < N; i++) large.push([i, (i + 1) % N, 1]);
for (let i = 0; i < N; i++) if ((i * 7 + 3) % N !== i) large.push([i, (i * 7 + 3) % N, N + i % 5]);
check(N, large, Array.from({length: N}, (_, i) => Array.from({length: N}, (_, j) => ((j - i) % N + N) % N)));
console.log('ALL WEEK 4 FLOYD JAVASCRIPT TESTS PASSED (108 cases)');
