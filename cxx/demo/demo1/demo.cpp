#include <iostream>
#include <string.h>
#include <sstream>
#include <queue>
using namespace std;
struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};// implement solution in this class
class Solution{
    public:
        struct ListNode* reverse(ListNode* list)
        {
            struct ListNode *pre = nullptr;
            struct ListNode *cur = list;
            struct ListNode *next = nullptr;
            while(cur != nullptr)
            {
                next = cur->next;
                cur->next = pre;
                pre = cur;
                cur = next;
            }
            list = pre;
            return list;
        }
        struct ListNode *create_demo_list()
        {
            struct ListNode *head = nullptr;
            struct ListNode *p = nullptr;
            struct ListNode *cur = head;
            for(int i = 1 ; i < 6; i++)
            {
                p = (struct ListNode *)malloc(sizeof(struct ListNode));
                //p = new sturct ListNode[1];
                
                if(p == nullptr)
                {
                    throw new runtime_error("can not malloc memory");
                }
                if(head == nullptr)
                {
                    head = p;
                }
                else
                {
                    cur->next = p;
                }
                cur  = p;
                memset(p, 0, sizeof(struct ListNode));
                p->val = i;
                cur = p;
            }
            return head;
        }
        void show_list_node( ListNode *l)
        {
            stringstream ss;
            struct ListNode *p = l;
            while (p)
            {
                ss << " " <<  p->val;
                p = p->next;
            }
            cout << ss.str() << endl;
        }

};
int main(void){
    // write a test code here
    Solution *s = new Solution(); 
    struct ListNode *origin = s->create_demo_list();
    cout << "show origin list" << endl;
    s->show_list_node(origin);
    cout << "show reserve list" << endl;
    struct ListNode *reverse =  s->reverse(origin);
    s->show_list_node(reverse);
    cout << "show reserve list done" << endl;
    
    return 0;

}

