// Time: O(n^2) worst, O(n) best (early exit). Space: O(1).
void bubbleSort(int* nums, int numsSize) {
    for (int end = numsSize - 1; end > 0; end--) {
        int swapped = 0;
        // 1. Compare adjacent pairs, bubbling the largest value to the end
        for (int i = 0; i < end; i++) {
            if (nums[i] > nums[i + 1]) {
                int tmp = nums[i];
                nums[i] = nums[i + 1];
                nums[i + 1] = tmp;
                swapped = 1;
            }
        }
        // 2. Early exit: a full pass with no swaps means already sorted
        if (!swapped) {
            break;
        }
    }
}
