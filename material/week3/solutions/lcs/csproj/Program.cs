using System;
using System.Text;
class Program {
    static int LcsLength(string a,string b) {
        int[] prev=new int[b.Length+1];
        foreach(char x in a) {
            int[] cur=new int[b.Length+1];
            for(int j=1;j<=b.Length;j++) cur[j]=x==b[j-1]?prev[j-1]+1:Math.Max(prev[j],cur[j-1]);
            prev=cur;
        }
        return prev[b.Length];
    }
    static bool IsSubsequence(string s,string t) {
        int k=0; foreach(char c in t) if(k<s.Length && s[k]==c) k++;
        return k==s.Length;
    }
    static void Check(string a,string b,int expected=-1) {
        string result=Solution.LongestCommonSubsequence(a,b);
        if(result==null || result.Length!=(expected<0?LcsLength(a,b):expected)
            || !IsSubsequence(result,a) || !IsSubsequence(result,b)) throw new Exception("LCS contract failed: "+a+" "+b);
    }
    static void Main() {
        Check("","",0);Check("","ABC",0);Check("ABC","",0);Check("ABC","DEF",0);Check("a","A",0);
        Check("ABCB","BDCAB",3);Check("ABCBDAB","BDCABA",4);Check("AGGTAB","GXTXAYB",4);Check("ABC","ABC",3);
        Check("ACE","ABCDE",3);Check("AAAA","AA",2);Check("XMJYAUZ","MZJAWXU",4);
        if(Solution.LongestCommonSubsequence("ABCB","BDCAB")!="BCB") throw new Exception("traceback");
        var rng=new Random(301);
        for(int t=0;t<100;t++) {
            var a=new StringBuilder();var b=new StringBuilder();
            for(int i=rng.Next(25);i>0;i--) a.Append("ABC"[rng.Next(3)]);
            for(int i=rng.Next(25);i>0;i--) b.Append("ABC"[rng.Next(3)]);
            Check(a.ToString(),b.ToString());
        }
        var x=new StringBuilder();var y=new StringBuilder();
        for(int i=0;i<500;i++){x.Append("AB");y.Append("BA");}
        Check(x.ToString(),y.ToString(),999);
        Console.WriteLine("ALL WEEK 3 LCS C# TESTS PASSED (113 cases)");
    }
}
