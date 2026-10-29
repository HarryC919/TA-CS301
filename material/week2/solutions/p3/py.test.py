import importlib.util
from pathlib import Path
import random

spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("py.solution.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def check(left, right):
    before_left, before_right = left[:], right[:]
    expected = sorted(left + right)
    result = module.merge_sorted(left, right)
    assert result == expected, (left, right, result, expected)
    assert left == before_left and right == before_right, "input mutated"
    assert result is not left and result is not right, "output aliases an input"
    if result:
        result[0] = 123456789
        assert left == before_left and right == before_right

for left, right in [([], []), ([], [1, 2]), ([1, 2], []), ([1], [1]),
                    ([1, 4, 9], [2, 2, 3, 10]), ([-10**9, 0], [0, 10**9]),
                    ([1, 2, 3], [9]), ([9], [1, 2, 3]), ([2]*5, [2]*3)]:
    check(left, right)
rng = random.Random(301)
for _ in range(100):
    check(sorted(rng.randrange(-20, 21) for _ in range(rng.randrange(60))),
          sorted(rng.randrange(-20, 21) for _ in range(rng.randrange(60))))
check(list(range(0, 200000, 2)), list(range(1, 200000, 2)))
print("ALL WEEK 2 PYTHON TESTS PASSED (110 cases)")
