using System;
using System.Diagnostics;

int failures = 0;
uint randomState = 12345u;

// Verify one answer, and also check that the input array was not modified.
void Check(string name, int[] input, long expected)
{
    int[] copy = (int[])input.Clone();
    long got = Solution.CountInversions(input);
    if (got != expected)
    {
        Console.WriteLine($"FAIL {name}: got {got}, want {expected}");
        failures++;
    }
    else if (!input.AsSpan().SequenceEqual(copy))
    {
        Console.WriteLine($"FAIL {name}: input array was modified");
        failures++;
    }
    else
    {
        Console.WriteLine($"PASS {name}");
    }
}

// Reference answer: O(n^2) double loop, only for small inputs.
long BruteForce(int[] nums)
{
    long count = 0;
    for (int i = 0; i < nums.Length; i++)
    {
        for (int j = i + 1; j < nums.Length; j++)
        {
            if (nums[i] > nums[j])
            {
                count++;
            }
        }
    }
    return count;
}

// Deterministic pseudo-random generator so every run tests the same data.
uint NextRandom()
{
    randomState = randomState * 1664525u + 1013904223u;
    return randomState;
}

int[] MakeRandom(int n, int minValue, int maxValue)
{
    int[] nums = new int[n];
    ulong range = (ulong)((long)maxValue - minValue + 1);
    for (int i = 0; i < n; i++)
    {
        nums[i] = (int)(minValue + (long)(NextRandom() % range));
    }
    return nums;
}

// Count pairs with different values; used to check the large random case.
long UnequalPairCount(int[] nums)
{
    int[] sorted = (int[])nums.Clone();
    Array.Sort(sorted);
    long unequalPairs = (long)nums.Length * (nums.Length - 1) / 2;
    int runStart = 0;
    while (runStart < sorted.Length)
    {
        int runEnd = runStart + 1;
        while (runEnd < sorted.Length && sorted[runEnd] == sorted[runStart])
        {
            runEnd++;
        }
        long runLength = runEnd - runStart;
        unequalPairs -= runLength * (runLength - 1) / 2;
        runStart = runEnd;
    }
    return unequalPairs;
}

// Fixed cases from the contract.
Check("case [1]", new[] { 1 }, 0);
Check("case [1,2,3,4]", new[] { 1, 2, 3, 4 }, 0);
Check("case [4,3,2,1]", new[] { 4, 3, 2, 1 }, 6);
Check("case [8,4,2,1]", new[] { 8, 4, 2, 1 }, 6);
Check("case [1,20,6,4,5]", new[] { 1, 20, 6, 4, 5 }, 5);
Check("case [2,2,2] (strict >)", new[] { 2, 2, 2 }, 0);

// Seeded random cross-check against the brute-force answer.
int[] randomSizes = { 1, 2, 3, 5, 10, 50, 300, 2000 };
foreach (int n in randomSizes)
{
    int[] nums = MakeRandom(n, -10000, 10000);
    Check($"random n={n} vs brute force", nums, BruteForce(nums));
}

// A descending array of 100,000 elements has n*(n-1)/2 = 4,999,950,000
// inversions, which does not fit in 32 bits.
const int LargeSize = 100000;
int[] descending = new int[LargeSize];
for (int i = 0; i < LargeSize; i++)
{
    descending[i] = LargeSize - i;
}
Check("descending 100,000 (64-bit)", descending, 4999950000L);

// Performance run on a random array of 100,000 values.
int[] large = MakeRandom(LargeSize, -1000000000, 1000000000);
int[] largeCopy = (int[])large.Clone();
Stopwatch stopwatch = Stopwatch.StartNew();
long largeCount = Solution.CountInversions(large);
stopwatch.Stop();
double seconds = stopwatch.Elapsed.TotalSeconds;
if (!large.AsSpan().SequenceEqual(largeCopy))
{
    Console.WriteLine("FAIL perf n=100,000: input array was modified");
    failures++;
}
else if (seconds > 2.0)
{
    Console.WriteLine($"FAIL perf n=100,000: {seconds:F3} s (expected under 2 s)");
    failures++;
}
else
{
    Console.WriteLine($"PASS perf n=100,000 ({seconds:F3} s)");
}

// Cross-check the large answer without O(n^2) work: for every pair of
// different values exactly one of the two orders is an inversion, so
// count(nums) + count(reverse(nums)) equals the number of unequal pairs.
int[] reversedLarge = (int[])large.Clone();
Array.Reverse(reversedLarge);
long reversedCount = Solution.CountInversions(reversedLarge);
long unequalPairs = UnequalPairCount(large);
if (largeCount + reversedCount == unequalPairs)
{
    Console.WriteLine("PASS large random consistency: count + reversed = unequal pairs");
}
else
{
    Console.WriteLine($"FAIL large random consistency: {largeCount} + {reversedCount} != {unequalPairs}");
    failures++;
}

if (failures == 0)
{
    Console.WriteLine("ALL TESTS PASSED");
    return 0;
}
Console.WriteLine($"{failures} TEST(S) FAILED");
return 1;
