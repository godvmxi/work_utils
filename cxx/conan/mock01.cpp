#include <gmock/gmock.h>
#include <gtest/gtest.h>
#include <iostream>
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

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}