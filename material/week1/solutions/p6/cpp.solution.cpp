#include <random>
#include <vector>

// Time: O(n) expected with random pivots; O(n^2) worst case.
// Space: O(n) for the copy, O(1) for iterative selection. Input is unchanged.
static void swapValues(int& first, int& second) {
    int tmp = first;
    first = second;
    second = tmp;
}

int findKthLargest(const std::vector<int>& nums, int k) {
    std::vector<int> working = nums;
    int size = static_cast<int>(working.size());
    static std::mt19937 generator(std::random_device{}());
    int target = size - k;
    int left = 0;
    int right = size - 1;
    while (left < right) {
        // 1. Partition into < pivot, == pivot, and > pivot regions.
        std::uniform_int_distribution<int> indices(left, right);
        int pivot = working[indices(generator)];
        int lt = left;
        int i = left;
        int gt = right;
        while (i <= gt) {
            if (working[i] < pivot) {
                swapValues(working[lt], working[i]);
                lt++;
                i++;
            } else if (working[i] > pivot) {
                swapValues(working[i], working[gt]);
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
