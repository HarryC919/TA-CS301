using System;

// Sort by length, stably, using insertion sort.
// Time: O(n^2) worst, O(n) best (already ordered by length). Space: O(n) for the new array.
// Returns a NEW array; the input is never modified. Strict '>' keeps
// equal-length words in their original relative order.
public static class Solution {
    public static string[] SortByLength(string[] words) {
        string[] result = new string[words.Length];
        Array.Copy(words, result, words.Length);

        for (int i = 1; i < result.Length; i++) {
            string key = result[i];
            int j = i - 1;

            // 1. Shift longer words one slot to the right.
            while (j >= 0 && result[j].Length > key.Length) {
                result[j + 1] = result[j];
                j--;
            }

            // 2. Drop the key into the gap.
            result[j + 1] = key;
        }
        return result;
    }
}
