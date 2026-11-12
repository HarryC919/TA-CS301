public class Solution {
    public static int CheapestRoute(int n, int[][] flights, int src, int dst, int k) {
        const int INF = int.MaxValue;
        // dist[v] = cheapest price to reach v using the flights allowed so far.
        int[] dist = new int[n];
        System.Array.Fill(dist, INF);
        dist[src] = 0;
        // At most k stops means at most k + 1 flights: one round per flight.
        for (int round = 0; round <= k; round++) {
            // TODO: relax every flight {u, v, price} for this round.
            // Read this round's starting distances, and do not let one round
            // chain two flights.
        }
        // TODO: return the price of reaching dst, or -1 if it is unreachable.
        throw new System.NotImplementedException();
    }
}
