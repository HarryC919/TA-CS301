#include <random>
#include <vector>

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
// Returns a NEW vector; the caller's vector nums is never modified.

static void swapValues(int& a, int& b) {
    int tmp = a;
    a = b;
    b = tmp;
}

// Return a uniformly random index in [low, high].
static int randomIndex(int low, int high) {
    static std::mt19937 generator(std::random_device{}());
    std::uniform_int_distribution<int> distribution(low, high);
    return distribution(generator);
}

// Sort arr[left..right] in place.
static void quickSortRange(std::vector<int>& arr, int left, int right) {
    if (left >= right) {
        return;  // 0 or 1 element: already sorted
    }

    // 1. Pick the pivot uniformly at random and move it to position `left`.
    int pivotIndex = randomIndex(left, right);
    swapValues(arr[left], arr[pivotIndex]);
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
            swapValues(arr[lt], arr[i]);
            lt++;
            i++;
        } else if (arr[i] > pivot) {
            swapValues(arr[i], arr[gt]);
            gt--;
        } else {
            i++;
        }
    }

    // 3. Recurse only on the strictly smaller and strictly larger parts.
    quickSortRange(arr, left, lt - 1);
    quickSortRange(arr, gt + 1, right);
}

std::vector<int> quickSort(const std::vector<int>& nums) {
    std::vector<int> result = nums;  // copy: never modify the caller's vector
    if (result.size() > 1) {
        quickSortRange(result, 0, static_cast<int>(result.size()) - 1);
    }
    return result;
}
