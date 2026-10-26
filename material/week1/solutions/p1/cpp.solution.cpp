#include <vector>

// Time: O(n^2) worst, O(n) best (early exit). Space: O(1).
void bubbleSort(std::vector<int>& nums) {
    for (int end = static_cast<int>(nums.size()) - 1; end > 0; end--) {
        bool swapped = false;
        // 1. Compare adjacent pairs, bubbling the largest value to the end
        for (int i = 0; i < end; i++) {
            if (nums[i] > nums[i + 1]) {
                std::swap(nums[i], nums[i + 1]);
                swapped = true;
            }
        }
        // 2. Early exit: a full pass with no swaps means already sorted
        if (!swapped) {
            break;
        }
    }
}
