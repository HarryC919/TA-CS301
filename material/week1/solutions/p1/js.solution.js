// Time: O(n^2) worst, O(n) best (early exit). Space: O(1).
function bubbleSort(nums) {
  for (let end = nums.length - 1; end > 0; end--) {
    let swapped = false;
    // 1. Compare adjacent pairs, bubbling the largest value to the end
    for (let i = 0; i < end; i++) {
      if (nums[i] > nums[i + 1]) {
        const tmp = nums[i];
        nums[i] = nums[i + 1];
        nums[i + 1] = tmp;
        swapped = true;
      }
    }
    // 2. Early exit: a full pass with no swaps means already sorted
    if (!swapped) {
      break;
    }
  }
}

module.exports = { bubbleSort };
