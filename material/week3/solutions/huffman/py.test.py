import importlib.util
from pathlib import Path
import random

spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("py.solution.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def optimal_cost(freq):
    # Oracle: total cost = sum of all merged weights (two-queue Huffman on sorted input).
    if len(freq) == 1:
        return freq[0]
    leaves, merged, cost = sorted(freq), [], 0
    i = j = 0
    def take():
        nonlocal i, j
        if j >= len(merged) or (i < len(leaves) and leaves[i] <= merged[j]):
            i += 1
            return leaves[i - 1]
        j += 1
        return merged[j - 1]
    for _ in range(len(freq) - 1):
        w = take() + take()
        merged.append(w)
        cost += w
    return cost

def check(freq):
    before = freq[:]
    codes = module.huffman_codes(freq)
    assert freq == before, "input mutated"
    assert isinstance(codes, list) and len(codes) == len(freq), codes
    assert all(code and set(code) <= {"0", "1"} for code in codes), codes
    ordered = sorted(codes)
    assert all(not b.startswith(a) for a, b in zip(ordered, ordered[1:])), "not prefix-free"
    assert sum(f * len(c) for f, c in zip(freq, codes)) == optimal_cost(freq), (freq, codes)

assert module.huffman_codes([7]) == ["0"]
for freq in [[7], [5, 5], [1, 1, 1, 1], [45, 13, 12, 16, 9, 5], [1, 2, 4, 8, 16],
             [10**6, 1, 1], [3] * 9]:
    check(freq)
rng = random.Random(301)
for _ in range(100):
    check([rng.randint(1, 50) for _ in range(rng.randint(1, 40))])
check([rng.randint(1, 10**6) for _ in range(1000)])
print("ALL WEEK 3 HUFFMAN PYTHON TESTS PASSED (108 cases)")
