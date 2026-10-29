# Recitation 2 — Exercise 3: Merge two sorted arrays

Inputs are non-null arrays of integers in nondecreasing order. Each length is
0–100,000; values are within −1,000,000,000 to 1,000,000,000. Do not validate
sortedness or use library sorting/merging calls in the solution.

Return a newly allocated array containing every occurrence from both inputs, in
nondecreasing order. Do not mutate either input or return an input array directly.
Choose from the left input first on ties (supports stable merging of tagged records).

Time: Θ(n+m) for nonempty total input, Θ(1) when both are empty. Output storage:
Θ(n+m), with O(1) auxiliary working space excluding the output.

- C: `int* mergeSorted(const int* left, int leftSize, const int* right, int rightSize, int* returnSize)`
  Caller supplies a non-null `returnSize`; sizes are nonnegative. A null input pointer
  is permitted only for size zero. Set the result length; return NULL for an empty
  result. Caller frees a nonempty result. On allocation failure return NULL and set
  length to zero. No output pointer may alias an input.
- C++: `std::vector<int> mergeSorted(const std::vector<int>& left, const std::vector<int>& right)`
- C#: `public static int[] MergeSorted(int[] left, int[] right)` in `Solution`.
- Java: `public static int[] mergeSorted(int[] left, int[] right)` in `Solution`.
- Python: `def merge_sorted(left: list[int], right: list[int]) -> list[int]`
- JavaScript: `function mergeSorted(left, right)`; export via `module.exports = { mergeSorted };`.

Harnesses cover empty arrays, one empty side, ties, unequal lengths, negative and
boundary values, deterministic generated cases, output independence, and a
200,000-element interleaved merge. Built-in sorts are permitted only in test oracles.
