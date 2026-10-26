// Insertion sort: sorts nums in place and returns the total number of shifts
// (each time an element is moved one position right to make room for the key).
// Time: O(n^2) worst, O(n) best (already sorted). Space: O(1).
function insertionSort(nums) {
    let shifts = 0;
    for (let i = 1; i < nums.length; i++) {
        const key = nums[i];
        let j = i - 1;
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

module.exports = { insertionSort };
