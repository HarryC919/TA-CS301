const EMPTY = 0, OCCUPIED = 1, DELETED = 2;

class HashTable {
    constructor(m) {
        // m is a prime >= 3, so every probe sequence visits all m slots.
        this.m = m;
        this.count = 0;  // number of OCCUPIED slots
        this.keys = new Array(m).fill(0);
        this.values = new Array(m).fill(0);
        this.state = new Array(m).fill(EMPTY);
    }

    probe(key, i) {
        // Double hashing: h1(k) = k mod m, h2(k) = 1 + (k mod (m - 1)).
        return (key % this.m + i * (1 + key % (this.m - 1))) % this.m;
    }

    put(key, value) {
        // TODO: for i = 0 .. m - 1, look at slot this.probe(key, i).
        // - OCCUPIED with this key: update the value and return true.
        // - DELETED: remember the first one, but keep probing.
        // - EMPTY: stop probing.
        // Then store the new key in the first DELETED slot if there was one,
        // otherwise in the EMPTY slot; return false if neither exists.
    }

    get(key) {
        // TODO: probe until the key is found (return its value) or an EMPTY
        // slot is reached; stop after m probes. Return -1 if absent.
    }

    remove(key) {
        // TODO: find the key as in get. Mark its slot DELETED (not EMPTY),
        // update this.count, and return true. Return false if absent.
    }

    size() {
        return this.count;
    }
}
module.exports = { HashTable };
