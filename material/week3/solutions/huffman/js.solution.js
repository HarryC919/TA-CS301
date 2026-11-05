// Provided helper: a binary min-heap of [weight, node] pairs.
class MinHeap {
    constructor() { this.items = []; }
    get size() { return this.items.length; }
    push(item) {
        const a = this.items;
        a.push(item);
        let i = a.length - 1;
        while (i > 0 && a[(i - 1) >> 1][0] > a[i][0]) {
            [a[i], a[(i - 1) >> 1]] = [a[(i - 1) >> 1], a[i]];
            i = (i - 1) >> 1;
        }
    }
    pop() {
        const a = this.items, top = a[0], last = a.pop();
        if (a.length > 0) {
            a[0] = last;
            let i = 0;
            for (;;) {
                const l = 2 * i + 1, r = l + 1;
                let s = i;
                if (l < a.length && a[l][0] < a[s][0]) s = l;
                if (r < a.length && a[r][0] < a[s][0]) s = r;
                if (s === i) break;
                [a[i], a[s]] = [a[s], a[i]];
                i = s;
            }
        }
        return top;
    }
}

// Time: O(n log n) to build the tree, plus the total code length to write codes.
// Space: O(n) nodes and heap entries, plus the returned code strings.
function huffmanCodes(freq) {
    const n = freq.length;
    if (n === 1) return ['0'];
    // Nodes 0..n-1 are leaves (symbols); nodes n..2n-2 are merged internal nodes.
    const left = new Array(2 * n - 1).fill(-1), right = new Array(2 * n - 1).fill(-1);
    const heap = new MinHeap();
    for (let i = 0; i < n; i++) heap.push([freq[i], i]);
    // Greedy step: merge the two lightest trees, n - 1 times.
    for (let node = n; node < 2 * n - 1; node++) {
        const [w1, a] = heap.pop();
        const [w2, b] = heap.pop();
        left[node] = a;
        right[node] = b;
        heap.push([w1 + w2, node]);
    }
    // Children are created before parents, so walk from the root downwards.
    const code = new Array(2 * n - 1).fill('');
    for (let node = 2 * n - 2; node >= n; node--) {
        code[left[node]] = code[node] + '0';
        code[right[node]] = code[node] + '1';
    }
    return code.slice(0, n);
}
module.exports = { huffmanCodes };
