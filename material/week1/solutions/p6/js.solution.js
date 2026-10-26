// Time: O(n) average, O(n^2) worst case. Space: O(n) for the working copy.
// Average O(n) intuition: each partition costs O(n), and we recurse into only one
// side, so the expected total work is n + n/2 + n/4 + ... = O(n).
// The caller's array is left unchanged: quickselect runs on a copy.

// Swaps two positions in the array, in place.
function swapValues(nums, first, second) {
  const tmp = nums[first];
  nums[first] = nums[second];
  nums[second] = tmp;
}

// Partitions nums[left..right] around a random pivot value.
// Returns the pivot's final index: smaller values left, larger values right.
function partition(nums, left, right) {
  // 1. Pick a random pivot and move it to the right end
  const offset = Math.floor(Math.random() * (right - left + 1));
  swapValues(nums, left + offset, right);
  const pivot = nums[right];

  // 2. Move every value smaller than the pivot to the front
  let store = left;
  for (let i = left; i < right; i++) {
    if (nums[i] < pivot) {
      swapValues(nums, store, i);
      store++;
    }
  }

  // 3. Put the pivot between the smaller and larger values
  swapValues(nums, store, right);
  return store;
}

// Quickselect: returns the value that belongs at targetIndex in sorted order.
function selectValue(nums, left, right, targetIndex) {
  const pivotIndex = partition(nums, left, right);
  if (pivotIndex === targetIndex) {
    return nums[pivotIndex];
  }
  if (pivotIndex < targetIndex) {
    // The target lies to the right: recurse only into that side
    return selectValue(nums, pivotIndex + 1, right, targetIndex);
  }
  // The target lies to the left: recurse only into that side
  return selectValue(nums, left, pivotIndex - 1, targetIndex);
}

function findKthLargest(nums, k) {
  // The kth largest value sits at ascending index nums.length - k.
  const working = nums.slice(); // copy so the caller's array is not modified
  const targetIndex = working.length - k;
  return selectValue(working, 0, working.length - 1, targetIndex);
}

module.exports = { findKthLargest };
