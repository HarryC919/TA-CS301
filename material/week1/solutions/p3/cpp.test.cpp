// Test harness for P3 (sort words by length, stably). Not shipped to students.
#include <algorithm>
#include <cstdio>
#include <random>
#include <string>
#include <vector>

// Defined in cpp.solution.cpp (solution files carry no header of their own).
std::vector<std::string> sortByLength(std::vector<std::string> words);

static int failures = 0;

// Prints one string array (used only in failure messages).
static void printWords(const char* label, const std::vector<std::string>& words) {
    printf("%s: [", label);
    for (size_t i = 0; i < words.size(); i++) {
        printf("%s\"%s\"", i == 0 ? "" : ", ", words[i].c_str());
    }
    printf("]\n");
}

// Sorts a copy of `input` with the solution, compares it against `expected`,
// and checks that the caller's vector was left untouched.
static void checkCase(const std::vector<std::string>& input,
                      const std::vector<std::string>& expected,
                      const char* name) {
    std::vector<std::string> inputBackup = input;
    std::vector<std::string> got = sortByLength(input);

    if (input != inputBackup) {
        printf("FAIL %s: input vector was modified\n", name);
        failures++;
        return;
    }

    if (got != expected) {
        printf("FAIL %s\n", name);
        printWords("  got ", got);
        printWords("  want", expected);
        failures++;
        return;
    }

    printf("PASS %s\n", name);
}

// Builds `count` seeded random lowercase words so every run is reproducible.
static std::vector<std::string> makeRandomWords(int count, int maxLength,
                                                unsigned int seed) {
    std::mt19937 generator(seed);
    std::uniform_int_distribution<int> lengthDistribution(1, maxLength);
    std::uniform_int_distribution<int> letterDistribution(0, 25);

    std::vector<std::string> words;
    words.reserve((size_t)count);
    for (int i = 0; i < count; i++) {
        int length = lengthDistribution(generator);
        std::string word;
        word.reserve((size_t)length);
        for (int k = 0; k < length; k++) {
            word.push_back((char)('a' + letterDistribution(generator)));
        }
        words.push_back(word);
    }
    return words;
}

// Cross-checks the solution against a library stable sort. The HARNESS may use
// a library sort as the oracle; the solution itself may not.
static void checkRandom(int count, int maxLength, unsigned int seed,
                        const char* name) {
    std::vector<std::string> words = makeRandomWords(count, maxLength, seed);
    std::vector<std::string> expected = words;
    std::stable_sort(expected.begin(), expected.end(),
                     [](const std::string& a, const std::string& b) {
                         return a.size() < b.size();
                     });
    checkCase(words, expected, name);
}

int main() {
    // Fixed cases from the contract.
    checkCase({"pear", "kiwi", "apple", "fig", "banana"},
              {"fig", "pear", "kiwi", "apple", "banana"},
              "case pear/kiwi/apple/fig/banana");
    checkCase({"a"}, {"a"}, "case single word [a]");
    checkCase({"bb", "aa", "cc"}, {"bb", "aa", "cc"},
              "case all equal length (order preserved)");
    checkCase({"ccc", "a", "bb", "ab", "ba"}, {"a", "bb", "ab", "ba", "ccc"},
              "case ties keep original order");
    checkCase({"abcd", "a", "abc", "ab"}, {"a", "ab", "abc", "abcd"},
              "case ascending lengths");
    checkCase({"a", std::string(100, 'q'), "bb"},
              {"a", "bb", std::string(100, 'q')},
              "case word of 100 characters");
    checkCase({"b", "a"}, {"b", "a"}, "case two equal-length words");

    // Seeded random cross-checks against the library stable-sort oracle.
    checkRandom(1000, 100, 12345, "random n=1000, lengths 1..100 (seed 12345)");
    checkRandom(1000, 6, 999, "random n=1000, many ties (lengths 1..6, seed 999)");

    if (failures == 0) {
        printf("ALL TESTS PASSED\n");
        return 0;
    }
    printf("%d TEST(S) FAILED\n", failures);
    return 1;
}
