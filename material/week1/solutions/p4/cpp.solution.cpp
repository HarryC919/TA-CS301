// Count inversions in O(n log n) by extending merge sort.
// An inversion is a pair (i, j) with i < j and nums[i] > nums[j].
// Time: O(n log n). Space: O(n) for the work copy and the temp array.
// The caller's vector is not modified: we copy it before sorting.
// The result type is long long (64-bit) because the answer can exceed 2^31.
#include <vector>

// Merge the two sorted halves nums[left..mid] and nums[mid+1..right]
// into nums[left..right], and return the inversions between the halves.
static long long mergeAndCount(std::vector<int>& nums, std::vector<int>& temp,
                               int left, int mid, int right) {
    int leftIndex = left;        // next element of the left half
    int rightIndex = mid + 1;    // next element of the right half
    int writeIndex = left;       // next free slot in temp
    long long inversions = 0;

    while (leftIndex <= mid && rightIndex <= right) {
        if (nums[leftIndex] <= nums[rightIndex]) {
            // The left value is not greater, so it forms no inversion.
            temp[writeIndex] = nums[leftIndex];
            writeIndex++;
            leftIndex++;
        } else {
            // nums[rightIndex] is smaller than every remaining left value,
            // and all of them come before it in the original array.
            inversions += static_cast<long long>(mid - leftIndex + 1);
            temp[writeIndex] = nums[rightIndex];
            writeIndex++;
            rightIndex++;
        }
    }

    // Copy what is left of one half (the other half is already used up).
    while (leftIndex <= mid) {
        temp[writeIndex] = nums[leftIndex];
        writeIndex++;
        leftIndex++;
    }
    while (rightIndex <= right) {
        temp[writeIndex] = nums[rightIndex];
        writeIndex++;
        rightIndex++;
    }

    // Put the merged run back so nums[left..right] is now sorted.
    for (int index = left; index <= right; index++) {
        nums[index] = temp[index];
    }
    return inversions;
}

// Sort nums[left..right] with merge sort, counting inversions on the way.
static long long mergeSort(std::vector<int>& nums, std::vector<int>& temp,
                           int left, int right) {
    if (left >= right) {
        return 0;  // one element (or none) has no inversions
    }
    int mid = left + (right - left) / 2;
    long long inversions = 0;
    inversions += mergeSort(nums, temp, left, mid);            // 1. sort left half
    inversions += mergeSort(nums, temp, mid + 1, right);       // 2. sort right half
    inversions += mergeAndCount(nums, temp, left, mid, right); // 3. merge and count
    return inversions;
}

long long countInversions(const std::vector<int>& nums) {
    if (nums.size() < 2) {
        return 0;
    }

    // Work on a copy so the caller's vector is never changed.
    std::vector<int> work = nums;
    std::vector<int> temp(nums.size());
    return mergeSort(work, temp, 0, static_cast<int>(nums.size()) - 1);
}
