using System.Collections.Generic;

public class Solution {
    public static string[] HuffmanCodes(int[] freq) {
        int n = freq.Length;
        if (n == 1) return new string[] { "0" };
        // Nodes 0..n-1 are leaves (symbols); nodes n..2n-2 are merged internal nodes.
        long[] weight = new long[2 * n - 1];
        int[] left = new int[2 * n - 1], right = new int[2 * n - 1];
        var heap = new PriorityQueue<int, long>();
        for (int i = 0; i < n; i++) {
            weight[i] = freq[i];
            heap.Enqueue(i, weight[i]);
        }
        // TODO: for node = n .. 2n-2, dequeue the two lightest trees, record them as
        // this node's children, set its weight, and enqueue it.
        // TODO: assign codes from the root (node 2n-2) down: left adds "0", right adds "1".
        // Return the codes of nodes 0..n-1.
        throw new System.NotImplementedException();
    }
}
