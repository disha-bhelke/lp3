#include <iostream>
#include <vector>
using namespace std;

int N;

bool isSafe(vector<vector<int>>& board, int row, int col){

    for (int i=0;i<row;i++){
        if (board[i][col]==1) return false;
    }

    for (int i=row-1, j=col-1; i>=0 && j>=0; i--, j--){
        if (board[i][j]==1) return false;
    }

    for (int i=row-1, j=col+1; i>=0 && j<N; i--, j++){
        if (board[i][j]==1) return false;
    }
    return true;
}

bool solve(vector<vector<int>>& board, int row){

    if (row==N) return true;

    for (int col=0;col<N;col++){
        if (isSafe(board,row,col)){
            board[row][col]=1;
            if (solve(board,row+1)) return true;
            board[row][col]=0;
        }
    }
    return false;
}

int main(){
    cout<<"Enter n: ";
    cin>>N;

    cout<<"Enter column no of first queen in 1st row: ";
    int c;
    cin>>c;

    vector<vector<int>> board(N,vector<int>(N,0));
    board[0][c-1]=1;

    if (solve(board,1)){
        cout<<"sucessful"<<endl;

        for (int i=0;i<N;i++){
            for (int j=0;j<N;j++) cout<<board[i][j]<<" ";
            cout<<endl;
        }
    }else{
        cout<<"doesnt exist"<<endl;
    }

}