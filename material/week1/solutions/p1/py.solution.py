# Time: O(n^2) worst, O(n) best (early exit). Space: O(1).
def bubble_sort(nums: list[int]) -> None:
    for end in range(len(nums) - 1, 0, -1):
        swapped = False
        # 1. Compare adjacent pairs, bubbling the largest value to the end
        for i in range(end):
            if nums[i] > nums[i + 1]:
                temp = nums[i]
                nums[i] = nums[i + 1]
                nums[i + 1] = temp
                swapped = True
        # 2. Early exit: a full pass with no swaps means already sorted
        if not swapped:
            break
