#include <vector>
// Time: O(n^3 + m). Space: O(n^2) for the distance matrix.
const int INF = 1000000000;
std::vector<std::vector<int>> floydWarshall(int n, const std::vector<std::vector<int>>& edges) {
    // Base case D_0: direct edges only, 0 on the diagonal, INF elsewhere.
    std::vector<std::vector<int>> D(n, std::vector<int>(n, INF));
    for (int i = 0; i < n; i++) D[i][i] = 0;
    for (const std::vector<int>& e : edges) {
        if (e[2] < D[e[0]][e[1]]) D[e[0]][e[1]] = e[2];  // keep the lightest parallel edge
    }
    // Round k allows vertex k as an intermediate vertex.
    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            if (D[i][k] == INF) continue;  // never add to INF
            for (int j = 0; j < n; j++) {
                // Key math function: go through k, or do not.
                if (D[k][j] != INF && D[i][k] + D[k][j] < D[i][j]) {
                    D[i][j] = D[i][k] + D[k][j];
                }
            }
        }
    }
    return D;
}
