const { quickSort } = require('./js.solution.js');

let failures = 0;
let checks = 0;

// Return the index of the first difference, or -1 when the arrays are equal.
function firstMismatch(a, b) {
  for (let i = 0; i < Math.min(a.length, b.length); i++) {
    if (a[i] !== b[i]) {
      return i;
    }
  }
  return a.length === b.length ? -1 : Math.min(a.length, b.length);
}

function sameArray(a, b) {
  if (a.length !== b.length) {
    return false;
  }
  for (let i = 0; i < a.length; i++) {
    if (a[i] !== b[i]) {
      return false;
    }
  }
  return true;
}

// Print the first mismatching position for a failed test case.
function printMismatch(name, result, expected, mismatch) {
  console.log(
    `FAIL ${name}: index ${mismatch} got ${result[mismatch]}, want ${expected[mismatch]}`
  );
}

// Check one fixed test case: the result values and that the caller's array
// was not modified.
function checkSorted(name, input, expected) {
  checks++;
  const original = input.slice();
  const result = quickSort(input);

  if (result.length !== expected.length) {
    console.log(`FAIL ${name}: length ${result.length}, want ${expected.length}`);
    failures++;
    return;
  }

  const mismatch = firstMismatch(result, expected);
  if (mismatch >= 0) {
    printMismatch(name, result, expected, mismatch);
    failures++;
  } else if (!sameArray(input, original)) {
    console.log(`FAIL ${name}: the input array was modified`);
    failures++;
  } else {
    console.log(`PASS ${name}`);
  }
}

// Check one n = 200,000 case: cross-check against Array.prototype.sort,
// confirm the input was not modified, and require the sort to finish well
// under 2 seconds.
function checkPerformance(name, input) {
  checks++;
  const expected = input.slice().sort((a, b) => a - b); // library sort as oracle
  const original = input.slice();

  const start = performance.now();
  const result = quickSort(input);
  const seconds = (performance.now() - start) / 1000;

  if (result.length !== expected.length) {
    console.log(`FAIL ${name}: length ${result.length}, want ${expected.length}`);
    failures++;
    return;
  }

  const mismatch = firstMismatch(result, expected);
  if (mismatch >= 0) {
    printMismatch(name, result, expected, mismatch);
    failures++;
  } else if (!sameArray(input, original)) {
    console.log(`FAIL ${name}: the input array was modified`);
    failures++;
  } else if (seconds >= 2.0) {
    console.log(`FAIL ${name}: ${seconds.toFixed(3)} s is not well under 2 s`);
    failures++;
  } else {
    console.log(`PASS ${name} (${seconds.toFixed(3)} s)`);
  }
}

// --- Fixed cases from the contract ---------------------------------------
checkSorted('[] -> []', [], []);
checkSorted('[1] -> [1]', [1], [1]);
checkSorted('[5,2,4,1,3] -> [1,2,3,4,5]', [5, 2, 4, 1, 3], [1, 2, 3, 4, 5]);
checkSorted('[3,1,3,3,2,3] -> [1,2,3,3,3,3]', [3, 1, 3, 3, 2, 3], [1, 2, 3, 3, 3, 3]);
checkSorted('[7,7,7,7] -> unchanged', [7, 7, 7, 7], [7, 7, 7, 7]);
checkSorted('[4,3,2,1] -> [1,2,3,4]', [4, 3, 2, 1], [1, 2, 3, 4]);
checkSorted('[-3,5,0,-3,2] -> [-3,-3,0,2,5]', [-3, 5, 0, -3, 2], [-3, -3, 0, 2, 5]);

// Seeded random cross-check against Array.prototype.sort, n = 1000.
{
  let seed = 12345;
  const nextValue = (maxExclusive) => {
    seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
    return seed % maxExclusive;
  };
  const n = 1000;
  const input = Array.from({ length: n }, () => nextValue(2000001) - 1000000);
  const expected = input.slice().sort((a, b) => a - b);
  checkSorted('random n=1000 cross-check', input, expected);
}

// --- Performance cases, n = 200,000 --------------------------------------
const N = 200000;
{
  let seed = 2024;
  const nextValue = (maxExclusive) => {
    seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
    return seed % maxExclusive;
  };
  const input = Array.from({ length: N }, () => nextValue(51)); // values in [0,50]
  checkPerformance('n=200000 random values in [0,50]', input);
}
checkPerformance('n=200000 all-equal', new Array(N).fill(42));
checkPerformance('n=200000 already sorted', Array.from({ length: N }, (_, i) => i));

console.log(`\n${checks} checks, ${failures} failed`);
if (failures > 0) {
  console.log('FAILED');
  process.exit(1);
}
console.log('All tests passed.');
