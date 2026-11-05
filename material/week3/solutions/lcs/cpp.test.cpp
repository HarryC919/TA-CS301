#include <algorithm>
#include <cassert>
#include <iostream>
#include <random>
#include <string>
#include <vector>
std::string longestCommonSubsequence(const std::string&, const std::string&);
int lcsLength(const std::string& a,const std::string& b) {
    std::vector<int> prev(b.size()+1,0);
    for(char x:a) {
        std::vector<int> cur(b.size()+1,0);
        for(std::size_t j=1;j<=b.size();j++) cur[j]=x==b[j-1]?prev[j-1]+1:std::max(prev[j],cur[j-1]);
        prev=cur;
    }
    return prev[b.size()];
}
bool isSubsequence(const std::string& s,const std::string& t) {
    std::size_t k=0; for(char c:t) if(k<s.size() && s[k]==c) k++;
    return k==s.size();
}
void check(const std::string& a,const std::string& b,int expected=-1) {
    std::string result=longestCommonSubsequence(a,b);
    assert((int)result.size()==(expected<0?lcsLength(a,b):expected));
    assert(isSubsequence(result,a) && isSubsequence(result,b));
}
int main() {
    check("","",0);check("","ABC",0);check("ABC","",0);check("ABC","DEF",0);check("a","A",0);
    check("ABCB","BDCAB",3);check("ABCBDAB","BDCABA",4);check("AGGTAB","GXTXAYB",4);check("ABC","ABC",3);
    check("ACE","ABCDE",3);check("AAAA","AA",2);check("XMJYAUZ","MZJAWXU",4);
    assert(longestCommonSubsequence("ABCB","BDCAB")=="BCB");
    std::mt19937 rng(301);
    for(int t=0;t<100;t++) {
        std::string a(rng()%25,'A'),b(rng()%25,'A');
        for(auto& c:a) c="ABC"[rng()%3];
        for(auto& c:b) c="ABC"[rng()%3];
        check(a,b);
    }
    std::string x,y;
    for(int i=0;i<500;i++){x+="AB";y+="BA";}
    check(x,y,999);
    std::cout << "ALL WEEK 3 LCS C++ TESTS PASSED (113 cases)\n";
}
