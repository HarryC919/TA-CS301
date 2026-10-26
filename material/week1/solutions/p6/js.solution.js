// Time: O(n) expected with random pivots; O(n^2) worst case.
// Space: O(n) for the copy, O(1) for the iterative selection itself.
function swapValues(nums, first, second) {
  const tmp = nums[first];
  nums[first] = nums[second];
  nums[second] = tmp;
}

function findKthLargest(nums, k) {
  const working = nums.slice();
  const target = working.length - k;
  let left = 0;
  let right = working.length - 1;
  while (left < right) {
    // 1. Partition into < pivot, == pivot, and > pivot regions.
    const pivot = working[left + Math.floor(Math.random() * (right - left + 1))];
    let lt = left;
    let i = left;
    let gt = right;
    while (i <= gt) {
      if (working[i] < pivot) {
        swapValues(working, lt, i);
        lt++;
        i++;
      } else if (working[i] > pivot) {
        swapValues(working, i, gt);
        gt--; // inspect the swapped-in value next
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

module.exports = { findKthLargest };
