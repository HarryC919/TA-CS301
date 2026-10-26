import importlib.util
import random
import sys
import time
from pathlib import Path

# Load py.solution.py, which cannot be imported as a normal module name
# because of the dots in its file name.
_solution_path = Path(__file__).parent / "py.solution.py"
_spec = importlib.util.spec_from_file_location("py.solution", _solution_path)
_module = importlib.util.module_from_spec(_spec)
sys.modules["py.solution"] = _module
_spec.loader.exec_module(_module)

quick_sort = _module.quick_sort

failures = 0
checks = 0


# Return the index of the first difference, or -1 when the lists are equal.
def first_mismatch(a: list[int], b: list[int]) -> int:
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            return i
    return -1 if len(a) == len(b) else min(len(a), len(b))


# Check one fixed test case: the result values and that the caller's list
# was not modified.
def check_sorted(name: str, input_values: list[int], expected: list[int]) -> None:
    global checks, failures
    checks += 1
    original = list(input_values)
    result = quick_sort(input_values)

    if len(result) != len(expected):
        print(f"FAIL {name}: length {len(result)}, want {len(expected)}")
        failures += 1
        return

    mismatch = first_mismatch(result, expected)
    if mismatch >= 0:
        print(f"FAIL {name}: index {mismatch} got {result[mismatch]}, want {expected[mismatch]}")
        failures += 1
    elif input_values != original:
        print(f"FAIL {name}: the input list was modified")
        failures += 1
    else:
        print(f"PASS {name}")


# Check one n = 200,000 case: cross-check against sorted(), confirm the input
# was not modified, and require the sort to finish well under 2 seconds.
def check_performance(name: str, input_values: list[int]) -> None:
    global checks, failures
    checks += 1
    expected = sorted(input_values)  # library sort as oracle
    original = list(input_values)

    start = time.perf_counter()
    result = quick_sort(input_values)
    seconds = time.perf_counter() - start

    if len(result) != len(expected):
        print(f"FAIL {name}: length {len(result)}, want {len(expected)}")
        failures += 1
        return

    mismatch = first_mismatch(result, expected)
    if mismatch >= 0:
        print(f"FAIL {name}: index {mismatch} got {result[mismatch]}, want {expected[mismatch]}")
        failures += 1
    elif input_values != original:
        print(f"FAIL {name}: the input list was modified")
        failures += 1
    elif seconds >= 2.0:
        print(f"FAIL {name}: {seconds:.3f} s is not well under 2 s")
        failures += 1
    else:
        print(f"PASS {name} ({seconds:.3f} s)")


# --- Fixed cases from the contract ---------------------------------------
check_sorted("[] -> []", [], [])
check_sorted("[1] -> [1]", [1], [1])
check_sorted("[5,2,4,1,3] -> [1,2,3,4,5]", [5, 2, 4, 1, 3], [1, 2, 3, 4, 5])
check_sorted("[3,1,3,3,2,3] -> [1,2,3,3,3,3]", [3, 1, 3, 3, 2, 3], [1, 2, 3, 3, 3, 3])
check_sorted("[7,7,7,7] -> unchanged", [7, 7, 7, 7], [7, 7, 7, 7])
check_sorted("[4,3,2,1] -> [1,2,3,4]", [4, 3, 2, 1], [1, 2, 3, 4])
check_sorted("[-3,5,0,-3,2] -> [-3,-3,0,2,5]", [-3, 5, 0, -3, 2], [-3, -3, 0, 2, 5])

# Seeded random cross-check against sorted(), n = 1000.
_rng = random.Random(12345)
_input = [_rng.randint(-1000000, 1000000) for _ in range(1000)]
check_sorted("random n=1000 cross-check", _input, sorted(_input))

# --- Performance cases, n = 200,000 --------------------------------------
_n = 200000
_rng = random.Random(2024)
check_performance("n=200000 random values in [0,50]", [_rng.randint(0, 50) for _ in range(_n)])
check_performance("n=200000 all-equal", [42] * _n)
check_performance("n=200000 already sorted", list(range(_n)))

print(f"\n{checks} checks, {failures} failed")
if failures > 0:
    print("FAILED")
    sys.exit(1)
print("All tests passed.")
