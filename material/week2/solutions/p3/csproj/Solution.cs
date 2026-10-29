// Time: O(n + m). Output: O(n + m). Extra working space: O(1).
public class Solution {
    public static int[] MergeSorted(int[] left, int[] right) {
        int[] result = new int[left.Length + right.Length];
        int i = 0, j = 0, k = 0;
        // Choose the smaller remaining head; choose left on ties.
        while (i < left.Length && j < right.Length) {
            if (left[i] <= right[j]) {
                result[k++] = left[i++];
            } else {
                result[k++] = right[j++];
            }
        }
        // Copy either remaining tail.
        while (i < left.Length) result[k++] = left[i++];
        while (j < right.Length) result[k++] = right[j++];
        return result;
    }
}
