#include <iostream>
#include <thread>
#include <functional>
using namespace std;

// implement solution in this class

class ZeroEvenOdd {
private:
    int m_N;   
public:
    ZeroEvenOdd(int n){
        m_N = n;
    }
    // printNumber(x) outputs "x", where x is an integer.
    void zero(function<void(int)> printNumber) {
    }
    void even(function<void(int)> printNumber) {
    }
    void odd(function<void(int)> printNumber) {
    }
};

class Tester {
public:
    Tester() {}
    void test(int n) {
        cout << endl << "n = " << n << " => ";
        ZeroEvenOdd zeo(n);
        try {
            std::thread threadA(_threadFun, 'A', std::ref(zeo));
            std::thread threadB(_threadFun, 'B', std::ref(zeo));
            std::thread threadC(_threadFun, 'C', std::ref(zeo));
            threadA.join();
            threadB.join();
            threadC.join();
        } catch (const std::exception& ex) {
            cout << endl << "!!!! " << ex.what() << endl;
        }
    }
private:
    // printNumber(x) outputs "x", where x is an integer.
    static void _printNmber(int no)
    {
        cout << no;
    }
    static void _threadFun(char id, ZeroEvenOdd& zeo) {
        if (id == 'A') zeo.zero(_printNmber);
        else if (id == 'B') zeo.even(_printNmber);
        else if (id == 'C') zeo.odd(_printNmber);
        else return;
    }
};
int main(void)
{
    Tester tester;
    for (int i=0; i<10; i++)
    {
        tester.test(i);
    }
    return 0;
}