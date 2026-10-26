using System;
using System.Diagnostics;
using System.Linq;

int failures = 0;
int checks = 0;

int[] CopyArray(int[] source)
{
    int[] copy = new int[source.Length];
    Array.Copy(source, copy, source.Length);
    return copy;
}

// Return the index of the first difference, or -1 when the arrays are equal.
int FirstMismatch(int[] a, int[] b)
{
    int n = Math.Min(a.Length, b.Length);
    for (int i = 0; i < n; i++)
    {
        if (a[i] != b[i])
        {
            return i;
        }
    }
    return a.Length == b.Length ? -1 : n;
}

// Print the first mismatching position for a failed test case.
void PrintMismatch(string name, int[] result, int[] expected, int mismatch)
{
    Console.WriteLine($"FAIL {name}: index {mismatch} got {result[mismatch]}, " +
                      $"want {expected[mismatch]}");
}

// Check one fixed test case: the result values and that the caller's array was not modified.
void CheckSorted(string name, int[] input, int[] expected)
{
    checks++;
    int[] inputCopy = CopyArray(input);
    int[] result = Solution.QuickSort(input);

    if (result.Length != expected.Length)
    {
        Console.WriteLine($"FAIL {name}: length {result.Length}, want {expected.Length}");
        failures++;
        return;
    }

    int mismatch = FirstMismatch(result, expected);
    if (mismatch >= 0)
    {
        PrintMismatch(name, result, expected, mismatch);
        failures++;
    }
    else if (!input.SequenceEqual(inputCopy))
    {
        Console.WriteLine($"FAIL {name}: the input array was modified");
        failures++;
    }
    else
    {
        Console.WriteLine($"PASS {name}");
    }
}

// Check one n = 200,000 case: cross-check against Array.Sort, confirm the input
// was not modified, and require the sort to finish well under 2 seconds.
void CheckPerformance(string name, int[] input)
{
    checks++;
    int[] expected = CopyArray(input);
    Array.Sort(expected);  // library sort as oracle
    int[] inputCopy = CopyArray(input);

    var watch = Stopwatch.StartNew();
    int[] result = Solution.QuickSort(input);
    watch.Stop();
    double seconds = watch.Elapsed.TotalSeconds;

    if (result.Length != expected.Length)
    {
        Console.WriteLine($"FAIL {name}: length {result.Length}, want {expected.Length}");
        failures++;
        return;
    }

    int mismatch = FirstMismatch(result, expected);
    if (mismatch >= 0)
    {
        PrintMismatch(name, result, expected, mismatch);
        failures++;
    }
    else if (!input.SequenceEqual(inputCopy))
    {
        Console.WriteLine($"FAIL {name}: the input array was modified");
        failures++;
    }
    else if (seconds >= 2.0)
    {
        Console.WriteLine($"FAIL {name}: {seconds:F3} s is not well under 2 s");
        failures++;
    }
    else
    {
        Console.WriteLine($"PASS {name} ({seconds:F3} s)");
    }
}

// --- Fixed cases from the contract ---------------------------------------
CheckSorted("[] -> []", Array.Empty<int>(), Array.Empty<int>());
CheckSorted("[1] -> [1]", new[] { 1 }, new[] { 1 });
CheckSorted("[5,2,4,1,3] -> [1,2,3,4,5]",
    new[] { 5, 2, 4, 1, 3 }, new[] { 1, 2, 3, 4, 5 });
CheckSorted("[3,1,3,3,2,3] -> [1,2,3,3,3,3]",
    new[] { 3, 1, 3, 3, 2, 3 }, new[] { 1, 2, 3, 3, 3, 3 });
CheckSorted("[7,7,7,7] -> unchanged",
    new[] { 7, 7, 7, 7 }, new[] { 7, 7, 7, 7 });
CheckSorted("[4,3,2,1] -> [1,2,3,4]",
    new[] { 4, 3, 2, 1 }, new[] { 1, 2, 3, 4 });
CheckSorted("[-3,5,0,-3,2] -> [-3,-3,0,2,5]",
    new[] { -3, 5, 0, -3, 2 }, new[] { -3, -3, 0, 2, 5 });

// Seeded random cross-check against Array.Sort, n = 1000.
{
    const int count = 1000;
    var rng = new Random(12345);
    int[] input = new int[count];
    for (int i = 0; i < count; i++)
    {
        input[i] = rng.Next(-1000000, 1000001);
    }
    int[] expected = CopyArray(input);
    Array.Sort(expected);
    CheckSorted("random n=1000 cross-check", input, expected);
}

// --- Performance cases, n = 200,000 --------------------------------------
const int n = 200000;
{
    var rng = new Random(2024);
    int[] input = new int[n];
    for (int i = 0; i < n; i++)
    {
        input[i] = rng.Next(0, 51);  // values in [0,50]: heavy duplicates
    }
    CheckPerformance("n=200000 random values in [0,50]", input);
}
{
    int[] input = Enumerable.Repeat(42, n).ToArray();  // all equal
    CheckPerformance("n=200000 all-equal", input);
}
{
    int[] input = Enumerable.Range(0, n).ToArray();  // already sorted
    CheckPerformance("n=200000 already sorted", input);
}

Console.WriteLine($"\n{checks} checks, {failures} failed");
if (failures > 0)
{
    Console.WriteLine("FAILED");
    return 1;
}
Console.WriteLine("All tests passed.");
return 0;
