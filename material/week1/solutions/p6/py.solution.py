import random

# Time: O(n) expected with random pivots; O(n^2) worst case.
# Space: O(n) for the copy, O(1) for the iterative selection itself.


def find_kth_largest(nums: list[int], k: int) -> int:
    working = nums[:]
    target = len(working) - k
    left, right = 0, len(working) - 1
    while left < right:
        # 1. Partition into < pivot, == pivot, and > pivot regions.
        pivot = working[random.randint(left, right)]
        lt, i, gt = left, left, right
        while i <= gt:
            if working[i] < pivot:
                working[lt], working[i] = working[i], working[lt]
                lt += 1
                i += 1
            elif working[i] > pivot:
                working[i], working[gt] = working[gt], working[i]
                gt -= 1  # inspect the swapped-in value before advancing i
            else:
                i += 1
        # 2. Keep only the region containing target; skip the entire equal band.
        if target < lt:
            right = lt - 1
        elif target > gt:
            left = gt + 1
        else:
            return pivot
    return working[left]
