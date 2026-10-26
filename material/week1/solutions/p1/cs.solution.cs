using System;

public static class Solution {
    // Time: O(n^2) worst, O(n) best (early exit). Space: O(1).
    public static void BubbleSort(int[] nums) {
        for (int end = nums.Length - 1; end > 0; end--) {
            bool swapped = false;
            // 1. Compare adjacent pairs, bubbling the largest value to the end
            for (int i = 0; i < end; i++) {
                if (nums[i] > nums[i + 1]) {
                    int temp = nums[i];
                    nums[i] = nums[i + 1];
                    nums[i + 1] = temp;
                    swapped = true;
                }
            }
            // 2. Early exit: a full pass with no swaps means already sorted
            if (!swapped) {
                break;
            }
        }
    }
}
