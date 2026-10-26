const { findKthLargest } = require('./js.solution.js');

let failures = 0;

// Wrapper that compares one quickselect call against the expected answer.
function check(nums, k, expected, name) {
  const got = findKthLargest(nums, k);
  if (got !== expected) {
    console.log(`FAIL ${name} (k=${k}): got ${got}, want ${expected}`);
    failures++;
  } else {
    console.log(`PASS ${name} (k=${k} -> ${got})`);
  }
}

// Seeded 32-bit xorshift: the random test data is identical on every run.
function makeRandom(seed) {
  let state = seed >>> 0;
  return function nextRandom() {
    state ^= state << 13;
    state >>>= 0;
    state ^= state >>> 17;
    state ^= state << 5;
    state >>>= 0;
    return state;
  };
}

// Fixed cases from the contract
check([3, 2, 1, 5, 6, 4], 2, 5, 'case [3,2,1,5,6,4]');
check([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4, 'case [3,2,3,1,2,4,5,5,6]');
check([1], 1, 1, 'case [1]');
check([2, 1], 1, 2, 'case [2,1] k=1');
check([2, 1], 2, 1, 'case [2,1] k=2');
check([-1, -5, 3], 1, 3, 'case [-1,-5,3]');
check([3, 3, 3], 2, 3, 'case [3,3,3]');

// Regression cases within the published 100,000-element limit.
check(new Array(2000).fill(3), 1000, 3, 'duplicate recursion regression');
for (const [name, data] of [
  ['all equal', new Array(100000).fill(7)],
  ['three values', Array.from({length: 100000}, (_, i) => i % 3 - 1)],
  ['sorted', Array.from({length: 100000}, (_, i) => Math.floor(i / 5) - 10000)],
  ['reverse sorted', Array.from({length: 100000}, (_, i) => 9999 - Math.floor(i / 5))]
]) {
  const oracle = data.slice().sort((a, b) => a - b);
  for (const k of [1, data.length / 2, data.length]) {
    check(data, k, oracle[data.length - k], name);
  }
}

// Seeded random cross-check against Array.prototype.sort, n = 200,000
const n = 200000;
const nextRandom = makeRandom(42);
const data = new Array(n);
for (let i = 0; i < n; i++) {
  data[i] = (nextRandom() % 20001) - 10000; // values in [-10000, 10000]
}
const sorted = data.slice().sort((a, b) => a - b);
for (const k of [1, n / 2, n]) {
  const copy = data.slice();
  const start = Date.now();
  const got = findKthLargest(copy, k);
  const elapsedMs = Date.now() - start;
  const expected = sorted[n - k];
  if (got !== expected) {
    console.log(`FAIL random n=200000 k=${k}: got ${got}, want ${expected}`);
    failures++;
  } else if (elapsedMs > 2000) {
    console.log(`FAIL random n=200000 k=${k}: too slow (${elapsedMs} ms)`);
    failures++;
  } else {
    console.log(`PASS random n=200000 k=${k} -> ${got} (${elapsedMs} ms)`);
  }
}

if (failures === 0) {
  console.log('ALL TESTS PASSED');
  process.exit(0);
}
console.log(`${failures} TEST(S) FAILED`);
process.exit(1);
