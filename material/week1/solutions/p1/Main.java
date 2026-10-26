import java.util.Arrays;
import java.util.Random;

// Test harness for P1 - bubble sort with early exit (verification only).
public class Main {
    private static int failures = 0;

    private static void check(int[] input, int[] expected, String name) {
        int[] nums = Arrays.copyOf(input, input.length);
        Solution.bubbleSort(nums); // in place
        if (!Arrays.equals(nums, expected)) {
            System.out.println("FAIL " + name + ": got " + Arrays.toString(nums)
                    + ", want " + Arrays.toString(expected));
            failures++;
            return;
        }
        System.out.println("PASS " + name);
    }

    public static void main(String[] args) {
        // Fixed cases from the contract
        check(new int[] { 1 }, new int[] { 1 }, "case [1]");
        check(new int[] { 5, 2, 4, 1, 3 }, new int[] { 1, 2, 3, 4, 5 },
                "case [5,2,4,1,3]");
        check(new int[] { 1, 2, 3, 4 }, new int[] { 1, 2, 3, 4 },
                "case [1,2,3,4] already sorted (early exit)");
        check(new int[] { 4, 3, 2, 1 }, new int[] { 1, 2, 3, 4 },
                "case [4,3,2,1] reverse sorted");
        check(new int[] { 2, 2, 1, 3, 2 }, new int[] { 1, 2, 2, 2, 3 },
                "case [2,2,1,3,2] duplicates");
        check(new int[] { -1, 5, 0, -10 }, new int[] { -10, -1, 0, 5 },
                "case [-1,5,0,-10] negatives");

        // Seeded random cross-check vs library sort, n = 1000
        Random rng = new Random(42);
        int[] data = new int[1000];
        for (int i = 0; i < data.length; i++) {
            data[i] = rng.nextInt(20001) - 10000; // values in [-10000, 10000]
        }
        int[] expected = Arrays.copyOf(data, data.length);
        Arrays.sort(expected); // the harness may use a library sort as the oracle
        int[] nums = Arrays.copyOf(data, data.length);
        Solution.bubbleSort(nums); // in place
        if (!Arrays.equals(nums, expected)) {
            System.out.println("FAIL case random n=1000 vs Arrays.sort");
            failures++;
        } else {
            System.out.println("PASS case random n=1000 vs Arrays.sort");
        }

        if (failures > 0) {
            System.out.println(failures + " TEST(S) FAILED");
            System.exit(1);
        }
        System.out.println("ALL TESTS PASSED");
    }
}
