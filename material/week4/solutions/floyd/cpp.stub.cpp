#include <vector>
const int INF = 1000000000;
std::vector<std::vector<int>> floydWarshall(int n, const std::vector<std::vector<int>>& edges) {
    // Base case D_0: 0 on the diagonal, INF elsewhere.
    std::vector<std::vector<int>> D(n, std::vector<int>(n, INF));
    for (int i = 0; i < n; i++) D[i][i] = 0;
    // TODO: load each edge {u, v, w}, keeping the lightest of parallel edges.
    // TODO: for k, then i, then j, apply the key math function in place.
    // Never add to an INF entry.
    (void)edges;
    return {};  // placeholder
}
