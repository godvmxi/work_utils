#include <gmock/gmock.h>
#include <gtest/gtest.h>
#include <iostream>
#include <zlib.h>
#include <boost/shared_ptr.hpp>
#include <boost/version.hpp>

#include <qrencode.h>

using ::testing::AtLeast;
using ::testing::NiceMock;
using ::testing::StrictMock;
using ::testing::Return;

class Turtle {
public:
    Turtle() {};
    virtual ~Turtle() {}
    virtual void PenUp() = 0;
    virtual void PenDown() = 0;
    virtual int  Count() = 0;
    #if 0
    virtual void Forward(int distance) = 0;
    virtual void Turn(int degrees) = 0;
    virtual void GoTo(int x, int y) = 0;
    virtual int GetX() const = 0;
    virtual int GetY() const = 0;
    #endif
};


class MockTurtle : public Turtle {
public:
    MockTurtle() {};
    ~MockTurtle() {};
    MOCK_METHOD(void, PenUp, (), (override));
    
    MOCK_METHOD(void, PenDown, (), (override));
    MOCK_METHOD(int, Count, (), (override));
    #if 0
    MOCK_METHOD(void, Forward, (int distance), (override));
    MOCK_METHOD(void, Turn, (int degrees), (override));
    MOCK_METHOD(void, GoTo, (int x, int y), (override));
    MOCK_METHOD(int, GetX, (), (const, override));
    MOCK_METHOD(int, GetY, (), (const, override));
    #endif
};

TEST(PainterTest, CanDrawSomething) {
    #if 0
    MockTurtle turtle;    
    EXPECT_CALL(turtle, PenDown)  
        .Times(AtLeast(2));
    #else
    NiceMock<MockTurtle> turtle;
    //StrictMock<MockTurtle> turtle;
    //MockTurtle turtle;
    #endif
  //Painter painter(&turtle);
    ON_CALL(turtle, Count()).WillByDefault(Return(1));
    turtle.PenDown(); 
    turtle.PenDown();
    std::cout << "Count: " << turtle.Count() << std::endl;
  //EXPECT_TRUE(turtle.PenDown()); 
}

void lib_tester_zlib()
{
    std::cout << "zlib version  : " << zlibVersion() <<std::endl;
}
void lib_tester_boost()
{
    std::cout << "boost version : " << BOOST_LIB_VERSION << std::endl;
    std::vector<boost::shared_ptr<int>> v;
    v.push_back(boost::shared_ptr<int>(new int(1)));
    v.push_back(boost::shared_ptr<int>(new int(2)));
    //std::cout << "boost shared_prt  : " << v << std::endl; 
    std::cout << "boost shared_prt size : " << v.size() << std::endl;
}
void lib_tester_qrencode()
{
    const char *QRTEXT = "欢迎来到我的的博客";
    QRcode *qrCode;
    int version = 5; //设置版本号，这里设为5，对应尺寸：37 * 37
    QRecLevel level = QR_ECLEVEL_H;
    QRencodeMode hint = QR_MODE_8;
    int casesensitive = 1;

    qrCode = QRcode_encodeString(QRTEXT, version, level, hint, casesensitive);
    if (NULL == qrCode)
    {
        std::cerr << "QRcode create fail"<< std::endl;
        return;
    }
    std::cout << "create qr instace ok" << std::endl;
}
void lib_tester()
{
    lib_tester_zlib();
    lib_tester_boost();
    lib_tester_qrencode();

}

int main(int argc, char **argv)
{
    lib_tester();
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}