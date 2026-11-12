#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define INF 1000000000
int* floydWarshall(int,const int*,int);
static int* bellmanFordAll(int n,const int* e,int m) {
    int* rows=malloc((size_t)(n*n)*sizeof(int)); assert(rows);
    for(int s=0;s<n;s++) {
        int* d=rows+s*n; for(int v=0;v<n;v++) d[v]=INF; d[s]=0;
        for(int r=0;r<n-1;r++) for(int i=0;i<m;i++)
            if(d[e[3*i]]!=INF && d[e[3*i]]+e[3*i+2]<d[e[3*i+1]]) d[e[3*i+1]]=d[e[3*i]]+e[3*i+2];
    }
    return rows;
}
static void check(int n,const int* e,int m,const int* expected) {
    int* before=malloc((size_t)(3*m+1)*sizeof(int)); assert(before);
    memcpy(before,e,(size_t)(3*m)*sizeof(int));
    int* result=floydWarshall(n,e,m);
    int* oracle=expected?NULL:bellmanFordAll(n,e,m);
    assert(result!=NULL);
    assert(memcmp(result,expected?expected:oracle,(size_t)(n*n)*sizeof(int))==0);
    assert(memcmp(before,e,(size_t)(3*m)*sizeof(int))==0);
    free(result); free(oracle); free(before);
}
int main(void) {
    int ex[]={0,1,3, 0,3,7, 1,0,8, 1,2,2, 2,0,5, 2,3,1, 3,0,2};
    int exD[]={0,3,5,6, 5,0,2,3, 3,6,0,1, 2,5,7,0};
    check(4,ex,7,exD);
    int oneD[]={0}; check(1,NULL,0,oneD);
    int neg[]={0,1,4, 0,2,5, 2,1,-3}, negD[]={0,2,5, INF,0,INF, INF,-3,0}; check(3,neg,3,negD);
    int un[]={0,1,1}, unD[]={0,1,INF, INF,0,INF, INF,INF,0}; check(3,un,1,unD);
    int guard[]={1,2,-5}, guardD[]={0,INF,INF, INF,0,-5, INF,INF,0}; check(3,guard,1,guardD);
    int par[]={0,1,5, 0,1,2, 1,0,4}, parD[]={0,2, 4,0}; check(2,par,3,parD);
    srand(301);
    for(int t=0;t<100;t++) {
        int n=1+rand()%8, tries=rand()%21, m=0, e[60], p[8];
        for(int i=0;i<n;i++) p[i]=rand()%21;
        // w = base + p[u] - p[v] with base >= 0: some edges are negative, no cycle is.
        for(int i=0;i<tries;i++){int u=rand()%n,v=rand()%n; if(u!=v){e[3*m]=u;e[3*m+1]=v;e[3*m+2]=rand()%21+p[u]-p[v];m++;}}
        check(n,e,m,NULL);
    }
    // Large: a weight-1 cycle plus heavier chords, so D[i][j] = (j - i) mod n.
    int N=200, m=0; int* large=malloc((size_t)(2*N*3)*sizeof(int)); int* exp=malloc((size_t)(N*N)*sizeof(int)); assert(large && exp);
    for(int i=0;i<N;i++){large[3*m]=i;large[3*m+1]=(i+1)%N;large[3*m+2]=1;m++;}
    for(int i=0;i<N;i++) if((i*7+3)%N!=i){large[3*m]=i;large[3*m+1]=(i*7+3)%N;large[3*m+2]=N+i%5;m++;}
    for(int i=0;i<N;i++) for(int j=0;j<N;j++) exp[i*N+j]=((j-i)%N+N)%N;
    check(N,large,m,exp); free(large); free(exp);
    puts("ALL WEEK 4 FLOYD C TESTS PASSED (108 cases)"); return 0;
}
