using System;
using System.Collections.Generic;
using System.Linq;
class Program {
    static int best;
    static void Walk(int[][] f,int city,int used,int cost,int dst,int k) {
        if(used==k+1) return;
        foreach(var e in f) if(e[0]==city) {
            if(e[1]==dst && (best<0 || cost+e[2]<best)) best=cost+e[2];
            Walk(f,e[1],used+1,cost+e[2],dst,k);
        }
    }
    static int EnumerateRoutes(int n,int[][] f,int src,int dst,int k) { best=src==dst?0:-1; Walk(f,src,0,0,dst,k); return best; }
    static int Layered(int n,int[][] f,int src,int dst,int k) {
        const long INF=long.MaxValue/4; var b=Enumerable.Repeat(INF,n).ToArray(); b[src]=0;
        long ans=src==dst?0:INF;
        for(int t=0;t<=k;t++) {
            var nx=Enumerable.Repeat(INF,n).ToArray();
            foreach(var e in f) nx[e[1]]=Math.Min(nx[e[1]],b[e[0]]+e[2]);
            b=nx; ans=Math.Min(ans,b[dst]);
        }
        return ans>=INF?-1:(int)ans;
    }
    static void Check(int n,int[][] f,int src,int dst,int k,int expected) {
        var before=f.Select(e=>(int[])e.Clone()).ToArray();
        int result=Solution.CheapestRoute(n,f,src,dst,k);
        if(result!=expected) throw new Exception($"CheapestRoute {src}->{dst} k={k}: got {result}, expected {expected}");
        if(f.Length!=before.Length || f.Where((e,i)=>!e.SequenceEqual(before[i])).Any()) throw new Exception("flights were modified");
    }
    static void Main() {
        int[][] sample={new[]{0,1,100},new[]{1,2,100},new[]{2,0,100},new[]{1,3,600},new[]{2,3,200}};
        int[][] trap={new[]{0,1,100},new[]{1,2,100},new[]{0,2,500}};
        int[][] chain={new[]{0,1,1},new[]{1,2,1},new[]{2,3,1}};
        Check(4,sample,0,3,1,700); Check(4,sample,0,3,2,400); Check(4,sample,0,0,0,0);
        Check(3,trap,0,2,0,500); Check(3,trap,0,2,1,200);
        Check(3,new[]{new[]{0,1,5}},0,2,2,-1); Check(4,chain,0,3,1,-1); Check(4,chain,0,3,2,3);
        Check(2,new[]{new[]{0,1,7},new[]{0,1,3}},0,1,0,3); Check(3,new[]{new[]{0,1,1},new[]{1,0,1},new[]{1,2,10}},0,2,2,11);
        Check(3,new[]{new[]{0,1,0},new[]{1,2,0}},0,2,1,0); Check(1,new int[0][],0,0,0,0); Check(3,new[]{new[]{1,2,4}},0,2,2,-1);
        var rng=new Random(301);
        for(int t=0;t<200;t++) {
            int n=1+rng.Next(6), m=rng.Next(13);
            var list=new List<int[]>();
            for(int i=0;i<m;i++){int u=rng.Next(n),v=rng.Next(n); if(u!=v) list.Add(new[]{u,v,rng.Next(21)});}
            var f=list.ToArray();
            int src=rng.Next(n),dst=rng.Next(n),k=rng.Next(Math.Min(n,4));
            int expected=EnumerateRoutes(n,f,src,dst,k);
            if(expected!=Layered(n,f,src,dst,k)) throw new Exception("oracles disagree");
            Check(n,f,src,dst,k,expected);
        }
        var large=new List<int[]>();
        for(int u=0;u<100;u++) for(int v=0;v<100;v++) if(u!=v) large.Add(new[]{u,v,(u*37+v*91)%10001});
        var lf=large.ToArray();
        foreach(var q in new[]{new[]{0,99,99},new[]{5,42,0},new[]{17,3,2}}) Check(100,lf,q[0],q[1],q[2],Layered(100,lf,q[0],q[1],q[2]));
        Console.WriteLine("ALL WEEK 4 STOPS C# TESTS PASSED (216 cases)");
    }
}
