"""Test harness for P1 - bubble sort with early exit (verification only)."""

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
    return module.bubble_sort


bubble_sort = load_solution()

failures = 0


def check(nums, expected, name):
    global failures
    bubble_sort(nums)  # in place
    if nums != expected:
        print(f"FAIL {name}: got {nums}, want {expected}")
        failures += 1
        return
    print(f"PASS {name}")


# Fixed cases from the contract
check([1], [1], "case [1]")
check([5, 2, 4, 1, 3], [1, 2, 3, 4, 5], "case [5,2,4,1,3]")
check([1, 2, 3, 4], [1, 2, 3, 4], "case [1,2,3,4] already sorted (early exit)")
check([4, 3, 2, 1], [1, 2, 3, 4], "case [4,3,2,1] reverse sorted")
check([2, 2, 1, 3, 2], [1, 2, 2, 2, 3], "case [2,2,1,3,2] duplicates")
check([-1, 5, 0, -10], [-10, -1, 0, 5], "case [-1,5,0,-10] negatives")

# Seeded random cross-check vs library sort, n = 1000
rng = random.Random(42)
data = [rng.randint(-10000, 10000) for _ in range(1000)]
actual = list(data)
bubble_sort(actual)
expected = sorted(data)  # the harness may use a library sort as the oracle
if actual != expected:
    print("FAIL case random n=1000 vs sorted()")
    failures += 1
else:
    print("PASS case random n=1000 vs sorted()")

if failures:
    print(f"{failures} TEST(S) FAILED")
    sys.exit(1)
print("ALL TESTS PASSED")
