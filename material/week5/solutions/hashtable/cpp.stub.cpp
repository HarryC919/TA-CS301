#include <vector>
class HashTable {
public:
    explicit HashTable(int m) : m(m), keys(m), values(m), state(m, EMPTY) {
        // m is a prime >= 3, so every probe sequence visits all m slots.
    }

    bool put(int key, int value) {
        // TODO: for i = 0 .. m - 1, look at slot probe(key, i).
        // - OCCUPIED with this key: update the value and return true.
        // - DELETED: remember the first one, but keep probing.
        // - EMPTY: stop probing.
        // Then store the new key in the first DELETED slot if there was one,
        // otherwise in the EMPTY slot; return false if neither exists.
        (void)key;
        (void)value;
        return false;  // placeholder
    }

    int get(int key) const {
        // TODO: probe until the key is found (return its value) or an EMPTY
        // slot is reached; stop after m probes. Return -1 if absent.
        (void)key;
        return -1;  // placeholder
    }

    bool remove(int key) {
        // TODO: find the key as in get. Mark its slot DELETED (not EMPTY),
        // update count, and return true. Return false if absent.
        (void)key;
        return false;  // placeholder
    }

    int size() const { return count; }

private:
    enum State : unsigned char { EMPTY, OCCUPIED, DELETED };
    int m;
    int count = 0;  // number of OCCUPIED slots
    std::vector<int> keys, values;
    std::vector<State> state;

    int probe(int key, int i) const {
        // Double hashing: h1(k) = k mod m, h2(k) = 1 + (k mod (m - 1)).
        return (int)((key % m + (long long)i * (1 + key % (m - 1))) % m);
    }
};
