import random

# Time: O(n) average, O(n^2) worst case. Space: O(n) for the working copy.
# Average O(n) intuition: each partition costs O(n), and we recurse into only one
# side, so the expected total work is n + n/2 + n/4 + ... = O(n).
# The caller's list is left unchanged: quickselect runs on a copy.


def swap_values(nums: list[int], first: int, second: int) -> None:
    # Swaps two positions in the list, in place.
    nums[first], nums[second] = nums[second], nums[first]


def partition(nums: list[int], left: int, right: int) -> int:
    # Partitions nums[left..right] around a random pivot value.
    # Returns the pivot's final index: smaller values left, larger values right.
    # 1. Pick a random pivot and move it to the right end
    pivot_index = random.randint(left, right)
    swap_values(nums, pivot_index, right)
    pivot = nums[right]

    # 2. Move every value smaller than the pivot to the front
    store = left
    for i in range(left, right):
        if nums[i] < pivot:
            swap_values(nums, store, i)
            store += 1

    # 3. Put the pivot between the smaller and larger values
    swap_values(nums, store, right)
    return store


def select_value(nums: list[int], left: int, right: int, target_index: int) -> int:
    # Quickselect: returns the value that belongs at target_index in sorted order.
    pivot_index = partition(nums, left, right)
    if pivot_index == target_index:
        return nums[pivot_index]
    if pivot_index < target_index:
        # The target lies to the right: recurse only into that side
        return select_value(nums, pivot_index + 1, right, target_index)
    # The target lies to the left: recurse only into that side
    return select_value(nums, left, pivot_index - 1, target_index)


def find_kth_largest(nums: list[int], k: int) -> int:
    # The kth largest value sits at ascending index len(nums) - k.
    working = nums[:]  # copy so the caller's list is not modified
    target_index = len(working) - k
    return select_value(working, 0, len(working) - 1, target_index)
