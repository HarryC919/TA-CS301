'use strict';

const { countInversions } = require('./js.solution.js');

let failures = 0;
let randomState = 12345;

// Verify one answer, and also check that the input array was not modified.
function check(name, input, expected) {
  const copy = input.slice();
  const got = countInversions(input);
  if (got !== expected) {
    console.log(`FAIL ${name}: got ${got}, want ${expected}`);
    failures += 1;
  } else if (!sameArray(input, copy)) {
    console.log(`FAIL ${name}: input array was modified`);
    failures += 1;
  } else {
    console.log(`PASS ${name}`);
  }
}

function sameArray(left, right) {
  if (left.length !== right.length) {
    return false;
  }
  for (let i = 0; i < left.length; i += 1) {
    if (left[i] !== right[i]) {
      return false;
    }
  }
  return true;
}

// Reference answer: O(n^2) double loop, only for small inputs.
function bruteForce(nums) {
  let count = 0;
  for (let i = 0; i < nums.length; i += 1) {
    for (let j = i + 1; j < nums.length; j += 1) {
      if (nums[i] > nums[j]) {
        count += 1;
      }
    }
  }
  return count;
}

// Deterministic pseudo-random generator so every run tests the same data.
function nextRandom() {
  randomState = (randomState * 1664525 + 1013904223) >>> 0;
  return randomState;
}

function makeRandom(n, minValue, maxValue) {
  const span = maxValue - minValue + 1;
  const nums = new Array(n);
  for (let i = 0; i < n; i += 1) {
    nums[i] = minValue + (nextRandom() % span);
  }
  return nums;
}

// Count pairs with different values; used to check the large random case.
function unequalPairCount(nums) {
  const ordered = nums.slice().sort((left, right) => left - right);
  let unequalPairs = (nums.length * (nums.length - 1)) / 2;
  let runStart = 0;
  while (runStart < ordered.length) {
    let runEnd = runStart + 1;
    while (runEnd < ordered.length && ordered[runEnd] === ordered[runStart]) {
      runEnd += 1;
    }
    const runLength = runEnd - runStart;
    unequalPairs -= (runLength * (runLength - 1)) / 2;
    runStart = runEnd;
  }
  return unequalPairs;
}

// Fixed cases from the contract.
check('case [1]', [1], 0);
check('case [1,2,3,4]', [1, 2, 3, 4], 0);
check('case [4,3,2,1]', [4, 3, 2, 1], 6);
check('case [8,4,2,1]', [8, 4, 2, 1], 6);
check('case [1,20,6,4,5]', [1, 20, 6, 4, 5], 5);
check('case [2,2,2] (strict >)', [2, 2, 2], 0);

// Seeded random cross-check against the brute-force answer.
const randomSizes = [1, 2, 3, 5, 10, 50, 300, 2000];
for (const n of randomSizes) {
  const nums = makeRandom(n, -10000, 10000);
  check(`random n=${n} vs brute force`, nums, bruteForce(nums));
}

// A descending array of 100,000 elements has n*(n-1)/2 = 4,999,950,000
// inversions, which does not fit in 32 bits.
const largeSize = 100000;
const descending = new Array(largeSize);
for (let i = 0; i < largeSize; i += 1) {
  descending[i] = largeSize - i;
}
check('descending 100,000 (64-bit)', descending, 4999950000);

// Performance run on a random array of 100,000 values.
const large = makeRandom(largeSize, -1000000000, 1000000000);
const largeCopy = large.slice();
const start = Date.now();
const largeCount = countInversions(large);
const seconds = (Date.now() - start) / 1000;
if (!sameArray(large, largeCopy)) {
  console.log('FAIL perf n=100,000: input array was modified');
  failures += 1;
} else if (seconds > 2.0) {
  console.log(`FAIL perf n=100,000: ${seconds.toFixed(3)} s (expected under 2 s)`);
  failures += 1;
} else {
  console.log(`PASS perf n=100,000 (${seconds.toFixed(3)} s)`);
}

// Cross-check the large answer without O(n^2) work: for every pair of
// different values exactly one of the two orders is an inversion, so
// count(nums) + count(reverse(nums)) equals the number of unequal pairs.
const reversedLarge = large.slice().reverse();
const reversedCount = countInversions(reversedLarge);
const unequalPairs = unequalPairCount(large);
if (largeCount + reversedCount === unequalPairs) {
  console.log('PASS large random consistency: count + reversed = unequal pairs');
} else {
  console.log(`FAIL large random consistency: ${largeCount} + ${reversedCount} != ${unequalPairs}`);
  failures += 1;
}

if (failures === 0) {
  console.log('ALL TESTS PASSED');
} else {
  console.log(`${failures} TEST(S) FAILED`);
  process.exit(1);
}
