// Time: O(n^3 + m). Space: O(n^2) for the distance matrix.
public class Solution {
    public const int INF = 1_000_000_000;

    public static int[][] FloydWarshall(int n, int[][] edges) {
        // Base case D_0: direct edges only, 0 on the diagonal, INF elsewhere.
        int[][] D = new int[n][];
        for (int i = 0; i < n; i++) {
            D[i] = new int[n];
            for (int j = 0; j < n; j++) D[i][j] = i == j ? 0 : INF;
        }
        foreach (int[] e in edges) {
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
}
