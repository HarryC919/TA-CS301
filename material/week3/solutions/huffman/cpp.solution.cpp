#include <functional>
#include <queue>
#include <string>
#include <utility>
#include <vector>
// Time: O(n log n) to build the tree, plus the total code length to write codes.
// Space: O(n) nodes and heap entries, plus the returned code strings.
std::vector<std::string> huffmanCodes(const std::vector<int>& freq) {
    int n = (int)freq.size();
    if (n == 1) return {"0"};
    // Nodes 0..n-1 are leaves (symbols); nodes n..2n-2 are merged internal nodes.
    std::vector<long long> weight(2 * n - 1, 0);
    std::vector<int> left(2 * n - 1, -1), right(2 * n - 1, -1);
    // Min-heap of (weight, node).
    std::priority_queue<std::pair<long long, int>, std::vector<std::pair<long long, int>>,
                        std::greater<std::pair<long long, int>>> heap;
    for (int i = 0; i < n; i++) {
        weight[i] = freq[i];
        heap.push({weight[i], i});
    }
    // Greedy step: merge the two lightest trees, n - 1 times.
    for (int node = n; node < 2 * n - 1; node++) {
        int a = heap.top().second; heap.pop();
        int b = heap.top().second; heap.pop();
        weight[node] = weight[a] + weight[b];
        left[node] = a;
        right[node] = b;
        heap.push({weight[node], node});
    }
    // Children are created before parents, so walk from the root downwards.
    std::vector<std::string> code(2 * n - 1);
    for (int node = 2 * n - 2; node >= n; node--) {
        code[left[node]] = code[node] + "0";
        code[right[node]] = code[node] + "1";
    }
    code.resize(n);
    return code;
}
