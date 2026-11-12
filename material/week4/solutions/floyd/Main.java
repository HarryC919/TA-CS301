import java.util.Arrays;
import java.util.Random;
public class Main {
    static final int INF=1_000_000_000;
    static int[][] bellmanFordAll(int n,int[][] edges) {
        int[][] rows=new int[n][n];
        for(int s=0;s<n;s++) {
            Arrays.fill(rows[s],INF); rows[s][s]=0;
            for(int r=0;r<n-1;r++) for(int[] e:edges)
                if(rows[s][e[0]]!=INF && rows[s][e[0]]+e[2]<rows[s][e[1]]) rows[s][e[1]]=rows[s][e[0]]+e[2];
        }
        return rows;
    }
    static void check(int n,int[][] edges,int[][] expected) {
        int[][] before=new int[edges.length][]; for(int i=0;i<edges.length;i++) before[i]=edges[i].clone();
        int[][] result=Solution.floydWarshall(n,edges);
        if(expected==null) expected=bellmanFordAll(n,edges);
        if(!Arrays.deepEquals(result,expected)) throw new AssertionError("floydWarshall n="+n+" "+Arrays.deepToString(edges)+": got "+Arrays.deepToString(result));
        if(!Arrays.deepEquals(edges,before)) throw new AssertionError("edges were modified");
    }
    public static void main(String[] args) {
        if(Solution.INF!=INF) throw new AssertionError("INF must be 1,000,000,000");
        check(4,new int[][]{{0,1,3},{0,3,7},{1,0,8},{1,2,2},{2,0,5},{2,3,1},{3,0,2}},
              new int[][]{{0,3,5,6},{5,0,2,3},{3,6,0,1},{2,5,7,0}});
        check(1,new int[0][],new int[][]{{0}});
        check(3,new int[][]{{0,1,4},{0,2,5},{2,1,-3}},new int[][]{{0,2,5},{INF,0,INF},{INF,-3,0}});
        check(3,new int[][]{{0,1,1}},new int[][]{{0,1,INF},{INF,0,INF},{INF,INF,0}});
        check(3,new int[][]{{1,2,-5}},new int[][]{{0,INF,INF},{INF,0,-5},{INF,INF,0}});
        check(2,new int[][]{{0,1,5},{0,1,2},{1,0,4}},new int[][]{{0,2},{4,0}});
        Random rng=new Random(301);
        for(int t=0;t<100;t++) {
            int n=1+rng.nextInt(8), m=rng.nextInt(21);
            int[] p=new int[n]; for(int i=0;i<n;i++) p[i]=rng.nextInt(21);
            java.util.List<int[]> list=new java.util.ArrayList<>();
            // w = base + p[u] - p[v] with base >= 0: some edges are negative, no cycle is.
            for(int i=0;i<m;i++){int u=rng.nextInt(n),v=rng.nextInt(n); if(u!=v) list.add(new int[]{u,v,rng.nextInt(21)+p[u]-p[v]});}
            check(n,list.toArray(new int[0][]),null);
        }
        // Large: a weight-1 cycle plus heavier chords, so D[i][j] = (j - i) mod n.
        int n=200; java.util.List<int[]> list=new java.util.ArrayList<>();
        for(int i=0;i<n;i++) list.add(new int[]{i,(i+1)%n,1});
        for(int i=0;i<n;i++) if((i*7+3)%n!=i) list.add(new int[]{i,(i*7+3)%n,n+i%5});
        int[][] expected=new int[n][n];
        for(int i=0;i<n;i++) for(int j=0;j<n;j++) expected[i][j]=((j-i)%n+n)%n;
        check(n,list.toArray(new int[0][]),expected);
        System.out.println("ALL WEEK 4 FLOYD JAVA TESTS PASSED (108 cases)");
    }
}
