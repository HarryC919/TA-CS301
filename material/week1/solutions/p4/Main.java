import java.util.Arrays;

// Test harness for countInversions.
// Build/run: cp java.solution.java Solution.java && javac Solution.java Main.java && java Main
public class Main {
    private static int failures = 0;
    private static int randomState = 12345;

    public static void main(String[] args) {
        // Fixed cases from the contract.
        check("case [1]", new int[] {1}, 0L);
        check("case [1,2,3,4]", new int[] {1, 2, 3, 4}, 0L);
        check("case [4,3,2,1]", new int[] {4, 3, 2, 1}, 6L);
        check("case [8,4,2,1]", new int[] {8, 4, 2, 1}, 6L);
        check("case [1,20,6,4,5]", new int[] {1, 20, 6, 4, 5}, 5L);
        check("case [2,2,2] (strict >)", new int[] {2, 2, 2}, 0L);

        // Seeded random cross-check against the brute-force answer.
        int[] randomSizes = {1, 2, 3, 5, 10, 50, 300, 2000};
        for (int n : randomSizes) {
            int[] nums = makeRandom(n, -10000, 10000);
            check("random n=" + n + " vs brute force", nums, bruteForce(nums));
        }

        // A descending array of 100,000 elements has n*(n-1)/2 = 4,999,950,000
        // inversions, which does not fit in 32 bits.
        final int largeSize = 100000;
        int[] descending = new int[largeSize];
        for (int i = 0; i < largeSize; i++) {
            descending[i] = largeSize - i;
        }
        check("descending 100,000 (64-bit)", descending, 4999950000L);

        // Performance run on a random array of 100,000 values.
        int[] large = makeRandom(largeSize, -1000000000, 1000000000);
        int[] largeCopy = large.clone();
        long start = System.nanoTime();
        long largeCount = Solution.countInversions(large);
        double seconds = (System.nanoTime() - start) / 1e9;
        if (!Arrays.equals(large, largeCopy)) {
            System.out.println("FAIL perf n=100,000: input array was modified");
            failures++;
        } else if (seconds > 2.0) {
            System.out.println("FAIL perf n=100,000: " + seconds + " s (expected under 2 s)");
            failures++;
        } else {
            System.out.println("PASS perf n=100,000 (" + seconds + " s)");
        }

        // Cross-check the large answer without O(n^2) work: for every pair of
        // different values exactly one of the two orders is an inversion, so
        // count(nums) + count(reverse(nums)) equals the number of unequal pairs.
        int[] reversedLarge = new int[largeSize];
        for (int i = 0; i < largeSize; i++) {
            reversedLarge[i] = large[largeSize - 1 - i];
        }
        long reversedCount = Solution.countInversions(reversedLarge);
        long unequalPairs = unequalPairCount(large);
        if (largeCount + reversedCount == unequalPairs) {
            System.out.println("PASS large random consistency: count + reversed = unequal pairs");
        } else {
            System.out.println("FAIL large random consistency: " + largeCount
                    + " + " + reversedCount + " != " + unequalPairs);
            failures++;
        }

        if (failures == 0) {
            System.out.println("ALL TESTS PASSED");
        } else {
            System.out.println(failures + " TEST(S) FAILED");
            System.exit(1);
        }
    }

    // Verify one answer, and also check that the input array was not modified.
    private static void check(String name, int[] input, long expected) {
        int[] copy = input.clone();
        long got = Solution.countInversions(input);
        if (got != expected) {
            System.out.println("FAIL " + name + ": got " + got + ", want " + expected);
            failures++;
        } else if (!Arrays.equals(input, copy)) {
            System.out.println("FAIL " + name + ": input array was modified");
            failures++;
        } else {
            System.out.println("PASS " + name);
        }
    }

    // Reference answer: O(n^2) double loop, only for small inputs.
    private static long bruteForce(int[] nums) {
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

    // Deterministic pseudo-random generator so every run tests the same data.
    private static int nextRandom() {
        randomState = randomState * 1664525 + 1013904223;
        return randomState;
    }

    private static int[] makeRandom(int n, int minValue, int maxValue) {
        int[] nums = new int[n];
        long range = (long)maxValue - minValue + 1;
        for (int i = 0; i < n; i++) {
            int offset = Math.floorMod(nextRandom(), (int)range);
            nums[i] = (int)((long)minValue + offset);
        }
        return nums;
    }

    // Count pairs with different values; used to check the large random case.
    private static long unequalPairCount(int[] nums) {
        int[] sorted = nums.clone();
        Arrays.sort(sorted);
        long unequalPairs = (long)nums.length * (nums.length - 1) / 2;
        int runStart = 0;
        while (runStart < sorted.length) {
            int runEnd = runStart + 1;
            while (runEnd < sorted.length && sorted[runEnd] == sorted[runStart]) {
                runEnd++;
            }
            long runLength = runEnd - runStart;
            unequalPairs -= runLength * (runLength - 1) / 2;
            runStart = runEnd;
        }
        return unequalPairs;
    }
}
