// Insertion sort: sorts nums in place and returns the total number of shifts
// (each time an element is moved one position right to make room for the key).
// Time: O(n^2) worst, O(n) best (already sorted). Space: O(1).

int insertionSort(int* nums, int numsSize) {
    int shifts = 0;
    for (int i = 1; i < numsSize; i++) {
        int key = nums[i];
        int j = i - 1;
        // 1. Shift elements greater than the key one position to the right
        while (j >= 0 && nums[j] > key) {
            nums[j + 1] = nums[j];
            shifts++;
            j--;
        }
        // 2. Insert the key into the gap
        nums[j + 1] = key;
    }
    return shifts;
}
