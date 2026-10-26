#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int insertionSort(int* nums, int numsSize);

static int failures = 0;

// Oracle 1 (shift count): brute-force inversion count, O(n^2) — allowed in the harness only.
static long long countInversionsBruteForce(const int* nums, int n) {
    long long count = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (nums[i] > nums[j]) {
                count++;
            }
        }
    }
    return count;
}

// Oracle 2 (final array): library sort, allowed in the harness only.
static int compareInts(const void* a, const void* b) {
    int x = *(const int*)a;
    int y = *(const int*)b;
    return (x > y) - (x < y);
}

static void checkFixed(const char* name, const int* input, int n,
                       const int* expected, int expectedShifts) {
    int* arr = malloc((size_t)n * sizeof(int));
    for (int i = 0; i < n; i++) {
        arr[i] = input[i];
    }
    int shifts = insertionSort(arr, n);
    int ok = (shifts == expectedShifts);
    for (int i = 0; i < n && ok; i++) {
        ok = (arr[i] == expected[i]);
    }
    printf("%s: %s (shifts=%d, expected=%d)\n",
           ok ? "PASS" : "FAIL", name, shifts, expectedShifts);
    if (!ok) {
        failures++;
    }
    free(arr);
}

static void checkRandom(int seed, int n, int valueRange) {
    int* arr = malloc((size_t)n * sizeof(int));
    int* original = malloc((size_t)n * sizeof(int));
    srand((unsigned int)seed);
    for (int i = 0; i < n; i++) {
        // values in [-valueRange, valueRange]
        arr[i] = rand() % (2 * valueRange + 1) - valueRange;
        original[i] = arr[i];
    }
    long long expectedShifts = countInversionsBruteForce(original, n);
    clock_t start = clock();
    int shifts = insertionSort(arr, n);
    double elapsed = (double)(clock() - start) / CLOCKS_PER_SEC;
    qsort(original, (size_t)n, sizeof(int), compareInts);
    int ok = ((long long)shifts == expectedShifts);
    for (int i = 0; i < n && ok; i++) {
        ok = (arr[i] == original[i]);
    }
    printf("%s: random n=%d seed=%d range=[-%d,%d] (shifts=%d, expected=%lld, %.3fs)\n",
           ok ? "PASS" : "FAIL", n, seed, valueRange, valueRange,
           shifts, expectedShifts, elapsed);
    if (!ok) {
        failures++;
    }
    free(arr);
    free(original);
}

static void checkDescending(int n) {
    int* arr = malloc((size_t)n * sizeof(int));
    int* expected = malloc((size_t)n * sizeof(int));
    for (int i = 0; i < n; i++) {
        arr[i] = n - i;        // n, n-1, ..., 1 (worst case)
        expected[i] = i + 1;   // 1, 2, ..., n
    }
    long long expectedShifts = (long long)n * (n - 1) / 2;
    clock_t start = clock();
    int shifts = insertionSort(arr, n);
    double elapsed = (double)(clock() - start) / CLOCKS_PER_SEC;
    int ok = ((long long)shifts == expectedShifts);
    for (int i = 0; i < n && ok; i++) {
        ok = (arr[i] == expected[i]);
    }
    printf("%s: descending n=%d (shifts=%d, expected=%lld, %.3fs)\n",
           ok ? "PASS" : "FAIL", n, shifts, expectedShifts, elapsed);
    if (!ok) {
        failures++;
    }
    free(arr);
    free(expected);
}

int main(void) {
    // Contract cases
    checkFixed("single element", (int[]){1}, 1, (int[]){1}, 0);
    checkFixed("already sorted", (int[]){1, 2, 3}, 3, (int[]){1, 2, 3}, 0);
    checkFixed("reverse sorted", (int[]){3, 2, 1}, 3, (int[]){1, 2, 3}, 3);
    checkFixed("example walkthrough", (int[]){5, 2, 4, 1}, 4, (int[]){1, 2, 4, 5}, 5);
    checkFixed("all equal (no shifts)", (int[]){2, 2, 2}, 3, (int[]){2, 2, 2}, 0);
    checkFixed("negative values", (int[]){-1, 5, 0, -10}, 4, (int[]){-10, -1, 0, 5}, 4);

    // Seeded random cross-checks vs brute-force inversion count + library sort
    checkRandom(42, 1000, 10000);
    checkRandom(7, 1000, 10000);
    checkRandom(1234, 1000, 10000);
    checkRandom(99, 1000, 3);      // heavy duplicates: stresses the strict '>' rule

    // Performance at the maximum constraint size (n = 1000)
    checkDescending(1000);

    if (failures > 0) {
        printf("%d FAILURE(S)\n", failures);
        return 1;
    }
    printf("ALL TESTS PASSED\n");
    return 0;
}
