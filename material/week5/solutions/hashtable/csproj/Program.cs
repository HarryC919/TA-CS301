using System;
class Program {
    static int cases = 0;
    static void Expect(object actual, object expected, string label) {
        cases++;
        if (!actual.Equals(expected)) throw new Exception(label + ": expected " + expected + ", got " + actual);
    }
    static void Main() {
        HashTable t = new HashTable(7);
        Expect(t.Get(3), -1, "get on empty"); Expect(t.Remove(3), false, "remove on empty"); Expect(t.Size(), 0, "empty size");
        Expect(t.Put(10, 100), true, "insert"); Expect(t.Get(10), 100, "get after insert"); Expect(t.Size(), 1, "size 1");
        Expect(t.Put(10, 111), true, "update"); Expect(t.Get(10), 111, "updated value"); Expect(t.Size(), 1, "update keeps size");
        Expect(t.Put(0, 0), true, "key 0, value 0"); Expect(t.Get(0), 0, "value 0 is not absent");
        t = new HashTable(7);
        t.Put(10, 1); t.Put(17, 2);
        Expect(t.Remove(10), true, "remove 10"); Expect(t.Get(17), 2, "tombstone keeps 17 reachable"); Expect(t.Get(10), -1, "10 gone");
        Expect(t.Remove(10), false, "second remove");
        Expect(t.Put(17, 3), true, "update 17 past tombstone"); Expect(t.Size(), 1, "no duplicate");
        Expect(t.Remove(17), true, "remove 17"); Expect(t.Get(17), -1, "no stale duplicate"); Expect(t.Size(), 0, "size 0");
        Expect(t.Put(10, 5), true, "re-insert"); Expect(t.Get(10), 5, "re-inserted value"); Expect(t.Size(), 1, "size after re-insert");
        t = new HashTable(11);
        foreach (int k in new int[]{22, 1, 13, 11, 24, 33}) Expect(t.Put(k, k * 10), true, "trace insert " + k);
        t.Remove(11); Expect(t.Get(33), 330, "Part A: 33 after removing 11");
        t = new HashTable(5);
        for (int k = 0; k < 5; k++) Expect(t.Put(k * 5, k), true, "fill " + k);
        Expect(t.Put(99, 1), false, "full: new key rejected"); Expect(t.Put(10, 7), true, "full: update allowed");
        Expect(t.Size(), 5, "full size"); Expect(t.Get(99), -1, "full: absent key");
        for (int k = 0; k < 5; k++) Expect(t.Remove(k * 5), true, "empty out " + k);
        Expect(t.Get(10), -1, "all tombstones: search stops after m probes"); Expect(t.Remove(3), false, "all tombstones remove");
        Expect(t.Put(99, 1), true, "all tombstones: insert reuses one"); Expect(t.Get(99), 1, "reused slot");
        var rng = new Random(301);
        foreach (int m in new int[]{3, 5, 7, 11, 13, 101}) {
            t = new HashTable(m);
            int[] oracle = new int[3 * m];
            Array.Fill(oracle, -1);
            int size = 0;
            for (int step = 0; step < 3000; step++) {
                int key = rng.Next(3 * m);
                double op = rng.NextDouble();
                if (op < 0.5) {
                    int value = rng.Next(1000);
                    bool ok = oracle[key] != -1 || size < m;
                    Expect(t.Put(key, value), ok, $"m={m}" + " put " + key);
                    if (ok) { if (oracle[key] == -1) size++; oracle[key] = value; }
                } else if (op < 0.75) {
                    Expect(t.Remove(key), oracle[key] != -1, $"m={m}" + " remove " + key);
                    if (oracle[key] != -1) size--;
                    oracle[key] = -1;
                } else {
                    Expect(t.Get(key), oracle[key], $"m={m}" + " get " + key);
                }
                Expect(t.Size(), size, $"m={m}" + " size");
            }
        }
        t = new HashTable(100003);
        int[] keys = new int[60000];
        for (int i = 0; i < keys.Length; i++) keys[i] = i * 7919;
        foreach (int k in keys) if (!t.Put(k, k % 1000000)) throw new Exception("large put " + k);
        foreach (int k in keys) if (t.Get(k) != k % 1000000 || t.Get(k + 1) != -1) throw new Exception("large get " + k);
        for (int i = 0; i < keys.Length; i += 2) if (!t.Remove(keys[i])) throw new Exception("large remove");
        for (int i = 0; i < keys.Length; i++)
            if (t.Get(keys[i]) != (i % 2 == 0 ? -1 : keys[i] % 1000000)) throw new Exception("large get after remove");
        Expect(t.Size(), 30000, "large size");
        Console.WriteLine("ALL WEEK 5 HASHTABLE C# TESTS PASSED (" + (cases + 3) + " checks)");
    }
}
