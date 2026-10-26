#include <algorithm>
#include <chrono>
#include <cstdio>
#include <vector>

void bubbleSort(std::vector<int>& nums);

static int failures = 0;

static void check(std::vector<int> input, const std::vector<int>& expected,
                  const char* name) {
    bubbleSort(input);
    if (input != expected) {
        printf("FAIL %s\n", name);
        failures++;
        return;
    }
    printf("PASS %s\n", name);
}

int main() {
    // Fixed cases from the contract
    check({1}, {1}, "case [1]");
    check({5, 2, 4, 1, 3}, {1, 2, 3, 4, 5}, "case [5,2,4,1,3]");
    check({1, 2, 3, 4}, {1, 2, 3, 4}, "case [1,2,3,4] already sorted");
    check({4, 3, 2, 1}, {1, 2, 3, 4}, "case [4,3,2,1] reverse sorted");
    check({2, 2, 1, 3, 2}, {1, 2, 2, 2, 3}, "case [2,2,1,3,2] duplicates");
    check({-1, 5, 0, -10}, {-10, -1, 0, 5}, "case [-1,5,0,-10] negatives");

    // Seeded random cross-check vs library sort, n = 1000
    {
        const int n = 1000;
        std::srand(42);
        std::vector<int> a(n), b(n);
        for (int i = 0; i < n; i++) {
            a[i] = (std::rand() % 20001) - 10000;  // values in [-10000, 10000]
            b[i] = a[i];
        }
        auto t0 = std::chrono::steady_clock::now();
        bubbleSort(a);  // in place
        double ms = std::chrono::duration<double, std::milli>(
                        std::chrono::steady_clock::now() - t0)
                        .count();
        std::sort(b.begin(), b.end());
        if (a != b) {
            printf("FAIL case random n=1000 vs std::sort\n");
            failures++;
        } else {
            printf("PASS case random n=1000 vs std::sort (%.1f ms)\n", ms);
        }
    }

    // Performance: worst case, n = 1000 reverse sorted (full n^2 passes)
    {
        const int n = 1000;
        std::vector<int> a(n);
        for (int i = 0; i < n; i++) {
            a[i] = n - i;
        }
        auto t0 = std::chrono::steady_clock::now();
        bubbleSort(a);
        double ms = std::chrono::duration<double, std::milli>(
                        std::chrono::steady_clock::now() - t0)
                        .count();
        std::vector<int> expected(n);
        for (int i = 0; i < n; i++) {
            expected[i] = i + 1;
        }
        if (a != expected) {
            printf("FAIL case perf reverse n=1000: not sorted\n");
            failures++;
        } else if (ms > 2000.0) {
            printf("FAIL case perf reverse n=1000: too slow (%.1f ms)\n", ms);
            failures++;
        } else {
            printf("PASS case perf reverse n=1000 (%.1f ms)\n", ms);
        }
    }

    if (failures == 0) {
        printf("ALL TESTS PASSED\n");
        return 0;
    }
    printf("%d TEST(S) FAILED\n", failures);
    return 1;
}
