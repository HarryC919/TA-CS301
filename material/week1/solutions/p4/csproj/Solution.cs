// Count inversions in O(n log n) by extending merge sort.
// An inversion is a pair (i, j) with i < j and nums[i] > nums[j].
// Time: O(n log n). Space: O(n) for the work copy and the temp array.
// The caller's array is not modified: we copy it before sorting.
// The result type is long (64-bit) because the answer can exceed 2^31.
using System;

public static class Solution
{
    public static long CountInversions(int[] nums)
    {
        if (nums.Length < 2)
        {
            return 0;
        }

        // Work on a copy so the caller's array is never changed.
        int[] work = new int[nums.Length];
        Array.Copy(nums, work, nums.Length);
        int[] temp = new int[nums.Length];
        return MergeSort(work, temp, 0, nums.Length - 1);
    }

    // Sort nums[left..right] with merge sort, counting inversions on the way.
    private static long MergeSort(int[] nums, int[] temp, int left, int right)
    {
        if (left >= right)
        {
            return 0;  // one element (or none) has no inversions
        }
        int mid = left + (right - left) / 2;
        long inversions = 0;
        inversions += MergeSort(nums, temp, left, mid);            // 1. sort left half
        inversions += MergeSort(nums, temp, mid + 1, right);       // 2. sort right half
        inversions += MergeAndCount(nums, temp, left, mid, right); // 3. merge and count
        return inversions;
    }

    // Merge the two sorted halves nums[left..mid] and nums[mid+1..right]
    // into nums[left..right], and return the inversions between the halves.
    private static long MergeAndCount(int[] nums, int[] temp, int left, int mid, int right)
    {
        int leftIndex = left;        // next element of the left half
        int rightIndex = mid + 1;    // next element of the right half
        int writeIndex = left;       // next free slot in temp
        long inversions = 0;

        while (leftIndex <= mid && rightIndex <= right)
        {
            if (nums[leftIndex] <= nums[rightIndex])
            {
                // The left value is not greater, so it forms no inversion.
                temp[writeIndex] = nums[leftIndex];
                writeIndex++;
                leftIndex++;
            }
            else
            {
                // nums[rightIndex] is smaller than every remaining left value,
                // and all of them come before it in the original array.
                inversions += mid - leftIndex + 1;
                temp[writeIndex] = nums[rightIndex];
                writeIndex++;
                rightIndex++;
            }
        }

        // Copy what is left of one half (the other half is already used up).
        while (leftIndex <= mid)
        {
            temp[writeIndex] = nums[leftIndex];
            writeIndex++;
            leftIndex++;
        }
        while (rightIndex <= right)
        {
            temp[writeIndex] = nums[rightIndex];
            writeIndex++;
            rightIndex++;
        }

        // Put the merged run back so nums[left..right] is now sorted.
        for (int index = left; index <= right; index++)
        {
            nums[index] = temp[index];
        }
        return inversions;
    }
}
