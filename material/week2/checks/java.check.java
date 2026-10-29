import java.util.Arrays;

// Re-run the Solution definition cell before running this check cell.
// These checks throw while the starter is still unchanged.
int[][][] cases = {
    {{}, {}, {}},
    {{}, {-2, 5}, {-2, 5}},
    {{1, 2}, {}, {1, 2}},
    {{1, 4, 9}, {2, 2, 3, 10}, {1, 2, 2, 3, 4, 9, 10}},
    {{2, 2}, {2}, {2, 2, 2}},
    {{-1000000000, 0}, {0, 1000000000}, {-1000000000, 0, 0, 1000000000}}
};
for (int[][] test : cases) {
    int[] left = test[0], right = test[1];
    int[] beforeLeft = left.clone(), beforeRight = right.clone();
    int[] result = Solution.mergeSorted(left, right);
    if (!Arrays.equals(result, test[2])) throw new AssertionError("Wrong merge result");
    if (!Arrays.equals(left, beforeLeft) || !Arrays.equals(right, beforeRight))
        throw new AssertionError("Inputs must not change");
    if (result == left || result == right) throw new AssertionError("Return a new array");
    if (result.length > 0) result[0] = 123456789;
    if (!Arrays.equals(left, beforeLeft) || !Arrays.equals(right, beforeRight))
        throw new AssertionError("Result must be independent");
}
int[] even = new int[100000], odd = new int[100000];
for (int i = 0; i < even.length; i++) { even[i] = 2 * i; odd[i] = 2 * i + 1; }
int[] large = Solution.mergeSorted(even, odd);
if (large.length != 200000) throw new AssertionError("Wrong result length");
for (int i = 0; i < large.length; i++) {
    if (large[i] != i) throw new AssertionError("Check the long interleaved merge");
}
System.out.println("Exercise 3 checks passed (6 edge cases + 200,000-element merge).");
