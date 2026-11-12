using System;
using System.Collections.Generic;
using System.Linq;
class Program {
    const int INF=1_000_000_000;
    static int[][] BellmanFordAll(int n,int[][] edges) {
        var rows=new int[n][];
        for(int s=0;s<n;s++) {
            rows[s]=Enumerable.Repeat(INF,n).ToArray(); rows[s][s]=0;
            for(int r=0;r<n-1;r++) foreach(var e in edges)
                if(rows[s][e[0]]!=INF && rows[s][e[0]]+e[2]<rows[s][e[1]]) rows[s][e[1]]=rows[s][e[0]]+e[2];
        }
        return rows;
    }
    static bool Same(int[][] a,int[][] b) => a.Length==b.Length && a.Zip(b).All(p=>p.First.SequenceEqual(p.Second));
    static void Check(int n,int[][] edges,int[][]? expected) {
        var before=edges.Select(e=>(int[])e.Clone()).ToArray();
        var result=Solution.FloydWarshall(n,edges);
        expected??=BellmanFordAll(n,edges);
        if(!Same(result,expected)) throw new Exception($"FloydWarshall n={n}: wrong matrix");
        if(!Same(edges,before)) throw new Exception("edges were modified");
    }
    static int[][] M(params int[][] rows) => rows;
    static void Main() {
        if(Solution.INF!=INF) throw new Exception("INF must be 1,000,000,000");
        Check(4,M(new[]{0,1,3},new[]{0,3,7},new[]{1,0,8},new[]{1,2,2},new[]{2,0,5},new[]{2,3,1},new[]{3,0,2}),
              M(new[]{0,3,5,6},new[]{5,0,2,3},new[]{3,6,0,1},new[]{2,5,7,0}));
        Check(1,new int[0][],M(new[]{0}));
        Check(3,M(new[]{0,1,4},new[]{0,2,5},new[]{2,1,-3}),M(new[]{0,2,5},new[]{INF,0,INF},new[]{INF,-3,0}));
        Check(3,M(new[]{0,1,1}),M(new[]{0,1,INF},new[]{INF,0,INF},new[]{INF,INF,0}));
        Check(3,M(new[]{1,2,-5}),M(new[]{0,INF,INF},new[]{INF,0,-5},new[]{INF,INF,0}));
        Check(2,M(new[]{0,1,5},new[]{0,1,2},new[]{1,0,4}),M(new[]{0,2},new[]{4,0}));
        var rng=new Random(301);
        for(int t=0;t<100;t++) {
            int n=1+rng.Next(8), m=rng.Next(21);
            var p=Enumerable.Range(0,n).Select(_=>rng.Next(21)).ToArray();
            var list=new List<int[]>();
            // w = base + p[u] - p[v] with base >= 0: some edges are negative, no cycle is.
            for(int i=0;i<m;i++){int u=rng.Next(n),v=rng.Next(n); if(u!=v) list.Add(new[]{u,v,rng.Next(21)+p[u]-p[v]});}
            Check(n,list.ToArray(),null);
        }
        // Large: a weight-1 cycle plus heavier chords, so D[i][j] = (j - i) mod n.
        int N=200; var large=new List<int[]>();
        for(int i=0;i<N;i++) large.Add(new[]{i,(i+1)%N,1});
        for(int i=0;i<N;i++) if((i*7+3)%N!=i) large.Add(new[]{i,(i*7+3)%N,N+i%5});
        var exp=new int[N][];
        for(int i=0;i<N;i++){exp[i]=new int[N]; for(int j=0;j<N;j++) exp[i][j]=((j-i)%N+N)%N;}
        Check(N,large.ToArray(),exp);
        Console.WriteLine("ALL WEEK 4 FLOYD C# TESTS PASSED (108 cases)");
    }
}
