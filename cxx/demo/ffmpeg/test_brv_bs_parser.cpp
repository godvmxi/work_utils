
//#include "BaseTest.hpp"
//#include "brv_yaml_helper.hpp"
#include "gtest/gtest.h"
#include <iostream>
#include <string>
#include "brv_bit_stream_parser.hpp"
#include "unistd.h"




extern "C" {
#include <libavutil/frame.h>
#include <libavutil/mem.h>
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
#include <libavutil/avutil.h>
};

#define TEST_START try {
#define TEST_END  \
    }             \
    catch (...) { \
    ASSERT_TRUE(false);\
    }

class InternalUnit : public testing::Test {
};

#define BS_RES_DIR "external/media/vcodec/stream/decoder"
using namespace br_video;
#define LOGT_BS_PARSER_D  (std::cerr<<"BS PARSER DBG  : ")
#define LOGT_BS_PARSER_I  (std::cout<<"BS PARSER INFO : ")
#define LOGT_BS_PARSER_E  (std::cerr<<"BS PARSER ERR  : ")
#define LOGT_BS_PARSER_W  (std::cout<<"BS PARSER WARN : ")
class TestBrvBsParser : public testing::Test
{
public:
    TestBrvBsParser(void){};
    ~TestBrvBsParser(void) {};
protected:
    virtual void SetUp();
    virtual void TearDown();
};


void TestBrvBsParser::SetUp()
{
}
void TestBrvBsParser::TearDown()
{

}


TEST_F(TestBrvBsParser, h264)
{
    bool ret = false;
    std::string bsFile="Jockey_1280x720_8bit.264";
    BrvBitStreamParser *parser = new(BrvBitStreamParser);
    ASSERT_TRUE(parser != nullptr);
    std::string filePath = std::string(BS_RES_DIR) + "/" + bsFile;
    LOGT_BS_PARSER_D << "open bs file: " << filePath << std::endl;
    ret = parser->open(filePath, 0);
    ASSERT_TRUE(ret != false);
    for(int i = 0; i < 10; i++)
    {
        ret = parser->GetNextFrame(nullptr, 2048);
        LOGT_BS_PARSER_D << "get next frame " << i << " ret: " << ret << std::endl;
        usleep(1000000);
    }

}




GTEST_API_ int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);

    int rc = RUN_ALL_TESTS();
    return rc;
}


