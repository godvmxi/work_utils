#include <iostream>
#include "logger.hpp"

int main(){
        initLogger("log/info.log", "log/warning.log", "log/error.log");
        LOG(INFO) << "info " << "test";
        LOG(INFO) << "info " << "test";
        LOG(WARNING) << "warning " << "test";
        LOG(WARNING) << "warning " << "test";
        LOG(ERROR) << "error " << "test";
        LOG(ERROR) << "error " << "test";
}