# Time: O(mn). Space: O(mn) table; output O(min(m, n)).
def longest_common_subsequence(a: str, b: str) -> str:
    m, n = len(a), len(b)
    # L[i][j] = LCS length of a[:i] and b[:j]; row 0 and column 0 stay 0.
    L = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Key math function: match the last characters, or drop one of them.
            if a[i - 1] == b[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    # Trace back from (m, n); prefer moving up on ties.
    chars = []
    i, j = m, n
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            chars.append(a[i - 1])
            i -= 1
            j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    # Characters were collected from the end backwards.
    chars.reverse()
    return "".join(chars)
