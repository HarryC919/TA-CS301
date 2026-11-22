// Expected O(1 / (1 - alpha)) probes per operation under uniform hashing,
// Theta(m) in the worst case. Space: O(m) for three arrays of length m.
#include <stdbool.h>
#include <stdlib.h>
enum { EMPTY = 0, OCCUPIED = 1, DELETED = 2 };
typedef struct HashTable {
    int m;
    int count;
    int* keys;
    int* values;
    unsigned char* state;
} HashTable;

HashTable* htCreate(int m) {
    // m is a prime >= 3, so every probe sequence visits all m slots.
    HashTable* t = malloc(sizeof(HashTable));
    if (t == NULL) return NULL;
    t->m = m;
    t->count = 0;
    t->keys = calloc((size_t)m, sizeof(int));
    t->values = calloc((size_t)m, sizeof(int));
    t->state = calloc((size_t)m, 1);  // all EMPTY
    if (t->keys == NULL || t->values == NULL || t->state == NULL) {
        free(t->keys);
        free(t->values);
        free(t->state);
        free(t);
        return NULL;
    }
    return t;
}

void htFree(HashTable* t) {
    if (t == NULL) return;
    free(t->keys);
    free(t->values);
    free(t->state);
    free(t);
}

static int probe(const HashTable* t, int key, int i) {
    // Double hashing: h1(k) = k mod m, h2(k) = 1 + (k mod (m - 1)).
    return (int)((key % t->m + (long long)i * (1 + key % (t->m - 1))) % t->m);
}

bool htPut(HashTable* t, int key, int value) {
    int firstDeleted = -1, emptySlot = -1;
    for (int i = 0; i < t->m; i++) {
        int slot = probe(t, key, i);
        if (t->state[slot] == EMPTY) {
            emptySlot = slot;  // the key cannot be stored further along
            break;
        }
        if (t->state[slot] == DELETED) {
            if (firstDeleted == -1) firstDeleted = slot;  // reuse later, keep looking
        } else if (t->keys[slot] == key) {
            t->values[slot] = value;  // update; size is unchanged
            return true;
        }
    }
    int target = firstDeleted != -1 ? firstDeleted : emptySlot;
    if (target == -1) return false;  // new key, and every slot is OCCUPIED
    t->keys[target] = key;
    t->values[target] = value;
    t->state[target] = OCCUPIED;
    t->count++;
    return true;
}

int htGet(const HashTable* t, int key) {
    for (int i = 0; i < t->m; i++) {
        int slot = probe(t, key, i);
        if (t->state[slot] == EMPTY) return -1;  // an EMPTY slot ends the search
        if (t->state[slot] == OCCUPIED && t->keys[slot] == key) return t->values[slot];
    }
    return -1;
}

bool htRemove(HashTable* t, int key) {
    for (int i = 0; i < t->m; i++) {
        int slot = probe(t, key, i);
        if (t->state[slot] == EMPTY) return false;
        if (t->state[slot] == OCCUPIED && t->keys[slot] == key) {
            // DELETED, not EMPTY: later keys may have probed past this slot.
            t->state[slot] = DELETED;
            t->count--;
            return true;
        }
    }
    return false;
}

int htSize(const HashTable* t) {
    return t->count;
}
