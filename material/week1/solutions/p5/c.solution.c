#include <stdlib.h>

// Time: O(n log n) average, O(n^2) worst (extremely unlikely: the pivot is random).
// Space: O(log n) average recursion depth, plus O(n) for the returned array.
//
// Quick sort with two safeguards:
//   1. The pivot index is chosen uniformly at random, so already-sorted inputs
//      are not the worst case.
//   2. The partition is 3-way (Dutch national flag), so every value equal to the
//      pivot lands in its final position and is never recursed into. That keeps
//      arrays with many duplicates fast instead of degrading to O(n^2).
//
// Returns a NEW array allocated with malloc; the caller owns it and must free() it.
// The input array nums is never modified.

static void swapValues(int* a, int* b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

// Sort arr[left..right] in place.
static void quickSortRange(int* arr, int left, int right) {
    if (left >= right) {
        return;  // 0 or 1 element: already sorted
    }

    // 1. Pick the pivot uniformly at random and move it to position `left`.
    int pivotIndex = left + rand() % (right - left + 1);
    swapValues(&arr[left], &arr[pivotIndex]);
    int pivot = arr[left];

    // 2. 3-way partition (Dutch national flag). When the loop ends:
    //      arr[left..lt-1]  <  pivot
    //      arr[lt..gt]      == pivot  (already in their final positions)
    //      arr[gt+1..right] >  pivot
    int lt = left;
    int i = left;
    int gt = right;
    while (i <= gt) {
        if (arr[i] < pivot) {
            swapValues(&arr[lt], &arr[i]);
            lt++;
            i++;
        } else if (arr[i] > pivot) {
            swapValues(&arr[i], &arr[gt]);
            gt--;
        } else {
            i++;
        }
    }

    // 3. Recurse only on the strictly smaller and strictly larger parts.
    quickSortRange(arr, left, lt - 1);
    quickSortRange(arr, gt + 1, right);
}

int* quickSort(const int* nums, int numsSize, int* returnSize) {
    *returnSize = 0;
    if (numsSize <= 0) {
        return NULL;  // empty input: nothing to sort
    }

    int* result = (int*)malloc((size_t)numsSize * sizeof(int));
    if (result == NULL) {
        return NULL;  // allocation failed
    }

    // Copy the input first so the caller's array is never modified.
    for (int i = 0; i < numsSize; i++) {
        result[i] = nums[i];
    }

    quickSortRange(result, 0, numsSize - 1);
    *returnSize = numsSize;
    return result;
}
