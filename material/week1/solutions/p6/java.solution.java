import java.util.Random;

public class Solution {
    private static final Random RANDOM = new Random();

    // Time: O(n) expected with random pivots; O(n^2) worst case.
    // Space: O(n) for the copy, O(1) for the iterative selection itself.
    public static int findKthLargest(int[] nums, int k) {
        int[] working = nums.clone();
        int target = working.length - k;
        int left = 0;
        int right = working.length - 1;
        while (left < right) {
            // 1. Partition into < pivot, == pivot, and > pivot regions.
            int pivot = working[left + RANDOM.nextInt(right - left + 1)];
            int lt = left;
            int i = left;
            int gt = right;
            while (i <= gt) {
                if (working[i] < pivot) {
                    swapValues(working, lt, i);
                    lt++;
                    i++;
                } else if (working[i] > pivot) {
                    swapValues(working, i, gt);
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

    private static void swapValues(int[] nums, int first, int second) {
        int tmp = nums[first];
        nums[first] = nums[second];
        nums[second] = tmp;
    }
}
