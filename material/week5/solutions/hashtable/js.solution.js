// Expected O(1 / (1 - alpha)) probes per operation under uniform hashing,
// Theta(m) in the worst case. Space: O(m) for three arrays of length m.
const EMPTY = 0, OCCUPIED = 1, DELETED = 2;

class HashTable {
    constructor(m) {
        // m is a prime >= 3, so every probe sequence visits all m slots.
        this.m = m;
        this.count = 0;
        this.keys = new Array(m).fill(0);
        this.values = new Array(m).fill(0);
        this.state = new Array(m).fill(EMPTY);
    }

    probe(key, i) {
        // Double hashing: h1(k) = k mod m, h2(k) = 1 + (k mod (m - 1)).
        return (key % this.m + i * (1 + key % (this.m - 1))) % this.m;
    }

    put(key, value) {
        let firstDeleted = -1, emptySlot = -1;
        for (let i = 0; i < this.m; i++) {
            const slot = this.probe(key, i);
            if (this.state[slot] === EMPTY) {
                emptySlot = slot;  // the key cannot be stored further along
                break;
            }
            if (this.state[slot] === DELETED) {
                if (firstDeleted === -1) firstDeleted = slot;  // reuse later, keep looking
            } else if (this.keys[slot] === key) {
                this.values[slot] = value;  // update; size is unchanged
                return true;
            }
        }
        const target = firstDeleted !== -1 ? firstDeleted : emptySlot;
        if (target === -1) return false;  // new key, and every slot is OCCUPIED
        this.keys[target] = key;
        this.values[target] = value;
        this.state[target] = OCCUPIED;
        this.count++;
        return true;
    }

    get(key) {
        for (let i = 0; i < this.m; i++) {
            const slot = this.probe(key, i);
            if (this.state[slot] === EMPTY) return -1;  // an EMPTY slot ends the search
            if (this.state[slot] === OCCUPIED && this.keys[slot] === key) return this.values[slot];
        }
        return -1;
    }

    remove(key) {
        for (let i = 0; i < this.m; i++) {
            const slot = this.probe(key, i);
            if (this.state[slot] === EMPTY) return false;
            if (this.state[slot] === OCCUPIED && this.keys[slot] === key) {
                // DELETED, not EMPTY: later keys may have probed past this slot.
                this.state[slot] = DELETED;
                this.count--;
                return true;
            }
        }
        return false;
    }

    size() {
        return this.count;
    }
}
module.exports = { HashTable };
