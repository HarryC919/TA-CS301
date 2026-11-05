using System;
using System.Linq;
class Program {
    static long OptimalCost(int[] freq) {
        // Oracle: total cost = sum of all merged weights (two-queue Huffman on sorted input).
        if(freq.Length==1) return freq[0];
        long[] leaves=freq.Select(f=>(long)f).ToArray(),merged=new long[freq.Length];
        Array.Sort(leaves);
        int i=0,j=0,m=0; long cost=0;
        for(int k=1;k<freq.Length;k++) {
            long w=0;
            for(int pick=0;pick<2;pick++)
                w+=(j>=m || (i<leaves.Length && leaves[i]<=merged[j]))?leaves[i++]:merged[j++];
            merged[m++]=w; cost+=w;
        }
        return cost;
    }
    static void Check(int[] freq) {
        int[] before=(int[])freq.Clone();
        string[] codes=Solution.HuffmanCodes(freq);
        if(!freq.SequenceEqual(before)) throw new Exception("input mutated");
        if(codes==null || codes.Length!=freq.Length) throw new Exception("wrong code count");
        long cost=0;
        for(int k=0;k<codes.Length;k++) {
            if(string.IsNullOrEmpty(codes[k]) || codes[k].Any(c=>c!='0' && c!='1')) throw new Exception("bad code");
            cost+=(long)freq[k]*codes[k].Length;
        }
        string[] ordered=(string[])codes.Clone(); Array.Sort(ordered,StringComparer.Ordinal);
        for(int k=1;k<ordered.Length;k++)
            if(ordered[k].StartsWith(ordered[k-1],StringComparison.Ordinal)) throw new Exception("not prefix-free");
        if(cost!=OptimalCost(freq)) throw new Exception("not optimal");
    }
    static void Main() {
        if(!Solution.HuffmanCodes([7]).SequenceEqual(["0"])) throw new Exception("single symbol");
        Check([7]);Check([5,5]);Check([1,1,1,1]);Check([45,13,12,16,9,5]);Check([1,2,4,8,16]);
        Check([1000000,1,1]);Check(Enumerable.Repeat(3,9).ToArray());
        var rng=new Random(301);
        for(int t=0;t<100;t++) {
            int[] f=new int[1+rng.Next(40)];
            for(int k=0;k<f.Length;k++) f[k]=1+rng.Next(50);
            Check(f);
        }
        int[] large=new int[1000];
        for(int k=0;k<large.Length;k++) large[k]=1+rng.Next(1000000);
        Check(large);
        Console.WriteLine("ALL WEEK 3 HUFFMAN C# TESTS PASSED (108 cases)");
    }
}
