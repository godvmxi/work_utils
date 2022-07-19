#include <fstream>
#include <string>
#include <iostream>
#include <map>
#include <vector>
#include <iomanip>
#include <stdint.h>
#include <sstream>
#include <string.h>
using namespace std;
void show_help(char *app)
{
    cout << "Usage: "<< endl << endl;
    cout << "  read from file \n    " << app << " largtest_x drop_duplcate [filePath] " << endl << endl;
    cout << "  read from stdin\n    "<< "cat your_file | " << app << " largtest_x drop_duplcate" << endl << endl;
    cout << "  para : " << endl;
    cout << "    largtest_x    : X value" << endl;
    cout << "    drop_duplcate : remove the the min & same value ids when largtest_x is less then real ids num"<< endl;
    cout << "\t\tTake the example in pdf [200,200,115,110] and X = 1" << endl;
    cout << "\t\t 0: output: " << endl;
    cout << "\t\t\t  ids of the first 200 " << endl;
    cout << "\t\t\t  ids of the second 200 " << endl;
    cout << "\t\t 1: output: " << endl;
    cout << "\t\t\t  ids of the first 200 " << endl;
}
 /**
* @brief get the ids list from the istream description
* @param ifs        istream handler, support ifstream and std::cin
* @param largestX   largest output lines
* @param dropLastSameValueIds drop the duplicate in the min value list to match the num X
*
* @return
*        vector<string> ids list
*/
vector<string> find_the_largest_ids_map(istream &ifs, uint32_t largestX, bool dropLastSameValueIds)
{
    vector<string> retArray;
    map<int32_t, vector<string>> resultMap;
    string ids;
    int32_t val = INT32_MIN;
    int32_t minValInResult = INT32_MIN;
    uint32_t currentIdsNum = 0;
    char line[512]; 

    //cout << "will find the largest " << largestX << " ids from: " << filePath <<endl;
    try
    {
        {
            while(!ifs.eof())
            {
                // error format check begin
                memset(line, 0, 512);
                ifs.getline(line, 512);
                string str(line);
                //empty line
                if(str.size() == 0)
                    continue;
                stringstream ss;
                ss << str;
                string strVal;
                ss >> ids >> strVal;
                //wrong format
                if(ids.size() == 0 || strVal.size() == 0)
                    continue;
                //error format check end
                val = atoi(strVal.c_str());
                //cout <<"  read : "<< setw(16) << setiosflags(ios::right) << ids <<  setw(8)  << val << endl;
                //cout << "if status: " << hex << setfill('0') << setw(8)<< ifs.rdstate() << endl;
                if(minValInResult == INT32_MIN)
                {
                    minValInResult = val;
                }
                if(currentIdsNum > largestX && val < minValInResult)
                {
                    //the largest ids is enough
                    //new smaller value,no need to add to the map
                    //cout << "     no need to add "  << ids << " val: " << val << endl;
                    continue;
                }
                //cout << "\t\tcurent min val: " << minValInResult << " in val: " << val  << endl;                
                map<int32_t, vector<string>>::iterator it = resultMap.find(val);
                if(it != resultMap.end())
                {
                    vector<string> *p = &(it->second);
                    p->push_back(ids);
                }
                else
                {
                    vector<string> t;
                    t.push_back(ids);
                    resultMap.insert(std::pair<int32_t, vector<string>>(val, t));
                }
                currentIdsNum++;
                //remove the useless min ids list from the result map
                if(val < minValInResult)
                {
                    minValInResult = val;
                }
                if(currentIdsNum > largestX)
                {
                    it = resultMap.find(minValInResult);
                    if(it == resultMap.end())
                    {
                        cout << "program error: " << minValInResult <<endl;
                        break;
                    }
                    vector<string> *p = &(it->second);
                    uint32_t minKeyNums = p->size();
                    if(currentIdsNum - minKeyNums >= largestX)
                    {
                        resultMap.erase(it);
                        //cout << "remove " << minValInResult << " num: " << minKeyNums << " next min: " << resultMap.rbegin()->first << endl;
                        currentIdsNum -= minKeyNums;
                        minValInResult = resultMap.begin()->first;
                    }
                }
                
            }
            uint32_t num = 0;
            for(map<int32_t, vector<string>>::reverse_iterator rit = resultMap.rbegin() ; rit != resultMap.rend(); rit++)
            {
                vector<string> *p = &(rit->second);
                for(uint32_t i = 0; i < p->size(); i++)
                {
                    //cout << "val: " << setw(16) << rit->first << " ids: " << setw(16) << p->at(i) << endl;
                    //cout << p->at(i) << endl;
                    retArray.push_back(p->at(i));
                    num++;
                    if(num >= largestX && dropLastSameValueIds)
                    {
                        break;
                    }
                }
            }
            return retArray;
        }
        #if 0
        else//open file fail
        {
            return retArray;
        }
        #endif
    }
    catch(exception &ex)
    {
        //cerr << "open data basae file : " << filePath << " error:" << ex.what() << endl;
        cerr << "open data basae file  error:" << ex.what() << endl;
        return retArray;
    }
}
int main(int argc, char** argv)
{
    char *filePath = nullptr;
    uint32_t removeDuplcatePara = 0;
    if(argc < 3)
    {
        show_help(argv[0]);
        return 0;
    }
    uint32_t largestX = atoi(argv[1]);
    removeDuplcatePara =atoi(argv[2]);
    //return 0;
    bool dropLastSameValueIds = removeDuplcatePara != 0? true: false;
    vector<string> resultArray;
    if(argc == 3)
    {
        //read from stdin
        resultArray =  find_the_largest_ids_map(cin, largestX, dropLastSameValueIds);
    }
    else
    {
        //read from file
        filePath = argv[3];
        ifstream lfs(filePath, ios_base::in);
        if(!lfs.is_open())
        {
            cerr << "open file failed" << endl;
            return 1;
        }
        resultArray =  find_the_largest_ids_map(lfs, largestX, dropLastSameValueIds);
    }
    
    for(auto s : resultArray)
    {
        cout << s << endl;
    }

    return 0;
}