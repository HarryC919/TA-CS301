import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

// Re-run the Solution definition cell before running this check cell.
// These checks throw while the starter is still unchanged.
// Expected costs are the optimal totals sum(freq[i] * code[i].length()).
int[] nines = new int[9];
Arrays.fill(nines, 3);
int[][] freqs = {{7}, {5, 5}, {1, 1, 1, 1}, {45, 13, 12, 16, 9, 5},
                 {1, 2, 4, 8, 16}, {1000000, 1, 1}, nines, {2, 3, 7, 1, 1}};
long[] costs = {7, 10, 8, 224, 56, 1000004, 87, 27};
for (int t = 0; t < freqs.length; t++) {
    int[] freq = freqs[t], before = freq.clone();
    String[] codes = Solution.huffmanCodes(freq);
    if (codes == null || codes.length != freq.length) throw new AssertionError("Return one code per symbol");
    if (!Arrays.equals(freq, before)) throw new AssertionError("Do not modify freq");
    long total = 0;
    for (int k = 0; k < codes.length; k++) {
        if (codes[k] == null || !codes[k].matches("[01]+")) throw new AssertionError("Bad code: " + codes[k]);
        total += (long) freq[k] * codes[k].length();
    }
    String[] ordered = codes.clone();
    Arrays.sort(ordered);
    for (int k = 1; k < ordered.length; k++)
        if (ordered[k].startsWith(ordered[k - 1])) throw new AssertionError("Not prefix-free: " + Arrays.toString(codes));
    if (total != costs[t]) throw new AssertionError(Arrays.toString(freq) + ": cost " + total + ", optimal " + costs[t]);
}

// Round trip: encode a message with your codes, then decode it bit by bit.
String[] codes = Solution.huffmanCodes(new int[] {45, 13, 12, 16, 9, 5});
Map<String, Character> symbolOf = new HashMap<>();
for (int k = 0; k < codes.length; k++) symbolOf.put(codes[k], "abcdef".charAt(k));
String message = "faceadbead";
StringBuilder bits = new StringBuilder();
for (char ch : message.toCharArray()) bits.append(codes["abcdef".indexOf(ch)]);
StringBuilder decoded = new StringBuilder();
String current = "";
for (char bit : bits.toString().toCharArray()) {
    current += bit;
    if (symbolOf.containsKey(current)) {
        decoded.append(symbolOf.get(current));
        current = "";
    }
}
if (!decoded.toString().equals(message) || !current.isEmpty()) throw new AssertionError("Round trip failed");
System.out.println("Huffman checks passed (8 cases + round trip: " + message.length() + " symbols in "
        + bits.length() + " bits, vs " + 3 * message.length() + " fixed).");
