# CS301 Week 1 Exercise Contracts — Single Source of Truth

You are implementing ONE exercise problem for a university course website (CS301, Week 1: Sorting Algorithms). This file defines everything. Follow it exactly — the signatures and contracts here will be printed verbatim on the course website, so they must match character-for-character in behavior and naming.

## Toolchain (all on PATH)

- C: `gcc` (C11)
- C++: `g++` (C++17, use `-std=c++17`)
- C#: `dotnet` CLI (SDK 10 installed; target `net10.0`). Test via a console project: `dotnet new console -o csproj`, add your `Solution.cs`, replace `Program.cs` with the harness, `dotnet run --project csproj`.
- Java: `javac`/`java` (Java 21). Every Java solution/stub declares `public class Solution` but lives in a file named `java.solution.java`, which javac rejects; the test recipe is therefore: `cp java.solution.java Solution.java && javac Solution.java Main.java && java Main && rm Solution.java`.
- Python: `python3` (3.13)
- JS: `node` (v24, CommonJS `require`)

## File layout (per problem, work ONLY inside your assigned directory)

Create and work exclusively inside: `/Users/harry/Desktop/School Stuff/TA-CS301/.tmp/sol/p<N>/` (N = your problem number).

Deliverable files (the website shows exactly these):

- `c.solution.c` — the function ONLY (+ `#include`s it needs). No `main`.
- `cpp.solution.cpp` — the function ONLY (+ includes). No `main`.
- `cs.solution.cs` — `using System;` + `public static class Solution { ... }`. No Main.
- `java.solution.java` — `public class Solution { ... }`. No main.
- `py.solution.py` — the function ONLY. No top-level test code.
- `js.solution.js` — the function + `module.exports = { <fnName> };`
- `*.stub.*` — same 6 languages: the exact signature with a `// TODO: implement ...` body, shown to students as starting templates. Use the canonical format below; **all six problems must look uniform**. Include only the headers/imports the signature needs, and make the TODO name the actual task (e.g. `// TODO: implement count inversions by extending merge sort.`). Stub bodies must at least be syntactically valid.

  C (`c.stub.c`):
  ```c
  // TODO: implement <one-line description>.
  <return-type> <fnName>(<params>) {
      <placeholder, e.g. return 0; — omit for void>
  }
  ```

  C++ (`cpp.stub.cpp`):
  ```cpp
  #include <vector>

  // TODO: implement <one-line description>.
  <return-type> <fnName>(<params>) {
      <placeholder, e.g. return 0; — omit for void>
  }
  ```

  C# (`cs.stub.cs`):
  ```csharp
  using System;

  public static class Solution {
      // TODO: implement <one-line description>.
      public static <return-type> <FnName>(<params>) {
          throw new NotImplementedException();
      }
  }
  ```

  Java (`java.stub.java`):
  ```java
  public class Solution {
      // TODO: implement <one-line description>.
      public static <return-type> <fnName>(<params>) {
          throw new UnsupportedOperationException();
      }
  }
  ```

  Python (`py.stub.py`):
  ```python
  # TODO: implement <one-line description>.
  def <fn_name>(<params>) -> <return-type>:
      pass
  ```

  JS (`js.stub.js`):
  ```js
  // TODO: implement <one-line description>.
  function <fnName>(<params>) {
  }

  module.exports = { <fnName> };
  ```

Test harness files (verification only, never shipped):

- `c.test.c` — contains `int main(void)` that calls the function from `c.solution.c`; compile both together: `gcc -std=c11 -Wall c.solution.c c.test.c -o ctest && ./ctest`
- `cpp.test.cpp` — same pattern: `g++ -std=c++17 -Wall cpp.solution.cpp cpp.test.cpp -o cpptest && ./cpptest`
- `csproj/` — dotnet console project: your `Solution.cs` + `Program.cs` harness (top-level statements). Run: `dotnet run --project csproj`
- `Main.java` — `public class Main` with `main()` that uses `Solution`: `cp java.solution.java Solution.java && javac Solution.java Main.java && java Main && rm Solution.java` (the copy is required because `public class Solution` must live in a file named `Solution.java`).
- `py.test.py` — `from py.solution import <fn_name>` + asserts: `python3 py.test.py`
- `js.test.js` — `require('./js.solution.js')` + asserts: `node js.test.js`

## Code style (the whole point is teaching)

- Beginner-readable: descriptive names, no clever one-liners, no external libraries.
- A short header comment with complexity, e.g. `// Time: O(n^2) worst, O(n) best (early exit). Space: O(1).`
- Comments only where they mark algorithm steps (e.g. `// 1. Compare adjacent pairs`, `// 2. Merge the two halves`).
- Solutions must implement the target algorithm manually — never call a library sort in the solution. (The TEST harness may use library sort as an oracle.)

## Problems

---

### P1 — Bubble Sort with Early Exit (Easy)

**Goal:** classic bubble sort, plus the `swapped`-flag optimization.

**Statement (final, shown on site):**

> Given an integer array `nums`, sort it **in place** in ascending order using bubble sort. Your implementation must include the early-exit optimization: set a `swapped` flag during each pass; if a complete pass makes no swaps, stop immediately (the array is already sorted).
>
> **Example:** `nums = [5,2,4,1,3]` → after the call `nums == [1,2,3,4,5]`. `nums = [1,2,3,4]` → already sorted, your code should stop after one pass.
>
> **Constraints:** 1 ≤ nums.length ≤ 1000; -10⁴ ≤ nums[i] ≤ 10⁴.

**Signatures:**

- C: `void bubbleSort(int* nums, int numsSize)`
- C++: `void bubbleSort(std::vector<int>& nums)` (include `<vector>`)
- C#: `public static void BubbleSort(int[] nums)`
- Java: `public static void bubbleSort(int[] nums)`
- Python: `def bubble_sort(nums: list[int]) -> None`
- JS: `function bubbleSort(nums) { } // sorts in place, returns nothing`

**Test cases:** [1]→[1]; [5,2,4,1,3]→[1,2,3,4,5]; [1,2,3,4]→unchanged; [4,3,2,1]→[1,2,3,4]; [2,2,1,3,2]→[1,2,2,2,3]; [-1,5,0,-10]→[-10,-1,0,5]; plus a seeded-random array of 1000 values cross-checked against the library sort (in-place: copy random into input, sort, compare).

---

### P2 — Insertion Sort: Count the Shifts (Easy)

**Goal:** insertion sort, and count element moves to build the inversion intuition.

**Statement:**

> Sort `nums` **in place** in ascending order using insertion sort, and return the total number of **shifts**. Each time an element is moved one position to the right to make room for the key, that is one shift. (Fact you will prove in Week 2: the total number of shifts equals the number of inversions in the array.)
>
> **Example:** `nums = [5,2,4,1]` → after the call `nums == [1,2,4,5]`, return `5`. Walkthrough: inserting 2 shifts the 5 once (1); inserting 4 shifts the 5 once (2); inserting 1 shifts 5, 4, and 2 (3 more) — total 5.
>
> **Constraints:** 1 ≤ nums.length ≤ 1000; -10⁴ ≤ nums[i] ≤ 10⁴. The result fits in a 32-bit int.

**Signatures:**

- C: `int insertionSort(int* nums, int numsSize)` (sorts in place, returns shift count)
- C++: `int insertionSort(std::vector<int>& nums)`
- C#: `public static int InsertionSort(int[] nums)`
- Java: `public static int insertionSort(int[] nums)`
- Python: `def insertion_sort(nums: list[int]) -> int`
- JS: `function insertionSort(nums) { } // sorts in place, returns shift count`

**Test cases:** [1]→0; [1,2,3]→0; [3,2,1]→3; [5,2,4,1]→5 with final array [1,2,4,5]; [2,2,2]→0 (equal keys must NOT shift: compare with `>`, not `>=`); random arrays of 1000 cross-checked against a brute-force inversion count O(n²) in the harness (max ~5×10⁵ pairs, fast enough).

---

### P3 — Sort by Length, Stably (Easy-Medium)

**Goal:** understand stability; pick and implement a stable sort.

**Statement:**

> Given an array of strings `words`, return a **new array** containing the words sorted by length in ascending order. Words of equal length must keep their original relative order — the sort must be **stable**. Implement the sorting algorithm yourself; do not use built-in sort functions.
>
> **Example:** `words = ["pear","kiwi","apple","fig","banana"]` → `["fig","pear","kiwi","apple","banana"]` ("pear" and "kiwi" both have length 4; "pear" comes first because it appeared first).
>
> **Constraints:** 1 ≤ words.length ≤ 1000; each word is 1–100 lowercase letters.

**Signatures:**

- C: `void sortByLength(char** words, int wordsSize)` — sorts the array of pointers **in place** (note this in the header comment).
- C++: `std::vector<std::string> sortByLength(std::vector<std::string> words)` — takes by value, returns sorted (include `<string>`, `<vector>`)
- C#: `public static string[] SortByLength(string[] words)`
- Java: `public static String[] sortByLength(String[] words)`
- Python: `def sort_by_length(words: list[str]) -> list[str]`
- JS: `function sortByLength(words) { } // return a new sorted array`

**Recommended algorithm:** insertion sort or merge sort (both stable when you only swap on strict inequality). Bubble sort works too. Quicksort is not stable — do not use it here.

**Test cases:** ["pear","kiwi","apple","fig","banana"]→["fig","pear","kiwi","apple","banana"]; ["a"]→["a"]; ["bb","aa","cc"]→["bb","aa","cc"] (all equal length → order preserved); ["ccc","a","bb","ab","ba"]→["a","bb","ab","ba","ccc"] (ties keep original order); ["abcd","a","abc","ab"]→["a","ab","abc","abcd"]; seeded random cross-check vs library stable sort (e.g. Python `sorted(words, key=len)` — the oracle may use library sort; the solution may not).

---

### P4 — Count Inversions (Medium)

**Goal:** the classic merge-sort modification; 64-bit awareness.

**Statement:**

> An **inversion** is a pair of indices `(i, j)` with `i < j` and `nums[i] > nums[j]`. Count the total number of inversions in `nums`. A brute-force O(n²) scan is too slow for the largest tests — the expected solution modifies merge sort to count inversions in O(n log n). The answer can exceed 2³¹, so use a 64-bit integer type.
>
> **Example:** `nums = [8,4,2,1]` → `6` (every pair is an inversion). `nums = [1,20,6,4,5]` → `5` — the inversions are (20,6), (20,4), (20,5), (6,4), (6,5).
>
> **Constraints:** 1 ≤ nums.length ≤ 100,000; -10⁹ ≤ nums[i] ≤ 10⁹. Return 64-bit.

**Signatures:**

- C: `long long countInversions(const int* nums, int numsSize)`
- C++: `long long countInversions(const std::vector<int>& nums)` (copy internally, don't destroy the caller's array)
- C#: `public static long CountInversions(int[] nums)`
- Java: `public static long countInversions(int[] nums)`
- Python: `def count_inversions(nums: list[int]) -> int` (Python ints are unbounded)
- JS: `function countInversions(nums) { } // returns a Number (2^53-safe; max answer here is ~5×10^9)`

**Test cases:** [1]→0; [1,2,3,4]→0; [4,3,2,1]→6; [8,4,2,1]→6; [1,20,6,4,5]→5; [2,2,2]→0 (strict `>`); descending array of 100,000 → 4,999,950,000 (proves 64-bit); seeded random arrays of n ≤ 2000 cross-checked against brute force; one n=100,000 random run for performance (should be instant; recursion depth log n).

---

### P5 — Quick Sort with Random Pivot and Duplicates (Medium)

**Goal:** quicksort done right: random pivot + 3-way partition.

**Statement:**

> Given an integer array `nums`, return a **new array** with the same values in ascending order, implemented as quick sort. Two requirements:
> 1. Choose the pivot **uniformly at random** (e.g. pick a random index and move it to the partition position).
> 2. Use a **3-way partition** (Dutch national flag): after partitioning, elements equal to the pivot are in their final positions, so you recurse only on the `<` and `>` regions. This keeps the sort O(n log n) even on inputs with many duplicate values — a plain 2-way partition degrades to O(n²) on an all-equal array.
>
> Do not modify the input array.
>
> **Example:** `nums = [5,2,4,1,3]` → `[1,2,3,4,5]`. `nums = [3,1,3,3,2,3]` → `[1,2,3,3,3,3]`.
>
> **Constraints:** 0 ≤ nums.length ≤ 100,000; -10⁶ ≤ nums[i] ≤ 10⁶. The tests include arrays with many duplicate values and fully sorted inputs.

**Signatures:**

- C: `int* quickSort(const int* nums, int numsSize, int* returnSize)` — returns a newly `malloc`'d array; note in the comment that the caller frees it. Handle `numsSize == 0` (return `NULL`, set `*returnSize = 0`).
- C++: `std::vector<int> quickSort(const std::vector<int>& nums)`
- C#: `public static int[] QuickSort(int[] nums)`
- Java: `public static int[] quickSort(int[] nums)`
- Python: `def quick_sort(nums: list[int]) -> list[int]`
- JS: `function quickSort(nums) { } // return a new sorted array`

**Test cases:** []→[]; [1]→[1]; [5,2,4,1,3]→[1,2,3,4,5]; [3,1,3,3,2,3]→[1,2,3,3,3,3]; [7,7,7,7]→unchanged (all-equal must be fast); [4,3,2,1]→[1,2,3,4]; [-3,5,0,-3,2]→[-3,-3,0,2,5]; input must not be mutated (check a copy); performance: seeded random n=200,000 with values in [0,50] (heavy duplicates) AND n=200,000 all-equal — both must finish in well under 2 seconds, result cross-checked against library sort.

---

### P6 — Kth Largest Element (Medium+, Quickselect)

**Goal:** order statistics via quickselect; ties into the course topic list.

**Statement:**

> Given an integer array `nums` and an integer `k`, return the **kth largest element** in sorted order (i.e. the element that would be at index `n - k` if the array were sorted ascending). The expected solution is **quickselect**: partition like quicksort, but recurse only into the side that contains the target index. Average time O(n), no full sort needed. (Sorting the whole array works here but defeats the purpose — the hidden tests are sized so an O(n log n) sort passes too, but try quickselect.)
>
> **Example:** `nums = [3,2,1,5,6,4], k = 2` → `5`. `nums = [3,2,3,1,2,4,5,5,6], k = 4` → `4`.
>
> **Constraints:** 1 ≤ k ≤ nums.length ≤ 100,000; -10⁴ ≤ nums[i] ≤ 10⁴.

**Signatures:**

- C: `int findKthLargest(int* nums, int numsSize, int k)` (may modify the input copy as needed; copy first if you want to preserve it)
- C++: `int findKthLargest(const std::vector<int>& nums, int k)`
- C#: `public static int FindKthLargest(int[] nums, int k)`
- Java: `public static int findKthLargest(int[] nums, int k)`
- Python: `def find_kth_largest(nums: list[int], k: int) -> int`
- JS: `function findKthLargest(nums, k) { }`

**Test cases:** [3,2,1,5,6,4] k=2→5; [3,2,3,1,2,4,5,5,6] k=4→4; [1] k=1→1; [2,1] k=1→2, k=2→1; [-1,-5,3] k=1→3; [3,3,3] k=2→3; seeded random n=200,000 cross-checked vs library sort/nth, quick runtime check.

---

## What to report back

End your run with a summary table: `language | status (PASS/FAIL) | notes`. Also flag anything in the contract you had to deviate from (deviations should be none — if a contract seems wrong, re-read it).
