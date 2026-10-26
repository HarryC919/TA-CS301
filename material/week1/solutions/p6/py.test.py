import importlib.util
import random
import sys
import time
from pathlib import Path

# The solution file is named "py.solution.py", so load it through an explicit
# module spec instead of a normal `from py.solution import ...` statement.
_solution_path = Path(__file__).resolve().parent / "py.solution.py"
_spec = importlib.util.spec_from_file_location("py_solution", str(_solution_path))
_solution = importlib.util.module_from_spec(_spec)
sys.modules["py_solution"] = _solution
_spec.loader.exec_module(_solution)

find_kth_largest = _solution.find_kth_largest
failures = 0


# Wrapper that compares one quickselect call against the expected answer.
def check(nums, k, expected, name):
    global failures
    got = find_kth_largest(list(nums), k)
    if got != expected:
        print(f"FAIL {name} (k={k}): got {got}, want {expected}")
        failures += 1
    else:
        print(f"PASS {name} (k={k} -> {got})")


# Fixed cases from the contract
check([3, 2, 1, 5, 6, 4], 2, 5, "case [3,2,1,5,6,4]")
check([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4, "case [3,2,3,1,2,4,5,5,6]")
check([1], 1, 1, "case [1]")
check([2, 1], 1, 2, "case [2,1] k=1")
check([2, 1], 2, 1, "case [2,1] k=2")
check([-1, -5, 3], 1, 3, "case [-1,-5,3]")
check([3, 3, 3], 2, 3, "case [3,3,3]")

# Regression: equal values must be removed as a band, without deep recursion.
check([3] * 2000, 1000, 3, "duplicate recursion regression")
for data, name in (([7] * 100000, "all equal"),
                   ([i % 3 - 1 for i in range(100000)], "three values"),
                   ([i // 5 - 10000 for i in range(100000)], "sorted"),
                   ([9999 - i // 5 for i in range(100000)], "reverse sorted")):
    oracle = sorted(data)
    for k in (1, len(data) // 2, len(data)):
        check(data, k, oracle[len(data) - k], name)

# Seeded random cross-check against sorted(), n = 200,000
n = 200000
rng = random.Random(42)
data = [rng.randint(-10000, 10000) for _ in range(n)]
oracle = sorted(data)
for k in (1, n // 2, n):
    copy = list(data)
    start = time.perf_counter()
    got = find_kth_largest(copy, k)
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    expected = oracle[n - k]
    if got != expected:
        print(f"FAIL random n=200000 k={k}: got {got}, want {expected}")
        failures += 1
    elif elapsed_ms > 2000.0:
        print(f"FAIL random n=200000 k={k}: too slow ({elapsed_ms:.1f} ms)")
        failures += 1
    else:
        print(f"PASS random n=200000 k={k} -> {got} ({elapsed_ms:.1f} ms)")

if failures == 0:
    print("ALL TESTS PASSED")
    sys.exit(0)
print(f"{failures} TEST(S) FAILED")
sys.exit(1)
