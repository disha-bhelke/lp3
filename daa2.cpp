#include <iostream>
#include <queue>
using namespace std;

struct Node{
    char ch;
    int freq;
    Node* left;
    Node* right;

    Node (char c, int f){
        ch=c;
        freq=f;
        left=nullptr;
        right=nullptr;
    }
};

struct Compare{
    bool operator()(Node* a, Node* b){
        return a->freq > b->freq;
    }
};

void generateCodes(Node* root, string code){
    if (root==nullptr) return;

    if (root->left==nullptr && root->right==nullptr){
        cout<<root->ch<<": "<<code<<endl;
        return;
    }

    generateCodes(root->left,code+"0");
    generateCodes(root->right,code+"1");
}

int main(){
    cout<<"Enter number of characters: ";
    int n;
    cin>>n;

    priority_queue<Node*, vector<Node*>, Compare> pq;

    cout<<"Enter char and freq:"<<endl;
    for (int i=0;i<n;i++){
        char ch;
        int freq;
        cin>>ch>>freq;
        pq.push(new Node(ch,freq));
    }

    //create tree
    while (pq.size()>1){
        Node* left=pq.top();
        pq.pop();

        Node* right=pq.top();
        pq.pop();

        Node* parent = new Node('$', left->freq+right->freq);
        parent->left=left;
        parent->right=right;

        pq.push(parent);
    }

    Node* root=pq.top();
    generateCodes(root,"");
}