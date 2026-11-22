public class HashTable {
    static final byte EMPTY = 0, OCCUPIED = 1, DELETED = 2;
    private final int m;
    private int count = 0;  // number of OCCUPIED slots
    private final int[] keys, values;
    private final byte[] state;

    public HashTable(int m) {
        // m is a prime >= 3, so every probe sequence visits all m slots.
        this.m = m;
        keys = new int[m];
        values = new int[m];
        state = new byte[m];  // all EMPTY
    }

    private int probe(int key, int i) {
        // Double hashing: h1(k) = k mod m, h2(k) = 1 + (k mod (m - 1)).
        return (int) ((key % m + (long) i * (1 + key % (m - 1))) % m);
    }

    public boolean put(int key, int value) {
        // TODO: for i = 0 .. m - 1, look at slot probe(key, i).
        // - OCCUPIED with this key: update the value and return true.
        // - DELETED: remember the first one, but keep probing.
        // - EMPTY: stop probing.
        // Then store the new key in the first DELETED slot if there was one,
        // otherwise in the EMPTY slot; return false if neither exists.
        throw new UnsupportedOperationException();
    }

    public int get(int key) {
        // TODO: probe until the key is found (return its value) or an EMPTY
        // slot is reached; stop after m probes. Return -1 if absent.
        throw new UnsupportedOperationException();
    }

    public boolean remove(int key) {
        // TODO: find the key as in get. Mark its slot DELETED (not EMPTY),
        // update count, and return true. Return false if absent.
        throw new UnsupportedOperationException();
    }

    public int size() {
        return count;
    }
}
