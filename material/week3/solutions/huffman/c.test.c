#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char** huffmanCodes(const int*,int);
static int cmpLong(const void* a,const void* b) {
    long long x=*(const long long*)a,y=*(const long long*)b; return (x>y)-(x<y);
}
static int cmpStr(const void* a,const void* b) {
    return strcmp(*(char* const*)a,*(char* const*)b);
}
static long long optimalCost(const int* freq,int n) {
    // Oracle: total cost = sum of all merged weights (two-queue Huffman on sorted input).
    if(n==1) return freq[0];
    long long *leaves=malloc(n*sizeof(long long)),*merged=malloc(n*sizeof(long long));
    assert(leaves && merged);
    for(int k=0;k<n;k++) leaves[k]=freq[k];
    qsort(leaves,n,sizeof(long long),cmpLong);
    int i=0,j=0,m=0; long long cost=0;
    for(int k=1;k<n;k++) {
        long long w=0;
        for(int pick=0;pick<2;pick++)
            w+=(j>=m || (i<n && leaves[i]<=merged[j]))?leaves[i++]:merged[j++];
        merged[m++]=w; cost+=w;
    }
    free(leaves); free(merged); return cost;
}
static void check(const int* freq,int n) {
    int* before=malloc(n*sizeof(int)); assert(before); memcpy(before,freq,n*sizeof(int));
    char** codes=huffmanCodes(freq,n);
    assert(codes!=NULL && memcmp(freq,before,n*sizeof(int))==0);
    long long cost=0;
    for(int k=0;k<n;k++) {
        assert(codes[k]!=NULL && codes[k][0]!='\0' && strspn(codes[k],"01")==strlen(codes[k]));
        cost+=(long long)freq[k]*(long long)strlen(codes[k]);
    }
    char** ordered=malloc(n*sizeof(char*)); assert(ordered); memcpy(ordered,codes,n*sizeof(char*));
    qsort(ordered,n,sizeof(char*),cmpStr);
    for(int k=1;k<n;k++) assert(strncmp(ordered[k],ordered[k-1],strlen(ordered[k-1]))!=0);
    assert(cost==optimalCost(freq,n));
    for(int k=0;k<n;k++) free(codes[k]);
    free(codes); free(ordered); free(before);
}
int main(void) {
    int one[]={7},two[]={5,5},four[]={1,1,1,1},clrs[]={45,13,12,16,9,5},skew[]={1,2,4,8,16};
    int big[]={1000000,1,1},nines[]={3,3,3,3,3,3,3,3,3};
    char** single=huffmanCodes(one,1); assert(single && strcmp(single[0],"0")==0); free(single[0]); free(single);
    check(one,1);check(two,2);check(four,4);check(clrs,6);check(skew,5);check(big,3);check(nines,9);
    srand(301);
    for(int t=0;t<100;t++) {
        int f[40],n=1+rand()%40;
        for(int k=0;k<n;k++) f[k]=1+rand()%50;
        check(f,n);
    }
    int* large=malloc(1000*sizeof(int)); assert(large);
    for(int k=0;k<1000;k++) large[k]=1+(int)(((long long)rand()*rand())%1000000);
    check(large,1000); free(large);
    puts("ALL WEEK 3 HUFFMAN C TESTS PASSED (108 cases)"); return 0;
}
