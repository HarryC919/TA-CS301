#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int findKthLargest(int* nums, int numsSize, int k);

static int failures = 0;

// Copies the input, runs quickselect on the copy, compares with the expected value.
static void check(const int* input, int n, int k, int expected, const char* name) {
    int* copy = malloc(n * sizeof(int));
    if (copy == NULL) {
        printf("FAIL %s: out of memory\n", name);
        failures++;
        return;
    }
    memcpy(copy, input, n * sizeof(int));
    int got = findKthLargest(copy, n, k);
    if (got != expected) {
        printf("FAIL %s (k=%d): got %d, want %d\n", name, k, got, expected);
        failures++;
    } else {
        printf("PASS %s (k=%d -> %d)\n", name, k, got);
    }
    free(copy);
}

static int compareInts(const void* first, const void* second) {
    int a = *(const int*)first;
    int b = *(const int*)second;
    return (a > b) - (a < b);
}

int main(void) {
    // Fixed cases from the contract
    {
        int input[] = {3, 2, 1, 5, 6, 4};
        check(input, 6, 2, 5, "case [3,2,1,5,6,4]");
    }
    {
        int input[] = {3, 2, 3, 1, 2, 4, 5, 5, 6};
        check(input, 9, 4, 4, "case [3,2,3,1,2,4,5,5,6]");
    }
    {
        int input[] = {1};
        check(input, 1, 1, 1, "case [1]");
    }
    {
        int input[] = {2, 1};
        check(input, 2, 1, 2, "case [2,1] k=1");
        check(input, 2, 2, 1, "case [2,1] k=2");
    }
    {
        int input[] = {-1, -5, 3};
        check(input, 3, 1, 3, "case [-1,-5,3]");
    }
    {
        int input[] = {3, 3, 3};
        check(input, 3, 2, 3, "case [3,3,3]");
    }

    // Seeded random cross-check against a library sort, n = 200,000
    {
        const int n = 200000;
        int* data = malloc(n * sizeof(int));
        int* sorted = malloc(n * sizeof(int));
        int* copy = malloc(n * sizeof(int));
        if (data == NULL || sorted == NULL || copy == NULL) {
            printf("FAIL random n=200000: out of memory\n");
            return 1;
        }
        srand(42);
        for (int i = 0; i < n; i++) {
            data[i] = rand() % 20001 - 10000;  // values in [-10000, 10000]
            sorted[i] = data[i];
        }
        qsort(sorted, n, sizeof(int), compareInts);

        int ks[] = {1, n / 2, n};
        for (int caseIndex = 0; caseIndex < 3; caseIndex++) {
            int k = ks[caseIndex];
            memcpy(copy, data, n * sizeof(int));
            clock_t start = clock();
            int got = findKthLargest(copy, n, k);
            double elapsedMs = 1000.0 * (double)(clock() - start) / CLOCKS_PER_SEC;
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
        free(data);
        free(sorted);
        free(copy);
    }

    if (failures == 0) {
        printf("ALL TESTS PASSED\n");
        return 0;
    }
    printf("%d TEST(S) FAILED\n", failures);
    return 1;
}
