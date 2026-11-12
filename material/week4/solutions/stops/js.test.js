const assert = require('node:assert/strict');
const {cheapestRoute} = require('./js.solution.js');
function enumerateRoutes(n, flights, src, dst, k) {
  let best = src === dst ? 0 : -1;
  (function walk(city, used, cost) {
    if (used === k + 1) return;
    for (const [u, v, price] of flights) if (u === city) {
      if (v === dst && (best < 0 || cost + price < best)) best = cost + price;
      walk(v, used + 1, cost + price);
    }
  })(src, 0, 0);
  return best;
}
function layered(n, flights, src, dst, k) {
  let b = new Array(n).fill(Infinity); b[src] = 0;
  let ans = src === dst ? 0 : Infinity;
  for (let t = 0; t <= k; t++) {
    const nx = new Array(n).fill(Infinity);
    for (const [u, v, price] of flights) nx[v] = Math.min(nx[v], b[u] + price);
    b = nx; ans = Math.min(ans, b[dst]);
  }
  return ans === Infinity ? -1 : ans;
}
function check(n, flights, src, dst, k, expected) {
  const before = JSON.stringify(flights);
  assert.equal(cheapestRoute(n, flights, src, dst, k), expected, `${JSON.stringify(flights)} ${src}->${dst} k=${k}`);
  assert.equal(JSON.stringify(flights), before, 'flights were modified');
}
const sample = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], trap = [[0,1,100],[1,2,100],[0,2,500]], chain = [[0,1,1],[1,2,1],[2,3,1]];
for (const c of [[4,sample,0,3,1,700],[4,sample,0,3,2,400],[4,sample,0,0,0,0],[3,trap,0,2,0,500],[3,trap,0,2,1,200],
  [3,[[0,1,5]],0,2,2,-1],[4,chain,0,3,1,-1],[4,chain,0,3,2,3],[2,[[0,1,7],[0,1,3]],0,1,0,3],
  [3,[[0,1,1],[1,0,1],[1,2,10]],0,2,2,11],[3,[[0,1,0],[1,2,0]],0,2,1,0],[1,[],0,0,0,0],[3,[[1,2,4]],0,2,2,-1]]) check(...c);
let seed = 301;
function next() { seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0; return seed; }
for (let t = 0; t < 200; t++) {
  const n = 1 + next() % 6, tries = next() % 13, flights = [];
  for (let i = 0; i < tries; i++) { const u = next() % n, v = next() % n; if (u !== v) flights.push([u, v, next() % 21]); }
  const src = next() % n, dst = next() % n, k = next() % Math.min(n, 4);
  const expected = enumerateRoutes(n, flights, src, dst, k);
  assert.equal(expected, layered(n, flights, src, dst, k));
  check(n, flights, src, dst, k, expected);
}
const large = [];
for (let u = 0; u < 100; u++) for (let v = 0; v < 100; v++) if (u !== v) large.push([u, v, (u * 37 + v * 91) % 10001]);
for (const [s, d, k] of [[0,99,99],[5,42,0],[17,3,2]]) check(100, large, s, d, k, layered(100, large, s, d, k));
console.log('ALL WEEK 4 STOPS JAVASCRIPT TESTS PASSED (216 cases)');
