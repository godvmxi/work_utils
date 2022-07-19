#include "brv_bit_stream_parser.hpp"
#include <iostream>
//#include "brv_dump.hpp"
#include <sstream>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>

extern "C" {
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
#include <libavutil/avutil.h>
};

namespace br_video
{
#define LOG_BS_PARSER_D  (std::cout<<"CASE DBG  : ")
#define LOG_BS_PARSER_I  (std::cout<<"CASE INFO : ")
#define LOG_BS_PARSER_E  (std::cout<<"CASE ERR  : ")
BrvBitStreamParser::BrvBitStreamParser():
m_libavCtx(nullptr),
m_curFrameIndex(0),
m_expectedFrameNum(0),
m_streamId(0)
{
    av_register_all();
}
BrvBitStreamParser::~BrvBitStreamParser()
{
    if(m_libavCtx)
    {

    }
}
bool BrvBitStreamParser::open(std::string filePath, int32_t streamId)
{
    if(m_libavCtx)//close last handler
    {
        LOG_BS_PARSER_D << "close last handler" << std::endl;
        avformat_free_context((AVFormatContext *)m_libavCtx);
        m_curFrameIndex = 0;
        m_libavCtx = nullptr;
    }
    if(avformat_open_input((AVFormatContext **)(&m_libavCtx), filePath.c_str(), nullptr, nullptr) < 0)
    {
        LOG_BS_PARSER_E << "open bitstream fail: " << filePath << std::endl;
        return false;
    }
    av_dump_format((AVFormatContext *)m_libavCtx, 0, filePath.c_str(), 0);
    m_streamId = streamId;
    return true;
}

bool BrvBitStreamParser::GetNextFrame(char *buf, uint32_t bufSize)
{
    if(m_libavCtx == nullptr)
    {
        LOG_BS_PARSER_E << "open bitstream first: " << std::endl;
        return false;
    }
    AVPacket *pkt = av_packet_alloc();
    while(1)
    {
        int ret = av_read_frame((AVFormatContext *)m_libavCtx, pkt);
        if(ret < 0)
        {
            if(pkt->stream_index != m_streamId)
            {
                continue;
            }
        }
        m_curFrameIndex++;
        LOG_BS_PARSER_D << "data size: " << pkt->size << std::endl;
        std::stringstream ss;
        ss << "dump hex frame : " << m_curFrameIndex << std::endl;
        for(int i = 0; i < 32; i++)
        {
            ss << " " << std::setw(2) << std::setfill('0') << std::hex << (int)(pkt->data[i]);
        }
        LOG_BS_PARSER_D << ss.str() << std::endl;
        break;
    }
    av_packet_free(&pkt);
    return false;
}
}
