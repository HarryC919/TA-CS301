import java.util.PriorityQueue;

// Time: O(n log n) to build the tree, plus the total code length to write codes.
// Space: O(n) nodes and heap entries, plus the returned code strings.
public class Solution {
    public static String[] huffmanCodes(int[] freq) {
        int n = freq.length;
        if (n == 1) return new String[] {"0"};
        // Nodes 0..n-1 are leaves (symbols); nodes n..2n-2 are merged internal nodes.
        long[] weight = new long[2 * n - 1];
        int[] left = new int[2 * n - 1], right = new int[2 * n - 1];
        PriorityQueue<Integer> heap = new PriorityQueue<>((x, y) -> Long.compare(weight[x], weight[y]));
        for (int i = 0; i < n; i++) {
            weight[i] = freq[i];
            heap.add(i);
        }
        // Greedy step: merge the two lightest trees, n - 1 times.
        for (int node = n; node < 2 * n - 1; node++) {
            int a = heap.poll(), b = heap.poll();
            weight[node] = weight[a] + weight[b];
            left[node] = a;
            right[node] = b;
            heap.add(node);
        }
        // Children are created before parents, so walk from the root downwards.
        String[] code = new String[2 * n - 1];
        code[2 * n - 2] = "";
        for (int node = 2 * n - 2; node >= n; node--) {
            code[left[node]] = code[node] + "0";
            code[right[node]] = code[node] + "1";
        }
        String[] result = new String[n];
        System.arraycopy(code, 0, result, 0, n);
        return result;
    }
}
