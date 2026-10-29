#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int* mergeSorted(const int*,int,const int*,int,int*);
static int cmp(const void* a,const void* b) {
    int x=*(const int*)a,y=*(const int*)b; return (x>y)-(x<y);
}
static void check(const int* a,int n,const int* b,int m) {
    int *ac=malloc((n+1)*sizeof(int)),*bc=malloc((m+1)*sizeof(int));
    int *expected=malloc((n+m+1)*sizeof(int));
    assert(ac && bc && expected);
    if(n) {memcpy(ac,a,n*sizeof(int));memcpy(expected,a,n*sizeof(int));}
    if(m) {memcpy(bc,b,m*sizeof(int));memcpy(expected+n,b,m*sizeof(int));}
    qsort(expected,n+m,sizeof(int),cmp);
    int size=-1; int* result=mergeSorted(a,n,b,m,&size);
    assert(size==n+m);
    if(n+m) {
        assert(result && result!=a && result!=b);
        assert(memcmp(result,expected,(n+m)*sizeof(int))==0);
        result[0]=123456789;
    } else assert(result==NULL);
    if(n) assert(memcmp(a,ac,n*sizeof(int))==0);
    if(m) assert(memcmp(b,bc,m*sizeof(int))==0);
    free(ac);free(bc);free(expected);free(result);
}
int main(void) {
    int a[]={1,4,9},b[]={2,2,3,10},one[]={1},two[]={1,2};
    int lo[]={-1000000000,0},hi[]={0,1000000000},tail[]={1,2,3},nine[]={9};
    int ties[]={2,2,2,2,2};
    check(NULL,0,NULL,0);check(NULL,0,two,2);check(two,2,NULL,0);
    check(one,1,one,1);check(a,3,b,4);check(lo,2,hi,2);
    check(tail,3,nine,1);check(nine,1,tail,3);check(ties,5,ties,3);
    srand(301);
    for(int t=0;t<100;t++) {
        int x[60],y[60],n=rand()%60,m=rand()%60;
        for(int i=0;i<n;i++) x[i]=rand()%41-20;
        for(int i=0;i<m;i++) y[i]=rand()%41-20;
        qsort(x,n,sizeof(int),cmp);qsort(y,m,sizeof(int),cmp);check(x,n,y,m);
    }
    int* x=malloc(100000*sizeof(int));int* y=malloc(100000*sizeof(int));assert(x && y);
    for(int i=0;i<100000;i++){x[i]=2*i;y[i]=2*i+1;}
    check(x,100000,y,100000);free(x);free(y);
    puts("ALL WEEK 2 C TESTS PASSED (110 cases)");return 0;
}
