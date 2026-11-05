def longest_common_subsequence(a: str, b: str) -> str:
    m, n = len(a), len(b)
    # L[i][j] = LCS length of a[:i] and b[:j]; row 0 and column 0 stay 0.
    L = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # TODO: fill L[i][j] with the key math function.
            # L uses prefix lengths; the last characters are a[i - 1] and b[j - 1].
            pass
    # TODO: trace back from (m, n) and return one LCS as a string.
    pass
