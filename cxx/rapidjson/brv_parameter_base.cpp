#include "brv_parameter_base.hpp"
#include <string>
#include <rapidjson/document.h>
#include <fstream>
#include <sstream>
#include <vector>
#include <iostream>
#include <iomanip>


//using namespace rapidjson;
//using namespace std;
#define LOG_PARA_D  (std::cout<<"DBG  : ")
#define LOG_PARA_I  (std::cout<<"INFO : ")
#define LOG_PARA_E  (std::cout<<"ERR  : ")
#define URI_MAX_LEN  60
namespace br_video
{
BrvParameterBase::BrvParameterBase(std::string filename):
m_cfgFile(filename)
{

}
BrvParameterBase::~BrvParameterBase()
{
}
bool BrvParameterBase::open()
{
    try
    {
        std::ifstream configFile(m_cfgFile);
        if(!configFile.is_open())
        {
            LOG_PARA_E <<  "open cfg file error" << m_cfgFile << std::endl;
            return false;
        }
        std::istreambuf_iterator<char> begin(configFile), end;
        std::string configData(begin, end);
        configFile.close();
        m_jsonDoc.Parse(configData.data());
        if(m_jsonDoc.IsObject() == false)
        {
            return false;
        }
        //LOG_PARA_D << "Version: " << m_jsonDoc["version"].GetString() << std::endl;

        if(parse_json_cfg()  == false)
        {
            LOG_PARA_E << "parse config file error happend\n" << std::endl;
        }
        return true;
    }
    catch(std::exception &ex)
    {
        LOG_PARA_D << "open para file error: " << ex.what() << std::endl;;
        return false;
    }
}
bool BrvParameterBase::is_open()
{
    return true;
}

void BrvParameterBase::set_value(std::string uri, BRV_PRAR_TYPE_T type, void *val)
{

}
bool BrvParameterBase::get_value(std::string uri, BRV_PRAR_TYPE_T type, void *val)
{
    std::map<std::string, BRV_PARA_OBJECT_T>::iterator iter = this->m_paraMap.find(uri);
    if(iter != this->m_paraMap.end())
    {
        BRV_PARA_OBJECT_T obj = iter->second;
        switch(obj.type)
        {
            case BRV_PARA_INT:
                *((int32_t *)val) = *((int32_t *)(obj.p));
                break;
            case BRV_PARA_FLOAT:
                *((float *)val) = *((float *)(obj.p));
                break;
            default:
                LOG_PARA_E << "NOT SUPPORT PARA TYPE " << obj.type << std::endl;
                break;
        }
        return true;
    }
    else
        return false;
}
uint32_t BrvParameterBase::override_cfg_from_cli()
{
    return 0;
}

bool BrvParameterBase::parse_json_cfg()
{
    do_travers_rapidjson_parse("", m_jsonDoc, "");
    #if 0
    for (rapidjson::Value::ConstMemberIterator iter = m_jsonDoc.MemberBegin(); iter != m_jsonDoc.MemberEnd(); ++iter)
    {
        std::string key = iter->name.GetString();
        do_travers_rapidjson_parse("", m_jsonDoc[key], key);
    }
    #endif
    return true;
}
void BrvParameterBase::do_travers_rapidjson_parse(const std::string &parentPath, const rapidjson::Value &jsNode, const std::string &key)
{
    std::string absPath;
    uint32_t pSize = parentPath.size();
    uint32_t kSzie = key.size();
    if(pSize * kSzie == 0)
    {
        absPath = parentPath + key;
    }
    else
    {
        absPath = parentPath + "/" + key;
    }
    BRV_PARA_OBJECT_T obj;
    obj.num = 0;
    obj.p = nullptr;
    bool *pBool =  nullptr;
    int32_t *pInt = nullptr;
    float *pFloat = nullptr;
    std::string *pStr = nullptr;
    std::vector<int32_t> *pVecInt =  nullptr;
    std::vector<float> *pVecFloat =  nullptr;
    std::vector<std::string> *pVecStr =  nullptr;
    
    std::stringstream ss;
    std::string subKey;
    std::string tmpKey;
    switch(jsNode.GetType())
    {
        case rapidjson::kNullType:
            obj.type = BRV_PARA_NULL;
            add_uri_value(absPath, obj);
            break;
        case rapidjson::kFalseType:
            obj.type = BRV_PARA_BOOL;
            pBool = new bool[1]();
            *pBool = false;
            obj.p = pBool;
            add_uri_value(absPath, obj);
            LOG_PARA_D << "Json URI : " << std::setw(URI_MAX_LEN) << std::left << absPath  << std::setw(10) <<  " bool: " <<  *pBool << std::endl;;
            break;
        case rapidjson::kTrueType:
            obj.type = BRV_PARA_BOOL;
            pBool = new bool[1]();
            *pBool = true;
            obj.p = pBool;
            add_uri_value(absPath, obj);
            LOG_PARA_D << "Json URI : " << std::setw(URI_MAX_LEN) << std::left << absPath  << std::setw(10) <<  " bool: " <<  *pBool << std::endl;;
            break;
        case rapidjson::kStringType:
            obj.type = BRV_PARA_STR;
            pStr = new std::string(jsNode.GetString());
            obj.p = pStr;
            add_uri_value(absPath, obj);
            LOG_PARA_D << "Json URI : " << std::setw(URI_MAX_LEN) << std::left << absPath  << std::setw(10) <<  " Str: " <<  *pStr << std::endl;;
            break;
        case rapidjson::kNumberType:
            if(jsNode.IsInt())
            {
                pInt = new int32_t(jsNode.GetInt());
                obj.p = pInt;
                obj.type = BRV_PARA_INT;
                add_uri_value(absPath, obj);
                LOG_PARA_D << "Json URI : " << std::setw(URI_MAX_LEN) << std::left << absPath  << std::setw(10) <<  " Int: " <<  *pInt << std::endl;;
            }
            else if(jsNode.IsFloat())
            {
                pFloat = new float[1];
                *pFloat = jsNode.GetFloat();
                obj.p = pFloat;
                obj.type = BRV_PARA_FLOAT;
                add_uri_value(absPath, obj);
                LOG_PARA_D << "Json URI : " << std::setw(URI_MAX_LEN) << std::left << absPath  << std::setw(10) <<  " Float: " <<  *pFloat << std::endl;;
            }
            else
            {
                return;
            }
            break;
        case rapidjson::kObjectType:
            obj.type = BRV_PARA_OBJ;
            obj.p = (void *)&jsNode;
            obj.num = jsNode.MemberCount();
            add_uri_value(absPath, obj);
            for(auto iter = jsNode.MemberBegin(); iter != jsNode.MemberEnd(); iter++)
            {
                subKey = iter->name.GetString();
                do_travers_rapidjson_parse(absPath, iter->value, subKey);
            }
            break;
        case rapidjson::kArrayType:
            for(uint32_t i = 0; i< jsNode.Size(); i++)
            {
                ss.clear();
                ss.str("");
                ss << i;
                subKey = ss.str();
                do_travers_rapidjson_parse(absPath, jsNode[i], subKey);
            }
            break;
        default:
            break;
    }

}
void BrvParameterBase::add_uri_value(std:: string uri, BRV_PARA_OBJECT_T obj)
{
    if(uri.size() == 0)
    {
        LOG_PARA_I << "skip uri empty" <<std::endl;
        return;
    }
    this->m_paraMap.insert({uri, obj});
}
std::string BrvParameterBase::get_parse_result_str()
{
    std::stringstream ss;
    std::map<std::string, BRV_PARA_OBJECT_T>::iterator iter = this->m_paraMap.begin();
    bool *pBool =  nullptr;
    int32_t *pInt = nullptr;
    float *pFloat = nullptr;
    std::string *pStr = nullptr;
    std::vector<int32_t> *pVecInt =  nullptr;
    std::vector<float> *pVecFloat =  nullptr;
    std::vector<std::string> *pVecStr =  nullptr;
    for(; iter != this->m_paraMap.end(); iter++)
    {
        
        BRV_PARA_OBJECT_T p = iter->second;
        ss << "Json URI : " << std::setw(URI_MAX_LEN) << std::left << iter->first << std::setw(10);
        switch(p.type)
        {
            case BRV_PARA_BOOL:
                ss << "bool            : " << *(bool *)p.p;
                break;
            case BRV_PARA_INT:
                ss << "int             : " << *(int32_t *)p.p;
                break;
            case BRV_PARA_FLOAT:
                ss << "int             : " << *(float *)p.p;
                break;
            case BRV_PARA_STR:
                ss << "int             : " << *(std::string *)p.p;
                break;
            case BRV_PARA_LIST_INT:
                ss << "list int        : " << p.num;
                pVecInt = (std::vector<int32_t> *)p.p;
                for(auto val : *pVecInt)
                {
                    ss << std::setw(10) <<  val << " ";
                }
                break;
            case BRV_PARA_LIST_FLOAT:
                ss << "list float      : " << p.num;
                pVecFloat = (std::vector<float> *)p.p;
                for(auto val : *pVecFloat)
                {
                    ss << std::setw(10) <<  val << " ";
                }
                break;
            case BRV_PARA_LIST_OBJ:
                ss << "list obj        : " << p.num;
                break;
            case BRV_PARA_LIST_STR:
                ss << "list string     : " << p.num;
                pVecStr = (std::vector<std::string> *)p.p;
                for(auto val : *pVecStr)
                {
                    ss << std::setw(10) <<  val << " ";
                }
                break;
            case BRV_PARA_OBJ:
                ss << "list obj        : ";
                break;
            default:
                ss << "Unknown         : " <<  p.type;
                break;
        }
        ss << std::endl;
    }
    return ss.str();
}

}