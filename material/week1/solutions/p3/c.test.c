// Test harness for P3 (sort words by length, stably). Not shipped to students.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sortByLength(char** words, int wordsSize);

static int failures = 0;

// Prints one string array (used only in failure messages).
static void printWords(const char* label, char** words, int count) {
    printf("%s: [", label);
    for (int i = 0; i < count; i++) {
        printf("%s\"%s\"", i == 0 ? "" : ", ", words[i]);
    }
    printf("]\n");
}

// Compares two string arrays element by element.
static int sameWords(char** got, char** want, int count) {
    for (int i = 0; i < count; i++) {
        if (strcmp(got[i], want[i]) != 0) {
            return 0;
        }
    }
    return 1;
}

// True if `after` holds exactly the same pointers as `before`, each used once.
// This proves the solution rearranged the pointer array instead of copying or
// dropping strings.
static int samePointerMultiset(char** before, char** after, int count) {
    int* used = calloc((size_t)count, sizeof(int));
    int ok = 1;
    for (int i = 0; i < count && ok; i++) {
        ok = 0;
        for (int j = 0; j < count; j++) {
            if (!used[j] && after[i] == before[j]) {
                used[j] = 1;
                ok = 1;
                break;
            }
        }
    }
    free(used);
    return ok;
}

// Sorts a copy of `input` with the solution, compares it against `expected`,
// and checks that only the pointers moved (the strings themselves are intact).
static void checkCase(char** input, int count, char** expected, const char* name) {
    char** work = malloc((size_t)count * sizeof(char*));
    for (int i = 0; i < count; i++) {
        work[i] = input[i];
    }

    sortByLength(work, count);

    if (!sameWords(work, expected, count)) {
        printf("FAIL %s\n", name);
        printWords("  got ", work, count);
        printWords("  want", expected, count);
        failures++;
    } else if (!samePointerMultiset(input, work, count)) {
        printf("FAIL %s: solution copied or dropped strings (expected in place)\n", name);
        failures++;
    } else {
        printf("PASS %s\n", name);
    }

    free(work);
}

#define RANDOM_COUNT 1000
#define MAX_WORD_LENGTH 100

// One entry for the library stable-sort oracle: a word plus its original
// index, so equal lengths can keep their original relative order.
typedef struct {
    char* word;
    int originalIndex;
} OracleItem;

// qsort comparator for the oracle: shorter word first, and equal lengths by
// original index. The ORACLE may use a library sort; the solution may not.
static int compareOracle(const void* a, const void* b) {
    const OracleItem* first = (const OracleItem*)a;
    const OracleItem* second = (const OracleItem*)b;
    size_t firstLength = strlen(first->word);
    size_t secondLength = strlen(second->word);
    if (firstLength < secondLength) {
        return -1;
    }
    if (firstLength > secondLength) {
        return 1;
    }
    return first->originalIndex - second->originalIndex;
}

// Builds `count` seeded random lowercase words, sorts them with the solution,
// and cross-checks the result against the oracle.
static void checkRandom(int count, int maxLength, unsigned int seed, const char* name) {
    static char buffers[RANDOM_COUNT][MAX_WORD_LENGTH + 1];
    char* words[RANDOM_COUNT];
    char* before[RANDOM_COUNT];
    char* expected[RANDOM_COUNT];
    OracleItem items[RANDOM_COUNT];

    srand(seed);
    for (int i = 0; i < count; i++) {
        int length = 1 + rand() % maxLength;
        for (int k = 0; k < length; k++) {
            buffers[i][k] = (char)('a' + rand() % 26);
        }
        buffers[i][length] = '\0';
        words[i] = buffers[i];
        before[i] = words[i];
    }

    for (int i = 0; i < count; i++) {
        items[i].word = words[i];
        items[i].originalIndex = i;
    }
    qsort(items, (size_t)count, sizeof(OracleItem), compareOracle);
    for (int i = 0; i < count; i++) {
        expected[i] = items[i].word;
    }

    sortByLength(words, count);

    if (!sameWords(words, expected, count)) {
        printf("FAIL %s\n", name);
        failures++;
    } else if (!samePointerMultiset(before, words, count)) {
        printf("FAIL %s: solution copied or dropped strings (expected in place)\n", name);
        failures++;
    } else {
        printf("PASS %s\n", name);
    }
}

int main(void) {
    // Fixed cases from the contract.
    {
        char* input[] = {"pear", "kiwi", "apple", "fig", "banana"};
        char* expected[] = {"fig", "pear", "kiwi", "apple", "banana"};
        checkCase(input, 5, expected, "case pear/kiwi/apple/fig/banana");
    }
    {
        char* input[] = {"a"};
        char* expected[] = {"a"};
        checkCase(input, 1, expected, "case single word [a]");
    }
    {
        // All words the same length: the output must equal the input order.
        char* input[] = {"bb", "aa", "cc"};
        char* expected[] = {"bb", "aa", "cc"};
        checkCase(input, 3, expected, "case all equal length (order preserved)");
    }
    {
        // "bb", "ab", and "ba" all have length 2 and keep their input order.
        char* input[] = {"ccc", "a", "bb", "ab", "ba"};
        char* expected[] = {"a", "bb", "ab", "ba", "ccc"};
        checkCase(input, 5, expected, "case ties keep original order");
    }
    {
        char* input[] = {"abcd", "a", "abc", "ab"};
        char* expected[] = {"a", "ab", "abc", "abcd"};
        checkCase(input, 4, expected, "case ascending lengths");
    }
    {
        // Longest allowed word: 100 lowercase letters.
        char longest[MAX_WORD_LENGTH + 1];
        memset(longest, 'q', MAX_WORD_LENGTH);
        longest[MAX_WORD_LENGTH] = '\0';
        char* input[] = {"a", longest, "bb"};
        char* expected[] = {"a", "bb", longest};
        checkCase(input, 3, expected, "case word of 100 characters");
    }
    {
        char* input[] = {"b", "a"};
        char* expected[] = {"b", "a"};
        checkCase(input, 2, expected, "case two equal-length words");
    }

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
