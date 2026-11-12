// Re-run the Solution definition cell before running this check cell.
// These checks throw while the starter is still unchanged.
final int I = 1_000_000_000;  // INF
Object[][] cases = {
    {4, new int[][]{{0, 1, 3}, {0, 3, 7}, {1, 0, 8}, {1, 2, 2}, {2, 0, 5}, {2, 3, 1}, {3, 0, 2}},
     new int[][]{{0, 3, 5, 6}, {5, 0, 2, 3}, {3, 6, 0, 1}, {2, 5, 7, 0}}, "worked example"},
    {1, new int[0][], new int[][]{{0}}, "one vertex"},
    {3, new int[][]{{0, 1, 4}, {0, 2, 5}, {2, 1, -3}}, new int[][]{{0, 2, 5}, {I, 0, I}, {I, -3, 0}}, "negative edge"},
    {3, new int[][]{{0, 1, 1}}, new int[][]{{0, 1, I}, {I, 0, I}, {I, I, 0}}, "unreachable pairs"},
    {3, new int[][]{{1, 2, -5}}, new int[][]{{0, I, I}, {I, 0, -5}, {I, I, 0}}, "never add to INF"},
    {2, new int[][]{{0, 1, 5}, {0, 1, 2}, {1, 0, 4}}, new int[][]{{0, 2}, {4, 0}}, "parallel edges"},
};
for (Object[] c : cases) {
    int[][] edges = (int[][]) c[1];
    String before = java.util.Arrays.deepToString(edges);
    int[][] result = Solution.floydWarshall((int) c[0], edges);
    if (!java.util.Arrays.deepEquals(result, (int[][]) c[2]))
        throw new AssertionError(c[3] + ": got " + java.util.Arrays.deepToString(result));
    if (!java.util.Arrays.deepToString(edges).equals(before))
        throw new AssertionError(c[3] + ": edges were modified");
}
int n = 200;
java.util.List<int[]> list = new java.util.ArrayList<>();
for (int i = 0; i < n; i++) list.add(new int[]{i, (i + 1) % n, 1});
for (int i = 0; i < n; i++) if ((i * 7 + 3) % n != i) list.add(new int[]{i, (i * 7 + 3) % n, n + i % 5});
int[][] large = Solution.floydWarshall(n, list.toArray(new int[0][]));
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
        if (large[i][j] != ((j - i) % n + n) % n) throw new AssertionError("Check the 200-vertex case");
System.out.println("Floyd-Warshall checks passed (6 cases + 200 vertices).");
