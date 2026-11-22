const assert = require('node:assert/strict');
const {HashTable} = require('./js.solution.js');
let cases = 0;
function expect(actual, expected, label) { cases++; assert.equal(actual, expected, label); }
let t = new HashTable(7);
expect(t.get(3), -1, 'get on empty'); expect(t.remove(3), false, 'remove on empty'); expect(t.size(), 0, 'empty size');
expect(t.put(10, 100), true, 'insert'); expect(t.get(10), 100, 'get after insert'); expect(t.size(), 1, 'size 1');
expect(t.put(10, 111), true, 'update'); expect(t.get(10), 111, 'updated value'); expect(t.size(), 1, 'update keeps size');
expect(t.put(0, 0), true, 'key 0, value 0'); expect(t.get(0), 0, 'value 0 is not absent');
t = new HashTable(7);
t.put(10, 1); t.put(17, 2);
expect(t.remove(10), true, 'remove 10'); expect(t.get(17), 2, 'tombstone keeps 17 reachable'); expect(t.get(10), -1, '10 gone');
expect(t.remove(10), false, 'second remove');
expect(t.put(17, 3), true, 'update 17 past tombstone'); expect(t.size(), 1, 'no duplicate');
expect(t.remove(17), true, 'remove 17'); expect(t.get(17), -1, 'no stale duplicate'); expect(t.size(), 0, 'size 0');
expect(t.put(10, 5), true, 're-insert'); expect(t.get(10), 5, 're-inserted value'); expect(t.size(), 1, 'size after re-insert');
t = new HashTable(11);
for (const k of [22, 1, 13, 11, 24, 33]) expect(t.put(k, k * 10), true, `trace insert ${k}`);
t.remove(11); expect(t.get(33), 330, 'Part A: 33 after removing 11');
t = new HashTable(5);
for (let k = 0; k < 5; k++) expect(t.put(k * 5, k), true, `fill ${k}`);
expect(t.put(99, 1), false, 'full: new key rejected'); expect(t.put(10, 7), true, 'full: update allowed');
expect(t.size(), 5, 'full size'); expect(t.get(99), -1, 'full: absent key');
for (let k = 0; k < 5; k++) expect(t.remove(k * 5), true, `empty out ${k}`);
expect(t.get(10), -1, 'all tombstones: search stops after m probes'); expect(t.remove(3), false, 'all tombstones remove');
expect(t.put(99, 1), true, 'all tombstones: insert reuses one'); expect(t.get(99), 1, 'reused slot');
let seed = 301;
function next() { seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0; return seed; }
for (const m of [3, 5, 7, 11, 13, 101]) {
  t = new HashTable(m);
  const oracle = new Array(3 * m).fill(-1);
  let size = 0;
  for (let step = 0; step < 3000; step++) {
    const key = next() % (3 * m), op = next() % 100;
    if (op < 50) {
      const value = next() % 1000, ok = oracle[key] !== -1 || size < m;
      expect(t.put(key, value), ok, `m=${m} put ${key}`);
      if (ok) { if (oracle[key] === -1) size++; oracle[key] = value; }
    } else if (op < 75) {
      expect(t.remove(key), oracle[key] !== -1, `m=${m} remove ${key}`);
      if (oracle[key] !== -1) size--;
      oracle[key] = -1;
    } else {
      expect(t.get(key), oracle[key], `m=${m} get ${key}`);
    }
    expect(t.size(), size, `m=${m} size`);
  }
}
t = new HashTable(100003);
const keys = Array.from({length: 60000}, (_, i) => i * 7919);
for (const k of keys) assert.equal(t.put(k, k % 1000000), true, 'large put');
for (const k of keys) assert.ok(t.get(k) === k % 1000000 && t.get(k + 1) === -1, 'large get');
for (let i = 0; i < keys.length; i += 2) assert.equal(t.remove(keys[i]), true, 'large remove');
keys.forEach((k, i) => assert.equal(t.get(k), i % 2 === 0 ? -1 : k % 1000000, 'large get after remove'));
expect(t.size(), 30000, 'large size');
console.log(`ALL WEEK 5 HASHTABLE JAVASCRIPT TESTS PASSED (${cases + 3} checks)`);
