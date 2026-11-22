// Expected O(1 / (1 - alpha)) probes per operation under uniform hashing,
// Theta(m) in the worst case. Space: O(m) for three arrays of length m.
#include <vector>
class HashTable {
public:
    explicit HashTable(int m) : m(m), keys(m), values(m), state(m, EMPTY) {
        // m is a prime >= 3, so every probe sequence visits all m slots.
    }

    bool put(int key, int value) {
        int firstDeleted = -1, emptySlot = -1;
        for (int i = 0; i < m; i++) {
            int slot = probe(key, i);
            if (state[slot] == EMPTY) {
                emptySlot = slot;  // the key cannot be stored further along
                break;
            }
            if (state[slot] == DELETED) {
                if (firstDeleted == -1) firstDeleted = slot;  // reuse later, keep looking
            } else if (keys[slot] == key) {
                values[slot] = value;  // update; size is unchanged
                return true;
            }
        }
        int target = firstDeleted != -1 ? firstDeleted : emptySlot;
        if (target == -1) return false;  // new key, and every slot is OCCUPIED
        keys[target] = key;
        values[target] = value;
        state[target] = OCCUPIED;
        count++;
        return true;
    }

    int get(int key) const {
        for (int i = 0; i < m; i++) {
            int slot = probe(key, i);
            if (state[slot] == EMPTY) return -1;  // an EMPTY slot ends the search
            if (state[slot] == OCCUPIED && keys[slot] == key) return values[slot];
        }
        return -1;
    }

    bool remove(int key) {
        for (int i = 0; i < m; i++) {
            int slot = probe(key, i);
            if (state[slot] == EMPTY) return false;
            if (state[slot] == OCCUPIED && keys[slot] == key) {
                // DELETED, not EMPTY: later keys may have probed past this slot.
                state[slot] = DELETED;
                count--;
                return true;
            }
        }
        return false;
    }

    int size() const { return count; }

private:
    enum State : unsigned char { EMPTY, OCCUPIED, DELETED };
    int m;
    int count = 0;
    std::vector<int> keys, values;
    std::vector<State> state;

    int probe(int key, int i) const {
        // Double hashing: h1(k) = k mod m, h2(k) = 1 + (k mod (m - 1)).
        return (int)((key % m + (long long)i * (1 + key % (m - 1))) % m);
    }
};
