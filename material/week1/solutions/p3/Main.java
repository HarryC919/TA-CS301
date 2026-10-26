import java.util.Arrays;
import java.util.Comparator;
import java.util.Random;

// Test harness for P3 (sort words by length, stably). Not shipped to students.
// Compile with: cp java.solution.java Solution.java && javac Solution.java Main.java
public class Main {
    private static int failures = 0;

    // Sorts a copy of `input` with the solution, compares it against `expected`,
    // and checks that the caller's array was left untouched.
    private static void check(String[] input, String[] expected, String name) {
        String[] inputBackup = input.clone();
        String[] got = Solution.sortByLength(input);

        if (!Arrays.equals(input, inputBackup)) {
            System.out.println("FAIL " + name + ": input array was modified");
            failures++;
            return;
        }

        if (!Arrays.equals(got, expected)) {
            System.out.println("FAIL " + name);
            System.out.println("  got  " + Arrays.toString(got));
            System.out.println("  want " + Arrays.toString(expected));
            failures++;
            return;
        }

        System.out.println("PASS " + name);
    }

    // Builds `count` seeded random lowercase words so every run is reproducible.
    private static String[] makeRandomWords(int count, int maxLength, long seed) {
        Random random = new Random(seed);
        String[] words = new String[count];
        for (int i = 0; i < count; i++) {
            int length = 1 + random.nextInt(maxLength);
            StringBuilder word = new StringBuilder();
            for (int k = 0; k < length; k++) {
                word.append((char) ('a' + random.nextInt(26)));
            }
            words[i] = word.toString();
        }
        return words;
    }

    // Cross-checks the solution against a library stable sort. The HARNESS may
    // use a library sort as the oracle; the solution itself may not.
    private static void checkRandom(int count, int maxLength, long seed, String name) {
        String[] words = makeRandomWords(count, maxLength, seed);
        String[] expected = words.clone();
        // Arrays.sort on an object array is stable, so equal lengths keep order.
        Arrays.sort(expected, Comparator.comparingInt(String::length));
        check(words, expected, name);
    }

    public static void main(String[] args) {
        // Fixed cases from the contract.
        check(new String[] {"pear", "kiwi", "apple", "fig", "banana"},
              new String[] {"fig", "pear", "kiwi", "apple", "banana"},
              "case pear/kiwi/apple/fig/banana");
        check(new String[] {"a"}, new String[] {"a"}, "case single word [a]");
        check(new String[] {"bb", "aa", "cc"}, new String[] {"bb", "aa", "cc"},
              "case all equal length (order preserved)");
        check(new String[] {"ccc", "a", "bb", "ab", "ba"},
              new String[] {"a", "bb", "ab", "ba", "ccc"},
              "case ties keep original order");
        check(new String[] {"abcd", "a", "abc", "ab"},
              new String[] {"a", "ab", "abc", "abcd"},
              "case ascending lengths");
        String longest = "q".repeat(100);
        check(new String[] {"a", longest, "bb"}, new String[] {"a", "bb", longest},
              "case word of 100 characters");
        check(new String[] {"b", "a"}, new String[] {"b", "a"},
              "case two equal-length words");

        // Seeded random cross-checks against the library stable-sort oracle.
        checkRandom(1000, 100, 12345L, "random n=1000, lengths 1..100 (seed 12345)");
        checkRandom(1000, 6, 999L, "random n=1000, many ties (lengths 1..6, seed 999)");

        if (failures == 0) {
            System.out.println("ALL TESTS PASSED");
            System.exit(0);
        }
        System.out.println(failures + " TEST(S) FAILED");
        System.exit(1);
    }
}
