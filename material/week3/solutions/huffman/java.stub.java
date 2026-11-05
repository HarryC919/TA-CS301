import java.util.PriorityQueue;

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
        // TODO: for node = n .. 2n-2, poll the two lightest trees, record them as
        // this node's children, set its weight, and add it back.
        // TODO: assign codes from the root (node 2n-2) down: left adds "0", right adds "1".
        // Return the codes of nodes 0..n-1.
        throw new UnsupportedOperationException();
    }
}
