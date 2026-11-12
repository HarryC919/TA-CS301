public class Solution {
    public static final int INF = 1_000_000_000;

    public static int[][] floydWarshall(int n, int[][] edges) {
        // Base case D_0: 0 on the diagonal, INF elsewhere.
        int[][] D = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) D[i][j] = i == j ? 0 : INF;
        }
        // TODO: load each edge {u, v, w}, keeping the lightest of parallel edges.
        // TODO: for k, then i, then j, apply the key math function in place.
        // Never add to an INF entry.
        throw new UnsupportedOperationException();
    }
}
