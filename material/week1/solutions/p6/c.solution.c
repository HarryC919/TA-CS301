#include <stdlib.h>

// Time: O(n) expected with random pivots; O(n^2) worst case.
// Space: O(1); may reorder the input, as allowed by the contract.
static void swapValues(int* first, int* second) {
    int tmp = *first;
    *first = *second;
    *second = tmp;
}

int findKthLargest(int* nums, int numsSize, int k) {
    int* working = nums;
    int size = numsSize;
    int target = size - k;
    int left = 0;
    int right = size - 1;
    while (left < right) {
        // 1. Partition into < pivot, == pivot, and > pivot regions.
        // Reject the short remainder so each index has equal probability.
        unsigned int width = (unsigned int)(right - left + 1);
        unsigned int range = (unsigned int)RAND_MAX + 1U;
        unsigned int limit = range - range % width;
        unsigned int draw;
        do { draw = (unsigned int)rand(); } while (draw >= limit);
        int pivot = working[left + (int)(draw % width)];
        int lt = left;
        int i = left;
        int gt = right;
        while (i <= gt) {
            if (working[i] < pivot) {
                swapValues(&working[lt], &working[i]);
                lt++;
                i++;
            } else if (working[i] > pivot) {
                swapValues(&working[i], &working[gt]);
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
