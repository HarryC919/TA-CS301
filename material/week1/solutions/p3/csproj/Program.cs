using System;
using System.Linq;

// Test harness for P3 (sort words by length, stably). Not shipped to students.
int failures = 0;

// Sorts a copy of `input` with the solution, compares it against `expected`,
// and checks that the caller's array was left untouched.
void Check(string[] input, string[] expected, string name)
{
    string[] inputBackup = (string[])input.Clone();
    string[] got = Solution.SortByLength(input);

    if (!input.SequenceEqual(inputBackup))
    {
        Console.WriteLine($"FAIL {name}: input array was modified");
        failures++;
        return;
    }

    if (!got.SequenceEqual(expected))
    {
        Console.WriteLine($"FAIL {name}");
        Console.WriteLine($"  got  [{string.Join(", ", got)}]");
        Console.WriteLine($"  want [{string.Join(", ", expected)}]");
        failures++;
        return;
    }

    Console.WriteLine($"PASS {name}");
}

// Builds `count` seeded random lowercase words so every run is reproducible.
string[] MakeRandomWords(int count, int maxLength, int seed)
{
    var rng = new Random(seed);
    var words = new string[count];
    for (int i = 0; i < count; i++)
    {
        int length = rng.Next(1, maxLength + 1);
        var letters = new char[length];
        for (int k = 0; k < length; k++)
        {
            letters[k] = (char)('a' + rng.Next(0, 26));
        }
        words[i] = new string(letters);
    }
    return words;
}

// Cross-checks the solution against a library stable sort. The HARNESS may use
// a library sort as the oracle; the solution itself may not.
void CheckRandom(int count, int maxLength, int seed, string name)
{
    string[] words = MakeRandomWords(count, maxLength, seed);
    // Enumerable.OrderBy is documented as a stable sort.
    string[] expected = words.OrderBy(word => word.Length).ToArray();
    Check(words, expected, name);
}

// Fixed cases from the contract.
Check(new[] { "pear", "kiwi", "apple", "fig", "banana" },
      new[] { "fig", "pear", "kiwi", "apple", "banana" },
      "case pear/kiwi/apple/fig/banana");
Check(new[] { "a" }, new[] { "a" }, "case single word [a]");
Check(new[] { "bb", "aa", "cc" }, new[] { "bb", "aa", "cc" },
      "case all equal length (order preserved)");
Check(new[] { "ccc", "a", "bb", "ab", "ba" },
      new[] { "a", "bb", "ab", "ba", "ccc" },
      "case ties keep original order");
Check(new[] { "abcd", "a", "abc", "ab" },
      new[] { "a", "ab", "abc", "abcd" },
      "case ascending lengths");
Check(new[] { "a", new string('q', 100), "bb" },
      new[] { "a", "bb", new string('q', 100) },
      "case word of 100 characters");
Check(new[] { "b", "a" }, new[] { "b", "a" },
      "case two equal-length words");

// Seeded random cross-checks against the library stable-sort oracle.
CheckRandom(1000, 100, 12345, "random n=1000, lengths 1..100 (seed 12345)");
CheckRandom(1000, 6, 999, "random n=1000, many ties (lengths 1..6, seed 999)");

if (failures == 0)
{
    Console.WriteLine("ALL TESTS PASSED");
    return 0;
}
Console.WriteLine($"{failures} TEST(S) FAILED");
return 1;
