// Re-run the Solution definition cell before running this check cell.
// These checks throw while the starter is still unchanged.
java.util.function.BiPredicate<String, String> isSubsequence = (s, t) -> {
    int k = 0;
    for (int i = 0; i < t.length() && k < s.length(); i++) if (s.charAt(k) == t.charAt(i)) k++;
    return k == s.length();
};
String[][] cases = {
    {"", "", "0"}, {"", "ABC", "0"}, {"ABC", "DEF", "0"}, {"a", "A", "0"},
    {"ABCB", "BDCAB", "3"}, {"ABCBDAB", "BDCABA", "4"}, {"AGGTAB", "GXTXAYB", "4"},
    {"ABC", "ABC", "3"}, {"ACE", "ABCDE", "3"}, {"AAAA", "AA", "2"}
};
for (String[] test : cases) {
    String result = Solution.longestCommonSubsequence(test[0], test[1]);
    if (result == null || result.length() != Integer.parseInt(test[2]))
        throw new AssertionError("Wrong LCS length for " + test[0] + ", " + test[1] + ": " + result);
    if (!isSubsequence.test(result, test[0]) || !isSubsequence.test(result, test[1]))
        throw new AssertionError("Not a common subsequence: " + result);
}
String large = Solution.longestCommonSubsequence("AB".repeat(500), "BA".repeat(500));
if (large == null || large.length() != 999 || !isSubsequence.test(large, "AB".repeat(500))
        || !isSubsequence.test(large, "BA".repeat(500)))
    throw new AssertionError("Check the 1,000 x 1,000 case");
System.out.println("Exercise 2 checks passed (10 cases + 1,000 x 1,000 input).");
