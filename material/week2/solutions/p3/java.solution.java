// Time: O(n + m). Output: O(n + m). Extra working space: O(1).
public class Solution {
    public static int[] mergeSorted(int[] left, int[] right) {
        int[] result = new int[left.length + right.length];
        int i = 0, j = 0, k = 0;
        // Choose the smaller remaining head; choose left on ties.
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                result[k++] = left[i++];
            } else {
                result[k++] = right[j++];
            }
        }
        // Copy either remaining tail.
        while (i < left.length) result[k++] = left[i++];
        while (j < right.length) result[k++] = right[j++];
        return result;
    }
}
