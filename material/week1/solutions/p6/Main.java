import java.util.Arrays;
import java.util.Random;

public class Main {
    private static int failures = 0;

    // Wrapper that compares one quickselect call against the expected answer.
    private static void check(int[] nums, int k, int expected, String name) {
        int got = Solution.findKthLargest(nums, k);
        if (got != expected) {
            System.out.println("FAIL " + name + " (k=" + k + "): got " + got
                    + ", want " + expected);
            failures++;
        } else {
            System.out.println("PASS " + name + " (k=" + k + " -> " + got + ")");
        }
    }

    public static void main(String[] args) {
        // Fixed cases from the contract
        check(new int[] {3, 2, 1, 5, 6, 4}, 2, 5, "case [3,2,1,5,6,4]");
        check(new int[] {3, 2, 3, 1, 2, 4, 5, 5, 6}, 4, 4, "case [3,2,3,1,2,4,5,5,6]");
        check(new int[] {1}, 1, 1, "case [1]");
        check(new int[] {2, 1}, 1, 2, "case [2,1] k=1");
        check(new int[] {2, 1}, 2, 1, "case [2,1] k=2");
        check(new int[] {-1, -5, 3}, 1, 3, "case [-1,-5,3]");
        check(new int[] {3, 3, 3}, 2, 3, "case [3,3,3]");

        // Seeded random cross-check against Arrays.sort, n = 200,000
        int n = 200000;
        Random rng = new Random(42);
        int[] data = new int[n];
        for (int i = 0; i < n; i++) {
            data[i] = rng.nextInt(20001) - 10000;  // values in [-10000, 10000]
        }
        int[] sorted = data.clone();
        Arrays.sort(sorted);

        int[] ks = {1, n / 2, n};
        for (int k : ks) {
            int[] copy = data.clone();
            long start = System.nanoTime();
            int got = Solution.findKthLargest(copy, k);
            double elapsedMs = (System.nanoTime() - start) / 1_000_000.0;
            int expected = sorted[n - k];
            if (got != expected) {
                System.out.println("FAIL random n=200000 k=" + k + ": got " + got
                        + ", want " + expected);
                failures++;
            } else if (elapsedMs > 2000.0) {
                System.out.printf("FAIL random n=200000 k=%d: too slow (%.1f ms)%n", k,
                        elapsedMs);
                failures++;
            } else {
                System.out.printf("PASS random n=200000 k=%d -> %d (%.1f ms)%n", k, got,
                        elapsedMs);
            }
        }

        if (failures == 0) {
            System.out.println("ALL TESTS PASSED");
            return;
        }
        System.out.println(failures + " TEST(S) FAILED");
        System.exit(1);
    }
}
