#include <iostream>
using namespace std;

int rec(int n){
    if (n<=1) return n;
    return rec(n-1)+rec(n-2);
}

void iter(int n){
    int i=0;
    int j=1;
    cout<<i<<" "<<j<<" ";
    for (int k=0;k<n-2;k++){
        cout<<i+j<<" ";
        int x=j;
        j=i+j;
        i=x;
    }
}

int main(){
    int n;
    cout<<"Enter number n: ";
    cin>>n;

    for (int i=0;i<n;i++){
        cout<<rec(i)<<" ";
    }
    iter(n);
}