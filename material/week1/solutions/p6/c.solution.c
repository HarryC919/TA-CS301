#include <stdlib.h>

// Time: O(n) average, O(n^2) worst case. Space: O(1) extra (nums is reordered in place).
// Average O(n) intuition: each partition costs O(n), and we recurse into only one
// side, so the expected total work is n + n/2 + n/4 + ... = O(n).
// May reorder the caller's array (allowed by the contract).

// Swaps two integer values in place.
static void swapValues(int* first, int* second) {
    int tmp = *first;
    *first = *second;
    *second = tmp;
}

// Partitions nums[left..right] around a random pivot value.
// Returns the pivot's final index: smaller values on the left, larger on the right.
static int partition(int* nums, int left, int right) {
    // 1. Pick a random pivot and move it to the right end
    int offset = rand() % (right - left + 1);
    swapValues(&nums[left + offset], &nums[right]);
    int pivot = nums[right];

    // 2. Move every value smaller than the pivot to the front
    int store = left;
    for (int i = left; i < right; i++) {
        if (nums[i] < pivot) {
            swapValues(&nums[store], &nums[i]);
            store++;
        }
    }

    // 3. Put the pivot between the smaller and larger values
    swapValues(&nums[store], &nums[right]);
    return store;
}

// Quickselect: returns the value that belongs at targetIndex in sorted order.
static int selectValue(int* nums, int left, int right, int targetIndex) {
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

// The kth largest value sits at ascending index numsSize - k.
// Uses rand() for the random pivot; call srand(...) once in main if you want a
// different random sequence on each run.
int findKthLargest(int* nums, int numsSize, int k) {
    int targetIndex = numsSize - k;
    return selectValue(nums, 0, numsSize - 1, targetIndex);
}
