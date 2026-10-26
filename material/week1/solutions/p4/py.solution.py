# Count inversions in O(n log n) by extending merge sort.
# An inversion is a pair (i, j) with i < j and nums[i] > nums[j].
# Time: O(n log n). Space: O(n) for the work copy and the temp array.
# The caller's list is not modified: we copy it before sorting.
# Python ints are unbounded, so the answer is exact even beyond 64 bits.


def count_inversions(nums: list[int]) -> int:
    if len(nums) < 2:
        return 0

    # Work on a copy so the caller's list is never changed.
    work = nums[:]
    temp = [0] * len(nums)
    return merge_sort(work, temp, 0, len(nums) - 1)


def merge_sort(nums: list[int], temp: list[int], left: int, right: int) -> int:
    # Sort nums[left..right] with merge sort, counting inversions on the way.
    if left >= right:
        return 0  # one element (or none) has no inversions
    mid = (left + right) // 2
    inversions = 0
    inversions += merge_sort(nums, temp, left, mid)             # 1. sort left half
    inversions += merge_sort(nums, temp, mid + 1, right)        # 2. sort right half
    inversions += merge_and_count(nums, temp, left, mid, right) # 3. merge and count
    return inversions


def merge_and_count(nums: list[int], temp: list[int], left: int, mid: int, right: int) -> int:
    # Merge the two sorted halves nums[left..mid] and nums[mid+1..right]
    # into nums[left..right], and return the inversions between the halves.
    left_index = left        # next element of the left half
    right_index = mid + 1    # next element of the right half
    write_index = left       # next free slot in temp
    inversions = 0

    while left_index <= mid and right_index <= right:
        if nums[left_index] <= nums[right_index]:
            # The left value is not greater, so it forms no inversion.
            temp[write_index] = nums[left_index]
            write_index += 1
            left_index += 1
        else:
            # nums[right_index] is smaller than every remaining left value,
            # and all of them come before it in the original array.
            inversions += mid - left_index + 1
            temp[write_index] = nums[right_index]
            write_index += 1
            right_index += 1

    # Copy what is left of one half (the other half is already used up).
    while left_index <= mid:
        temp[write_index] = nums[left_index]
        write_index += 1
        left_index += 1
    while right_index <= right:
        temp[write_index] = nums[right_index]
        write_index += 1
        right_index += 1

    # Put the merged run back so nums[left..right] is now sorted.
    for index in range(left, right + 1):
        nums[index] = temp[index]
    return inversions
