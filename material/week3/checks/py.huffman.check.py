# Run this cell after implementing and running the huffman_codes cell.
# These checks fail while the starter is still unchanged.
# Expected costs are the optimal totals sum(freq[i] * len(code[i])).
cases = [
    ([7], 7), ([5, 5], 10), ([1, 1, 1, 1], 8), ([45, 13, 12, 16, 9, 5], 224),
    ([1, 2, 4, 8, 16], 56), ([1000000, 1, 1], 1000004), ([3] * 9, 87), ([2, 3, 7, 1, 1], 27),
]
for freq, cost in cases:
    before = freq[:]
    codes = huffman_codes(freq)
    assert isinstance(codes, list) and len(codes) == len(freq), f"Return one code per symbol, got {codes!r}"
    assert freq == before, "Do not modify freq"
    assert all(isinstance(c, str) and c and set(c) <= {"0", "1"} for c in codes), codes
    ordered = sorted(codes)
    assert all(not b.startswith(a) for a, b in zip(ordered, ordered[1:])), ("not prefix-free", codes)
    total = sum(f * len(c) for f, c in zip(freq, codes))
    assert total == cost, (freq, codes, f"cost {total}, optimal {cost}")

# Round trip: encode a message with your codes, then decode it bit by bit.
codes = huffman_codes([45, 13, 12, 16, 9, 5])
symbol_of = {code: "abcdef"[i] for i, code in enumerate(codes)}
message = "faceadbead"
bits = "".join(codes["abcdef".index(ch)] for ch in message)
decoded, current = [], ""
for bit in bits:
    current += bit
    if current in symbol_of:
        decoded.append(symbol_of[current])
        current = ""
assert "".join(decoded) == message and current == "", "Round trip failed"
print(f"Huffman checks passed (8 cases + round trip: {len(message)} symbols in {len(bits)} bits, vs {3 * len(message)} fixed).")
