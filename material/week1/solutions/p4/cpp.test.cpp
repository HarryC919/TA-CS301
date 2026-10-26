#include <algorithm>
#include <chrono>
#include <cstddef>
#include <cstdio>
#include <vector>

long long countInversions(const std::vector<int>& nums);

namespace {

int failures = 0;

// Verify one answer, and also check that the input vector was not modified.
void check(const char* name, const std::vector<int>& input, long long expected) {
    std::vector<int> copy = input;
    long long got = countInversions(input);
    if (got != expected) {
        std::printf("FAIL %s: got %lld, want %lld\n", name, got, expected);
        failures++;
    } else if (input != copy) {
        std::printf("FAIL %s: input array was modified\n", name);
        failures++;
    } else {
        std::printf("PASS %s\n", name);
    }
}

// Reference answer: O(n^2) double loop, only for small inputs.
long long bruteForce(const std::vector<int>& nums) {
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

// Deterministic pseudo-random generator so every run tests the same data.
unsigned int nextRandom(unsigned int& state) {
    state = state * 1664525u + 1013904223u;
    return state;
}

std::vector<int> makeRandom(int n, unsigned int& state, int minValue, int maxValue) {
    std::vector<int> nums(static_cast<std::size_t>(n));
    unsigned int range = static_cast<unsigned int>(
        static_cast<long long>(maxValue) - minValue + 1);
    for (int i = 0; i < n; i++) {
        long long offset = static_cast<long long>(nextRandom(state) % range);
        nums[static_cast<std::size_t>(i)] = static_cast<int>(minValue + offset);
    }
    return nums;
}

// Count pairs with different values; used to check the large random case.
long long unequalPairCount(const std::vector<int>& nums) {
    std::vector<int> sorted = nums;
    std::sort(sorted.begin(), sorted.end());
    long long size = static_cast<long long>(nums.size());
    long long unequalPairs = size * (size - 1) / 2;
    std::size_t runStart = 0;
    while (runStart < sorted.size()) {
        std::size_t runEnd = runStart + 1;
        while (runEnd < sorted.size() && sorted[runEnd] == sorted[runStart]) {
            runEnd++;
        }
        long long runLength = static_cast<long long>(runEnd - runStart);
        unequalPairs -= runLength * (runLength - 1) / 2;
        runStart = runEnd;
    }
    return unequalPairs;
}

}  // namespace

int main() {
    // Fixed cases from the contract.
    check("case [1]", {1}, 0);
    check("case [1,2,3,4]", {1, 2, 3, 4}, 0);
    check("case [4,3,2,1]", {4, 3, 2, 1}, 6);
    check("case [8,4,2,1]", {8, 4, 2, 1}, 6);
    check("case [1,20,6,4,5]", {1, 20, 6, 4, 5}, 5);
    check("case [2,2,2] (strict >)", {2, 2, 2}, 0);

    // Seeded random cross-check against the brute-force answer.
    unsigned int state = 12345u;
    const int randomSizes[] = {1, 2, 3, 5, 10, 50, 300, 2000};
    for (int n : randomSizes) {
        std::vector<int> nums = makeRandom(n, state, -10000, 10000);
        char name[64];
        std::snprintf(name, sizeof(name), "random n=%d vs brute force", n);
        check(name, nums, bruteForce(nums));
    }

    // A descending array of 100,000 elements has n*(n-1)/2 = 4,999,950,000
    // inversions, which does not fit in 32 bits.
    const int largeSize = 100000;
    std::vector<int> descending(static_cast<std::size_t>(largeSize));
    for (int i = 0; i < largeSize; i++) {
        descending[static_cast<std::size_t>(i)] = largeSize - i;
    }
    check("descending 100,000 (64-bit)", descending, 4999950000LL);

    // Performance run on a random array of 100,000 values.
    std::vector<int> large = makeRandom(largeSize, state, -1000000000, 1000000000);
    std::vector<int> largeCopy = large;
    auto start = std::chrono::steady_clock::now();
    long long largeCount = countInversions(large);
    auto finish = std::chrono::steady_clock::now();
    double seconds = std::chrono::duration<double>(finish - start).count();
    if (large != largeCopy) {
        std::printf("FAIL perf n=100,000: input array was modified\n");
        failures++;
    } else if (seconds > 2.0) {
        std::printf("FAIL perf n=100,000: %.3f s (expected under 2 s)\n", seconds);
        failures++;
    } else {
        std::printf("PASS perf n=100,000 (%.3f s)\n", seconds);
    }

    // Cross-check the large answer without O(n^2) work: for every pair of
    // different values exactly one of the two orders is an inversion, so
    // count(nums) + count(reverse(nums)) equals the number of unequal pairs.
    std::vector<int> reversedLarge(large.rbegin(), large.rend());
    long long reversedCount = countInversions(reversedLarge);
    long long unequalPairs = unequalPairCount(large);
    if (largeCount + reversedCount == unequalPairs) {
        std::printf("PASS large random consistency: count + reversed = unequal pairs\n");
    } else {
        std::printf("FAIL large random consistency: %lld + %lld != %lld\n",
                    largeCount, reversedCount, unequalPairs);
        failures++;
    }

    if (failures == 0) {
        std::printf("ALL TESTS PASSED\n");
        return 0;
    }
    std::printf("%d TEST(S) FAILED\n", failures);
    return 1;
}
