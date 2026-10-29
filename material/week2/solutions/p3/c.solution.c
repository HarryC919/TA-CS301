#include <stdlib.h>
// Time: O(n + m). Output: O(n + m). Extra working space: O(1).
int* mergeSorted(const int* left, int leftSize, const int* right, int rightSize, int* returnSize) {
    int total = leftSize + rightSize;
    *returnSize = 0;
    if (total == 0) return NULL;
    int* result = malloc((size_t)total * sizeof(int));
    if (result == NULL) return NULL;
    int i = 0, j = 0, k = 0;
    // Choose the smaller remaining head; choose left on ties.
    while (i < leftSize && j < rightSize) {
        if (left[i] <= right[j]) result[k++] = left[i++];
        else result[k++] = right[j++];
    }
    // Copy either remaining tail.
    while (i < leftSize) result[k++] = left[i++];
    while (j < rightSize) result[k++] = right[j++];
    *returnSize = total;
    return result;
}
