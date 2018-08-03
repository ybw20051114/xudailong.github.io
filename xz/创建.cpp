#include <bits/stdc++.h>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <direct.h>
#include <io.h>
using namespace std;
#define ll long long
#define pqq priority_queue
#define itt ::iterator
int sum;
void getFiles(string cate_dir)
{
    // vector<string> files;//存放文件名
    string x = cate_dir;
    // cout<<
    x += "\\*";
    _finddata_t file;
    long lf;
    sum++;
    for(int i = 1; i < sum; i++)
        cout << "\t";
    cout << cate_dir << endl;
    for(int i = 1; i < sum; i++)
        cout << "\t";
    cout << "{\n";
    //输入文件夹路径
    if ((lf = _findfirst(x.c_str(), &file)) == -1)
    {
        cout << cate_dir << " not found!!!" << endl;
    }
    else
    {
        while(_findnext(lf, &file) == 0)
        {
            //输出文件名
            
            if (file.attrib & _A_SUBDIR)
            {
                if (strcmp(file.name, ".") == 0 || strcmp(file.name, "..") == 0)
                {
                    continue;
                    
                }
                string x = cate_dir + "\\" + file.name ;
                // for(int i = 1; i <= sum; i++)
                // cout << "\t";
                // cout << file.name << endl;
                
                getFiles(x);
            }
            else
            {
                for(int i = 1; i <= sum; i++)
                    cout << "\t";
                cout << file.name << endl;
            }
            
        }
    }
    _findclose(lf);
    //排序，按从小到大排序
    for(int i = 1; i < sum; i++)
        cout << "\t";
    cout << "}\n";
    sum--;
    // sort(files.begin(), files.end());
    return ;
}
map<string, int> aa;
int main(void)
{
    char current_address[500];
    memset(current_address, 0, 500);
    getcwd(current_address, 500); //获取当前路径
    // cout << current_address << endl;
    
    getFiles((string)current_address);
    // for (int i = 0; i < files.size(); i++)
    // {
    // cout<<files[i]<<endl;
    // }
    cin.get();
    return 0;
}