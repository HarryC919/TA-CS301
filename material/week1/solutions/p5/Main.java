import java.util.Arrays;
import java.util.Random;

public class Main {
    private static int failures = 0;
    private static int checks = 0;

    // Return the index of the first difference, or -1 when the arrays are equal.
    private static int firstMismatch(int[] a, int[] b) {
        int n = Math.min(a.length, b.length);
        for (int i = 0; i < n; i++) {
            if (a[i] != b[i]) {
                return i;
            }
        }
        return a.length == b.length ? -1 : n;
    }

    // Check one fixed test case: the result values and that the caller's array
    // was not modified.
    private static void checkSorted(String name, int[] input, int[] expected) {
        checks++;
        int[] inputCopy = input.clone();
        int[] result = Solution.quickSort(input);

        if (result.length != expected.length) {
            System.out.println("FAIL " + name + ": length " + result.length
                    + ", want " + expected.length);
            failures++;
            return;
        }

        int mismatch = firstMismatch(result, expected);
        if (mismatch >= 0) {
            System.out.println("FAIL " + name + ": index " + mismatch + " got "
                    + result[mismatch] + ", want " + expected[mismatch]);
            failures++;
        } else if (!Arrays.equals(input, inputCopy)) {
            System.out.println("FAIL " + name + ": the input array was modified");
            failures++;
        } else {
            System.out.println("PASS " + name);
        }
    }

    // Check one n = 200,000 case: cross-check against Arrays.sort, confirm the
    // input was not modified, and require the sort to finish well under 2 seconds.
    private static void checkPerformance(String name, int[] input) {
        checks++;
        int[] expected = input.clone();
        Arrays.sort(expected);  // library sort as oracle
        int[] inputCopy = input.clone();

        long start = System.nanoTime();
        int[] result = Solution.quickSort(input);
        double seconds = (System.nanoTime() - start) / 1e9;

        if (result.length != expected.length) {
            System.out.println("FAIL " + name + ": length " + result.length
                    + ", want " + expected.length);
            failures++;
            return;
        }

        int mismatch = firstMismatch(result, expected);
        if (mismatch >= 0) {
            System.out.println("FAIL " + name + ": index " + mismatch + " got "
                    + result[mismatch] + ", want " + expected[mismatch]);
            failures++;
        } else if (!Arrays.equals(input, inputCopy)) {
            System.out.println("FAIL " + name + ": the input array was modified");
            failures++;
        } else if (seconds >= 2.0) {
            System.out.println("FAIL " + name + ": " + String.format("%.3f", seconds)
                    + " s is not well under 2 s");
            failures++;
        } else {
            System.out.println("PASS " + name + " (" + String.format("%.3f", seconds) + " s)");
        }
    }

    public static void main(String[] args) {
        // --- Fixed cases from the contract --------------------------------
        checkSorted("[] -> []", new int[0], new int[0]);
        checkSorted("[1] -> [1]", new int[] {1}, new int[] {1});
        checkSorted("[5,2,4,1,3] -> [1,2,3,4,5]",
                new int[] {5, 2, 4, 1, 3}, new int[] {1, 2, 3, 4, 5});
        checkSorted("[3,1,3,3,2,3] -> [1,2,3,3,3,3]",
                new int[] {3, 1, 3, 3, 2, 3}, new int[] {1, 2, 3, 3, 3, 3});
        checkSorted("[7,7,7,7] -> unchanged",
                new int[] {7, 7, 7, 7}, new int[] {7, 7, 7, 7});
        checkSorted("[4,3,2,1] -> [1,2,3,4]",
                new int[] {4, 3, 2, 1}, new int[] {1, 2, 3, 4});
        checkSorted("[-3,5,0,-3,2] -> [-3,-3,0,2,5]",
                new int[] {-3, 5, 0, -3, 2}, new int[] {-3, -3, 0, 2, 5});

        // Seeded random cross-check against Arrays.sort, n = 1000.
        {
            final int n = 1000;
            Random rng = new Random(12345);
            int[] input = new int[n];
            for (int i = 0; i < n; i++) {
                input[i] = rng.nextInt(2000001) - 1000000;
            }
            int[] expected = input.clone();
            Arrays.sort(expected);
            checkSorted("random n=1000 cross-check", input, expected);
        }

        // --- Performance cases, n = 200,000 -------------------------------
        final int n = 200000;
        {
            Random rng = new Random(2024);
            int[] input = new int[n];
            for (int i = 0; i < n; i++) {
                input[i] = rng.nextInt(51);  // values in [0,50]: heavy duplicates
            }
            checkPerformance("n=200000 random values in [0,50]", input);
        }
        {
            int[] input = new int[n];
            Arrays.fill(input, 42);  // all equal
            checkPerformance("n=200000 all-equal", input);
        }
        {
            int[] input = new int[n];
            for (int i = 0; i < n; i++) {
                input[i] = i;  // already sorted (random pivot keeps this fast)
            }
            checkPerformance("n=200000 already sorted", input);
        }

        System.out.println("\n" + checks + " checks, " + failures + " failed");
        if (failures > 0) {
            System.out.println("FAILED");
            System.exit(1);
        }
        System.out.println("All tests passed.");
    }
}
