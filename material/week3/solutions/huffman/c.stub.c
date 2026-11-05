#include <stdlib.h>
#include <string.h>
// Provided helper: a binary min-heap of node ids, ordered by weight[id].
typedef struct {
    int* ids;
    int size;
    const long long* weight;
} MinHeap;

static void heapSwap(MinHeap* h, int i, int j) {
    int t = h->ids[i];
    h->ids[i] = h->ids[j];
    h->ids[j] = t;
}

static void heapPush(MinHeap* h, int id) {
    int i = h->size++;
    h->ids[i] = id;
    while (i > 0 && h->weight[h->ids[(i - 1) / 2]] > h->weight[h->ids[i]]) {
        heapSwap(h, i, (i - 1) / 2);
        i = (i - 1) / 2;
    }
}

static int heapPop(MinHeap* h) {
    int top = h->ids[0];
    h->ids[0] = h->ids[--h->size];
    int i = 0;
    for (;;) {
        int l = 2 * i + 1, r = l + 1, s = i;
        if (l < h->size && h->weight[h->ids[l]] < h->weight[h->ids[s]]) s = l;
        if (r < h->size && h->weight[h->ids[r]] < h->weight[h->ids[s]]) s = r;
        if (s == i) return top;
        heapSwap(h, i, s);
        i = s;
    }
}

char** huffmanCodes(const int* freq, int n) {
    // TODO: return a malloc'd array of n malloc'd strings ("0" when n == 1).
    // Suggested arrays for nodes 0..2n-2: weight (long long), parent, depth,
    // and bit ('0' left child, '1' right child); plus n ints for the heap:
    //     MinHeap heap = {ids, 0, weight};
    // Push every leaf, then for node = n .. 2n-2 pop two, merge, and push node.
    // Compute depths from the root down, then write each leaf's bits from the back.
    // On allocation failure, free everything and return NULL.
    return NULL;
}
