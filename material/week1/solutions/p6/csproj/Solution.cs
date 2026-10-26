using System;

public static class Solution {

    // Time: O(n) expected with random pivots; O(n^2) worst case.
    // Space: O(n) for the copy, O(1) for the iterative selection itself.
    public static int FindKthLargest(int[] nums, int k) {
        int[] working = (int[])nums.Clone();
        int target = working.Length - k;
        int left = 0;
        int right = working.Length - 1;
        while (left < right) {
            // 1. Partition into < pivot, == pivot, and > pivot regions.
            int pivot = working[left + Random.Shared.Next(right - left + 1)];
            int lt = left;
            int i = left;
            int gt = right;
            while (i <= gt) {
                if (working[i] < pivot) {
                    SwapValues(working, lt, i);
                    lt++;
                    i++;
                } else if (working[i] > pivot) {
                    SwapValues(working, i, gt);
                    gt--;  // inspect the swapped-in value before advancing i
                } else {
                    i++;
                }
            }
            // 2. Keep only the region containing target; skip the entire equal band.
            if (target < lt) {
                right = lt - 1;
            } else if (target > gt) {
                left = gt + 1;
            } else {
                return pivot;
            }
        }
        return working[left];
    }

    private static void SwapValues(int[] nums, int first, int second) {
        int tmp = nums[first];
        nums[first] = nums[second];
        nums[second] = tmp;
    }
}
