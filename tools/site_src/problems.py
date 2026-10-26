"""Content for the Week 1 exercises page (COMPSCI 301).

This module is build-time only: `build_exercises.py` renders it into
`site/week1-exercises.html`. The published site has no build step.

Prose fields are trusted HTML fragments authored by the TA (they may contain
`<code>` markup). Reference solutions and starter templates are read from
`.tmp/sol/p<N>/` and HTML-escaped by the builder.
"""

LANGS = [
    ("c", "C", "c"),
    ("cpp", "C++", "cpp"),
    ("cs", "C#", "cs"),
    ("java", "Java", "java"),
    ("py", "Python", "py"),
    ("js", "JavaScript", "js"),
]

DEFAULT_LANG = "java"

PROBLEMS = [
    {
        "number": 1,
        "slug": "problem-1",
        "title": "Bubble Sort with Early Exit",
        "difficulty": "Easy",
        "difficulty_class": "easy",
        "topics": ["Bubble sort", "Early exit", "In place"],
        "statement": [
            "Given an integer array <code>nums</code>, sort it <strong>in place</strong> in ascending order using bubble sort.",
            "Your implementation must include the early-exit optimization: track whether any swap happened during a pass. "
            "If a full pass makes no swaps, the array is already sorted, so stop immediately.",
        ],
        "examples": [
            {
                "label": "Example 1",
                "input": "nums = [5, 2, 4, 1, 3]",
                "output": "nums = [1, 2, 3, 4, 5]",
                "explanation": "After the call the array is sorted in place; the function returns nothing.",
            },
            {
                "label": "Example 2",
                "input": "nums = [1, 2, 3, 4]",
                "output": "nums = [1, 2, 3, 4]",
                "explanation": "Already sorted: the first pass makes no swaps, so the loop exits after one pass. This is the O(n) best case.",
            },
        ],
        "constraints": [
            "1 &le; <code>nums.length</code> &le; 1000",
            "-10<sup>4</sup> &le; <code>nums[i]</code> &le; 10<sup>4</sup>",
            "Sort in place, in ascending order. The function returns nothing.",
            "Do not use a built-in sort.",
        ],
        "sig_note": "The array is sorted in place in all six languages &mdash; the caller observes the result through the input array.",
        "hints": [
            "Compare adjacent pairs: for each pass, walk <code>j</code> from <code>0</code> to <code>n - 1 - pass</code> and swap <code>nums[j]</code> with <code>nums[j+1]</code> whenever they are out of order.",
            "Reset an <code>swapped</code> flag to <code>false</code> at the start of every pass, set it to <code>true</code> whenever you swap, and stop as soon as a pass finishes with no swaps.",
            "An already-sorted array must take a single pass. If your loop always runs the full n&nbsp;&minus;&nbsp;1 passes, the early exit is not wired up correctly.",
        ],
        "notes_anchor": "bubble-sort",
        "notes_label": "Bubble sort",
    },
    {
        "number": 2,
        "slug": "problem-2",
        "title": "Insertion Sort: Count the Shifts",
        "difficulty": "Easy",
        "difficulty_class": "easy",
        "topics": ["Insertion sort", "Adaptive sorting", "Counting"],
        "statement": [
            "Sort <code>nums</code> <strong>in place</strong> in ascending order using insertion sort, then return the total number of "
            "<strong>shifts</strong> performed.",
            "A shift is one element moving one position to the right to make room for the key. In the inner loop, each element you "
            "pass over and move right counts as one shift. Compare with strict <code>&gt;</code> so that equal elements are never shifted.",
            "The total number of shifts is exactly the number of inversions in the array (the argument is sketched on the notes page).",
        ],
        "examples": [
            {
                "label": "Example 1",
                "input": "nums = [5, 2, 4, 1]",
                "output": "return 5 (and nums = [1, 2, 4, 5])",
                "explanation": "Insert 2: 5 shifts once (1). Insert 4: 5 shifts once (2). Insert 1: 5, 4, and 2 each shift once (5 in total).",
            },
            {
                "label": "Example 2",
                "input": "nums = [1, 2, 3]",
                "output": "return 0",
                "explanation": "Already sorted: nothing ever shifts.",
            },
            {
                "label": "Example 3",
                "input": "nums = [2, 2, 2]",
                "output": "return 0",
                "explanation": "Equal keys do not count as out of order, so nothing shifts.",
            },
        ],
        "constraints": [
            "1 &le; <code>nums.length</code> &le; 1000",
            "-10<sup>4</sup> &le; <code>nums[i]</code> &le; 10<sup>4</sup>",
            "The shift count fits in a 32-bit integer.",
            "Sort in place. Do not use a built-in sort.",
        ],
        "sig_note": "The return value is the shift count; the sorted order is observed through the modified input array.",
        "hints": [
            "Keep a sorted prefix <code>nums[0..i-1]</code>. For each <code>nums[i]</code>, save it as <code>key</code>, shift every larger element one step right, then put <code>key</code> into the hole.",
            "Count one shift per element moved right &mdash; that is, inside the inner loop, not once per insertion.",
            "Use <code>nums[j-1] &gt; key</code>, not <code>&gt;=</code>. With <code>&gt;=</code>, the all-equal array shifts every element and returns 6 instead of 0.",
        ],
        "notes_anchor": "insertion-sort",
        "notes_label": "Insertion sort",
    },
    {
        "number": 3,
        "slug": "problem-3",
        "title": "Stable Sort by Word Length",
        "difficulty": "Easy&ndash;Medium",
        "difficulty_class": "easy",
        "topics": ["Stability", "Insertion sort", "Merge sort"],
        "statement": [
            "Given an array of strings <code>words</code>, return a new array containing the words sorted by length in ascending order.",
            "Words of equal length must keep their original relative order &mdash; the sort must be <strong>stable</strong>. Implement the "
            "sorting yourself; built-in sort functions are not allowed.",
            "Insertion sort stays stable if you shift only elements strictly greater than the key; merge sort stays stable if the merge "
            "takes from the left half on a tie. Quick sort is not "
            "stable, so do not use it here. In C the function sorts the given array of pointers in place; in the other five languages it "
            "returns a sorted array.",
        ],
        "examples": [
            {
                "label": "Example 1",
                "input": 'words = ["pear", "kiwi", "apple", "fig", "banana"]',
                "output": '["fig", "pear", "kiwi", "apple", "banana"]',
                "explanation": "Lengths are 3, 4, 5, 6. \u201cpear\u201d and \u201ckiwi\u201d are both length 4, and \u201cpear\u201d came first, so it stays first.",
            },
            {
                "label": "Example 2",
                "input": 'words = ["bb", "aa", "cc"]',
                "output": '["bb", "aa", "cc"]',
                "explanation": "All words have length 2, so a stable sort changes nothing.",
            },
            {
                "label": "Example 3",
                "input": 'words = ["ccc", "a", "bb", "ab", "ba"]',
                "output": '["a", "bb", "ab", "ba", "ccc"]',
                "explanation": "\u201cab\u201d and \u201cba\u201d are both length 2 and keep their original order.",
            },
        ],
        "constraints": [
            "1 &le; <code>words.length</code> &le; 1000",
            "Each word is 1&ndash;100 lowercase English letters.",
            "The sort must be stable. Do not use a built-in sort.",
        ],
        "sig_note": "C sorts the pointer array in place and returns nothing; the other five languages return the sorted array.",
        "hints": [
            "Insertion sort: move each word left past every word that is <em>longer</em>, stopping at a shorter or equal-length neighbour. Equal-length words therefore never jump over each other.",
            "Merge sort: when the two fronts have equal length, take the one from the left half. That single <code>&lt;=</code> comparison is what makes the merge stable.",
            "Test Example 3 carefully: the three length-2 words must stay in their original order, so compare lengths only and never the strings themselves.",
        ],
        "notes_anchor": "stability",
        "notes_label": "Stability",
    },
    {
        "number": 4,
        "slug": "problem-4",
        "title": "Count Inversions",
        "difficulty": "Medium",
        "difficulty_class": "medium",
        "topics": ["Merge sort", "Counting", "64-bit integers"],
        "statement": [
            "An <strong>inversion</strong> is a pair of indices <code>(i, j)</code> with <code>i &lt; j</code> and <code>nums[i] &gt; nums[j]</code>. "
            "Return the total number of inversions in <code>nums</code>.",
            "A brute-force double loop is O(n<sup>2</sup>), which is too slow for the largest tests. The expected solution modifies merge "
            "sort to count inversions while merging, in O(n log n).",
            "The answer can exceed 2<sup>31</sup>, so use a 64-bit integer type (<code>long long</code>, <code>long</code>, or Python's "
            "unbounded <code>int</code>). The function must not destroy the caller's array.",
        ],
        "examples": [
            {
                "label": "Example 1",
                "input": "nums = [8, 4, 2, 1]",
                "output": "return 6",
                "explanation": "Every one of the six pairs is out of order.",
            },
            {
                "label": "Example 2",
                "input": "nums = [1, 20, 6, 4, 5]",
                "output": "return 5",
                "explanation": "The inversions are (20,6), (20,4), (20,5), (6,4) and (6,5).",
            },
            {
                "label": "Example 3",
                "input": "nums = [2, 2, 2]",
                "output": "return 0",
                "explanation": "Equal values are not inversions: the comparison is strict.",
            },
        ],
        "constraints": [
            "1 &le; <code>nums.length</code> &le; 100,000",
            "-10<sup>9</sup> &le; <code>nums[i]</code> &le; 10<sup>9</sup>",
            "Return a 64-bit integer. Python integers are already unbounded.",
            "Do not modify the input array. Do not use a built-in sort in the solution.",
        ],
        "sig_note": "C++ receives the array as a <code>const</code> reference &mdash; copy it internally before sorting. C receives a <code>const</code> pointer.",
        "hints": [
            "Recap merge sort: recursively sort the two halves, then merge. The counting happens during the merge, not afterwards.",
            "When you take an element from the right half, every element still unmerged in the left half is larger than it. That is <code>left.length - i</code> new inversions.",
            "Trust but verify: on <code>[4,3,2,1]</code> the recursion should produce 1 pair from the bottom call, then 2, then 3 as the halves merge &mdash; 6 in total.",
        ],
        "notes_anchor": "merge-sort",
        "notes_label": "Merge sort",
    },
    {
        "number": 5,
        "slug": "problem-5",
        "title": "Quick Sort: Random Pivot, 3-Way Partition",
        "difficulty": "Medium",
        "difficulty_class": "medium",
        "topics": ["Quick sort", "Randomization", "Duplicates"],
        "statement": [
            "Given an integer array <code>nums</code>, return a <strong>new array</strong> with the same values sorted in ascending order, "
            "implemented as quick sort.",
            "Two requirements. First, choose the pivot <strong>uniformly at random</strong> (pick a random index and move it to the "
            "partition position). Second, use a <strong>3-way partition</strong> (the Dutch national flag algorithm): after partitioning, "
            "all values equal to the pivot are already in their final positions, so you recurse only on the strictly-smaller and "
            "strictly-larger regions.",
            "A plain 2-way partition degrades to O(n<sup>2</sup>) on an array where every value is equal. The 3-way version stays "
            "O(n log n) on duplicates. Do not modify the input array.",
        ],
        "examples": [
            {
                "label": "Example 1",
                "input": "nums = [5, 2, 4, 1, 3]",
                "output": "[1, 2, 3, 4, 5]",
                "explanation": "The input array itself is unchanged.",
            },
            {
                "label": "Example 2",
                "input": "nums = [3, 1, 3, 3, 2, 3]",
                "output": "[1, 2, 3, 3, 3, 3]",
                "explanation": "All four 3s are grouped by the partition and never examined again: that is why duplicates are cheap here.",
            },
        ],
        "constraints": [
            "0 &le; <code>nums.length</code> &le; 100,000",
            "-10<sup>6</sup> &le; <code>nums[i]</code> &le; 10<sup>6</sup>",
            "The tests include many duplicates, fully sorted inputs, and an empty array.",
            "Do not modify the input array. Do not use a built-in sort.",
        ],
        "sig_note": "C returns a <code>malloc</code>'d array and writes its length to <code>*returnSize</code> (the caller frees it; for an empty input return <code>NULL</code> with <code>*returnSize = 0</code>).",
        "hints": [
            "3-way partition scans one index <code>i</code> through the region: smaller than pivot &rarr; swap to the front and advance; equal &rarr; advance; larger &rarr; swap to the back and <em>do not advance</em> (the swapped-in value still needs checking).",
            "Randomness: <code>rand() % (hi - lo + 1) + lo</code> in C, <code>std::uniform_int_distribution</code> in C++, <code>Random.Next(lo, hi + 1)</code> in C#, <code>ThreadLocalRandom.current().nextInt(lo, hi + 1)</code> in Java, <code>random.randint(lo, hi)</code> in Python, <code>Math.floor(Math.random() * (hi - lo + 1)) + lo</code> in JS. Swap the chosen index with <code>nums[lo]</code> before partitioning.",
            "Recurse on <code>[lo, lt-1]</code> and <code>[gt+1, hi]</code>, never on the equal band. Base case: a region of size 0 or 1. If your code times out on 200,000 equal values, you still have a 2-way partition.",
        ],
        "notes_anchor": "quick-sort",
        "notes_label": "Quick sort",
    },
    {
        "number": 6,
        "slug": "problem-6",
        "title": "Kth Largest Element (Quickselect)",
        "difficulty": "Medium+",
        "difficulty_class": "medium",
        "topics": ["Quickselect", "Order statistics", "Partition"],
        "statement": [
            "Given an integer array <code>nums</code> and an integer <code>k</code>, return the <strong>k-th largest</strong> element in "
            "sorted order &mdash; that is, the element at index <code>n - k</code> if the array were sorted ascending. <code>k</code> is "
            "1-based, so <code>k = 1</code> asks for the maximum.",
            "The expected solution is <strong>quickselect</strong>: partition like quicksort, but recurse only into the side that contains "
            "the target index. Average time O(n), with no need to sort everything.",
            "Sorting the whole array also passes the tests, but it defeats the purpose. Duplicates matter here: <code>[3, 3, 3]</code> "
            "with <code>k = 2</code> must return <code>3</code>.",
        ],
        "examples": [
            {
                "label": "Example 1",
                "input": "nums = [3, 2, 1, 5, 6, 4], k = 2",
                "output": "5",
                "explanation": "Sorted: [1, 2, 3, 4, 5, 6]. The second largest is 5.",
            },
            {
                "label": "Example 2",
                "input": "nums = [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4",
                "output": "4",
                "explanation": "Sorted: [1, 2, 2, 3, 3, 4, 5, 5, 6]. Index n - k = 5 holds 4.",
            },
        ],
        "constraints": [
            "1 &le; <code>k</code> &le; <code>nums.length</code> &le; 100,000",
            "-10<sup>4</sup> &le; <code>nums[i]</code> &le; 10<sup>4</sup>",
            "The array can contain many duplicate values.",
            "Do not use a built-in sort. O(n log n) passes, but the point is O(n) on average.",
        ],
        "sig_note": "C receives a mutable pointer, so it may copy and partition the input. C++ receives a <code>const</code> reference &mdash; copy it before partitioning.",
        "hints": [
            "Quickselect is quicksort that skips work: partition, then look at where the pivot landed. If that index is <code>n - k</code>, the pivot is the answer; otherwise recurse into the side containing the target.",
            "Why O(n) on average? Each partition costs the size of the current region, and the expected region size halves: n + n/2 + n/4 + &hellip; &asymp; 2n.",
            "Reuse the 3-way partition from Problem 5. If the equal band contains index <code>n - k</code>, the answer is the pivot value itself &mdash; no recursion needed.",
        ],
        "notes_anchor": "order-statistics",
        "notes_label": "Order statistics (preview)",
    },
]


SIGNATURES = {
    1: {
        "c": "void bubbleSort(int* nums, int numsSize)",
        "cpp": "void bubbleSort(std::vector<int>& nums)",
        "cs": "public static void BubbleSort(int[] nums)",
        "java": "public static void bubbleSort(int[] nums)",
        "py": "def bubble_sort(nums: list[int]) -> None",
        "js": "function bubbleSort(nums)",
    },
    2: {
        "c": "int insertionSort(int* nums, int numsSize)",
        "cpp": "int insertionSort(std::vector<int>& nums)",
        "cs": "public static int InsertionSort(int[] nums)",
        "java": "public static int insertionSort(int[] nums)",
        "py": "def insertion_sort(nums: list[int]) -> int",
        "js": "function insertionSort(nums)",
    },
    3: {
        "c": "void sortByLength(char** words, int wordsSize)",
        "cpp": "std::vector<std::string> sortByLength(std::vector<std::string> words)",
        "cs": "public static string[] SortByLength(string[] words)",
        "java": "public static String[] sortByLength(String[] words)",
        "py": "def sort_by_length(words: list[str]) -> list[str]",
        "js": "function sortByLength(words)",
    },
    4: {
        "c": "long long countInversions(const int* nums, int numsSize)",
        "cpp": "long long countInversions(const std::vector<int>& nums)",
        "cs": "public static long CountInversions(int[] nums)",
        "java": "public static long countInversions(int[] nums)",
        "py": "def count_inversions(nums: list[int]) -> int",
        "js": "function countInversions(nums)",
    },
    5: {
        "c": "int* quickSort(const int* nums, int numsSize, int* returnSize)",
        "cpp": "std::vector<int> quickSort(const std::vector<int>& nums)",
        "cs": "public static int[] QuickSort(int[] nums)",
        "java": "public static int[] quickSort(int[] nums)",
        "py": "def quick_sort(nums: list[int]) -> list[int]",
        "js": "function quickSort(nums)",
    },
    6: {
        "c": "int findKthLargest(int* nums, int numsSize, int k)",
        "cpp": "int findKthLargest(const std::vector<int>& nums, int k)",
        "cs": "public static int FindKthLargest(int[] nums, int k)",
        "java": "public static int findKthLargest(int[] nums, int k)",
        "py": "def find_kth_largest(nums: list[int], k: int) -> int",
        "js": "function findKthLargest(nums, k)",
    },
}
