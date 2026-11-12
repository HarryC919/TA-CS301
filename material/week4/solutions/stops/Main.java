import java.util.Arrays;
import java.util.Random;
public class Main {
    static int best;
    static void walk(int[][] f,int city,int used,int cost,int dst,int k) {
        if(used==k+1) return;
        for(int[] e:f) if(e[0]==city) {
            if(e[1]==dst && (best<0 || cost+e[2]<best)) best=cost+e[2];
            walk(f,e[1],used+1,cost+e[2],dst,k);
        }
    }
    static int enumerateRoutes(int n,int[][] f,int src,int dst,int k) {
        best=src==dst?0:-1; walk(f,src,0,0,dst,k); return best;
    }
    static int layered(int n,int[][] f,int src,int dst,int k) {
        final long INF=Long.MAX_VALUE/4; long[] b=new long[n]; Arrays.fill(b,INF); b[src]=0;
        long ans=src==dst?0:INF;
        for(int t=0;t<=k;t++) {
            long[] nx=new long[n]; Arrays.fill(nx,INF);
            for(int[] e:f) nx[e[1]]=Math.min(nx[e[1]],b[e[0]]+e[2]);
            b=nx; ans=Math.min(ans,b[dst]);
        }
        return ans>=INF?-1:(int)ans;
    }
    static void check(int n,int[][] f,int src,int dst,int k,int expected) {
        int[][] before=new int[f.length][]; for(int i=0;i<f.length;i++) before[i]=f[i].clone();
        int result=Solution.cheapestRoute(n,f,src,dst,k);
        if(result!=expected) throw new AssertionError("cheapestRoute "+Arrays.deepToString(f)+" "+src+"->"+dst+" k="+k+": got "+result+", expected "+expected);
        if(!Arrays.deepEquals(f,before)) throw new AssertionError("flights were modified");
    }
    public static void main(String[] args) {
        int[][] sample={{0,1,100},{1,2,100},{2,0,100},{1,3,600},{2,3,200}};
        int[][] trap={{0,1,100},{1,2,100},{0,2,500}};
        int[][] chain={{0,1,1},{1,2,1},{2,3,1}};
        check(4,sample,0,3,1,700); check(4,sample,0,3,2,400); check(4,sample,0,0,0,0);
        check(3,trap,0,2,0,500); check(3,trap,0,2,1,200);
        check(3,new int[][]{{0,1,5}},0,2,2,-1); check(4,chain,0,3,1,-1); check(4,chain,0,3,2,3);
        check(2,new int[][]{{0,1,7},{0,1,3}},0,1,0,3); check(3,new int[][]{{0,1,1},{1,0,1},{1,2,10}},0,2,2,11);
        check(3,new int[][]{{0,1,0},{1,2,0}},0,2,1,0); check(1,new int[0][],0,0,0,0); check(3,new int[][]{{1,2,4}},0,2,2,-1);
        Random rng=new Random(301);
        for(int t=0;t<200;t++) {
            int n=1+rng.nextInt(6), m=rng.nextInt(13);
            java.util.List<int[]> list=new java.util.ArrayList<>();
            for(int i=0;i<m;i++){int u=rng.nextInt(n),v=rng.nextInt(n); if(u!=v) list.add(new int[]{u,v,rng.nextInt(21)});}
            int[][] f=list.toArray(new int[0][]);
            int src=rng.nextInt(n),dst=rng.nextInt(n),k=rng.nextInt(Math.min(n,4));
            int expected=enumerateRoutes(n,f,src,dst,k);
            if(expected!=layered(n,f,src,dst,k)) throw new AssertionError("oracles disagree");
            check(n,f,src,dst,k,expected);
        }
        int n=100; int[][] f=new int[n*(n-1)][]; int idx=0;
        for(int u=0;u<n;u++) for(int v=0;v<n;v++) if(u!=v) f[idx++]=new int[]{u,v,(u*37+v*91)%10001};
        int[][] large={{0,99,99},{5,42,0},{17,3,2}};
        for(int[] q:large) check(n,f,q[0],q[1],q[2],layered(n,f,q[0],q[1],q[2]));
        System.out.println("ALL WEEK 4 STOPS JAVA TESTS PASSED (216 cases)");
    }
}
