#include <cstdio>
#include <cstdlib>
#include <vector>
#include "cpp.solution.cpp"
static int cases = 0;
static unsigned long long seed = 301;
static unsigned next() { seed = seed * 6364136223846793005ULL + 1442695040888963407ULL; return (unsigned)(seed >> 33); }
static void expect(long long actual, long long expected, const char* label, int extra) {
    cases++;
    if (actual != expected) {
        fprintf(stderr, "%s (%d): expected %lld, got %lld\n", label, extra, expected, actual);
        exit(1);
    }
}
int main() {
    HashTable t(7);
    expect(t.get(3), -1, "get on empty", 0); expect(t.remove(3), false, "remove on empty", 0); expect(t.size(), 0, "empty size", 0);
    expect(t.put(10, 100), true, "insert", 0); expect(t.get(10), 100, "get after insert", 0); expect(t.size(), 1, "size 1", 0);
    expect(t.put(10, 111), true, "update", 0); expect(t.get(10), 111, "updated value", 0); expect(t.size(), 1, "update keeps size", 0);
    expect(t.put(0, 0), true, "key 0, value 0", 0); expect(t.get(0), 0, "value 0 is not absent", 0);
    t = HashTable(7);
    t.put(10, 1); t.put(17, 2);
    expect(t.remove(10), true, "remove 10", 0); expect(t.get(17), 2, "tombstone keeps 17 reachable", 0); expect(t.get(10), -1, "10 gone", 0);
    expect(t.remove(10), false, "second remove", 0);
    expect(t.put(17, 3), true, "update 17 past tombstone", 0); expect(t.size(), 1, "no duplicate", 0);
    expect(t.remove(17), true, "remove 17", 0); expect(t.get(17), -1, "no stale duplicate", 0); expect(t.size(), 0, "size 0", 0);
    expect(t.put(10, 5), true, "re-insert", 0); expect(t.get(10), 5, "re-inserted value", 0); expect(t.size(), 1, "size after re-insert", 0);
    t = HashTable(11);
    int trace[] = {22, 1, 13, 11, 24, 33};
    for (int i = 0; i < 6; i++) expect(t.put(trace[i], trace[i] * 10), true, "trace insert", trace[i]);
    t.remove(11); expect(t.get(33), 330, "Part A: 33 after removing 11", 0);
    t = HashTable(5);
    for (int k = 0; k < 5; k++) expect(t.put(k * 5, k), true, "fill", k);
    expect(t.put(99, 1), false, "full: new key rejected", 0); expect(t.put(10, 7), true, "full: update allowed", 0);
    expect(t.size(), 5, "full size", 0); expect(t.get(99), -1, "full: absent key", 0);
    for (int k = 0; k < 5; k++) expect(t.remove(k * 5), true, "empty out", k);
    expect(t.get(10), -1, "all tombstones: search stops after m probes", 0); expect(t.remove(3), false, "all tombstones remove", 0);
    expect(t.put(99, 1), true, "all tombstones: insert reuses one", 0); expect(t.get(99), 1, "reused slot", 0);
    int ms[] = {3, 5, 7, 11, 13, 101};
    for (int a = 0; a < 6; a++) {
        int m = ms[a], size = 0;
        std::vector<int> oracle(3 * m);
        for (int k = 0; k < 3 * m; k++) oracle[k] = -1;
        t = HashTable(m);
        for (int step = 0; step < 3000; step++) {
            int key = (int)(next() % (unsigned)(3 * m));
            unsigned op = next() % 100;
            if (op < 50) {
                int value = (int)(next() % 1000);
                bool ok = oracle[key] != -1 || size < m;
                expect(t.put(key, value), ok, "random put", m);
                if (ok) { if (oracle[key] == -1) size++; oracle[key] = value; }
            } else if (op < 75) {
                expect(t.remove(key), oracle[key] != -1, "random remove", m);
                if (oracle[key] != -1) size--;
                oracle[key] = -1;
            } else {
                expect(t.get(key), oracle[key], "random get", m);
            }
            expect(t.size(), size, "random size", m);
        }
    }
    t = HashTable(100003);
    for (int i = 0; i < 60000; i++) if (!t.put(i * 7919, (i * 7919) % 1000000)) { fprintf(stderr, "large put\n"); return 1; }
    for (int i = 0; i < 60000; i++) {
        int k = i * 7919;
        if (t.get(k) != k % 1000000 || t.get(k + 1) != -1) { fprintf(stderr, "large get\n"); return 1; }
    }
    for (int i = 0; i < 60000; i += 2) if (!t.remove(i * 7919)) { fprintf(stderr, "large remove\n"); return 1; }
    for (int i = 0; i < 60000; i++) {
        int k = i * 7919;
        if (t.get(k) != (i % 2 == 0 ? -1 : k % 1000000)) { fprintf(stderr, "large get after remove\n"); return 1; }
    }
    expect(t.size(), 30000, "large size", 0);
    printf("ALL WEEK 5 HASHTABLE C++ TESTS PASSED (%d checks)\n", cases + 3);
    return 0;
}
