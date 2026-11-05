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

// Time: O(n log n) to build the tree, plus the total code length to write codes.
// Space: O(n) nodes and heap entries, plus the returned code strings.
char** huffmanCodes(const int* freq, int n) {
    char** codes = calloc((size_t)n, sizeof(char*));
    if (codes == NULL) return NULL;
    if (n == 1) {
        codes[0] = malloc(2);
        if (codes[0] == NULL) {
            free(codes);
            return NULL;
        }
        strcpy(codes[0], "0");
        return codes;
    }
    // Nodes 0..n-1 are leaves (symbols); nodes n..2n-2 are merged internal nodes.
    int total = 2 * n - 1;
    long long* weight = malloc((size_t)total * sizeof(long long));
    int* parent = malloc((size_t)total * sizeof(int));
    int* depth = malloc((size_t)total * sizeof(int));
    char* bit = malloc((size_t)total);  // '0' for a left child, '1' for a right child
    int* ids = malloc((size_t)n * sizeof(int));
    if (weight == NULL || parent == NULL || depth == NULL || bit == NULL || ids == NULL) goto fail;
    MinHeap heap = {ids, 0, weight};
    for (int i = 0; i < n; i++) {
        weight[i] = freq[i];
        heapPush(&heap, i);
    }
    // Greedy step: merge the two lightest trees, n - 1 times.
    for (int node = n; node < total; node++) {
        int a = heapPop(&heap), b = heapPop(&heap);
        weight[node] = weight[a] + weight[b];
        parent[a] = node;
        parent[b] = node;
        bit[a] = '0';
        bit[b] = '1';
        heapPush(&heap, node);
    }
    // Parents are created after children, so walk from the root downwards.
    depth[total - 1] = 0;
    for (int node = total - 2; node >= 0; node--) depth[node] = depth[parent[node]] + 1;
    // Each leaf's code is the path of bits from the root; write it from the back.
    for (int i = 0; i < n; i++) {
        codes[i] = malloc((size_t)depth[i] + 1);
        if (codes[i] == NULL) goto fail;
        codes[i][depth[i]] = '\0';
        int v = i;
        for (int k = depth[i] - 1; k >= 0; k--) {
            codes[i][k] = bit[v];
            v = parent[v];
        }
    }
    free(weight); free(parent); free(depth); free(bit); free(ids);
    return codes;
fail:
    for (int i = 0; i < n; i++) free(codes[i]);
    free(codes);
    free(weight); free(parent); free(depth); free(bit); free(ids);
    return NULL;
}
