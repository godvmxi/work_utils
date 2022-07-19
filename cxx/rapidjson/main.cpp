#include <brv_parameter_base.hpp>
#include <iostream>
#include <string>
using namespace br_video;
using namespace std;
int main(int argc, char **argv)
{
    BrvParameterBase *para = new BrvParameterBase(argv[1]);
    para->open();
    if(para->is_open())
    {
        cout << "show all json key val --> " << endl;
        string result = para->get_parse_result_str();
        cout <<  result << endl;
    }
    else{
        std::cout << "open json para error" << std::endl;
        delete para;
    }
}