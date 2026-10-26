// Test harness for P2 - insertion sort counting shifts (verification only).
const assert = require('assert');
const { insertionSort } = require('./js.solution.js');

let failures = 0;

// Oracle 1 (shift count): brute-force inversion count, O(n^2) - harness only.
function countInversionsBruteForce(nums) {
  let count = 0;
  for (let i = 0; i < nums.length; i++) {
    for (let j = i + 1; j < nums.length; j++) {
      if (nums[i] > nums[j]) {
        count++;
      }
    }
  }
  return count;
}

function checkFixed(name, input, expected, expectedShifts) {
  const nums = input.slice();
  const shifts = insertionSort(nums); // in place
  let ok = shifts === expectedShifts;
  for (let i = 0; i < nums.length && ok; i++) {
    ok = nums[i] === expected[i];
  }
  if (!ok) {
    console.log(`FAIL ${name} (shifts=${shifts}, expected=${expectedShifts})`);
    failures++;
    return;
  }
  console.log(`PASS ${name} (shifts=${shifts})`);
}

// Seeded random cross-checks. Math.random() cannot be seeded, so use a
// small deterministic LCG.
let seed = 42;
function nextRandom() {
  seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
  return seed;
}

function checkRandom(randomSeed, n, valueRange) {
  seed = randomSeed;
  const original = [];
  for (let i = 0; i < n; i++) {
    original.push((nextRandom() % (2 * valueRange + 1)) - valueRange);
  }
  const expectedShifts = countInversionsBruteForce(original);
  const nums = original.slice();
  const shifts = insertionSort(nums);
  const expected = original.slice().sort((a, b) => a - b); // oracle 2: library sort
  let ok = shifts === expectedShifts;
  for (let i = 0; i < n && ok; i++) {
    ok = nums[i] === expected[i];
  }
  if (!ok) {
    console.log(
      `FAIL random n=${n} seed=${randomSeed} (shifts=${shifts}, expected=${expectedShifts})`
    );
    failures++;
    return;
  }
  console.log(`PASS random n=${n} seed=${randomSeed} (shifts=${shifts})`);
}

// Fixed cases from the contract
checkFixed('case [1]', [1], [1], 0);
checkFixed('case [1,2,3]', [1, 2, 3], [1, 2, 3], 0);
checkFixed('case [3,2,1]', [3, 2, 1], [1, 2, 3], 3);
checkFixed('case [5,2,4,1]', [5, 2, 4, 1], [1, 2, 4, 5], 5);
checkFixed('case [2,2,2] equal keys', [2, 2, 2], [2, 2, 2], 0);
checkFixed('case [-1,5,0,-10] negatives', [-1, 5, 0, -10], [-10, -1, 0, 5], 4);

// Seeded random cross-checks: shifts vs brute force, array vs library sort
checkRandom(42, 1000, 10000);
checkRandom(7, 1000, 10000);
checkRandom(1234, 1000, 10000);
checkRandom(99, 1000, 3); // heavy duplicates: stresses the strict '>' rule

if (failures > 0) {
  console.log(`${failures} TEST(S) FAILED`);
  process.exit(1);
}
console.log('ALL TESTS PASSED');
