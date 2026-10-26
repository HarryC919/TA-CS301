#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

long long countInversions(const int* nums, int numsSize);

static int failures = 0;

// Verify one answer, and also check that the input array was not modified.
static void check(const char* name, const int* input, int numsSize, long long expected) {
    int* copy = malloc((size_t)numsSize * sizeof(int));
    memcpy(copy, input, (size_t)numsSize * sizeof(int));
    long long got = countInversions(input, numsSize);
    int unchanged = memcmp(copy, input, (size_t)numsSize * sizeof(int)) == 0;
    if (got != expected) {
        printf("FAIL %s: got %lld, want %lld\n", name, got, expected);
        failures++;
    } else if (!unchanged) {
        printf("FAIL %s: input array was modified\n", name);
        failures++;
    } else {
        printf("PASS %s\n", name);
    }
    free(copy);
}

// Reference answer: O(n^2) double loop, only for small inputs.
static long long bruteForce(const int* nums, int numsSize) {
    long long count = 0;
    for (int i = 0; i < numsSize; i++) {
        for (int j = i + 1; j < numsSize; j++) {
            if (nums[i] > nums[j]) {
                count++;
            }
        }
    }
    return count;
}

// Deterministic pseudo-random generator so every run tests the same data.
static unsigned int nextRandom(unsigned int* state) {
    *state = *state * 1664525u + 1013904223u;
    return *state;
}

static void fillRandom(int* nums, int numsSize, unsigned int* state,
                       int minValue, int maxValue) {
    unsigned int range = (unsigned int)((long long)maxValue - minValue + 1);
    for (int i = 0; i < numsSize; i++) {
        nums[i] = (int)((long long)minValue + (long long)(nextRandom(state) % range));
    }
}

static int compareInts(const void* first, const void* second) {
    int left = *(const int*)first;
    int right = *(const int*)second;
    if (left < right) {
        return -1;
    }
    if (left > right) {
        return 1;
    }
    return 0;
}

// Count pairs with different values; used to check the large random case.
static long long unequalPairCount(const int* nums, int numsSize) {
    int* sorted = malloc((size_t)numsSize * sizeof(int));
    memcpy(sorted, nums, (size_t)numsSize * sizeof(int));
    qsort(sorted, (size_t)numsSize, sizeof(int), compareInts);
    long long unequalPairs = (long long)numsSize * (numsSize - 1) / 2;
    int runStart = 0;
    while (runStart < numsSize) {
        int runEnd = runStart + 1;
        while (runEnd < numsSize && sorted[runEnd] == sorted[runStart]) {
            runEnd++;
        }
        long long runLength = runEnd - runStart;
        unequalPairs -= runLength * (runLength - 1) / 2;
        runStart = runEnd;
    }
    free(sorted);
    return unequalPairs;
}

int main(void) {
    // Fixed cases from the contract.
    {
        int input[] = {1};
        check("case [1]", input, 1, 0);
    }
    {
        int input[] = {1, 2, 3, 4};
        check("case [1,2,3,4]", input, 4, 0);
    }
    {
        int input[] = {4, 3, 2, 1};
        check("case [4,3,2,1]", input, 4, 6);
    }
    {
        int input[] = {8, 4, 2, 1};
        check("case [8,4,2,1]", input, 4, 6);
    }
    {
        int input[] = {1, 20, 6, 4, 5};
        check("case [1,20,6,4,5]", input, 5, 5);
    }
    {
        int input[] = {2, 2, 2};
        check("case [2,2,2] (strict >)", input, 3, 0);
    }

    // Seeded random cross-check against the brute-force answer.
    unsigned int state = 12345u;
    int randomSizes[] = {1, 2, 3, 5, 10, 50, 300, 2000};
    int randomSizeCount = (int)(sizeof(randomSizes) / sizeof(randomSizes[0]));
    for (int s = 0; s < randomSizeCount; s++) {
        int n = randomSizes[s];
        int* nums = malloc((size_t)n * sizeof(int));
        fillRandom(nums, n, &state, -10000, 10000);
        long long expected = bruteForce(nums, n);
        char name[64];
        snprintf(name, sizeof(name), "random n=%d vs brute force", n);
        check(name, nums, n, expected);
        free(nums);
    }

    // A descending array of 100,000 elements has n*(n-1)/2 = 4,999,950,000
    // inversions, which does not fit in 32 bits.
    const int largeSize = 100000;
    int* descending = malloc((size_t)largeSize * sizeof(int));
    for (int i = 0; i < largeSize; i++) {
        descending[i] = largeSize - i;
    }
    check("descending 100,000 (64-bit)", descending, largeSize, 4999950000LL);
    free(descending);

    // Performance run on a random array of 100,000 values.
    int* large = malloc((size_t)largeSize * sizeof(int));
    fillRandom(large, largeSize, &state, -1000000000, 1000000000);
    int* largeCopy = malloc((size_t)largeSize * sizeof(int));
    memcpy(largeCopy, large, (size_t)largeSize * sizeof(int));
    clock_t start = clock();
    long long largeCount = countInversions(large, largeSize);
    double seconds = (double)(clock() - start) / CLOCKS_PER_SEC;
    if (memcmp(largeCopy, large, (size_t)largeSize * sizeof(int)) != 0) {
        printf("FAIL perf n=100,000: input array was modified\n");
        failures++;
    } else if (seconds > 2.0) {
        printf("FAIL perf n=100,000: %.3f s (expected under 2 s)\n", seconds);
        failures++;
    } else {
        printf("PASS perf n=100,000 (%.3f s)\n", seconds);
    }
    free(largeCopy);

    // Cross-check the large answer without O(n^2) work: for every pair of
    // different values exactly one of the two orders is an inversion, so
    // count(nums) + count(reverse(nums)) equals the number of unequal pairs.
    int* reversed = malloc((size_t)largeSize * sizeof(int));
    for (int i = 0; i < largeSize; i++) {
        reversed[i] = large[largeSize - 1 - i];
    }
    long long reversedCount = countInversions(reversed, largeSize);
    long long unequalPairs = unequalPairCount(large, largeSize);
    if (largeCount + reversedCount == unequalPairs) {
        printf("PASS large random consistency: count + reversed = unequal pairs\n");
    } else {
        printf("FAIL large random consistency: %lld + %lld != %lld\n",
               largeCount, reversedCount, unequalPairs);
        failures++;
    }
    free(reversed);
    free(large);

    if (failures == 0) {
        printf("ALL TESTS PASSED\n");
        return 0;
    }
    printf("%d TEST(S) FAILED\n", failures);
    return 1;
}
