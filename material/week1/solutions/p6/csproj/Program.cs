using System;
using System.Diagnostics;

int failures = 0;

// Wrapper that compares one quickselect call against the expected answer.
void Check(int[] nums, int k, int expected, string name)
{
    int got = Solution.FindKthLargest(nums, k);
    if (got != expected)
    {
        Console.WriteLine($"FAIL {name} (k={k}): got {got}, want {expected}");
        failures++;
    }
    else
    {
        Console.WriteLine($"PASS {name} (k={k} -> {got})");
    }
}

// Fixed cases from the contract
Check(new[] { 3, 2, 1, 5, 6, 4 }, 2, 5, "case [3,2,1,5,6,4]");
Check(new[] { 3, 2, 3, 1, 2, 4, 5, 5, 6 }, 4, 4, "case [3,2,3,1,2,4,5,5,6]");
Check(new[] { 1 }, 1, 1, "case [1]");
Check(new[] { 2, 1 }, 1, 2, "case [2,1] k=1");
Check(new[] { 2, 1 }, 2, 1, "case [2,1] k=2");
Check(new[] { -1, -5, 3 }, 1, 3, "case [-1,-5,3]");
Check(new[] { 3, 3, 3 }, 2, 3, "case [3,3,3]");

// Regression cases: equal keys, few distinct keys, and ordered inputs.
for (int scenario = 0; scenario < 4; scenario++)
{
    var input = new int[100000];
    for (int i = 0; i < input.Length; i++)
        input[i] = scenario == 0 ? 7 : scenario == 1 ? i % 3 - 1
            : scenario == 2 ? i / 5 - 10000 : 9999 - i / 5;
    var oracle = (int[])input.Clone();
    Array.Sort(oracle);
    foreach (int k in new[] {1, input.Length / 2, input.Length})
        Check(input, k, oracle[input.Length - k], "duplicate/order regression");
}

// Seeded random cross-check against Array.Sort, n = 200,000
{
    const int n = 200000;
    var rng = new Random(42);
    var data = new int[n];
    for (int i = 0; i < n; i++)
    {
        data[i] = rng.Next(-10000, 10001); // values in [-10000, 10000]
    }
    var sorted = (int[])data.Clone();
    Array.Sort(sorted);

    int[] ks = { 1, n / 2, n };
    foreach (int k in ks)
    {
        var copy = (int[])data.Clone();
        var stopwatch = Stopwatch.StartNew();
        int got = Solution.FindKthLargest(copy, k);
        stopwatch.Stop();
        long elapsedMs = stopwatch.ElapsedMilliseconds;
        int expected = sorted[n - k];
        if (got != expected)
        {
            Console.WriteLine($"FAIL random n=200000 k={k}: got {got}, want {expected}");
            failures++;
        }
        else if (elapsedMs > 2000)
        {
            Console.WriteLine($"FAIL random n=200000 k={k}: too slow ({elapsedMs} ms)");
            failures++;
        }
        else
        {
            Console.WriteLine($"PASS random n=200000 k={k} -> {got} ({elapsedMs} ms)");
        }
    }
}

if (failures == 0)
{
    Console.WriteLine("ALL TESTS PASSED");
    return 0;
}
Console.WriteLine($"{failures} TEST(S) FAILED");
return 1;
