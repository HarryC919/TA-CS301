import java.util.Arrays;
import java.util.Random;

// Test harness for P2 - insertion sort counting shifts (verification only).
public class Main {
    private static int failures = 0;

    // Oracle 1 (shift count): brute-force inversion count, O(n^2) - harness only.
    private static long countInversionsBruteForce(int[] nums) {
        long count = 0;
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] > nums[j]) {
                    count++;
                }
            }
        }
        return count;
    }

    private static void checkFixed(String name, int[] input, int[] expected,
                                   int expectedShifts) {
        int[] nums = Arrays.copyOf(input, input.length);
        int shifts = Solution.insertionSort(nums); // in place
        boolean ok = shifts == expectedShifts;
        for (int i = 0; i < nums.length && ok; i++) {
            ok = nums[i] == expected[i];
        }
        if (!ok) {
            System.out.println("FAIL " + name + " (shifts=" + shifts
                    + ", expected=" + expectedShifts + ")");
            failures++;
            return;
        }
        System.out.println("PASS " + name + " (shifts=" + shifts + ")");
    }

    private static void checkRandom(int seed, int n, int valueRange) {
        Random rng = new Random(seed);
        int[] original = new int[n];
        for (int i = 0; i < n; i++) {
            original[i] = rng.nextInt(2 * valueRange + 1) - valueRange;
        }
        long expectedShifts = countInversionsBruteForce(original);
        int[] nums = Arrays.copyOf(original, n);
        int shifts = Solution.insertionSort(nums);
        Arrays.sort(original); // oracle: library sort
        boolean ok = shifts == expectedShifts;
        for (int i = 0; i < n && ok; i++) {
            ok = nums[i] == original[i];
        }
        if (!ok) {
            System.out.println("FAIL random n=" + n + " seed=" + seed
                    + " (shifts=" + shifts + ", expected=" + expectedShifts + ")");
            failures++;
            return;
        }
        System.out.println("PASS random n=" + n + " seed=" + seed
                + " (shifts=" + shifts + ")");
    }

    public static void main(String[] args) {
        // Fixed cases from the contract
        checkFixed("case [1]", new int[] { 1 }, new int[] { 1 }, 0);
        checkFixed("case [1,2,3]", new int[] { 1, 2, 3 }, new int[] { 1, 2, 3 }, 0);
        checkFixed("case [3,2,1]", new int[] { 3, 2, 1 }, new int[] { 1, 2, 3 }, 3);
        checkFixed("case [5,2,4,1]", new int[] { 5, 2, 4, 1 },
                new int[] { 1, 2, 4, 5 }, 5);
        checkFixed("case [2,2,2] equal keys", new int[] { 2, 2, 2 },
                new int[] { 2, 2, 2 }, 0);
        checkFixed("case [-1,5,0,-10] negatives", new int[] { -1, 5, 0, -10 },
                new int[] { -10, -1, 0, 5 }, 4);

        // Seeded random cross-checks: shifts vs brute force, array vs library sort
        checkRandom(42, 1000, 10000);
        checkRandom(7, 1000, 10000);
        checkRandom(1234, 1000, 10000);
        checkRandom(99, 1000, 3); // heavy duplicates: stresses the strict '>' rule

        if (failures > 0) {
            System.out.println(failures + " TEST(S) FAILED");
            System.exit(1);
        }
        System.out.println("ALL TESTS PASSED");
    }
}
