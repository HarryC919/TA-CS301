using System;

int failures = 0;

// Oracle 1 (shift count): brute-force inversion count, O(n^2) - harness only.
long CountInversionsBruteForce(int[] nums)
{
    long count = 0;
    for (int i = 0; i < nums.Length; i++)
    {
        for (int j = i + 1; j < nums.Length; j++)
        {
            if (nums[i] > nums[j]) count++;
        }
    }
    return count;
}

void CheckFixed(string name, int[] input, int[] expected, int expectedShifts)
{
    int[] nums = (int[])input.Clone();
    int shifts = Solution.InsertionSort(nums); // in place
    bool ok = shifts == expectedShifts;
    for (int i = 0; i < nums.Length && ok; i++)
    {
        ok = nums[i] == expected[i];
    }
    if (!ok)
    {
        Console.WriteLine($"FAIL {name} (shifts={shifts}, expected={expectedShifts})");
        failures++;
        return;
    }
    Console.WriteLine($"PASS {name} (shifts={shifts})");
}

void CheckRandom(int seed, int n, int valueRange)
{
    var rng = new Random(seed);
    var original = new int[n];
    for (int i = 0; i < n; i++)
    {
        original[i] = rng.Next(-valueRange, valueRange + 1); // values in [-valueRange, valueRange]
    }
    long expectedShifts = CountInversionsBruteForce(original);
    var nums = (int[])original.Clone();
    int shifts = Solution.InsertionSort(nums);
    Array.Sort(original); // oracle: library sort
    bool ok = shifts == expectedShifts;
    for (int i = 0; i < n && ok; i++)
    {
        ok = nums[i] == original[i];
    }
    if (!ok)
    {
        Console.WriteLine(
            $"FAIL random n={n} seed={seed} (shifts={shifts}, expected={expectedShifts})");
        failures++;
        return;
    }
    Console.WriteLine($"PASS random n={n} seed={seed} (shifts={shifts})");
}

// Fixed cases from the contract
CheckFixed("case [1]", new[] { 1 }, new[] { 1 }, 0);
CheckFixed("case [1,2,3]", new[] { 1, 2, 3 }, new[] { 1, 2, 3 }, 0);
CheckFixed("case [3,2,1]", new[] { 3, 2, 1 }, new[] { 1, 2, 3 }, 3);
CheckFixed("case [5,2,4,1]", new[] { 5, 2, 4, 1 }, new[] { 1, 2, 4, 5 }, 5);
CheckFixed("case [2,2,2] equal keys", new[] { 2, 2, 2 }, new[] { 2, 2, 2 }, 0);
CheckFixed("case [-1,5,0,-10] negatives", new[] { -1, 5, 0, -10 }, new[] { -10, -1, 0, 5 }, 4);

// Seeded random cross-checks: shifts vs brute force, array vs library sort
CheckRandom(42, 1000, 10000);
CheckRandom(7, 1000, 10000);
CheckRandom(1234, 1000, 10000);
CheckRandom(99, 1000, 3); // heavy duplicates: stresses the strict '>' rule

if (failures == 0)
{
    Console.WriteLine("ALL TESTS PASSED");
    return 0;
}
Console.WriteLine($"{failures} TEST(S) FAILED");
return 1;
