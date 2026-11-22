// Re-run the HashTable definition cell before running this check cell.
// These checks throw while the starter is still unchanged.
java.util.function.BiConsumer<Object[], String> expect = (pair, label) -> {
    if (!pair[0].equals(pair[1]))
        throw new AssertionError(label + ": expected " + pair[1] + ", got " + pair[0]);
};
HashTable t = new HashTable(7);
expect.accept(new Object[]{t.get(3), -1}, "get on an empty table");
expect.accept(new Object[]{t.remove(3), false}, "remove on an empty table");
expect.accept(new Object[]{t.put(10, 100), true}, "insert 10");
expect.accept(new Object[]{t.get(10), 100}, "get after insert");
expect.accept(new Object[]{t.put(10, 111), true}, "update 10");
expect.accept(new Object[]{t.get(10) + "/" + t.size(), "111/1"}, "update changes the value, not the size");
expect.accept(new Object[]{t.put(0, 0), true}, "key 0 with value 0");
expect.accept(new Object[]{t.get(0), 0}, "value 0 is a real value, not 'absent'");

// Bug 1: 10 -> slot 3; 17 collides at slot 3 and goes to slot 2.
t = new HashTable(7);
t.put(10, 1);
t.put(17, 2);
expect.accept(new Object[]{t.remove(10), true}, "remove 10");
expect.accept(new Object[]{t.get(17), 2}, "bug 1: after removing 10, 17 must still be found (use DELETED, not EMPTY)");
expect.accept(new Object[]{t.remove(10), false}, "removing 10 twice");
// Bug 2: slot 3 is now DELETED; 17 is still stored further along in slot 2.
expect.accept(new Object[]{t.put(17, 3), true}, "update 17");
expect.accept(new Object[]{t.size(), 1}, "bug 2: put must not stop at the first DELETED slot and store a duplicate 17");
expect.accept(new Object[]{t.remove(17), true}, "remove 17");
expect.accept(new Object[]{t.get(17), -1}, "bug 2: no stale copy of 17 is left behind");

// Part A table: remove 11, then 33 (probes 0 -> 4 -> 8) must still be found.
t = new HashTable(11);
for (int k : new int[]{22, 1, 13, 11, 24, 33}) t.put(k, k * 10);
t.remove(11);
expect.accept(new Object[]{t.get(33), 330}, "Part A: 33 after removing 11");

// Full table, then a table with only DELETED slots.
t = new HashTable(5);
for (int k = 0; k < 5; k++) expect.accept(new Object[]{t.put(k * 5, k), true}, "fill slot " + k);
expect.accept(new Object[]{t.put(99, 1), false}, "full table: a new key is rejected");
expect.accept(new Object[]{t.put(10, 7), true}, "full table: updating an existing key still works");
for (int k = 0; k < 5; k++) t.remove(k * 5);
expect.accept(new Object[]{t.get(10), -1}, "all slots DELETED: search must stop after m probes");
expect.accept(new Object[]{t.put(99, 1), true}, "all slots DELETED: insert reuses one");
expect.accept(new Object[]{t.get(99) + "/" + t.size(), "1/1"}, "after reusing a DELETED slot");

// Random operations against a direct-address table (keys are small here).
java.util.Random rng = new java.util.Random(301);
for (int m : new int[]{3, 7, 101}) {
    t = new HashTable(m);
    int[] oracle = new int[3 * m];
    java.util.Arrays.fill(oracle, -1);
    int size = 0;
    for (int step = 0; step < 2000; step++) {
        int key = rng.nextInt(3 * m);
        double op = rng.nextDouble();
        String where = "m = " + m + ", step " + step + ": ";
        if (op < 0.5) {
            int value = rng.nextInt(1000);
            boolean ok = oracle[key] != -1 || size < m;
            expect.accept(new Object[]{t.put(key, value), ok}, where + "put(" + key + ", " + value + ")");
            if (ok) { if (oracle[key] == -1) size++; oracle[key] = value; }
        } else if (op < 0.75) {
            expect.accept(new Object[]{t.remove(key), oracle[key] != -1}, where + "remove(" + key + ")");
            if (oracle[key] != -1) size--;
            oracle[key] = -1;
        } else {
            expect.accept(new Object[]{t.get(key), oracle[key]}, where + "get(" + key + ")");
        }
        expect.accept(new Object[]{t.size(), size}, where + "size()");
    }
}

// Larger table: 60,000 keys in 100,003 slots (load factor about 0.6).
t = new HashTable(100003);
for (int i = 0; i < 60000; i++) t.put(i * 7919, (i * 7919) % 1000000);
for (int i = 0; i < 60000; i += 2) t.remove(i * 7919);
if (t.size() != 30000) throw new AssertionError("large table: size after 60,000 puts and 30,000 removes");
for (int i = 0; i < 60000; i++)
    if (t.get(i * 7919) != (i % 2 == 0 ? -1 : (i * 7919) % 1000000)) throw new AssertionError("large table: wrong get");
System.out.println("Exercise 2 checks passed (bugs 1 and 2, full and all-DELETED tables, 6,000 random operations, 100,003 slots).");
