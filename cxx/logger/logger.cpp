#include <cstdlib>
#include <ctime>
#include "logger.h"

std::ofstream Logger::m_info_file;
std::ofstream Logger::m_warn_file;
std::ofstream Logger::m_error_file;

void initLogger(const std::string &info_filename, const std::string &warn_filename, 
                                const std::string &error_filename){
        Logger::m_info_file.open(info_filename.c_str(), std::ofstream::app);
        Logger::m_warn_file.open(warn_filename.c_str(), std::ofstream::app);
        Logger::m_error_file.open(error_filename.c_str(), std::ofstream::app);
}

std::ostream &Logger::getStream(log_rank_t log_rank){
        if(log_rank == INFO){
                return m_info_file.is_open() ? m_info_file : std::cout;
        }
        if(log_rank == WARNING){
                return m_warn_file.is_open() ? m_warn_file : std::cout;
        }
        if(log_rank == ERROR){
                return m_error_file.is_open() ? m_error_file : std::cout;
        }
}

std::ostream &Logger::start(log_rank_t log_rank, const int line, const std::string &fun){
        time_t tm;
        time(&tm);
        char time_string[128];
        strftime(time_string, sizeof(time_string),"[%Y.%m.%d %X] ", localtime(&tm));
        return getStream(log_rank) << time_string 
                                                           << "function[" << fun <<"] " 
                                                           << "line[" << line <<"] " 
                                                           << std::flush;
}

Logger::~Logger(){
        getStream(m_log_rank) << std::endl << std::flush;
        if(m_log_rank == FATAL){
                m_info_file.close();
                m_warn_file.close();
                m_error_file.close();
                abort();
        }
}