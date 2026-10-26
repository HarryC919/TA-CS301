#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <vector>

int findKthLargest(const std::vector<int>& nums, int k);

static int failures = 0;

// Wrapper that compares one quickselect call against the expected answer.
static void check(std::vector<int> nums, int k, int expected, const char* name) {
    int got = findKthLargest(nums, k);
    if (got != expected) {
        printf("FAIL %s (k=%d): got %d, want %d\n", name, k, got, expected);
        failures++;
    } else {
        printf("PASS %s (k=%d -> %d)\n", name, k, got);
    }
}

int main() {
    // Fixed cases from the contract
    check({3, 2, 1, 5, 6, 4}, 2, 5, "case [3,2,1,5,6,4]");
    check({3, 2, 3, 1, 2, 4, 5, 5, 6}, 4, 4, "case [3,2,3,1,2,4,5,5,6]");
    check({1}, 1, 1, "case [1]");
    check({2, 1}, 1, 2, "case [2,1] k=1");
    check({2, 1}, 2, 1, "case [2,1] k=2");
    check({-1, -5, 3}, 1, 3, "case [-1,-5,3]");
    check({3, 3, 3}, 2, 3, "case [3,3,3]");

    // Seeded random cross-check against a library sort, n = 200,000
    {
        const int n = 200000;
        std::srand(42);
        std::mt19937 rng(42);
        std::uniform_int_distribution<int> values(-10000, 10000);
        std::vector<int> data(n);
        for (int i = 0; i < n; i++) {
            data[i] = values(rng);
        }
        std::vector<int> sorted = data;
        std::sort(sorted.begin(), sorted.end());

        int ks[] = {1, n / 2, n};
        for (int caseIndex = 0; caseIndex < 3; caseIndex++) {
            int k = ks[caseIndex];
            std::vector<int> copy = data;
            auto start = std::chrono::steady_clock::now();
            int got = findKthLargest(copy, k);
            auto stop = std::chrono::steady_clock::now();
            double elapsedMs =
                std::chrono::duration<double, std::milli>(stop - start).count();
            int expected = sorted[n - k];
            if (got != expected) {
                printf("FAIL random n=200000 k=%d: got %d, want %d\n", k, got, expected);
                failures++;
            } else if (elapsedMs > 2000.0) {
                printf("FAIL random n=200000 k=%d: too slow (%.1f ms)\n", k, elapsedMs);
                failures++;
            } else {
                printf("PASS random n=200000 k=%d -> %d (%.1f ms)\n", k, got, elapsedMs);
            }
        }
    }

    if (failures == 0) {
        printf("ALL TESTS PASSED\n");
        return 0;
    }
    printf("%d TEST(S) FAILED\n", failures);
    return 1;
}
