import java.util.Random;
public class Main {
    static int cases = 0;
    static void expect(Object actual, Object expected, String label) {
        cases++;
        if (!actual.equals(expected)) throw new AssertionError(label + ": expected " + expected + ", got " + actual);
    }
    public static void main(String[] args) {
        HashTable t = new HashTable(7);
        expect(t.get(3), -1, "get on empty"); expect(t.remove(3), false, "remove on empty"); expect(t.size(), 0, "empty size");
        expect(t.put(10, 100), true, "insert"); expect(t.get(10), 100, "get after insert"); expect(t.size(), 1, "size 1");
        expect(t.put(10, 111), true, "update"); expect(t.get(10), 111, "updated value"); expect(t.size(), 1, "update keeps size");
        expect(t.put(0, 0), true, "key 0, value 0"); expect(t.get(0), 0, "value 0 is not absent");
        t = new HashTable(7);
        t.put(10, 1); t.put(17, 2);
        expect(t.remove(10), true, "remove 10"); expect(t.get(17), 2, "tombstone keeps 17 reachable"); expect(t.get(10), -1, "10 gone");
        expect(t.remove(10), false, "second remove");
        expect(t.put(17, 3), true, "update 17 past tombstone"); expect(t.size(), 1, "no duplicate");
        expect(t.remove(17), true, "remove 17"); expect(t.get(17), -1, "no stale duplicate"); expect(t.size(), 0, "size 0");
        expect(t.put(10, 5), true, "re-insert"); expect(t.get(10), 5, "re-inserted value"); expect(t.size(), 1, "size after re-insert");
        t = new HashTable(11);
        for (int k : new int[]{22, 1, 13, 11, 24, 33}) expect(t.put(k, k * 10), true, "trace insert " + k);
        t.remove(11); expect(t.get(33), 330, "Part A: 33 after removing 11");
        t = new HashTable(5);
        for (int k = 0; k < 5; k++) expect(t.put(k * 5, k), true, "fill " + k);
        expect(t.put(99, 1), false, "full: new key rejected"); expect(t.put(10, 7), true, "full: update allowed");
        expect(t.size(), 5, "full size"); expect(t.get(99), -1, "full: absent key");
        for (int k = 0; k < 5; k++) expect(t.remove(k * 5), true, "empty out " + k);
        expect(t.get(10), -1, "all tombstones: search stops after m probes"); expect(t.remove(3), false, "all tombstones remove");
        expect(t.put(99, 1), true, "all tombstones: insert reuses one"); expect(t.get(99), 1, "reused slot");
        Random rng = new Random(301);
        for (int m : new int[]{3, 5, 7, 11, 13, 101}) {
            t = new HashTable(m);
            int[] oracle = new int[3 * m];
            java.util.Arrays.fill(oracle, -1);
            int size = 0;
            for (int step = 0; step < 3000; step++) {
                int key = rng.nextInt(3 * m);
                double op = rng.nextDouble();
                if (op < 0.5) {
                    int value = rng.nextInt(1000);
                    boolean ok = oracle[key] != -1 || size < m;
                    expect(t.put(key, value), ok, "m=" + m + " put " + key);
                    if (ok) { if (oracle[key] == -1) size++; oracle[key] = value; }
                } else if (op < 0.75) {
                    expect(t.remove(key), oracle[key] != -1, "m=" + m + " remove " + key);
                    if (oracle[key] != -1) size--;
                    oracle[key] = -1;
                } else {
                    expect(t.get(key), oracle[key], "m=" + m + " get " + key);
                }
                expect(t.size(), size, "m=" + m + " size");
            }
        }
        int m = 100003;
        t = new HashTable(m);
        int[] keys = new int[60000];
        for (int i = 0; i < keys.length; i++) keys[i] = i * 7919;
        for (int k : keys) if (!t.put(k, k % 1000000)) throw new AssertionError("large put " + k);
        for (int k : keys) if (t.get(k) != k % 1000000 || t.get(k + 1) != -1) throw new AssertionError("large get " + k);
        for (int i = 0; i < keys.length; i += 2) if (!t.remove(keys[i])) throw new AssertionError("large remove");
        for (int i = 0; i < keys.length; i++)
            if (t.get(keys[i]) != (i % 2 == 0 ? -1 : keys[i] % 1000000)) throw new AssertionError("large get after remove");
        expect(t.size(), 30000, "large size");
        System.out.println("ALL WEEK 5 HASHTABLE JAVA TESTS PASSED (" + (cases + 3) + " checks)");
    }
}
