import random

# Time: O(n log n) average, O(n^2) worst (extremely unlikely: the pivot is random).
# Space: O(log n) average recursion depth, plus O(n) for the returned array.
#
# Quick sort with two safeguards:
#   1. The pivot index is chosen uniformly at random, so already-sorted inputs
#      are not the worst case.
#   2. The partition is 3-way (Dutch national flag), so every value equal to the
#      pivot lands in its final position and is never recursed into. That keeps
#      arrays with many duplicates fast instead of degrading to O(n^2).
#
# Returns a NEW list; the caller's list nums is never modified.


def quick_sort(nums: list[int]) -> list[int]:
    result = list(nums)  # copy: never modify the caller's list
    if len(result) > 1:
        _quick_sort_range(result, 0, len(result) - 1)
    return result


# Sort arr[left..right] in place.
def _quick_sort_range(arr: list[int], left: int, right: int) -> None:
    if left >= right:
        return  # 0 or 1 element: already sorted

    # 1. Pick the pivot uniformly at random and move it to position `left`.
    pivot_index = random.randint(left, right)
    arr[left], arr[pivot_index] = arr[pivot_index], arr[left]
    pivot = arr[left]

    # 2. 3-way partition (Dutch national flag). When the loop ends:
    #      arr[left..lt-1]  <  pivot
    #      arr[lt..gt]      == pivot  (already in their final positions)
    #      arr[gt+1..right] >  pivot
    lt = left
    i = left
    gt = right
    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1

    # 3. Recurse only on the strictly smaller and strictly larger parts.
    _quick_sort_range(arr, left, lt - 1)
    _quick_sort_range(arr, gt + 1, right)
