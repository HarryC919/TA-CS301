#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int cheapestRoute(int,const int*,int,int,int,int);
static int best;
static void walk(const int* f,int m,int city,int used,int cost,int dst,int k) {
    if(used==k+1) return;
    for(int i=0;i<m;i++) if(f[3*i]==city) {
        if(f[3*i+1]==dst && (best<0 || cost+f[3*i+2]<best)) best=cost+f[3*i+2];
        walk(f,m,f[3*i+1],used+1,cost+f[3*i+2],dst,k);
    }
}
static int enumerateRoutes(const int* f,int m,int src,int dst,int k) { best=src==dst?0:-1; walk(f,m,src,0,0,dst,k); return best; }
static int layered(int n,const int* f,int m,int src,int dst,int k) {
    const long long INF=1LL<<60; long long b[100],nx[100]; long long ans=src==dst?0:INF;
    for(int v=0;v<n;v++) b[v]=INF; b[src]=0;
    for(int t=0;t<=k;t++) {
        for(int v=0;v<n;v++) nx[v]=INF;
        for(int i=0;i<m;i++){long long c=b[f[3*i]]+f[3*i+2]; if(c<nx[f[3*i+1]]) nx[f[3*i+1]]=c;}
        for(int v=0;v<n;v++) b[v]=nx[v];
        if(b[dst]<ans) ans=b[dst];
    }
    return ans>=INF?-1:(int)ans;
}
static void check(int n,const int* f,int m,int src,int dst,int k,int expected) {
    int* before=malloc((size_t)(3*m+1)*sizeof(int)); assert(before);
    memcpy(before,f,(size_t)(3*m)*sizeof(int));
    int result=cheapestRoute(n,f,m,src,dst,k);
    if(result!=expected) fprintf(stderr,"cheapestRoute %d->%d k=%d: got %d, expected %d\n",src,dst,k,result,expected);
    assert(result==expected);
    assert(memcmp(before,f,(size_t)(3*m)*sizeof(int))==0);
    free(before);
}
int main(void) {
    int sample[]={0,1,100, 1,2,100, 2,0,100, 1,3,600, 2,3,200};
    int trap[]={0,1,100, 1,2,100, 0,2,500};
    int chain[]={0,1,1, 1,2,1, 2,3,1};
    int one[]={0,1,5}, par[]={0,1,7, 0,1,3}, cyc[]={0,1,1, 1,0,1, 1,2,10}, zero[]={0,1,0, 1,2,0}, far[]={1,2,4};
    check(4,sample,5,0,3,1,700); check(4,sample,5,0,3,2,400); check(4,sample,5,0,0,0,0);
    check(3,trap,3,0,2,0,500); check(3,trap,3,0,2,1,200);
    check(3,one,1,0,2,2,-1); check(4,chain,3,0,3,1,-1); check(4,chain,3,0,3,2,3);
    check(2,par,2,0,1,0,3); check(3,cyc,3,0,2,2,11); check(3,zero,2,0,2,1,0);
    check(1,NULL,0,0,0,0,0); check(3,far,1,0,2,2,-1);
    srand(301);
    for(int t=0;t<200;t++) {
        int n=1+rand()%6, tries=rand()%13, m=0, f[39];
        for(int i=0;i<tries;i++){int u=rand()%n,v=rand()%n; if(u!=v){f[3*m]=u;f[3*m+1]=v;f[3*m+2]=rand()%21;m++;}}
        int src=rand()%n,dst=rand()%n,k=rand()%(n<4?n:4);
        int expected=enumerateRoutes(f,m,src,dst,k);
        assert(expected==layered(n,f,m,src,dst,k));
        check(n,f,m,src,dst,k,expected);
    }
    int* large=malloc(100*99*3*sizeof(int)); assert(large); int m=0;
    for(int u=0;u<100;u++) for(int v=0;v<100;v++) if(u!=v){large[3*m]=u;large[3*m+1]=v;large[3*m+2]=(u*37+v*91)%10001;m++;}
    int q[3][3]={{0,99,99},{5,42,0},{17,3,2}};
    for(int i=0;i<3;i++) check(100,large,m,q[i][0],q[i][1],q[i][2],layered(100,large,m,q[i][0],q[i][1],q[i][2]));
    free(large);
    puts("ALL WEEK 4 STOPS C TESTS PASSED (216 cases)"); return 0;
}
