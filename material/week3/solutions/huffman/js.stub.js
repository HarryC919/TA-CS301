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

function huffmanCodes(freq) {
    const n = freq.length;
    if (n === 1) return ['0'];
    // Nodes 0..n-1 are leaves (symbols); nodes n..2n-2 are merged internal nodes.
    const left = new Array(2 * n - 1).fill(-1), right = new Array(2 * n - 1).fill(-1);
    const heap = new MinHeap();
    for (let i = 0; i < n; i++) heap.push([freq[i], i]);
    // TODO: for node = n .. 2n-2, pop the two lightest [weight, node] pairs, record them
    // as this node's children, and push [their total weight, node].
    // TODO: assign codes from the root (node 2n-2) down: left adds '0', right adds '1'.
    // Return the codes of nodes 0..n-1.
}
module.exports = { huffmanCodes };
