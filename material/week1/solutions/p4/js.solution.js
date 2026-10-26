// Count inversions in O(n log n) by extending merge sort.
// An inversion is a pair (i, j) with i < j and nums[i] > nums[j].
// Time: O(n log n). Space: O(n) for the work copy and the temp array.
// The caller's array is not modified: we copy it before sorting.
// Returns a Number. The largest answer here is n * (n - 1) / 2 for
// n = 100,000, which is 4,999,950,000 — well below 2^53, so it is exact.

function countInversions(nums) {
  if (nums.length < 2) {
    return 0;
  }

  // Work on a copy so the caller's array is never changed.
  const work = nums.slice();
  const temp = new Array(nums.length);
  return mergeSort(work, temp, 0, nums.length - 1);
}

// Sort nums[left..right] with merge sort, counting inversions on the way.
function mergeSort(nums, temp, left, right) {
  if (left >= right) {
    return 0; // one element (or none) has no inversions
  }
  const mid = Math.floor((left + right) / 2);
  let inversions = 0;
  inversions += mergeSort(nums, temp, left, mid);            // 1. sort left half
  inversions += mergeSort(nums, temp, mid + 1, right);       // 2. sort right half
  inversions += mergeAndCount(nums, temp, left, mid, right); // 3. merge and count
  return inversions;
}

// Merge the two sorted halves nums[left..mid] and nums[mid+1..right]
// into nums[left..right], and return the inversions between the halves.
function mergeAndCount(nums, temp, left, mid, right) {
  let leftIndex = left;      // next element of the left half
  let rightIndex = mid + 1;  // next element of the right half
  let writeIndex = left;     // next free slot in temp
  let inversions = 0;

  while (leftIndex <= mid && rightIndex <= right) {
    if (nums[leftIndex] <= nums[rightIndex]) {
      // The left value is not greater, so it forms no inversion.
      temp[writeIndex] = nums[leftIndex];
      writeIndex += 1;
      leftIndex += 1;
    } else {
      // nums[rightIndex] is smaller than every remaining left value,
      // and all of them come before it in the original array.
      inversions += mid - leftIndex + 1;
      temp[writeIndex] = nums[rightIndex];
      writeIndex += 1;
      rightIndex += 1;
    }
  }

  // Copy what is left of one half (the other half is already used up).
  while (leftIndex <= mid) {
    temp[writeIndex] = nums[leftIndex];
    writeIndex += 1;
    leftIndex += 1;
  }
  while (rightIndex <= right) {
    temp[writeIndex] = nums[rightIndex];
    writeIndex += 1;
    rightIndex += 1;
  }

  // Put the merged run back so nums[left..right] is now sorted.
  for (let index = left; index <= right; index += 1) {
    nums[index] = temp[index];
  }
  return inversions;
}

module.exports = { countInversions };
