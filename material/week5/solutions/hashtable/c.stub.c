#include <stdbool.h>
#include <stdlib.h>
enum { EMPTY = 0, OCCUPIED = 1, DELETED = 2 };
typedef struct HashTable {
    int m;
    int count;  // number of OCCUPIED slots
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
    // TODO: for i = 0 .. m - 1, look at slot probe(t, key, i).
    // - OCCUPIED with this key: update the value and return true.
    // - DELETED: remember the first one, but keep probing.
    // - EMPTY: stop probing.
    // Then store the new key in the first DELETED slot if there was one,
    // otherwise in the EMPTY slot (update t->count); return false if neither exists.
    (void)t;
    (void)key;
    (void)value;
    return false;  // placeholder
}

int htGet(const HashTable* t, int key) {
    // TODO: probe until the key is found (return its value) or an EMPTY
    // slot is reached; stop after m probes. Return -1 if absent.
    (void)probe;  // silences an unused-function warning; delete this line
    (void)t;
    (void)key;
    return -1;  // placeholder
}

bool htRemove(HashTable* t, int key) {
    // TODO: find the key as in htGet. Mark its slot DELETED (not EMPTY),
    // update t->count, and return true. Return false if absent.
    (void)t;
    (void)key;
    return false;  // placeholder
}

int htSize(const HashTable* t) {
    return t->count;
}
