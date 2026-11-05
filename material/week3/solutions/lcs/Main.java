import java.util.Random;
public class Main {
    static int lcsLength(String a,String b) {
        int[] prev=new int[b.length()+1];
        for(int i=0;i<a.length();i++) {
            int[] cur=new int[b.length()+1];
            for(int j=1;j<=b.length();j++)
                cur[j]=a.charAt(i)==b.charAt(j-1)?prev[j-1]+1:Math.max(prev[j],cur[j-1]);
            prev=cur;
        }
        return prev[b.length()];
    }
    static boolean isSubsequence(String s,String t) {
        int k=0; for(int i=0;i<t.length()&&k<s.length();i++) if(s.charAt(k)==t.charAt(i)) k++;
        return k==s.length();
    }
    static void check(String a,String b,int expected) {
        String result=Solution.longestCommonSubsequence(a,b);
        if(result==null || result.length()!=(expected<0?lcsLength(a,b):expected)
            || !isSubsequence(result,a) || !isSubsequence(result,b)) throw new AssertionError("LCS contract failed: "+a+" "+b);
    }
    public static void main(String[] args) {
        String[][] cases={{"","","0"},{"","ABC","0"},{"ABC","","0"},{"ABC","DEF","0"},{"a","A","0"},
            {"ABCB","BDCAB","3"},{"ABCBDAB","BDCABA","4"},{"AGGTAB","GXTXAYB","4"},{"ABC","ABC","3"},
            {"ACE","ABCDE","3"},{"AAAA","AA","2"},{"XMJYAUZ","MZJAWXU","4"}};
        for(String[] c:cases) check(c[0],c[1],Integer.parseInt(c[2]));
        if(!Solution.longestCommonSubsequence("ABCB","BDCAB").equals("BCB")) throw new AssertionError("traceback");
        Random rng=new Random(301);
        for(int t=0;t<100;t++) {
            StringBuilder a=new StringBuilder(),b=new StringBuilder();
            for(int i=rng.nextInt(25);i>0;i--) a.append("ABC".charAt(rng.nextInt(3)));
            for(int i=rng.nextInt(25);i>0;i--) b.append("ABC".charAt(rng.nextInt(3)));
            check(a.toString(),b.toString(),-1);
        }
        check("AB".repeat(500),"BA".repeat(500),999);
        System.out.println("ALL WEEK 3 LCS JAVA TESTS PASSED (113 cases)");
    }
}
