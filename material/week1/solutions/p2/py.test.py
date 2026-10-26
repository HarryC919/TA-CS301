"""Test harness for P2 - insertion sort counting shifts (verification only)."""

import importlib.util
import os
import random
import sys

sys.dont_write_bytecode = True  # keep the directory free of __pycache__.


def load_solution():
    """Load py.solution.py by path (its dotted file name is not importable)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "py.solution.py")
    spec = importlib.util.spec_from_file_location("py_solution", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.insertion_sort


insertion_sort = load_solution()

failures = 0


def count_inversions_brute_force(nums):
    """Oracle 1 (shift count): brute-force inversion count, O(n^2) - harness only."""
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j]:
                count += 1
    return count


def check_fixed(name, nums, expected, expected_shifts):
    global failures
    arr = list(nums)
    shifts = insertion_sort(arr)  # in place
    if shifts != expected_shifts or arr != expected:
        print(f"FAIL {name} (shifts={shifts}, expected={expected_shifts})")
        failures += 1
        return
    print(f"PASS {name} (shifts={shifts})")


def check_random(seed, n, value_range):
    global failures
    rng = random.Random(seed)
    original = [rng.randint(-value_range, value_range) for _ in range(n)]
    expected_shifts = count_inversions_brute_force(original)
    arr = list(original)
    shifts = insertion_sort(arr)  # in place
    expected = sorted(original)  # oracle 2: library sort
    if shifts != expected_shifts or arr != expected:
        print(f"FAIL random n={n} seed={seed} (shifts={shifts}, "
              f"expected={expected_shifts})")
        failures += 1
        return
    print(f"PASS random n={n} seed={seed} (shifts={shifts})")


# Fixed cases from the contract
check_fixed("case [1]", [1], [1], 0)
check_fixed("case [1,2,3]", [1, 2, 3], [1, 2, 3], 0)
check_fixed("case [3,2,1]", [3, 2, 1], [1, 2, 3], 3)
check_fixed("case [5,2,4,1]", [5, 2, 4, 1], [1, 2, 4, 5], 5)
check_fixed("case [2,2,2] equal keys", [2, 2, 2], [2, 2, 2], 0)
check_fixed("case [-1,5,0,-10] negatives", [-1, 5, 0, -10], [-10, -1, 0, 5], 4)

# Seeded random cross-checks: shifts vs brute force, array vs library sort
check_random(42, 1000, 10000)
check_random(7, 1000, 10000)
check_random(1234, 1000, 10000)
check_random(99, 1000, 3)  # heavy duplicates: stresses the strict '>' rule

if failures:
    print(f"{failures} TEST(S) FAILED")
    sys.exit(1)
print("ALL TESTS PASSED")
