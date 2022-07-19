#pragma once
#include "brv_parameter_base.hpp"
#include <string>
#include <rapidjson/document.h>
#include <map>
#include <map>
namespace br_video
{
typedef enum{
    BRV_PARA_NULL = -1,
    BRV_PARA_BOOL = 0,
    BRV_PARA_INT = 1,
    BRV_PARA_FLOAT = 2,
    BRV_PARA_STR = 3,
    BRV_PARA_OBJ = 4,
    BRV_PARA_LIST_INT = 5,
    BRV_PARA_LIST_FLOAT = 6,
    BRV_PARA_LIST_STR = 7,
    BRV_PARA_LIST_OBJ = 8,
    BRV_PARA_MAX = 100
}BRV_PRAR_TYPE_T;
typedef struct
{
    BRV_PRAR_TYPE_T type;
    void *p;
    int32_t num; //only works on list uri
}BRV_PARA_OBJECT_T;
class BrvParameterBase
{
public:
    BrvParameterBase(std::string filename);
    virtual ~BrvParameterBase();
    bool open();
    bool is_open();
    void set_value(std::string uri, BRV_PRAR_TYPE_T type, void *val);
    bool get_value(std::string uri, BRV_PRAR_TYPE_T type, void *val);
    std::string get_parse_result_str();
private:
    rapidjson::Document m_jsonDoc;
    std::map<std::string, BRV_PARA_OBJECT_T> m_paraMap;
    std::string m_cfgFile;



    uint32_t override_cfg_from_cli();
    void do_travers_rapidjson_parse(const std::string &parentPath, const rapidjson::Value &root, const std::string &key);
    bool parse_json_cfg();
    void add_uri_value(std:: string uri, BRV_PARA_OBJECT_T obj);
};
}