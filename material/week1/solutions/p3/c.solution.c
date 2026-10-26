#include <string.h>

// Sort by length, stably, using insertion sort.
// Time: O(n^2) worst, O(n) best (already ordered by length). Space: O(1).
// NOTE: sorts the array of pointers IN PLACE — the char* entries are
// rearranged; the string contents are never modified.
void sortByLength(char** words, int wordsSize) {
    for (int i = 1; i < wordsSize; i++) {
        char* key = words[i];
        int keyLength = (int)strlen(key);
        int j = i - 1;

        // 1. Shift longer words one slot to the right.
        //    Strict '>' (not >=) keeps equal-length words in original order.
        while (j >= 0 && (int)strlen(words[j]) > keyLength) {
            words[j + 1] = words[j];
            j--;
        }

        // 2. Drop the key into the gap.
        words[j + 1] = key;
    }
}
