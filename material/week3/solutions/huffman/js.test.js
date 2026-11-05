const assert = require('node:assert/strict');
const {huffmanCodes} = require('./js.solution.js');
function optimalCost(freq) {
  // Oracle: total cost = sum of all merged weights (two-queue Huffman on sorted input).
  if (freq.length === 1) return freq[0];
  const leaves = freq.slice().sort((x,y)=>x-y), merged = [];
  let i = 0, j = 0, cost = 0;
  const take = () => (j >= merged.length || (i < leaves.length && leaves[i] <= merged[j])) ? leaves[i++] : merged[j++];
  for (let k = 1; k < freq.length; k++) { const w = take() + take(); merged.push(w); cost += w; }
  return cost;
}
function check(freq) {
  const before = freq.slice();
  const codes = huffmanCodes(freq);
  assert.deepEqual(freq, before);
  assert.ok(Array.isArray(codes) && codes.length === freq.length);
  for (const c of codes) assert.match(c, /^[01]+$/);
  const ordered = codes.slice().sort();
  for (let k = 1; k < ordered.length; k++) assert.ok(!ordered[k].startsWith(ordered[k-1]), 'not prefix-free');
  assert.equal(freq.reduce((s, f, k) => s + f * codes[k].length, 0), optimalCost(freq));
}
assert.deepEqual(huffmanCodes([7]), ['0']);
for (const f of [[7],[5,5],[1,1,1,1],[45,13,12,16,9,5],[1,2,4,8,16],[1000000,1,1],Array(9).fill(3)]) check(f);
let seed=301;
function next() { seed=(Math.imul(seed,1664525)+1013904223)>>>0; return seed; }
for (let t=0;t<100;t++) check(Array.from({length: 1 + next()%40}, () => 1 + next()%50));
check(Array.from({length: 1000}, () => 1 + next()%1000000));
console.log('ALL WEEK 3 HUFFMAN JAVASCRIPT TESTS PASSED (108 cases)');
