#include <iostream>
#include <string.h> 
#include <vector>
#include <random>
#include <algorithm>

using namespace std;

vector<string> transpose(const vector<string> data) {
    vector<string> result(data[0].size(), string(data.size(), ' '));
    for (vector<int>::size_type i = 0; i < data[0].size(); i++)
        for (std::vector<int>::size_type j = 0; j < data.size(); j++) {
            result[i][j] = data[j][i];
        }
    return result;
}

string stringGenerator (int N){
  string word;
  static const char alphabet[] = "abcdefghijklmnopqrstuvwxyz";
  for (int i = 0; i < N; ++i) {
    word += alphabet[rand() % (sizeof(alphabet)-1)];
  }
  std::sort(word.begin(), word.end());
  return word;
}

int main() {
  int N, M;
  N = 10; M = 10;
  vector<string> data;
  for (int i = 0; i < M; ++i)
       data.push_back(stringGenerator(N));
  auto res = transpose(data);

  //Rules
  for (int i = 0; i < N; i++)
  {
      cout << "r" << (i % 3) << " ";
      for (int j = 0; j < M; j++)
          cout << res[i][j];
      cout << endl;
  }

  //Queries
  for (int i = 0; i < N; i++)
  {
      int random = rand() % N;
      cout << "r" << (i % 3) << " ";
      for (int j = 0; j < M; j++)
          if (j != random)
              cout << res[i][j];
          else 
              cout << "X";
      cout << endl;
  }


}
