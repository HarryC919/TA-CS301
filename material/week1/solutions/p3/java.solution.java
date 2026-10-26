// Sort by length, stably, using insertion sort.
// Time: O(n^2) worst, O(n) best (already ordered by length).
// Space: O(n) for the new array. Returns a NEW array; the input is never modified.
// Strict '>' (not '>=') keeps equal-length words in their original relative order.
public class Solution {
    public static String[] sortByLength(String[] words) {
        String[] result = words.clone();

        for (int i = 1; i < result.length; i++) {
            String key = result[i];
            int j = i - 1;

            // 1. Shift longer words one slot to the right.
            //    Strict '>' keeps equal-length words in their original order.
            while (j >= 0 && result[j].length() > key.length()) {
                result[j + 1] = result[j];
                j--;
            }

            // 2. Drop the key into the gap.
            result[j + 1] = key;
        }
        return result;
    }
}
