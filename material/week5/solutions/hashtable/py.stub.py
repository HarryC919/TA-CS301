EMPTY, OCCUPIED, DELETED = 0, 1, 2


class HashTable:
    def __init__(self, m: int):
        # m is a prime >= 3, so every probe sequence visits all m slots.
        self.m = m
        self.count = 0  # number of OCCUPIED slots
        self.keys = [0] * m
        self.values = [0] * m
        self.state = [EMPTY] * m

    def probe(self, key: int, i: int) -> int:
        # Double hashing: h1(k) = k mod m, h2(k) = 1 + (k mod (m - 1)).
        return (key % self.m + i * (1 + key % (self.m - 1))) % self.m

    def put(self, key: int, value: int) -> bool:
        # TODO: for i = 0 .. m - 1, look at slot probe(key, i).
        # - OCCUPIED with this key: update the value and return True.
        # - DELETED: remember the first one, but keep probing.
        # - EMPTY: stop probing.
        # Then store the new key in the first DELETED slot if there was one,
        # otherwise in the EMPTY slot; return False if neither exists.
        pass

    def get(self, key: int) -> int:
        # TODO: probe until the key is found (return its value) or an EMPTY
        # slot is reached; stop after m probes. Return -1 if absent.
        pass

    def remove(self, key: int) -> bool:
        # TODO: find the key as in get. Mark its slot DELETED (not EMPTY),
        # update count, and return True. Return False if absent.
        pass

    def size(self) -> int:
        return self.count
