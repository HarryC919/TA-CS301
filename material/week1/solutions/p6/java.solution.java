import java.util.Random;

public class Solution {
    // Time: O(n) average, O(n^2) worst case. Space: O(n) for the working copy.
    // Average O(n) intuition: each partition costs O(n), and we recurse into only
    // one side, so the expected total work is n + n/2 + n/4 + ... = O(n).
    private static final Random RANDOM = new Random();

    public static int findKthLargest(int[] nums, int k) {
        // Work on a copy so the caller's array is not modified.
        int[] working = nums.clone();
        int targetIndex = working.length - k;
        return selectValue(working, 0, working.length - 1, targetIndex);
    }

    // Swaps two positions in the array, in place.
    private static void swapValues(int[] nums, int first, int second) {
        int tmp = nums[first];
        nums[first] = nums[second];
        nums[second] = tmp;
    }

    // Partitions nums[left..right] around a random pivot value.
    // Returns the pivot's final index: smaller values left, larger values right.
    private static int partition(int[] nums, int left, int right) {
        // 1. Pick a random pivot and move it to the right end
        int offset = RANDOM.nextInt(right - left + 1);
        swapValues(nums, left + offset, right);
        int pivot = nums[right];

        // 2. Move every value smaller than the pivot to the front
        int store = left;
        for (int i = left; i < right; i++) {
            if (nums[i] < pivot) {
                swapValues(nums, store, i);
                store++;
            }
        }

        // 3. Put the pivot between the smaller and larger values
        swapValues(nums, store, right);
        return store;
    }

    // Quickselect: returns the value that belongs at targetIndex in sorted order.
    private static int selectValue(int[] nums, int left, int right, int targetIndex) {
        int pivotIndex = partition(nums, left, right);
        if (pivotIndex == targetIndex) {
            return nums[pivotIndex];
        }
        if (pivotIndex < targetIndex) {
            // The target lies to the right: recurse only into that side
            return selectValue(nums, pivotIndex + 1, right, targetIndex);
        }
        // The target lies to the left: recurse only into that side
        return selectValue(nums, left, pivotIndex - 1, targetIndex);
    }
}
