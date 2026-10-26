#include <algorithm>
#include <cstdio>
#include <vector>

int insertionSort(std::vector<int>& nums);

static int failures = 0;

// Oracle 1 (shift count): brute-force inversion count, O(n^2) - harness only.
static long long countInversionsBruteForce(const std::vector<int>& nums) {
    long long count = 0;
    for (std::size_t i = 0; i < nums.size(); i++) {
        for (std::size_t j = i + 1; j < nums.size(); j++) {
            if (nums[i] > nums[j]) {
                count++;
            }
        }
    }
    return count;
}

static void checkFixed(const char* name, std::vector<int> input,
                       const std::vector<int>& expected, int expectedShifts) {
    int shifts = insertionSort(input);
    if (shifts != expectedShifts || input != expected) {
        printf("FAIL %s (shifts=%d, expected=%d)\n", name, shifts, expectedShifts);
        failures++;
        return;
    }
    printf("PASS %s (shifts=%d)\n", name, shifts);
}

static void checkRandom(int seed, int n, int valueRange) {
    std::srand(seed);
    std::vector<int> original(n);
    for (int i = 0; i < n; i++) {
        // values in [-valueRange, valueRange]
        original[i] = std::rand() % (2 * valueRange + 1) - valueRange;
    }
    long long expectedShifts = countInversionsBruteForce(original);
    std::vector<int> nums = original;
    int shifts = insertionSort(nums);
    std::sort(original.begin(), original.end());  // oracle: library sort
    if (static_cast<long long>(shifts) != expectedShifts || nums != original) {
        printf("FAIL random n=%d seed=%d (shifts=%d, expected=%lld)\n",
               n, seed, shifts, expectedShifts);
        failures++;
        return;
    }
    printf("PASS random n=%d seed=%d (shifts=%d)\n", n, seed, shifts);
}

int main() {
    // Fixed cases from the contract
    checkFixed("case [1]", {1}, {1}, 0);
    checkFixed("case [1,2,3]", {1, 2, 3}, {1, 2, 3}, 0);
    checkFixed("case [3,2,1]", {3, 2, 1}, {1, 2, 3}, 3);
    checkFixed("case [5,2,4,1]", {5, 2, 4, 1}, {1, 2, 4, 5}, 5);
    checkFixed("case [2,2,2] equal keys", {2, 2, 2}, {2, 2, 2}, 0);
    checkFixed("case [-1,5,0,-10] negatives", {-1, 5, 0, -10}, {-10, -1, 0, 5}, 4);

    // Seeded random cross-checks: shifts vs brute force, array vs library sort
    checkRandom(42, 1000, 10000);
    checkRandom(7, 1000, 10000);
    checkRandom(1234, 1000, 10000);
    checkRandom(99, 1000, 3);  // heavy duplicates: stresses the strict '>' rule

    if (failures > 0) {
        printf("%d FAILURE(S)\n", failures);
        return 1;
    }
    printf("ALL TESTS PASSED\n");
    return 0;
}
