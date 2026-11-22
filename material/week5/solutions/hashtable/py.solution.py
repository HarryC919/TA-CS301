# Expected O(1 / (1 - alpha)) probes per operation under uniform hashing,
# Theta(m) in the worst case. Space: O(m) for three arrays of length m.
EMPTY, OCCUPIED, DELETED = 0, 1, 2


class HashTable:
    def __init__(self, m: int):
        # m is a prime >= 3, so every probe sequence visits all m slots.
        self.m = m
        self.count = 0
        self.keys = [0] * m
        self.values = [0] * m
        self.state = [EMPTY] * m

    def probe(self, key: int, i: int) -> int:
        # Double hashing: h1(k) = k mod m, h2(k) = 1 + (k mod (m - 1)).
        return (key % self.m + i * (1 + key % (self.m - 1))) % self.m

    def put(self, key: int, value: int) -> bool:
        first_deleted = -1
        for i in range(self.m):
            slot = self.probe(key, i)
            if self.state[slot] == EMPTY:
                break  # the key cannot be stored further along
            if self.state[slot] == DELETED:
                if first_deleted == -1:
                    first_deleted = slot  # reuse later, but keep looking for key
            elif self.keys[slot] == key:
                self.values[slot] = value  # update; size is unchanged
                return True
        else:
            slot = -1  # m probes and no EMPTY slot
        if first_deleted != -1:
            slot = first_deleted
        if slot == -1:
            return False  # new key, and every slot is OCCUPIED
        self.keys[slot], self.values[slot], self.state[slot] = key, value, OCCUPIED
        self.count += 1
        return True

    def get(self, key: int) -> int:
        for i in range(self.m):
            slot = self.probe(key, i)
            if self.state[slot] == EMPTY:
                return -1  # an EMPTY slot ends every probe sequence through it
            if self.state[slot] == OCCUPIED and self.keys[slot] == key:
                return self.values[slot]
        return -1

    def remove(self, key: int) -> bool:
        for i in range(self.m):
            slot = self.probe(key, i)
            if self.state[slot] == EMPTY:
                return False
            if self.state[slot] == OCCUPIED and self.keys[slot] == key:
                # DELETED, not EMPTY: later keys may have probed past this slot.
                self.state[slot] = DELETED
                self.count -= 1
                return True
        return False

    def size(self) -> int:
        return self.count
