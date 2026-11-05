import java.util.Arrays;
import java.util.Random;
public class Main {
    static long optimalCost(int[] freq) {
        // Oracle: total cost = sum of all merged weights (two-queue Huffman on sorted input).
        if(freq.length==1) return freq[0];
        long[] leaves=new long[freq.length],merged=new long[freq.length];
        for(int k=0;k<freq.length;k++) leaves[k]=freq[k];
        Arrays.sort(leaves);
        int i=0,j=0,m=0; long cost=0;
        for(int k=1;k<freq.length;k++) {
            long w=0;
            for(int pick=0;pick<2;pick++)
                w+=(j>=m || (i<leaves.length && leaves[i]<=merged[j]))?leaves[i++]:merged[j++];
            merged[m++]=w; cost+=w;
        }
        return cost;
    }
    static void check(int[] freq) {
        int[] before=freq.clone();
        String[] codes=Solution.huffmanCodes(freq);
        if(!Arrays.equals(freq,before)) throw new AssertionError("input mutated");
        if(codes==null || codes.length!=freq.length) throw new AssertionError("wrong code count");
        long cost=0;
        for(int k=0;k<codes.length;k++) {
            if(codes[k]==null || !codes[k].matches("[01]+")) throw new AssertionError("bad code");
            cost+=(long)freq[k]*codes[k].length();
        }
        String[] ordered=codes.clone(); Arrays.sort(ordered);
        for(int k=1;k<ordered.length;k++)
            if(ordered[k].startsWith(ordered[k-1])) throw new AssertionError("not prefix-free");
        if(cost!=optimalCost(freq)) throw new AssertionError("not optimal: "+Arrays.toString(freq));
    }
    public static void main(String[] args) {
        if(!Arrays.equals(Solution.huffmanCodes(new int[]{7}),new String[]{"0"})) throw new AssertionError("single symbol");
        int[] nines=new int[9]; Arrays.fill(nines,3);
        int[][] cases={{7},{5,5},{1,1,1,1},{45,13,12,16,9,5},{1,2,4,8,16},{1000000,1,1},nines};
        for(int[] f:cases) check(f);
        Random rng=new Random(301);
        for(int t=0;t<100;t++) {
            int[] f=new int[1+rng.nextInt(40)];
            for(int k=0;k<f.length;k++) f[k]=1+rng.nextInt(50);
            check(f);
        }
        int[] large=new int[1000];
        for(int k=0;k<large.length;k++) large[k]=1+rng.nextInt(1000000);
        check(large);
        System.out.println("ALL WEEK 3 HUFFMAN JAVA TESTS PASSED (108 cases)");
    }
}
