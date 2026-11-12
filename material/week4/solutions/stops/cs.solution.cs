// Time: O(k * m) for m flights. Space: O(n) for two distance arrays.
public class Solution {
    public static int CheapestRoute(int n, int[][] flights, int src, int dst, int k) {
        const int INF = int.MaxValue;
        // dist[v] = cheapest price to reach v using the flights allowed so far.
        int[] dist = new int[n];
        System.Array.Fill(dist, INF);
        dist[src] = 0;
        // At most k stops means at most k + 1 flights: one round per flight.
        for (int round = 0; round <= k; round++) {
            // Read the previous round and write into a copy, so one round
            // never chains two flights.
            int[] newDist = (int[])dist.Clone();
            foreach (int[] flight in flights) {
                int u = flight[0], v = flight[1], price = flight[2];
                if (dist[u] != INF && dist[u] + price < newDist[v]) {
                    newDist[v] = dist[u] + price;
                }
            }
            dist = newDist;
        }
        return dist[dst] == INF ? -1 : dist[dst];
    }
}
