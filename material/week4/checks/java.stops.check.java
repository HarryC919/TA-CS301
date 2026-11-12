// Re-run the Solution definition cell before running this check cell.
// These checks throw while the starter is still unchanged.
int[][] sample = {{0, 1, 100}, {1, 2, 100}, {2, 0, 100}, {1, 3, 600}, {2, 3, 200}};
int[][] trap = {{0, 1, 100}, {1, 2, 100}, {0, 2, 500}};
int[][] chain = {{0, 1, 1}, {1, 2, 1}, {2, 3, 1}};
Object[][] cases = {
    {4, sample, 0, 3, 1, 700, "sample, k = 1"},
    {4, sample, 0, 3, 2, 400, "sample, k = 2"},
    {4, sample, 0, 0, 0, 0, "src == dst"},
    {3, trap, 0, 2, 0, 500, "in-place trap: one round must not chain two flights"},
    {3, trap, 0, 2, 1, 200, "trap, k = 1"},
    {3, new int[][]{{0, 1, 5}}, 0, 2, 2, -1, "unreachable destination"},
    {4, chain, 0, 3, 1, -1, "route needs too many stops"},
    {4, chain, 0, 3, 2, 3, "chain, k = 2"},
    {2, new int[][]{{0, 1, 7}, {0, 1, 3}}, 0, 1, 0, 3, "parallel flights"},
    {3, new int[][]{{0, 1, 1}, {1, 0, 1}, {1, 2, 10}}, 0, 2, 2, 11, "cycle"},
    {3, new int[][]{{0, 1, 0}, {1, 2, 0}}, 0, 2, 1, 0, "zero prices"},
};
for (Object[] c : cases) {
    int[][] flights = (int[][]) c[1];
    String before = java.util.Arrays.deepToString(flights);
    int result = Solution.cheapestRoute((int) c[0], flights, (int) c[2], (int) c[3], (int) c[4]);
    if (result != (int) c[5])
        throw new AssertionError(c[6] + ": expected " + c[5] + ", got " + result);
    if (!java.util.Arrays.deepToString(flights).equals(before))
        throw new AssertionError(c[6] + ": flights were modified");
}
int[][] large = new int[100 * 99][];
int index = 0;
for (int u = 0; u < 100; u++)
    for (int v = 0; v < 100; v++)
        if (u != v) large[index++] = new int[]{u, v, (u * 37 + v * 91) % 10001};
if (Solution.cheapestRoute(100, large, 0, 99, 99) != 2464)
    throw new AssertionError("Check the 100-city, 9,900-flight case");
System.out.println("Exercise 3 checks passed (11 cases + 100 cities, 9,900 flights, k = 99).");
