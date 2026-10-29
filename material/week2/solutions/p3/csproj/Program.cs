using System;
class Program {
    static void Check(int[] a,int[] b) {
        int[] ac=(int[])a.Clone(),bc=(int[])b.Clone(),expected=new int[a.Length+b.Length];
        Array.Copy(a,0,expected,0,a.Length);Array.Copy(b,0,expected,a.Length,b.Length);
        Array.Sort(expected);
        int[] result=Solution.MergeSorted(a,b);
        if(!result.AsSpan().SequenceEqual(expected) || !a.AsSpan().SequenceEqual(ac)
            || !b.AsSpan().SequenceEqual(bc) || ReferenceEquals(result,a) || ReferenceEquals(result,b))
            throw new Exception("merge contract failed");
        if(result.Length>0) result[0]=123456789;
        if(!a.AsSpan().SequenceEqual(ac) || !b.AsSpan().SequenceEqual(bc)) throw new Exception("output alias");
    }
    static void Main() {
        Check([],[]);Check([],[1,2]);Check([1,2],[]);Check([1],[1]);
        Check([1,4,9],[2,2,3,10]);Check([-1000000000,0],[0,1000000000]);
        Check([1,2,3],[9]);Check([9],[1,2,3]);Check([2,2,2,2,2],[2,2,2]);
        var rng=new Random(301);
        for(int t=0;t<100;t++) {
            int[] a=new int[rng.Next(60)],b=new int[rng.Next(60)];
            for(int i=0;i<a.Length;i++) a[i]=rng.Next(41)-20;
            for(int i=0;i<b.Length;i++) b[i]=rng.Next(41)-20;
            Array.Sort(a);Array.Sort(b);Check(a,b);
        }
        int[] x=new int[100000],y=new int[100000];
        for(int i=0;i<x.Length;i++){x[i]=2*i;y[i]=2*i+1;}Check(x,y);
        Console.WriteLine("ALL WEEK 2 C# TESTS PASSED (110 cases)");
    }
}
