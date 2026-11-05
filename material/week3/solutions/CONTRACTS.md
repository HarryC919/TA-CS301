# Recitation 3 — code contracts

## Exercise 2: Longest common subsequence (`lcs/`)

Inputs are two non-null strings of 0–1,000 ASCII characters each; comparison is
case-sensitive. Return one longest common subsequence as a new string. Several
answers may be valid; checks compare the length and that the result is a
subsequence of both inputs, not a particular string. The reference traceback
prefers moving up (dropping the last character of `a`) on ties, so it returns
`"BCB"` for `("ABCB", "BDCAB")`. Do not modify the inputs.

Time: Θ(mn). Space: Θ(mn) for the length table (needed for the traceback), plus
the O(min(m, n)) result.

- C: `char* longestCommonSubsequence(const char* a, const char* b)`
  Inputs are non-null and NUL-terminated. Return a newly allocated NUL-terminated
  string (an empty string, not NULL, when the LCS is empty); the caller frees it.
  Return NULL only on allocation failure.
- C++: `std::string longestCommonSubsequence(const std::string& a, const std::string& b)`
- C#: `public static string LongestCommonSubsequence(string a, string b)` in `Solution`.
- Java: `public static String longestCommonSubsequence(String a, String b)` in `Solution`.
- Python: `def longest_common_subsequence(a: str, b: str) -> str`
- JavaScript: `function longestCommonSubsequence(a, b)`; export via `module.exports = { longestCommonSubsequence };`.

Harnesses cover empty inputs, no common character, case sensitivity, identical
strings, one string a subsequence of the other, repeated characters, the worked
examples, 100 deterministic random cases over `{A, B, C}`, and a 1,000 × 1,000
input (`"AB"·500` vs `"BA"·500`, LCS length 999). The harness length oracle is a
separate two-row DP.

## Extra: Huffman coding (`huffman/`)

Input: a non-null array `freq` of n positive integers, 1 ≤ n ≤ 1,000 and each
value 1–1,000,000 (so every merged weight fits in a 32-bit signed integer; the
references use 64-bit weights anyway). Symbol i has frequency `freq[i]`.

Return n code strings over `{'0', '1'}`, where entry i is the code of symbol i.
The codes must be prefix-free and minimize `Σ freq[i] · length(code[i])`. Ties make
the code non-unique; checks verify prefix-freeness and optimal total cost, not
exact strings. With a single symbol, return `["0"]`. Do not modify `freq`.

Time: O(n log n) with a binary heap, plus the total length of the returned codes.
Space: O(n) for the tree and heap, plus the returned codes.

- C: `char** huffmanCodes(const int* freq, int n)`
  Return a newly allocated array of n newly allocated NUL-terminated strings; the
  caller frees each string and then the array. Return NULL on allocation failure
  (after freeing partial work). Starter and reference include a provided `MinHeap`.
- C++: `std::vector<std::string> huffmanCodes(const std::vector<int>& freq)`
- C#: `public static string[] HuffmanCodes(int[] freq)` in `Solution` (`PriorityQueue<int, long>`).
- Java: `public static String[] huffmanCodes(int[] freq)` in `Solution` (`PriorityQueue`).
- Python: `def huffman_codes(freq: list[int]) -> list[str]` (`heapq`).
- JavaScript: `function huffmanCodes(freq)`; export via `module.exports = { huffmanCodes };`.
  Starter and reference include a provided `MinHeap` class.

Harnesses cover one symbol, two equal symbols, all-equal frequencies, the worked
example (cost 224), powers of two (a skewed tree), one dominant symbol, 100
deterministic random cases, and n = 1,000 with frequencies up to 1,000,000. The
cost oracle is the two-queue method on sorted frequencies; library sorts are
used only in harnesses.
