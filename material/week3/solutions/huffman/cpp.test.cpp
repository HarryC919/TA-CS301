#include <algorithm>
#include <cassert>
#include <iostream>
#include <random>
#include <string>
#include <vector>
std::vector<std::string> huffmanCodes(const std::vector<int>&);
long long optimalCost(const std::vector<int>& freq) {
    // Oracle: total cost = sum of all merged weights (two-queue Huffman on sorted input).
    if(freq.size()==1) return freq[0];
    std::vector<long long> leaves(freq.begin(),freq.end()),merged;
    std::sort(leaves.begin(),leaves.end());
    std::size_t i=0,j=0; long long cost=0;
    auto take=[&]{ return (j>=merged.size() || (i<leaves.size() && leaves[i]<=merged[j]))?leaves[i++]:merged[j++]; };
    for(std::size_t k=1;k<freq.size();k++) { long long w=take(); w+=take(); merged.push_back(w); cost+=w; }
    return cost;
}
void check(const std::vector<int>& freq) {
    auto before=freq;
    auto codes=huffmanCodes(freq);
    assert(freq==before && codes.size()==freq.size());
    long long cost=0;
    for(std::size_t k=0;k<codes.size();k++) {
        assert(!codes[k].empty() && codes[k].find_first_not_of("01")==std::string::npos);
        cost+=(long long)freq[k]*(long long)codes[k].size();
    }
    auto ordered=codes; std::sort(ordered.begin(),ordered.end());
    for(std::size_t k=1;k<ordered.size();k++) assert(ordered[k].compare(0,ordered[k-1].size(),ordered[k-1])!=0);
    assert(cost==optimalCost(freq));
}
int main() {
    assert(huffmanCodes({7})==std::vector<std::string>{"0"});
    check({7});check({5,5});check({1,1,1,1});check({45,13,12,16,9,5});check({1,2,4,8,16});
    check({1000000,1,1});check(std::vector<int>(9,3));
    std::mt19937 rng(301);
    for(int t=0;t<100;t++) {
        std::vector<int> f(1+rng()%40);
        for(auto& x:f) x=1+int(rng()%50);
        check(f);
    }
    std::vector<int> large(1000);
    for(auto& x:large) x=1+int(rng()%1000000);
    check(large);
    std::cout << "ALL WEEK 3 HUFFMAN C++ TESTS PASSED (108 cases)\n";
}
