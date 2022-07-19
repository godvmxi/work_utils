#pragma once

#include <string>

namespace br_video
{
class BrvBitStreamParser
{
public:
    BrvBitStreamParser();
    ~BrvBitStreamParser();
    bool open(std::string filePath, int32_t streamId = 0);
    bool GetNextFrame(char *mem, uint32_t bufSize);
    void SetFrameNum(uint32_t frameNum){m_expectedFrameNum = frameNum;};

private:
    void *m_libavCtx;
    uint32_t m_curFrameIndex;
    uint32_t m_expectedFrameNum;
    int32_t m_streamId;
};

}