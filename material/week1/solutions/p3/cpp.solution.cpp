#include <string>
#include <vector>

// Sort by length, stably, using insertion sort.
// Time: O(n^2) worst, O(n) best (already ordered by length). Space: O(1) extra.
// Takes the vector by value and returns it sorted, so the caller's
// array is never modified.
std::vector<std::string> sortByLength(std::vector<std::string> words) {
    for (int i = 1; i < (int)words.size(); i++) {
        std::string key = words[i];
        int keyLength = (int)key.size();
        int j = i - 1;

        // 1. Shift longer words one slot to the right.
        //    Strict '>' (not >=) keeps equal-length words in original order.
        while (j >= 0 && (int)words[j].size() > keyLength) {
            words[j + 1] = words[j];
            j--;
        }

        // 2. Drop the key into the gap.
        words[j + 1] = key;
    }
    return words;
}
