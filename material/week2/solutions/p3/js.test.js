const assert = require('node:assert/strict');
const {mergeSorted} = require('./js.solution.js');
function check(left, right) {
  const a = left.slice(), b = right.slice();
  const expected = left.concat(right).sort((x,y)=>x-y);
  const result = mergeSorted(left, right);
  assert.deepEqual(result, expected);
  assert.deepEqual(left, a); assert.deepEqual(right, b);
  assert.notEqual(result, left); assert.notEqual(result, right);
  if (result.length) result[0] = 123456789;
  assert.deepEqual(left, a); assert.deepEqual(right, b);
}
for (const [a,b] of [[[],[]],[[],[1,2]],[[1,2],[]],[[1],[1]],
  [[1,4,9],[2,2,3,10]],[[-1000000000,0],[0,1000000000]],
  [[1,2,3],[9]],[[9],[1,2,3]],[[2,2,2,2,2],[2,2,2]]]) check(a,b);
let seed=301;
function next() { seed=(Math.imul(seed,1664525)+1013904223)>>>0; return seed; }
for(let t=0;t<100;t++) {
  const a=Array.from({length:next()%60},()=>next()%41-20).sort((x,y)=>x-y);
  const b=Array.from({length:next()%60},()=>next()%41-20).sort((x,y)=>x-y);
  check(a,b);
}
check(Array.from({length:100000},(_,i)=>2*i),Array.from({length:100000},(_,i)=>2*i+1));
console.log('ALL WEEK 2 JAVASCRIPT TESTS PASSED (110 cases)');
