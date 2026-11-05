#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char* longestCommonSubsequence(const char*,const char*);
static int lcsLength(const char* a,const char* b) {
    int n=(int)strlen(b); int* prev=calloc(n+1,sizeof(int)); int* cur=calloc(n+1,sizeof(int));
    assert(prev && cur);
    for(const char* x=a;*x;x++) {
        for(int j=1;j<=n;j++) cur[j]=*x==b[j-1]?prev[j-1]+1:(prev[j]>cur[j-1]?prev[j]:cur[j-1]);
        int* t=prev;prev=cur;cur=t;
    }
    int r=prev[n]; free(prev); free(cur); return r;
}
static int isSubsequence(const char* s,const char* t) {
    for(;*t;t++) if(*s && *s==*t) s++;
    return *s=='\0';
}
static void check(const char* a,const char* b,int expected) {
    char* ac=malloc(strlen(a)+1); char* bc=malloc(strlen(b)+1); assert(ac && bc);
    strcpy(ac,a); strcpy(bc,b);
    char* result=longestCommonSubsequence(a,b);
    assert(result!=NULL && result!=a && result!=b);
    assert((int)strlen(result)==(expected<0?lcsLength(a,b):expected));
    assert(isSubsequence(result,a) && isSubsequence(result,b));
    assert(strcmp(a,ac)==0 && strcmp(b,bc)==0);
    free(result); free(ac); free(bc);
}
int main(void) {
    check("","",0);check("","ABC",0);check("ABC","",0);check("ABC","DEF",0);check("a","A",0);
    check("ABCB","BDCAB",3);check("ABCBDAB","BDCABA",4);check("AGGTAB","GXTXAYB",4);check("ABC","ABC",3);
    check("ACE","ABCDE",3);check("AAAA","AA",2);check("XMJYAUZ","MZJAWXU",4);
    char* r=longestCommonSubsequence("ABCB","BDCAB"); assert(r && strcmp(r,"BCB")==0); free(r);
    srand(301);
    for(int t=0;t<100;t++) {
        char a[30],b[30]; int n=rand()%25,m=rand()%25;
        for(int i=0;i<n;i++) a[i]="ABC"[rand()%3]; a[n]='\0';
        for(int i=0;i<m;i++) b[i]="ABC"[rand()%3]; b[m]='\0';
        check(a,b,-1);
    }
    char* x=malloc(1001); char* y=malloc(1001); assert(x && y);
    for(int i=0;i<1000;i++){x[i]="AB"[i%2];y[i]="BA"[i%2];} x[1000]=y[1000]='\0';
    check(x,y,999); free(x); free(y);
    puts("ALL WEEK 3 LCS C TESTS PASSED (113 cases)"); return 0;
}
