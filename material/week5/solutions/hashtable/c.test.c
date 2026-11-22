#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
typedef struct HashTable HashTable;
HashTable* htCreate(int m);
void htFree(HashTable* t);
bool htPut(HashTable* t, int key, int value);
int htGet(const HashTable* t, int key);
bool htRemove(HashTable* t, int key);
int htSize(const HashTable* t);
static int cases = 0;
static unsigned long long seed = 301;
static unsigned next(void) { seed = seed * 6364136223846793005ULL + 1442695040888963407ULL; return (unsigned)(seed >> 33); }
static void expect(long long actual, long long expected, const char* label, int extra) {
    cases++;
    if (actual != expected) {
        fprintf(stderr, "%s (%d): expected %lld, got %lld\n", label, extra, expected, actual);
        exit(1);
    }
}
int main(void) {
    HashTable* t = htCreate(7);
    expect(htGet(t, 3), -1, "get on empty", 0); expect(htRemove(t, 3), false, "remove on empty", 0); expect(htSize(t), 0, "empty size", 0);
    expect(htPut(t, 10, 100), true, "insert", 0); expect(htGet(t, 10), 100, "get after insert", 0); expect(htSize(t), 1, "size 1", 0);
    expect(htPut(t, 10, 111), true, "update", 0); expect(htGet(t, 10), 111, "updated value", 0); expect(htSize(t), 1, "update keeps size", 0);
    expect(htPut(t, 0, 0), true, "key 0, value 0", 0); expect(htGet(t, 0), 0, "value 0 is not absent", 0);
    htFree(t);
    t = htCreate(7);
    htPut(t, 10, 1); htPut(t, 17, 2);
    expect(htRemove(t, 10), true, "remove 10", 0); expect(htGet(t, 17), 2, "tombstone keeps 17 reachable", 0); expect(htGet(t, 10), -1, "10 gone", 0);
    expect(htRemove(t, 10), false, "second remove", 0);
    expect(htPut(t, 17, 3), true, "update 17 past tombstone", 0); expect(htSize(t), 1, "no duplicate", 0);
    expect(htRemove(t, 17), true, "remove 17", 0); expect(htGet(t, 17), -1, "no stale duplicate", 0); expect(htSize(t), 0, "size 0", 0);
    expect(htPut(t, 10, 5), true, "re-insert", 0); expect(htGet(t, 10), 5, "re-inserted value", 0); expect(htSize(t), 1, "size after re-insert", 0);
    htFree(t);
    t = htCreate(11);
    int trace[] = {22, 1, 13, 11, 24, 33};
    for (int i = 0; i < 6; i++) expect(htPut(t, trace[i], trace[i] * 10), true, "trace insert", trace[i]);
    htRemove(t, 11); expect(htGet(t, 33), 330, "Part A: 33 after removing 11", 0);
    htFree(t);
    t = htCreate(5);
    for (int k = 0; k < 5; k++) expect(htPut(t, k * 5, k), true, "fill", k);
    expect(htPut(t, 99, 1), false, "full: new key rejected", 0); expect(htPut(t, 10, 7), true, "full: update allowed", 0);
    expect(htSize(t), 5, "full size", 0); expect(htGet(t, 99), -1, "full: absent key", 0);
    for (int k = 0; k < 5; k++) expect(htRemove(t, k * 5), true, "empty out", k);
    expect(htGet(t, 10), -1, "all tombstones: search stops after m probes", 0); expect(htRemove(t, 3), false, "all tombstones remove", 0);
    expect(htPut(t, 99, 1), true, "all tombstones: insert reuses one", 0); expect(htGet(t, 99), 1, "reused slot", 0);
    htFree(t);
    int ms[] = {3, 5, 7, 11, 13, 101};
    for (int a = 0; a < 6; a++) {
        int m = ms[a], size = 0;
        int* oracle = malloc((size_t)(3 * m) * sizeof(int));
        for (int k = 0; k < 3 * m; k++) oracle[k] = -1;
        t = htCreate(m);
        for (int step = 0; step < 3000; step++) {
            int key = (int)(next() % (unsigned)(3 * m));
            unsigned op = next() % 100;
            if (op < 50) {
                int value = (int)(next() % 1000);
                bool ok = oracle[key] != -1 || size < m;
                expect(htPut(t, key, value), ok, "random put", m);
                if (ok) { if (oracle[key] == -1) size++; oracle[key] = value; }
            } else if (op < 75) {
                expect(htRemove(t, key), oracle[key] != -1, "random remove", m);
                if (oracle[key] != -1) size--;
                oracle[key] = -1;
            } else {
                expect(htGet(t, key), oracle[key], "random get", m);
            }
            expect(htSize(t), size, "random size", m);
        }
        htFree(t);
        free(oracle);
    }
    t = htCreate(100003);
    for (int i = 0; i < 60000; i++) if (!htPut(t, i * 7919, (i * 7919) % 1000000)) { fprintf(stderr, "large put\n"); return 1; }
    for (int i = 0; i < 60000; i++) {
        int k = i * 7919;
        if (htGet(t, k) != k % 1000000 || htGet(t, k + 1) != -1) { fprintf(stderr, "large get\n"); return 1; }
    }
    for (int i = 0; i < 60000; i += 2) if (!htRemove(t, i * 7919)) { fprintf(stderr, "large remove\n"); return 1; }
    for (int i = 0; i < 60000; i++) {
        int k = i * 7919;
        if (htGet(t, k) != (i % 2 == 0 ? -1 : k % 1000000)) { fprintf(stderr, "large get after remove\n"); return 1; }
    }
    expect(htSize(t), 30000, "large size", 0);
    htFree(t);
    printf("ALL WEEK 5 HASHTABLE C TESTS PASSED (%d checks)\n", cases + 3);
    return 0;
}
