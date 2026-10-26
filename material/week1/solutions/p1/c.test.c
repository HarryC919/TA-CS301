#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void bubbleSort(int* nums, int numsSize);

static int failures = 0;

// Copies input, sorts it with bubbleSort, compares against expected.
static void check(const int* input, int n, const int* expected, const char* name) {
    int* a = malloc(n * sizeof(int));
    memcpy(a, input, n * sizeof(int));
    bubbleSort(a, n);
    for (int i = 0; i < n; i++) {
        if (a[i] != expected[i]) {
            printf("FAIL %s: index %d got %d, want %d\n", name, i, a[i], expected[i]);
            failures++;
            free(a);
            return;
        }
    }
    printf("PASS %s\n", name);
    free(a);
}

static int cmpInt(const void* pa, const void* pb) {
    int a = *(const int*)pa, b = *(const int*)pb;
    return (a > b) - (a < b);
}

int main(void) {
    // Fixed cases from the contract
    {
        int in[] = {1}, exp[] = {1};
        check(in, 1, exp, "case [1]");
    }
    {
        int in[] = {5, 2, 4, 1, 3}, exp[] = {1, 2, 3, 4, 5};
        check(in, 5, exp, "case [5,2,4,1,3]");
    }
    {
        int in[] = {1, 2, 3, 4}, exp[] = {1, 2, 3, 4};
        check(in, 4, exp, "case [1,2,3,4] already sorted");
    }
    {
        int in[] = {4, 3, 2, 1}, exp[] = {1, 2, 3, 4};
        check(in, 4, exp, "case [4,3,2,1] reverse sorted");
    }
    {
        int in[] = {2, 2, 1, 3, 2}, exp[] = {1, 2, 2, 2, 3};
        check(in, 5, exp, "case [2,2,1,3,2] duplicates");
    }
    {
        int in[] = {-1, 5, 0, -10}, exp[] = {-10, -1, 0, 5};
        check(in, 4, exp, "case [-1,5,0,-10] negatives");
    }

    // Seeded random cross-check vs library sort (qsort), n = 1000
    {
        const int n = 1000;
        int* a = malloc(n * sizeof(int));
        int* b = malloc(n * sizeof(int));
        srand(42);
        for (int i = 0; i < n; i++) {
            a[i] = (rand() % 20001) - 10000;  // values in [-10000, 10000]
            b[i] = a[i];
        }
        clock_t t0 = clock();
        bubbleSort(a, n);  // in place
        double ms = 1000.0 * (clock() - t0) / CLOCKS_PER_SEC;
        qsort(b, n, sizeof(int), cmpInt);
        if (memcmp(a, b, n * sizeof(int)) != 0) {
            printf("FAIL case random n=1000 vs qsort\n");
            failures++;
        } else {
            printf("PASS case random n=1000 vs qsort (%.1f ms)\n", ms);
        }
        free(a);
        free(b);
    }

    // Performance: worst case, n = 1000 reverse sorted (full n^2 passes)
    {
        const int n = 1000;
        int* a = malloc(n * sizeof(int));
        for (int i = 0; i < n; i++) {
            a[i] = n - i;
        }
        clock_t t0 = clock();
        bubbleSort(a, n);
        double ms = 1000.0 * (clock() - t0) / CLOCKS_PER_SEC;
        int ok = 1;
        for (int i = 0; i < n; i++) {
            if (a[i] != i + 1) ok = 0;
        }
        if (!ok) {
            printf("FAIL case perf reverse n=1000: not sorted\n");
            failures++;
        } else if (ms > 2000.0) {
            printf("FAIL case perf reverse n=1000: too slow (%.1f ms)\n", ms);
            failures++;
        } else {
            printf("PASS case perf reverse n=1000 (%.1f ms)\n", ms);
        }
        free(a);
    }

    if (failures == 0) {
        printf("ALL TESTS PASSED\n");
        return 0;
    }
    printf("%d TEST(S) FAILED\n", failures);
    return 1;
}
