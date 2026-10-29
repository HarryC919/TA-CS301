import java.util.Arrays;
import java.util.Random;
public class Main {
    static void check(int[] a,int[] b) {
        int[] ac=a.clone(),bc=b.clone(),expected=Arrays.copyOf(a,a.length+b.length);
        System.arraycopy(b,0,expected,a.length,b.length);Arrays.sort(expected);
        int[] result=Solution.mergeSorted(a,b);
        if(!Arrays.equals(result,expected) || !Arrays.equals(a,ac) || !Arrays.equals(b,bc)
            || result==a || result==b) throw new AssertionError("merge contract failed");
        if(result.length>0) result[0]=123456789;
        if(!Arrays.equals(a,ac) || !Arrays.equals(b,bc)) throw new AssertionError("output alias");
    }
    public static void main(String[] args) {
        int[][][] cases={{{},{}},{{},{1,2}},{{1,2},{}},{{1},{1}},
            {{1,4,9},{2,2,3,10}},{{-1000000000,0},{0,1000000000}},
            {{1,2,3},{9}},{{9},{1,2,3}},{{2,2,2,2,2},{2,2,2}}};
        for(int[][] pair:cases) check(pair[0],pair[1]);
        Random rng=new Random(301);
        for(int t=0;t<100;t++) {
            int[] a=new int[rng.nextInt(60)],b=new int[rng.nextInt(60)];
            for(int i=0;i<a.length;i++) a[i]=rng.nextInt(41)-20;
            for(int i=0;i<b.length;i++) b[i]=rng.nextInt(41)-20;
            Arrays.sort(a);Arrays.sort(b);check(a,b);
        }
        int[] a=new int[100000],b=new int[100000];
        for(int i=0;i<a.length;i++){a[i]=2*i;b[i]=2*i+1;}check(a,b);
        System.out.println("ALL WEEK 2 JAVA TESTS PASSED (110 cases)");
    }
}
