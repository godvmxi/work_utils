#include "rapidjson/document.h"     // rapidjson's DOM-style API
#include "rapidjson/prettywriter.h" // for stringify JSON
#include <cstdio>
#include <iostream>

using namespace rapidjson;
using namespace std;

int cc_json(Value& js_value, int d = 0){
    string tmp;
    char buf ;
    if(js_value.IsNull() ||js_value.IsBool() ||js_value.IsNumber() ||js_value.IsString())
    {
        for(int i = 0; i < d+1; i++){
            cout << "  ";
        }
    }
    if(js_value.IsNull())
    {
        cout << "(null)";
    }else if(js_value.IsBool())
    {
        cout << (js_value.GetBool()) ;
        cout << "(bool)";
    }else if(js_value.IsObject())
    {
        for(auto iter = js_value.MemberBegin(); iter != js_value.MemberEnd(); ++iter)
        {
            auto key = (iter->name).GetString();
            for(int i = 0; i < d; i++){
                cout << "  ";
            }
            cout << "- "<< key <<  "(object): ";
            cout << endl;
            cc_json(js_value[key], d+1);
            if(js_value[key].IsArray()) continue;
            if(iter+1 == js_value.MemberEnd()) continue;
            cout <<endl;
        }
    }else if(js_value.IsArray())
    {
        //buf = TYPE_ARRAY_START;
        for(auto i = 0; i < js_value.Size(); ++i)
        {
            cc_json(js_value[i], d);
            cout <<endl;
        }
        //buf = TYPE_OBJECT_ARRAY_END;
    }else if(js_value.IsNumber())
    {
        cout << (js_value.GetDouble()) ;
        cout << "(number)";
    }else if(js_value.IsString())
    {
        cout << (js_value.GetString()) ;
        cout << "(string)";
    }else
    {
        cout << "(error)";
    }
    return 0;
}
int main(){
    std::string load_str = " { \"hello\" : \"world\", \"t\" : true , \"f\" : false, \"n\": null, \"i\":123, \"pi\": 3.1416, \"a\":[1, 2, 3, 4],\"abc\":{\"ded\":[\"ddd\",\"eee\"]} } ";
    cout << "Original JSON:"<< endl << load_str.c_str() << endl;
    rapidjson::Document readdoc;
    readdoc.Parse<0>(load_str.c_str());
    if(readdoc.HasParseError())
    {
        cout << "GetParseError" << endl;;
    }
    cout << "------遍历开始------" << endl;
    cc_json(readdoc, 0);
    cout << "------遍历结束------" <<endl;
}