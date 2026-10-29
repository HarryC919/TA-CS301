# Time: O(n + m). Output: O(n + m). Extra working space: O(1).
def merge_sorted(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0
    # Choose the smaller remaining head; choose left on ties.
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # Copy either remaining tail without changing the inputs.
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result
