#include <cassert>
#include <iostream>
#include <random>
#include <vector>
using Matrix = std::vector<std::vector<int>>;
static const int INF=1000000000;  // must match the solution's INF
Matrix floydWarshall(int, const Matrix&);
static Matrix bellmanFordAll(int n,const Matrix& edges) {
    Matrix rows(n,std::vector<int>(n,INF));
    for(int s=0;s<n;s++) {
        rows[s][s]=0;
        for(int r=0;r<n-1;r++) for(const auto& e:edges)
            if(rows[s][e[0]]!=INF && rows[s][e[0]]+e[2]<rows[s][e[1]]) rows[s][e[1]]=rows[s][e[0]]+e[2];
    }
    return rows;
}
static void check(int n,const Matrix& edges,Matrix expected={}) {
    Matrix before=edges;
    Matrix result=floydWarshall(n,edges);
    if(expected.empty()) expected=bellmanFordAll(n,edges);
    assert(result==expected);
    assert(edges==before);
}
int main() {
    const int I=INF;
    check(4,{{0,1,3},{0,3,7},{1,0,8},{1,2,2},{2,0,5},{2,3,1},{3,0,2}},{{0,3,5,6},{5,0,2,3},{3,6,0,1},{2,5,7,0}});
    check(1,{},{{0}});
    check(3,{{0,1,4},{0,2,5},{2,1,-3}},{{0,2,5},{I,0,I},{I,-3,0}});
    check(3,{{0,1,1}},{{0,1,I},{I,0,I},{I,I,0}});
    check(3,{{1,2,-5}},{{0,I,I},{I,0,-5},{I,I,0}});
    check(2,{{0,1,5},{0,1,2},{1,0,4}},{{0,2},{4,0}});
    std::mt19937 rng(301);
    for(int t=0;t<100;t++) {
        int n=1+rng()%8, tries=rng()%21; std::vector<int> p(n); for(auto& x:p) x=rng()%21;
        Matrix e;
        // w = base + p[u] - p[v] with base >= 0: some edges are negative, no cycle is.
        for(int i=0;i<tries;i++){int u=rng()%n,v=rng()%n; if(u!=v) e.push_back({u,v,(int)(rng()%21)+p[u]-p[v]});}
        check(n,e);
    }
    // Large: a weight-1 cycle plus heavier chords, so D[i][j] = (j - i) mod n.
    int N=200; Matrix large, exp(N,std::vector<int>(N));
    for(int i=0;i<N;i++) large.push_back({i,(i+1)%N,1});
    for(int i=0;i<N;i++) if((i*7+3)%N!=i) large.push_back({i,(i*7+3)%N,N+i%5});
    for(int i=0;i<N;i++) for(int j=0;j<N;j++) exp[i][j]=((j-i)%N+N)%N;
    check(N,large,exp);
    std::cout << "ALL WEEK 4 FLOYD C++ TESTS PASSED (108 cases)\n";
}
