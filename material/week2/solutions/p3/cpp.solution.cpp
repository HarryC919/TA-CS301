#include <vector>
// Time: O(n + m). Output: O(n + m). Extra working space: O(1).
std::vector<int> mergeSorted(const std::vector<int>& left, const std::vector<int>& right) {
    std::vector<int> result;
    result.reserve(left.size() + right.size());
    size_t i = 0, j = 0;
    // Choose the smaller remaining head; choose left on ties.
    while (i < left.size() && j < right.size()) {
        if (left[i] <= right[j]) result.push_back(left[i++]);
        else result.push_back(right[j++]);
    }
    // Copy either remaining tail.
    while (i < left.size()) result.push_back(left[i++]);
    while (j < right.size()) result.push_back(right[j++]);
    return result;
}
