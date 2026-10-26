'use strict';

// Test harness for P3 (sort words by length, stably). Not shipped to students.
const { sortByLength } = require('./js.solution.js');

let failures = 0;

// Sorts a copy of `input` with the solution, compares it against `expected`,
// and checks that the caller's array was left untouched.
function check(inputWords, expected, name) {
    const original = inputWords.slice();
    const got = sortByLength(inputWords);

    if (inputWords.length !== original.length
        || inputWords.some((word, index) => word !== original[index])) {
        console.log(`FAIL ${name}: input array was modified`);
        failures++;
        return;
    }

    if (got.length !== expected.length
        || got.some((word, index) => word !== expected[index])) {
        console.log(`FAIL ${name}`);
        console.log(`  got  ${JSON.stringify(got)}`);
        console.log(`  want ${JSON.stringify(expected)}`);
        failures++;
        return;
    }

    console.log(`PASS ${name}`);
}

// Small deterministic PRNG (mulberry32) so the random tests are reproducible.
function makeRandom(seed) {
    let state = seed >>> 0;
    return function nextValue() {
        state = (state + 0x6D2B79F5) >>> 0;
        let value = state;
        value = Math.imul(value ^ (value >>> 15), value | 1);
        value ^= value + Math.imul(value ^ (value >>> 7), value | 61);
        return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
    };
}

// Builds `count` seeded random lowercase words.
function makeRandomWords(count, maxLength, seed) {
    const nextValue = makeRandom(seed);
    const letters = 'abcdefghijklmnopqrstuvwxyz';
    const words = [];
    for (let i = 0; i < count; i++) {
        const length = 1 + Math.floor(nextValue() * maxLength);
        let word = '';
        for (let k = 0; k < length; k++) {
            word += letters[Math.floor(nextValue() * letters.length)];
        }
        words.push(word);
    }
    return words;
}

// Cross-checks the solution against a library stable sort. The HARNESS may use
// a library sort as the oracle; the solution itself may not.
function checkRandom(count, maxLength, seed, name) {
    const words = makeRandomWords(count, maxLength, seed);
    const expected = words.slice().sort((a, b) => a.length - b.length);
    check(words, expected, name);
}

// Fixed cases from the contract.
check(['pear', 'kiwi', 'apple', 'fig', 'banana'],
      ['fig', 'pear', 'kiwi', 'apple', 'banana'],
      'case pear/kiwi/apple/fig/banana');
check(['a'], ['a'], 'case single word [a]');
check(['bb', 'aa', 'cc'], ['bb', 'aa', 'cc'],
      'case all equal length (order preserved)');
check(['ccc', 'a', 'bb', 'ab', 'ba'], ['a', 'bb', 'ab', 'ba', 'ccc'],
      'case ties keep original order');
check(['abcd', 'a', 'abc', 'ab'], ['a', 'ab', 'abc', 'abcd'],
      'case ascending lengths');
check(['a', 'q'.repeat(100), 'bb'], ['a', 'bb', 'q'.repeat(100)],
      'case word of 100 characters');
check(['b', 'a'], ['b', 'a'], 'case two equal-length words');

// Seeded random cross-checks against the library stable-sort oracle.
checkRandom(1000, 100, 12345, 'random n=1000, lengths 1..100 (seed 12345)');
checkRandom(1000, 6, 999, 'random n=1000, many ties (lengths 1..6, seed 999)');

if (failures === 0) {
    console.log('ALL TESTS PASSED');
    process.exit(0);
}
console.log(`${failures} TEST(S) FAILED`);
process.exit(1);
