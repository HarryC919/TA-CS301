def sort_by_length(words: list[str]) -> list[str]:
    """Return a NEW list with the words sorted by length, stably.

    Insertion sort; strict '>' keeps equal-length words in original order.
    Time: O(n^2) worst, O(n) best (already ordered by length). Space: O(n).
    """
    result = list(words)  # copy: the caller's list is never modified

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1

        # 1. Shift longer words one slot to the right.
        while j >= 0 and len(result[j]) > len(key):
            result[j + 1] = result[j]
            j -= 1

        # 2. Drop the key into the gap.
        result[j + 1] = key

    return result
