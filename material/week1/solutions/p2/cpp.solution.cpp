#include <vector>

// Insertion sort: sorts nums in place and returns the total number of shifts
// (each time an element is moved one position right to make room for the key).
// Time: O(n^2) worst, O(n) best (already sorted). Space: O(1).

int insertionSort(std::vector<int>& nums) {
    int shifts = 0;
    for (std::size_t i = 1; i < nums.size(); i++) {
        int key = nums[i];
        std::size_t j = i;
        // 1. Shift elements greater than the key one position to the right
        while (j > 0 && nums[j - 1] > key) {
            nums[j] = nums[j - 1];
            shifts++;
            j--;
        }
        // 2. Insert the key into the gap
        nums[j] = key;
    }
    return shifts;
}
