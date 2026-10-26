import java.util.Random;

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
// Returns a NEW array; the caller's array nums is never modified.
public class Solution {
    // One shared random generator for all pivot choices.
    private static final Random RANDOM = new Random();

    public static int[] quickSort(int[] nums) {
        int[] result = nums.clone();  // copy: never modify the caller's array
        if (result.length > 1) {
            quickSortRange(result, 0, result.length - 1);
        }
        return result;
    }

    // Sort arr[left..right] in place.
    private static void quickSortRange(int[] arr, int left, int right) {
        if (left >= right) {
            return;  // 0 or 1 element: already sorted
        }

        // 1. Pick the pivot uniformly at random and move it to position `left`.
        int pivotIndex = left + RANDOM.nextInt(right - left + 1);
        swapValues(arr, left, pivotIndex);
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
                swapValues(arr, lt, i);
                lt++;
                i++;
            } else if (arr[i] > pivot) {
                swapValues(arr, i, gt);
                gt--;
            } else {
                i++;
            }
        }

        // 3. Recurse only on the strictly smaller and strictly larger parts.
        quickSortRange(arr, left, lt - 1);
        quickSortRange(arr, gt + 1, right);
    }

    private static void swapValues(int[] arr, int a, int b) {
        int tmp = arr[a];
        arr[a] = arr[b];
        arr[b] = tmp;
    }
}
