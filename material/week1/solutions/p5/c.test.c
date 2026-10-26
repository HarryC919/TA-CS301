#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Function under test (defined in c.solution.c).
int* quickSort(const int* nums, int numsSize, int* returnSize);

static int failures = 0;
static int checks = 0;

// Return 1 when the first n values of a and b are equal.
static int arraysEqual(const int* a, const int* b, int n) {
    for (int i = 0; i < n; i++) {
        if (a[i] != b[i]) {
            return 0;
        }
    }
    return 1;
}

// Return the index of the first difference, or -1 when the arrays are equal.
static int firstMismatch(const int* a, const int* b, int n) {
    for (int i = 0; i < n; i++) {
        if (a[i] != b[i]) {
            return i;
        }
    }
    return -1;
}

// Check one fixed test case: the result values, the reported size, and that
// the caller's array was not modified.
static void checkSorted(const char* name, const int* input, int n, const int* expected) {
    checks++;
    int* inputCopy = NULL;
    if (n > 0) {
        inputCopy = (int*)malloc(sizeof(int) * (size_t)n);
        for (int i = 0; i < n; i++) {
            inputCopy[i] = input[i];
        }
    }

    int returnSize = -1;
    int* result = quickSort(input, n, &returnSize);
    int mismatch = (n > 0 && result != NULL) ? firstMismatch(result, expected, n) : -1;

    if (returnSize != n) {
        printf("FAIL %s: returnSize = %d, want %d\n", name, returnSize, n);
        failures++;
    } else if (n == 0 && result != NULL) {
        printf("FAIL %s: empty input should return NULL\n", name);
        failures++;
    } else if (n > 0 && result == NULL) {
        printf("FAIL %s: got NULL result\n", name);
        failures++;
    } else if (mismatch >= 0) {
        printf("FAIL %s: index %d got %d, want %d\n",
               name, mismatch, result[mismatch], expected[mismatch]);
        failures++;
    } else if (n > 0 && !arraysEqual(input, inputCopy, n)) {
        printf("FAIL %s: the input array was modified\n", name);
        failures++;
    } else {
        printf("PASS %s\n", name);
    }

    free(result);
    free(inputCopy);
}

static int compareInts(const void* a, const void* b) {
    int x = *(const int*)a;
    int y = *(const int*)b;
    if (x < y) {
        return -1;
    }
    if (x > y) {
        return 1;
    }
    return 0;
}

// Check one n = 200,000 case: cross-check against qsort, confirm the input was
// not modified, and require the sort to finish well under 2 seconds.
static void checkPerformance(const char* name, const int* input, int n) {
    checks++;
    int* expected = (int*)malloc(sizeof(int) * (size_t)n);
    int* inputCopy = (int*)malloc(sizeof(int) * (size_t)n);
    for (int i = 0; i < n; i++) {
        expected[i] = input[i];
        inputCopy[i] = input[i];
    }
    qsort(expected, (size_t)n, sizeof(int), compareInts);  // library sort as oracle

    clock_t start = clock();
    int returnSize = 0;
    int* result = quickSort(input, n, &returnSize);
    double seconds = (double)(clock() - start) / (double)CLOCKS_PER_SEC;

    int mismatch = (result != NULL) ? firstMismatch(result, expected, n) : -1;

    if (returnSize != n) {
        printf("FAIL %s: returnSize = %d, want %d\n", name, returnSize, n);
        failures++;
    } else if (result == NULL) {
        printf("FAIL %s: got NULL result\n", name);
        failures++;
    } else if (mismatch >= 0) {
        printf("FAIL %s: index %d got %d, want %d\n",
               name, mismatch, result[mismatch], expected[mismatch]);
        failures++;
    } else if (!arraysEqual(input, inputCopy, n)) {
        printf("FAIL %s: the input array was modified\n", name);
        failures++;
    } else if (seconds >= 2.0) {
        printf("FAIL %s: %.3f s is not well under 2 s\n", name, seconds);
        failures++;
    } else {
        printf("PASS %s (%.3f s)\n", name, seconds);
    }

    free(result);
    free(expected);
    free(inputCopy);
}

static unsigned int randomState = 12345u;

// Deterministic pseudo-random numbers for building the test inputs.
static unsigned int nextRandom(void) {
    randomState = randomState * 1664525u + 1013904223u;
    return randomState;
}

int main(void) {
    // --- Fixed cases from the contract ------------------------------------
    checkSorted("[] -> []", NULL, 0, NULL);
    {
        int input[] = {1};
        int expected[] = {1};
        checkSorted("[1] -> [1]", input, 1, expected);
    }
    {
        int input[] = {5, 2, 4, 1, 3};
        int expected[] = {1, 2, 3, 4, 5};
        checkSorted("[5,2,4,1,3] -> [1,2,3,4,5]", input, 5, expected);
    }
    {
        int input[] = {3, 1, 3, 3, 2, 3};
        int expected[] = {1, 2, 3, 3, 3, 3};
        checkSorted("[3,1,3,3,2,3] -> [1,2,3,3,3,3]", input, 6, expected);
    }
    {
        int input[] = {7, 7, 7, 7};
        int expected[] = {7, 7, 7, 7};
        checkSorted("[7,7,7,7] -> unchanged", input, 4, expected);
    }
    {
        int input[] = {4, 3, 2, 1};
        int expected[] = {1, 2, 3, 4};
        checkSorted("[4,3,2,1] -> [1,2,3,4]", input, 4, expected);
    }
    {
        int input[] = {-3, 5, 0, -3, 2};
        int expected[] = {-3, -3, 0, 2, 5};
        checkSorted("[-3,5,0,-3,2] -> [-3,-3,0,2,5]", input, 5, expected);
    }

    // Seeded random cross-check against qsort, n = 1000.
    {
        const int n = 1000;
        int* input = (int*)malloc(sizeof(int) * (size_t)n);
        int* expected = (int*)malloc(sizeof(int) * (size_t)n);
        for (int i = 0; i < n; i++) {
            input[i] = (int)(nextRandom() % 2000001u) - 1000000;
            expected[i] = input[i];
        }
        qsort(expected, (size_t)n, sizeof(int), compareInts);
        checkSorted("random n=1000 cross-check", input, n, expected);
        free(input);
        free(expected);
    }

    // --- Performance cases, n = 200,000 -----------------------------------
    {
        const int n = 200000;
        int* input = (int*)malloc(sizeof(int) * (size_t)n);
        for (int i = 0; i < n; i++) {
            input[i] = (int)(nextRandom() % 51u);  // values in [0,50]: heavy duplicates
        }
        checkPerformance("n=200000 random values in [0,50]", input, n);
        free(input);
    }
    {
        const int n = 200000;
        int* input = (int*)malloc(sizeof(int) * (size_t)n);
        for (int i = 0; i < n; i++) {
            input[i] = 42;  // all equal
        }
        checkPerformance("n=200000 all-equal", input, n);
        free(input);
    }
    {
        const int n = 200000;
        int* input = (int*)malloc(sizeof(int) * (size_t)n);
        for (int i = 0; i < n; i++) {
            input[i] = i;  // already sorted (random pivot keeps this fast)
        }
        checkPerformance("n=200000 already sorted", input, n);
        free(input);
    }

    printf("\n%d checks, %d failed\n", checks, failures);
    if (failures > 0) {
        printf("FAILED\n");
        return 1;
    }
    printf("All tests passed.\n");
    return 0;
}
