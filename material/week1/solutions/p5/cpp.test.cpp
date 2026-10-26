#include <algorithm>
#include <chrono>
#include <cstdio>
#include <random>
#include <vector>

// Function under test (defined in cpp.solution.cpp).
std::vector<int> quickSort(const std::vector<int>& nums);

static int failures = 0;
static int checks = 0;

// Return the index of the first difference, or -1 when the vectors are equal.
static int firstMismatch(const std::vector<int>& a, const std::vector<int>& b) {
    for (std::size_t i = 0; i < a.size(); i++) {
        if (a[i] != b[i]) {
            return static_cast<int>(i);
        }
    }
    return -1;
}

// Check one fixed test case: the result values and that the caller's vector
// was not modified.
static void checkSorted(const char* name, const std::vector<int>& input,
                        const std::vector<int>& expected) {
    checks++;
    std::vector<int> inputCopy = input;
    std::vector<int> result = quickSort(input);

    if (result.size() != expected.size()) {
        printf("FAIL %s: length %zu, want %zu\n", name, result.size(), expected.size());
        failures++;
        return;
    }

    int mismatch = firstMismatch(result, expected);
    if (mismatch >= 0) {
        printf("FAIL %s: index %d got %d, want %d\n",
               name, mismatch, result[mismatch], expected[mismatch]);
        failures++;
    } else if (input != inputCopy) {
        printf("FAIL %s: the input vector was modified\n", name);
        failures++;
    } else {
        printf("PASS %s\n", name);
    }
}

// Check one n = 200,000 case: cross-check against std::sort, confirm the input
// was not modified, and require the sort to finish well under 2 seconds.
static void checkPerformance(const char* name, const std::vector<int>& input) {
    checks++;
    std::vector<int> expected = input;
    std::sort(expected.begin(), expected.end());  // library sort as oracle
    std::vector<int> inputCopy = input;

    auto start = std::chrono::steady_clock::now();
    std::vector<int> result = quickSort(input);
    auto finish = std::chrono::steady_clock::now();
    double seconds = std::chrono::duration<double>(finish - start).count();

    if (result.size() != expected.size()) {
        printf("FAIL %s: length %zu, want %zu\n", name, result.size(), expected.size());
        failures++;
        return;
    }

    int mismatch = firstMismatch(result, expected);
    if (mismatch >= 0) {
        printf("FAIL %s: index %d got %d, want %d\n",
               name, mismatch, result[mismatch], expected[mismatch]);
        failures++;
    } else if (input != inputCopy) {
        printf("FAIL %s: the input vector was modified\n", name);
        failures++;
    } else if (seconds >= 2.0) {
        printf("FAIL %s: %.3f s is not well under 2 s\n", name, seconds);
        failures++;
    } else {
        printf("PASS %s (%.3f s)\n", name, seconds);
    }
}

int main() {
    // --- Fixed cases from the contract ------------------------------------
    checkSorted("[] -> []", {}, {});
    checkSorted("[1] -> [1]", {1}, {1});
    checkSorted("[5,2,4,1,3] -> [1,2,3,4,5]", {5, 2, 4, 1, 3}, {1, 2, 3, 4, 5});
    checkSorted("[3,1,3,3,2,3] -> [1,2,3,3,3,3]", {3, 1, 3, 3, 2, 3}, {1, 2, 3, 3, 3, 3});
    checkSorted("[7,7,7,7] -> unchanged", {7, 7, 7, 7}, {7, 7, 7, 7});
    checkSorted("[4,3,2,1] -> [1,2,3,4]", {4, 3, 2, 1}, {1, 2, 3, 4});
    checkSorted("[-3,5,0,-3,2] -> [-3,-3,0,2,5]", {-3, 5, 0, -3, 2}, {-3, -3, 0, 2, 5});

    // Seeded random cross-check against std::sort, n = 1000.
    {
        const int n = 1000;
        std::mt19937 rng(12345);
        std::uniform_int_distribution<int> value(-1000000, 1000000);
        std::vector<int> input(n);
        for (int i = 0; i < n; i++) {
            input[i] = value(rng);
        }
        std::vector<int> expected = input;
        std::sort(expected.begin(), expected.end());
        checkSorted("random n=1000 cross-check", input, expected);
    }

    // --- Performance cases, n = 200,000 -----------------------------------
    const int n = 200000;
    {
        std::mt19937 rng(2024);
        std::uniform_int_distribution<int> value(0, 50);  // heavy duplicates
        std::vector<int> input(n);
        for (int i = 0; i < n; i++) {
            input[i] = value(rng);
        }
        checkPerformance("n=200000 random values in [0,50]", input);
    }
    {
        std::vector<int> input(n, 42);  // all equal
        checkPerformance("n=200000 all-equal", input);
    }
    {
        std::vector<int> input(n);
        for (int i = 0; i < n; i++) {
            input[i] = i;  // already sorted (random pivot keeps this fast)
        }
        checkPerformance("n=200000 already sorted", input);
    }

    printf("\n%d checks, %d failed\n", checks, failures);
    if (failures > 0) {
        printf("FAILED\n");
        return 1;
    }
    printf("All tests passed.\n");
    return 0;
}
