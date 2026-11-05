using System.Collections.Generic;

// Time: O(n log n) to build the tree, plus the total code length to write codes.
// Space: O(n) nodes and heap entries, plus the returned code strings.
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
        // Greedy step: merge the two lightest trees, n - 1 times.
        for (int node = n; node < 2 * n - 1; node++) {
            int a = heap.Dequeue(), b = heap.Dequeue();
            weight[node] = weight[a] + weight[b];
            left[node] = a;
            right[node] = b;
            heap.Enqueue(node, weight[node]);
        }
        // Children are created before parents, so walk from the root downwards.
        string[] code = new string[2 * n - 1];
        code[2 * n - 2] = "";
        for (int node = 2 * n - 2; node >= n; node--) {
            code[left[node]] = code[node] + "0";
            code[right[node]] = code[node] + "1";
        }
        string[] result = new string[n];
        System.Array.Copy(code, result, n);
        return result;
    }
}
