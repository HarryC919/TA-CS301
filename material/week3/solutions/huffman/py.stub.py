import heapq

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
    # TODO: for node = n .. 2n-2, pop the two lightest trees, record them as
    # this node's children, set its weight, and push it back.
    # TODO: assign codes from the root (node 2n-2) down: left adds "0", right adds "1".
    # Return the codes of nodes 0..n-1.
    pass
