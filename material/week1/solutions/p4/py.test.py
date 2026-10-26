import importlib.util
import sys
import time
from pathlib import Path

# The solution file is literally named "py.solution.py", so load it by path and
# register it under that dotted name (a flat file is not importable by itself).
_spec = importlib.util.spec_from_file_location(
    "py.solution", Path(__file__).parent / "py.solution.py"
)
_module = importlib.util.module_from_spec(_spec)
sys.modules["py.solution"] = _module
_spec.loader.exec_module(_module)

from py.solution import count_inversions  # noqa: E402

failures = 0
random_state = 12345


def check(name, input_list, expected):
    """Verify one answer, and also check that the input list was not modified."""
    global failures
    copied = input_list[:]
    got = count_inversions(input_list)
    if got != expected:
        print(f"FAIL {name}: got {got}, want {expected}")
        failures += 1
    elif input_list != copied:
        print(f"FAIL {name}: input array was modified")
        failures += 1
    else:
        print(f"PASS {name}")


def brute_force(nums):
    """Reference answer: O(n^2) double loop, only for small inputs."""
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j]:
                count += 1
    return count


def next_random():
    """Deterministic pseudo-random generator so every run tests the same data."""
    global random_state
    random_state = (random_state * 1664525 + 1013904223) & 0xFFFFFFFF
    return random_state


def make_random(n, min_value, max_value):
    span = max_value - min_value + 1
    return [min_value + next_random() % span for _ in range(n)]


def unequal_pair_count(nums):
    """Count pairs with different values; used to check the large random case."""
    ordered = sorted(nums)
    unequal_pairs = len(nums) * (len(nums) - 1) // 2
    run_start = 0
    while run_start < len(ordered):
        run_end = run_start + 1
        while run_end < len(ordered) and ordered[run_end] == ordered[run_start]:
            run_end += 1
        run_length = run_end - run_start
        unequal_pairs -= run_length * (run_length - 1) // 2
        run_start = run_end
    return unequal_pairs


# Fixed cases from the contract.
check("case [1]", [1], 0)
check("case [1,2,3,4]", [1, 2, 3, 4], 0)
check("case [4,3,2,1]", [4, 3, 2, 1], 6)
check("case [8,4,2,1]", [8, 4, 2, 1], 6)
check("case [1,20,6,4,5]", [1, 20, 6, 4, 5], 5)
check("case [2,2,2] (strict >)", [2, 2, 2], 0)

# Seeded random cross-check against the brute-force answer.
for n in [1, 2, 3, 5, 10, 50, 300, 2000]:
    nums = make_random(n, -10000, 10000)
    check(f"random n={n} vs brute force", nums, brute_force(nums))

# A descending array of 100,000 elements has n*(n-1)/2 = 4,999,950,000
# inversions, which does not fit in 32 bits.
large_size = 100000
descending = [large_size - i for i in range(large_size)]
check("descending 100,000 (64-bit)", descending, 4999950000)

# Performance run on a random array of 100,000 values.
large = make_random(large_size, -1000000000, 1000000000)
large_copy = large[:]
start = time.perf_counter()
large_count = count_inversions(large)
seconds = time.perf_counter() - start
if large != large_copy:
    print("FAIL perf n=100,000: input array was modified")
    failures += 1
elif seconds > 2.0:
    print(f"FAIL perf n=100,000: {seconds:.3f} s (expected under 2 s)")
    failures += 1
else:
    print(f"PASS perf n=100,000 ({seconds:.3f} s)")

# Cross-check the large answer without O(n^2) work: for every pair of different
# values exactly one of the two orders is an inversion, so
# count(nums) + count(reverse(nums)) equals the number of unequal pairs.
reversed_large = large[::-1]
reversed_count = count_inversions(reversed_large)
unequal_pairs = unequal_pair_count(large)
if large_count + reversed_count == unequal_pairs:
    print("PASS large random consistency: count + reversed = unequal pairs")
else:
    print(f"FAIL large random consistency: {large_count} + {reversed_count} != {unequal_pairs}")
    failures += 1

if failures == 0:
    print("ALL TESTS PASSED")
    sys.exit(0)
print(f"{failures} TEST(S) FAILED")
sys.exit(1)
