# Run this cell after implementing and running the HashTable cell.
# These checks fail while the starter is still unchanged.
def expect(actual, expected, label):
    assert actual == expected, f"{label}: expected {expected!r}, got {actual!r}"

t = HashTable(7)
expect(t.get(3), -1, "get on an empty table")
expect(t.remove(3), False, "remove on an empty table")
expect(t.put(10, 100), True, "insert 10")
expect(t.get(10), 100, "get after insert")
expect(t.put(10, 111), True, "update 10")
expect((t.get(10), t.size()), (111, 1), "update changes the value, not the size")
expect(t.put(0, 0), True, "key 0 with value 0")
expect(t.get(0), 0, "value 0 is a real value, not 'absent'")

# Bug 1: 10 -> slot 3; 17 collides at slot 3 and goes to slot 2.
t = HashTable(7)
t.put(10, 1)
t.put(17, 2)
expect(t.remove(10), True, "remove 10")
expect(t.get(17), 2, "bug 1: after removing 10, 17 must still be found (use DELETED, not EMPTY)")
expect(t.remove(10), False, "removing 10 twice")
# Bug 2: slot 3 is now DELETED; 17 is still stored further along in slot 2.
expect(t.put(17, 3), True, "update 17")
expect(t.size(), 1, "bug 2: put must not stop at the first DELETED slot and store a duplicate 17")
expect(t.remove(17), True, "remove 17")
expect(t.get(17), -1, "bug 2: no stale copy of 17 is left behind")

# Part A table: remove 11, then 33 (probes 0 -> 4 -> 8) must still be found.
t = HashTable(11)
for k in [22, 1, 13, 11, 24, 33]:
    t.put(k, k * 10)
t.remove(11)
expect(t.get(33), 330, "Part A: 33 after removing 11")

# Full table, then a table with only DELETED slots.
t = HashTable(5)
for k in range(5):
    expect(t.put(k * 5, k), True, f"fill slot {k}")
expect(t.put(99, 1), False, "full table: a new key is rejected")
expect(t.put(10, 7), True, "full table: updating an existing key still works")
for k in range(5):
    t.remove(k * 5)
expect(t.get(10), -1, "all slots DELETED: search must stop after m probes")
expect(t.put(99, 1), True, "all slots DELETED: insert reuses one")
expect((t.get(99), t.size()), (1, 1), "after reusing a DELETED slot")

# Random operations against a direct-address table (keys are small here).
import random
rng = random.Random(301)
for m in [3, 7, 101]:
    t, oracle, size = HashTable(m), [-1] * (3 * m), 0
    for step in range(2000):
        key, op = rng.randrange(3 * m), rng.random()
        if op < 0.5:
            value, ok = rng.randrange(1000), oracle[key] != -1 or size < m
            expect(t.put(key, value), ok, f"m = {m}, step {step}: put({key}, {value})")
            if ok:
                size += oracle[key] == -1
                oracle[key] = value
        elif op < 0.75:
            expect(t.remove(key), oracle[key] != -1, f"m = {m}, step {step}: remove({key})")
            size -= oracle[key] != -1
            oracle[key] = -1
        else:
            expect(t.get(key), oracle[key], f"m = {m}, step {step}: get({key})")
        expect(t.size(), size, f"m = {m}, step {step}: size()")

# Larger table: 60,000 keys in 100,003 slots (load factor about 0.6).
t = HashTable(100_003)
keys = [i * 7919 for i in range(60_000)]
for k in keys:
    t.put(k, k % 1_000_000)
for k in keys[::2]:
    t.remove(k)
assert t.size() == 30_000, "large table: size after 60,000 puts and 30,000 removes"
assert all(t.get(k) == (-1 if i % 2 == 0 else k % 1_000_000) for i, k in enumerate(keys)), "large table: wrong get"
print("Exercise 2 checks passed (bugs 1 and 2, full and all-DELETED tables, 6,000 random operations, 100,003 slots).")
