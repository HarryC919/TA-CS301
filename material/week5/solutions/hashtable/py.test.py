import importlib.util
from pathlib import Path
import random

spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("py.solution.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
HashTable = module.HashTable
cases = 0

def expect(actual, expected, label):
    global cases
    cases += 1
    assert actual == expected, f"{label}: expected {expected!r}, got {actual!r}"

# Empty table, insert, update.
t = HashTable(7)
expect(t.get(3), -1, "get on empty"); expect(t.remove(3), False, "remove on empty"); expect(t.size(), 0, "empty size")
expect(t.put(10, 100), True, "insert"); expect(t.get(10), 100, "get after insert"); expect(t.size(), 1, "size 1")
expect(t.put(10, 111), True, "update"); expect(t.get(10), 111, "updated value"); expect(t.size(), 1, "update keeps size")
expect(t.put(0, 0), True, "key 0, value 0"); expect(t.get(0), 0, "value 0 is not absent")
# Bug 1: removing 10 must not hide 17 (10 -> slot 3, 17 collides at 3, goes to slot 2).
t = HashTable(7)
t.put(10, 1); t.put(17, 2)
expect(t.remove(10), True, "remove 10"); expect(t.get(17), 2, "tombstone keeps 17 reachable"); expect(t.get(10), -1, "10 gone")
expect(t.remove(10), False, "second remove")
# Bug 2: put must not create a duplicate past a tombstone.
expect(t.put(17, 3), True, "update 17 past tombstone"); expect(t.size(), 1, "no duplicate")
expect(t.remove(17), True, "remove 17"); expect(t.get(17), -1, "no stale duplicate"); expect(t.size(), 0, "size 0")
# Re-insert reuses a tombstone.
expect(t.put(10, 5), True, "re-insert"); expect(t.get(10), 5, "re-inserted value"); expect(t.size(), 1, "size after re-insert")
# Part A trace table, m = 11.
t = HashTable(11)
for k in [22, 1, 13, 11, 24, 33]:
    expect(t.put(k, k * 10), True, f"trace insert {k}")
expect([t.keys[s] if t.state[s] == module.OCCUPIED else None for s in range(11)],
       [22, 1, 13, None, 11, None, None, 24, 33, None, None], "Part A slots")
t.remove(11); expect(t.get(33), 330, "Part A: 33 after removing 11")
# Full table and an all-tombstone table.
t = HashTable(5)
for k in range(5):
    expect(t.put(k * 5, k), True, f"fill {k}")
expect(t.put(99, 1), False, "full: new key rejected"); expect(t.put(10, 7), True, "full: update allowed")
expect(t.size(), 5, "full size"); expect(t.get(99), -1, "full: absent key")
for k in range(5):
    expect(t.remove(k * 5), True, f"empty out {k}")
expect(t.get(10), -1, "all tombstones: search stops after m probes"); expect(t.remove(3), False, "all tombstones remove")
expect(t.put(99, 1), True, "all tombstones: insert reuses one"); expect(t.get(99), 1, "reused slot")
# Randomized against a direct-address oracle (keys are small here).
rng = random.Random(301)
for m in [3, 5, 7, 11, 13, 101]:
    t, oracle, size = HashTable(m), [-1] * (3 * m), 0
    for _ in range(3000):
        key, op = rng.randrange(3 * m), rng.random()
        if op < 0.5:
            value = rng.randrange(1000)
            ok = oracle[key] != -1 or size < m
            expect(t.put(key, value), ok, f"m={m} put {key}")
            if ok:
                size += oracle[key] == -1
                oracle[key] = value
        elif op < 0.75:
            expect(t.remove(key), oracle[key] != -1, f"m={m} remove {key}")
            size -= oracle[key] != -1
            oracle[key] = -1
        else:
            expect(t.get(key), oracle[key], f"m={m} get {key}")
        expect(t.size(), size, f"m={m} size")
# Large: 60,000 keys in m = 100,003 (alpha about 0.6), then removals.
m = 100_003
t = HashTable(m)
keys = [i * 7919 for i in range(60_000)]
for k in keys:
    assert t.put(k, k % 1_000_000)
for k in keys:
    assert t.get(k) == k % 1_000_000 and t.get(k + 1) == -1
for k in keys[::2]:
    assert t.remove(k)
for i, k in enumerate(keys):
    assert t.get(k) == (-1 if i % 2 == 0 else k % 1_000_000)
assert t.size() == 30_000
cases += 4
print(f"ALL WEEK 5 HASHTABLE PYTHON TESTS PASSED ({cases} checks)")
