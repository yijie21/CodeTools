#include<iostream>
using namespace std;
int main() {
    int x = 0;
    int n;
    cin >> n;
    string s;
    while(cin >> s) {
        if(s.find('+')) {
            x++;
        } else if(s.find('-')) {
            x--;
        }
    }
    cout << x;
}