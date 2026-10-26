using System;
using System.Diagnostics;

int failures = 0;

void Check(int[] input, int[] expected, string name)
{
    int[] a = (int[])input.Clone();
    Solution.BubbleSort(a); // in place
    for (int i = 0; i < a.Length; i++)
    {
        if (a[i] != expected[i])
        {
            Console.WriteLine($"FAIL {name}: index {i} got {a[i]}, want {expected[i]}");
            failures++;
            return;
        }
    }
    Console.WriteLine($"PASS {name}");
}

// Fixed cases from the contract
Check(new[] { 1 }, new[] { 1 }, "case [1]");
Check(new[] { 5, 2, 4, 1, 3 }, new[] { 1, 2, 3, 4, 5 }, "case [5,2,4,1,3]");
Check(new[] { 1, 2, 3, 4 }, new[] { 1, 2, 3, 4 }, "case [1,2,3,4] already sorted");
Check(new[] { 4, 3, 2, 1 }, new[] { 1, 2, 3, 4 }, "case [4,3,2,1] reverse sorted");
Check(new[] { 2, 2, 1, 3, 2 }, new[] { 1, 2, 2, 2, 3 }, "case [2,2,1,3,2] duplicates");
Check(new[] { -1, 5, 0, -10 }, new[] { -10, -1, 0, 5 }, "case [-1,5,0,-10] negatives");

// Seeded random cross-check vs library sort, n = 1000
{
    const int n = 1000;
    var rng = new Random(42);
    var a = new int[n];
    var b = new int[n];
    for (int i = 0; i < n; i++)
    {
        a[i] = rng.Next(-10000, 10001); // values in [-10000, 10000]
        b[i] = a[i];
    }
    var sw = Stopwatch.StartNew();
    Solution.BubbleSort(a); // in place
    sw.Stop();
    Array.Sort(b);
    bool ok = true;
    for (int i = 0; i < n && ok; i++)
    {
        if (a[i] != b[i]) ok = false;
    }
    if (!ok)
    {
        Console.WriteLine("FAIL case random n=1000 vs Array.Sort");
        failures++;
    }
    else
    {
        Console.WriteLine($"PASS case random n=1000 vs Array.Sort ({sw.ElapsedMilliseconds} ms)");
    }
}

// Performance: worst case, n = 1000 reverse sorted (full n^2 passes)
{
    const int n = 1000;
    var a = new int[n];
    for (int i = 0; i < n; i++)
    {
        a[i] = n - i;
    }
    var sw = Stopwatch.StartNew();
    Solution.BubbleSort(a);
    sw.Stop();
    bool ok = true;
    for (int i = 0; i < n && ok; i++)
    {
        if (a[i] != i + 1) ok = false;
    }
    if (!ok)
    {
        Console.WriteLine("FAIL case perf reverse n=1000: not sorted");
        failures++;
    }
    else if (sw.ElapsedMilliseconds > 2000)
    {
        Console.WriteLine($"FAIL case perf reverse n=1000: too slow ({sw.ElapsedMilliseconds} ms)");
        failures++;
    }
    else
    {
        Console.WriteLine($"PASS case perf reverse n=1000 ({sw.ElapsedMilliseconds} ms)");
    }
}

if (failures == 0)
{
    Console.WriteLine("ALL TESTS PASSED");
    return 0;
}
Console.WriteLine($"{failures} TEST(S) FAILED");
return 1;
