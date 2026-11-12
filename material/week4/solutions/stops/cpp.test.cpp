#include <algorithm>
#include <cassert>
#include <iostream>
#include <random>
#include <vector>
using Flights = std::vector<std::vector<int>>;
int cheapestRoute(int, const Flights&, int, int, int);
static int best;
static void walk(const Flights& f,int city,int used,int cost,int dst,int k) {
    if(used==k+1) return;
    for(const auto& e:f) if(e[0]==city) {
        if(e[1]==dst && (best<0 || cost+e[2]<best)) best=cost+e[2];
        walk(f,e[1],used+1,cost+e[2],dst,k);
    }
}
static int enumerateRoutes(const Flights& f,int src,int dst,int k) { best=src==dst?0:-1; walk(f,src,0,0,dst,k); return best; }
static int layered(int n,const Flights& f,int src,int dst,int k) {
    const long long INF=1LL<<60; std::vector<long long> b(n,INF); b[src]=0; long long ans=src==dst?0:INF;
    for(int t=0;t<=k;t++) {
        std::vector<long long> nx(n,INF);
        for(const auto& e:f) nx[e[1]]=std::min(nx[e[1]],b[e[0]]+e[2]);
        b=nx; ans=std::min(ans,b[dst]);
    }
    return ans>=INF?-1:(int)ans;
}
static void check(int n,const Flights& f,int src,int dst,int k,int expected) {
    Flights before=f;
    int result=cheapestRoute(n,f,src,dst,k);
    if(result!=expected) std::cerr<<"cheapestRoute "<<src<<"->"<<dst<<" k="<<k<<": got "<<result<<", expected "<<expected<<"\n";
    assert(result==expected);
    assert(f==before);
}
int main() {
    Flights sample={{0,1,100},{1,2,100},{2,0,100},{1,3,600},{2,3,200}}, trap={{0,1,100},{1,2,100},{0,2,500}}, chain={{0,1,1},{1,2,1},{2,3,1}};
    check(4,sample,0,3,1,700); check(4,sample,0,3,2,400); check(4,sample,0,0,0,0);
    check(3,trap,0,2,0,500); check(3,trap,0,2,1,200);
    check(3,{{0,1,5}},0,2,2,-1); check(4,chain,0,3,1,-1); check(4,chain,0,3,2,3);
    check(2,{{0,1,7},{0,1,3}},0,1,0,3); check(3,{{0,1,1},{1,0,1},{1,2,10}},0,2,2,11);
    check(3,{{0,1,0},{1,2,0}},0,2,1,0); check(1,{},0,0,0,0); check(3,{{1,2,4}},0,2,2,-1);
    std::mt19937 rng(301);
    for(int t=0;t<200;t++) {
        int n=1+rng()%6, tries=rng()%13; Flights f;
        for(int i=0;i<tries;i++){int u=rng()%n,v=rng()%n; if(u!=v) f.push_back({u,v,(int)(rng()%21)});}
        int src=rng()%n,dst=rng()%n,k=rng()%std::min(n,4);
        int expected=enumerateRoutes(f,src,dst,k);
        assert(expected==layered(n,f,src,dst,k));
        check(n,f,src,dst,k,expected);
    }
    Flights large;
    for(int u=0;u<100;u++) for(int v=0;v<100;v++) if(u!=v) large.push_back({u,v,(u*37+v*91)%10001});
    for(auto q:std::vector<std::vector<int>>{{0,99,99},{5,42,0},{17,3,2}}) check(100,large,q[0],q[1],q[2],layered(100,large,q[0],q[1],q[2]));
    std::cout << "ALL WEEK 4 STOPS C++ TESTS PASSED (216 cases)\n";
}
