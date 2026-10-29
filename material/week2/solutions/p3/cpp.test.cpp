#include <algorithm>
#include <cassert>
#include <iostream>
#include <random>
#include <vector>
std::vector<int> mergeSorted(const std::vector<int>&, const std::vector<int>&);
void check(std::vector<int> a, std::vector<int> b) {
    auto ac=a, bc=b, expected=a;
    expected.insert(expected.end(), b.begin(), b.end());
    std::sort(expected.begin(), expected.end());
    auto result=mergeSorted(a,b);
    assert(result==expected && a==ac && b==bc);
    if (!result.empty()) result[0]=123456789;
    assert(a==ac && b==bc);
}
int main() {
    check({},{}); check({},{1,2}); check({1,2},{}); check({1},{1});
    check({1,4,9},{2,2,3,10}); check({-1000000000,0},{0,1000000000});
    check({1,2,3},{9}); check({9},{1,2,3}); check({2,2,2,2,2},{2,2,2});
    std::mt19937 rng(301);
    for(int t=0;t<100;t++) {
        std::vector<int> a(rng()%60), b(rng()%60);
        for(auto& x:a) x=int(rng()%41)-20;
        for(auto& x:b) x=int(rng()%41)-20;
        std::sort(a.begin(),a.end()); std::sort(b.begin(),b.end()); check(a,b);
    }
    std::vector<int> a(100000),b(100000);
    for(int i=0;i<100000;i++) {a[i]=2*i;b[i]=2*i+1;} check(a,b);
    std::cout << "ALL WEEK 2 C++ TESTS PASSED (110 cases)\n";
}
