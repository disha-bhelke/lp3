#include <iostream>
#include <vector>
using namespace std;

int getIdx(vector<int>& arr, int low, int high){
    int pivot=arr[high];
    int i=low-1;

    for (int j=low;j<high;j++){
        if (arr[j]<=pivot){
            i++;
            swap(arr[i],arr[j]);
        }
    }
    swap(arr[i+1],arr[high]);
    return i+1;
}

int randomidx(vector<int>& arr, int low, int high){
    int ri=low+rand()%(high-low+1);

    swap(arr[ri],arr[high]);
    return getIdx(arr,low,high);
}

void quicksort(vector<int>& arr, int low, int high){
    if (low<high){
        int pi=randomidx(arr,low,high);

        quicksort(arr,low,pi-1);
        quicksort(arr,pi+1,high);
    }
}

int main(){
    cout<<"=====MERGE SORT====="<<endl;
    cout<<"Enter number of elements"<<endl;
    int n;
    cin>>n;

    vector<int> arr;
    for (int i=0;i<n;i++){
        int ele;
        cin>>ele;
        arr.push_back(ele);
    }
    quicksort(arr,0,n-1);

    cout<<"Sorted array: ";
    for (int i=0;i<n;i++) cout<<arr[i]<<" ";
}