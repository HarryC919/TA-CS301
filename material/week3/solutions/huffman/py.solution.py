import heapq

# Time: O(n log n) to build the tree, plus the total code length to write codes.
# Space: O(n) nodes and heap entries, plus the returned code strings.
def huffman_codes(freq: list[int]) -> list[str]:
    n = len(freq)
    if n == 1:
        return ["0"]
    # Nodes 0..n-1 are leaves (symbols); nodes n..2n-2 are merged internal nodes.
    weight = freq[:] + [0] * (n - 1)
    left = [-1] * (2 * n - 1)
    right = [-1] * (2 * n - 1)
    heap = [(freq[i], i) for i in range(n)]
    heapq.heapify(heap)
    # Greedy step: merge the two lightest trees, n - 1 times.
    for node in range(n, 2 * n - 1):
        w1, a = heapq.heappop(heap)
        w2, b = heapq.heappop(heap)
        weight[node] = w1 + w2
        left[node], right[node] = a, b
        heapq.heappush(heap, (weight[node], node))
    # Children are created before parents, so walk from the root downwards.
    code = [""] * (2 * n - 1)
    for node in range(2 * n - 2, n - 1, -1):
        code[left[node]] = code[node] + "0"
        code[right[node]] = code[node] + "1"
    return code[:n]
