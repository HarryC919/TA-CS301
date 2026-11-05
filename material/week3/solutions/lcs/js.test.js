const assert = require('node:assert/strict');
const {longestCommonSubsequence} = require('./js.solution.js');
function lcsLength(a, b) {
  let prev = new Array(b.length + 1).fill(0);
  for (const x of a) {
    const cur = [0];
    for (let j = 1; j <= b.length; j++) cur.push(x === b[j-1] ? prev[j-1] + 1 : Math.max(prev[j], cur[j-1]));
    prev = cur;
  }
  return prev[b.length];
}
function isSubsequence(s, t) { let k = 0; for (const c of t) if (k < s.length && s[k] === c) k++; return k === s.length; }
function check(a, b, expected) {
  const result = longestCommonSubsequence(a, b);
  assert.equal(typeof result, 'string');
  assert.equal(result.length, expected === undefined ? lcsLength(a, b) : expected);
  assert.ok(isSubsequence(result, a) && isSubsequence(result, b));
}
for (const [a,b,e] of [['','',0],['','ABC',0],['ABC','',0],['ABC','DEF',0],['a','A',0],
  ['ABCB','BDCAB',3],['ABCBDAB','BDCABA',4],['AGGTAB','GXTXAYB',4],['ABC','ABC',3],
  ['ACE','ABCDE',3],['AAAA','AA',2],['XMJYAUZ','MZJAWXU',4]]) check(a,b,e);
assert.equal(longestCommonSubsequence('ABCB','BDCAB'),'BCB');
let seed=301;
function next() { seed=(Math.imul(seed,1664525)+1013904223)>>>0; return seed; }
const word = () => Array.from({length: next()%25}, () => 'ABC'[next()%3]).join('');
for (let t=0;t<100;t++) check(word(), word());
check('AB'.repeat(500),'BA'.repeat(500),999);
console.log('ALL WEEK 3 LCS JAVASCRIPT TESTS PASSED (113 cases)');
