// Test harness for P1 - bubble sort with early exit (verification only).
const assert = require('assert');
const { bubbleSort } = require('./js.solution.js');

let failures = 0;

function check(input, expected, name) {
  const nums = input.slice();
  bubbleSort(nums); // in place
  try {
    assert.deepStrictEqual(nums, expected);
    console.log(`PASS ${name}`);
  } catch (err) {
    console.log(`FAIL ${name}: got [${nums}], want [${expected}]`);
    failures++;
  }
}

// Fixed cases from the contract
check([1], [1], 'case [1]');
check([5, 2, 4, 1, 3], [1, 2, 3, 4, 5], 'case [5,2,4,1,3]');
check([1, 2, 3, 4], [1, 2, 3, 4], 'case [1,2,3,4] already sorted (early exit)');
check([4, 3, 2, 1], [1, 2, 3, 4], 'case [4,3,2,1] reverse sorted');
check([2, 2, 1, 3, 2], [1, 2, 2, 2, 3], 'case [2,2,1,3,2] duplicates');
check([-1, 5, 0, -10], [-10, -1, 0, 5], 'case [-1,5,0,-10] negatives');

// Seeded random cross-check vs library sort, n = 1000.
// Math.random() cannot be seeded, so use a small deterministic LCG.
let seed = 42;
function nextRandom() {
  seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
  return seed;
}

const data = [];
for (let i = 0; i < 1000; i++) {
  data.push((nextRandom() % 20001) - 10000); // values in [-10000, 10000]
}
const actual = data.slice();
bubbleSort(actual); // in place
const expected = data.slice().sort((a, b) => a - b); // library sort as the oracle
try {
  assert.deepStrictEqual(actual, expected);
  console.log('PASS case random n=1000 vs Array#sort');
} catch (err) {
  console.log('FAIL case random n=1000 vs Array#sort');
  failures++;
}

if (failures > 0) {
  console.log(`${failures} TEST(S) FAILED`);
  process.exit(1);
}
console.log('ALL TESTS PASSED');
