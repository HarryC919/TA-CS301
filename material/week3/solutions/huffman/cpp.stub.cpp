#include <functional>
#include <queue>
#include <string>
#include <utility>
#include <vector>
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
    // TODO: for node = n .. 2n-2, pop the two lightest trees, record them as
    // this node's children, set its weight, and push it back.
    // TODO: assign codes from the root (node 2n-2) down: left adds "0", right adds "1".
    // Return the codes of nodes 0..n-1.
    return {};
}
