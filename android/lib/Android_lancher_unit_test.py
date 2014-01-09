import autotestunit
import time

case_1 =     [  
                  {'point':['app1_0','app1_a'],     'check':[ ['app1','main'] ] } ,
                  {'point':['back_0','back_a'],     'check':[ [ 'app1','null' ]  ] } 
            ]
case_2 =     [  
                  {'point':['app1_0','app1_a'],     'check':[ ['app1','main'] ] } ,
                  {'point':['home'],                'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_a'],     'check':[ ['app1','main'] ] } ,
                  {'point':['back_0','back_a'],     'check':[ [ 'app1','null' ]  ] } 
            ]
case_3 =     [  
                  {'point':['app1_0','app1_a'],     'check':[ ['app1','main'] ] } ,
                  {'point':['home'],                'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_a'],     'check':[ ['app1','main'] ] } ,
                  {'point':['back_0','back_a'],     'check':[ [ 'app1','null' ]  ] } 
            ]
case_4 =     [  
                  {'point':['app1_0','app1_a'],     'check':[ ['app1','main'] ]  } ,
                  {'point':['home'],                'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['home'],                'check':[ ['app1','main'] ] } ,
                  {'point':['back_0','back_a'],     'check':[ [ 'app1','null' ]  ] } 
            ] #????

case_5 =     [  
                  {'point':['app1_0','app1_a'],     'check':[ ['app1','main'] ] } ,
                  {'point':['home'],                'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],     'check':[ ['app1','extend'] ] } ,
                  {'point':['home'],                'check':[ [ 'app1','extend' ]  ] } ,
                  {'point':['back_0','back_b'],     'check':[ [ 'app1','null' ]  ] } 
            ]
case_6 =     [  
                  {'point':['app1_0','app1_a'],     'check':[ ['app1','main'] ] } ,
                  {'point':['home'],                'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],     'check':[ ['app1','extend'] ] } ,
                  {'point':['back_0','back_a'],     'check':[ [ 'app1','extend' ]  ] } ,
                  {'point':['back_0','back_b'],     'check':[ ['app1','null'] ] } 
            ]
case_7 =     [  
                  {'point':['app1_0','app1_a'],     'check':[ ['app1','main'] ] } ,
                  {'point':['home'],                'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],     'check':[ ['app1','extend'] ] } ,
                  {'point':['back_0','back_b'],     'check':[ [ 'app1','null' ]  ] }  
            ]
case_8 =     [  
                  {'point':['app1_0','app1_a'],     'check':[ ['app1','main'] ] } ,
                  {'point':['home'] ,               'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],     'check':[ ['app1','extend'] ] } ,
                  {'point':['app1_0','app1_a'],     'check':[ [ 'app1','main' ]  ] } ,
                  {'point':['back_0','back_a'],     'check':[ [ 'app1','null' ]  ] }   
                  
            ]
case_9 =     [  
                  {'point':['app1_0','app1_a'],     'check':[ ['app1','main'] ] } ,
                  {'point':['home'],                'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],     'check':[ ['app1','extend'] ] } ,
                  {'point':['back_0','back_b'],     'check':[ [ 'app1','null' ]  ] } 
            ]
case_10 =     [  
                  {'point':['app1_0','app1_a'],     'check':[ ['app1','main'] ] } ,
                  {'point':['home'],                'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],     'check':[ ['app1','extend'] ] } ,
                  {'point':['app2_0','app2_a'],     'check':[ ['app1','extend'],['app2','main'] ] } ,
                  {'point':['home'],                'check':[ ['app2','pip'] ,['app1','extend'] ] } ,
                  
                  
                  {'point':['back_0','back_a'],     'check':[ ['app2','pip'] ,['app1','extend'] ] } ,
                  {'point':['app2_0','app2_a'],     'check':[ ['app2','main'],['app1','extend'] ] } ,
                  {'point':['back_0','back_a'],     'check':[ ['app2','null'],['app1','extend'] ] } ,
                  {'point':['back_0','back_b'],     'check':[ ['app1','null'] ] } 
               
            ]
case_11 =     [  
                  {'point':['app1_0','app1_a'],     'check':[ ['app1','main'] ] } ,
                  {'point':['home'],                'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],     'check':[ ['app1','extend'] ] } ,
                  {'point':['app2_0','app2_a'],     'check':[ ['app1','extend'],['app2','main'] ] } ,
                  {'point':['home'],                'check':[ ['app2','pip'] ,['app1','extend'] ] } ,
                  
                  
                  {'point':['back_0','back_b'],     'check':[ ['app2','pip'] ,['app1','null'] ] } ,
                  {'point':['home'],     'check':[ ['app2','main']] } ,
                  {'point':['back_0','back_a'],     'check':[ ['app2','null'] ] }  
            ]
case_12 =     [  
                  {'point':['app1_0','app1_a'],     'check':[ ['app1','main']                   ] } , 
                  {'point':['home'],                'check':[ [ 'app1','pip' ]                  ] } ,
                  {'point':['app1_0','app1_b'],     'check':[ ['app1','extend']                 ] } ,
                  {'point':['app2_0','app2_a'],     'check':[ ['app1','extend'],['app2','main'] ] } ,
                  {'point':['home'],                'check':[ ['app2','pip'] ,['app1','extend'] ] } ,                 
                  
                  {'point':['home'],                'check':[ ['app2','main'] ,['app1','extend'] ] } ,
                  {'point':['back_0','back_a'],     'check':[ ['app2','null'],['app1','extend'] ] } ,
                  {'point':['back_0','back_b'],     'check':[ ['app1','null'] ] } 
            ]
case_13 =     [  
                   {'point':['app1_0','app1_a'],'check':[ ['app1','main'] ] } ,
                  {'point':['home'],'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],'check':[ ['app1','extend'] ] } ,
                  {'point':['app2_0','app2_a'],'check':[ ['app1','extend'],['app2','main'] ] } ,
                  {'point':['home'],'check':[ ['app2','pip'] ,['app1','extend'] ] } ,
                  
                  
                  {'point':['app1_0','app1_a'],'check':[ ['app1','main'] ,['app2','null'] ] } ,
                  {'point':['back_0','back_a'],'check':[ ['app2','null'] ] }
            ]
case_14 =     [  
                  {'point':['app1_0','app1_a'],'check':[ ['app1','main'] ] } ,
                  {'point':['home'],'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],'check':[ ['app1','extend'] ] } ,
                  {'point':['app2_0','app2_a'],'check':[ ['app1','extend'],['app2','main'] ] } ,
                  {'point':['home'],'check':[ ['app2','pip'] ,['app1','extend'] ] } ,
                  
                  
                  {'point':['app1_0','app1_b'],'check':[ ['app1','extend'] ,['app2','pip'] ] } ,
                  {'point':['back_0','back_b'],'check':[ ['app1','null'] ,['app2','pip'] ] } ,
                  {'point':['app2_0','app2_a'],'check':[ ['app2','main'] ] } ,
                  {'point':['back_0','back_a'],'check':[ ['app2','null'] ] }
            ]
case_15 =     [  
                  {'point':['app1_0','app1_a'],'check':[ ['app1','main'] ] } ,
                  {'point':['home'],'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],'check':[ ['app1','extend'] ] } ,
                  {'point':['app2_0','app2_a'],'check':[ ['app1','extend'],['app2','main'] ] } ,
                  {'point':['home'],'check':[ ['app2','pip'] ,['app1','extend'] ] } ,
                  
                  {'point':['app2_0','app2_a'],'check':[ ['app1','extend'] ,['app2','main'] ] } ,
                  {'point':['back_0','back_b'],'check':[ ['app1','null'] ,['app2','main'] ] } ,
                  {'point':['back_0','back_a'],'check':[ ['app2','null'] ] }
            ]
case_16 =     [  
                  {'point':['app1_0','app1_a'],'check':[ ['app1','main'] ] } ,
                 {'point':['home'],'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],'check':[ ['app1','extend'] ] } ,
                  {'point':['app2_0','app2_a'],'check':[ ['app1','extend'],['app2','main'] ] } ,
                  {'point':['home'],'check':[ ['app2','pip'] ,['app1','extend'] ] } ,
                  
                  
                  {'point':['app2_0','app2_b'],'check':[ ['app2','extend'] ,['app1','null'] ] } ,
                  {'point':['back_0','back_b'],'check':[ ['app2','null'] ] }
            ]
case_17 =     [  
                  {'point':['app1_0','app1_a'],'check':[ ['app1','main'] ] } ,
                  {'point':['home'],'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],'check':[ ['app1','extend'] ] } ,
                  {'point':['app2_0','app2_a'],'check':[ ['app1','extend'],['app2','main'] ] } ,
                  {'point':['home'],'check':[ ['app2','pip'] ,['app1','extend'] ] } ,
                  
                  
                  {'point':['app3_0','app3_a'],'check':[ ['app3','main'] ,['app1','extend'],['app2','null'] ] } ,
                  {'point':['back_0','back_a'],'check':[ ['app3','null'],['app1','extend'] ] },
                  {'point':['back_0','back_b'],'check':[ ['app1','null'] ] }
            ]
case_18 =     [  
                  {'point':['app1_0','app1_a'],'check':[ ['app1','main'] ] } ,
                  {'point':['home'],'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],'check':[ ['app1','extend'] ] } ,
                  {'point':['app2_0','app2_a'],'check':[ ['app1','extend'],['app2','main'] ] } ,
                  {'point':['home'],'check':[ ['app2','pip'] ,['app1','extend'] ] } ,
                  
                  
                  {'point':['app3_0','app3_b'],'check':[ ['app2','pip'] ,['app3','extend'],['app1','null'] ] } ,
                  {'point':['app2_0','app2_a'],'check':[ ['app2','main'],['app3','extend'] ] },
                  {'point':['back_0','back_a'],'check':[ ['app2','null'],['app3','extend'] ] },
                  {'point':['back_0','back_b'],'check':[ ['app3','null'] ] }
            ]
case_19 =     [  
                  {'point':['app1_0','app1_a'],'check':[ ['app1','main'] ] } ,
                  {'point':['home'],'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],'check':[ ['app1','extend'] ] } ,
                  {'point':['app2_0','app2_a'],'check':[ ['app1','extend'],['app2','main'] ] } ,
                  {'point':['back_0','back_a'],'check':[  ['app2','null'] ,['app1','extend'] ] } ,
                  {'point':['back_0','back_b'],'check':[ ['app1','null'] ] }
            ]
case_20 =     [  
                  {'point':['app1_0','app1_a'],'check':[ ['app1','main'] ] } ,
                  {'point':['home'],'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],'check':[ ['app1','extend'] ] } ,
                  {'point':['app2_0','app2_a'],'check':[ ['app1','extend'],['app2','main'] ] } ,
                  
                  
                  {'point':['back_0','back_b'],'check':[ ['app2','main'] ,['app1','null'] ] } ,
                  {'point':['back_0','back_a'],'check':[ ['app2','null'] ] }
            ]
case_21 =     [  
                  {'point':['app1_0','app1_a'],'check':[ ['app1','main'] ] } ,
                  {'point':['home'],'check':[ [ 'app1','pip' ]  ] } ,
                  {'point':['app1_0','app1_b'],'check':[ ['app1','extend'] ] } ,
                  
                  
                  {'point':['app2_0','app2_b'],'check':[ ['app2','extend'] ] } ,
                  
                  
                  {'point':['back_0','back_b'],'check':[ ['app2','null']  ] } 
            ]
case_22 =     [  
                  {'point':['app1_0','app1_a'],'check':[ ['app1','main'] ] } ,
                  {'point':['home'],'check':[ [ 'app1','pip' ]  ] } ,
                  
                  {'point':['app2_0','app2_a'],'check':[ ['app1','null'],['app2','main']  ] } ,
                  
                  
                  {'point':['back_0','back_a'], 'check':[ ['app2','null'] ] } 
            ]
case_23 =     [  
                  {'point':['app1_0','app1_a'], 'check':[ ['app1','main'] ] } ,
                  {'point':['home'],'check':[ [ 'app1','pip' ]  ] } ,
                  
                  {'point':['app2_0','app2_b'],'check':[ ['app1','pip'],['app2','extend']  ] } ,
                  
                  {'point':['home',],    'check':[ ['app1','main'],['app2','extend']  ] } ,
                  
                  {'point':['back_0','back_a'], 'check':[ ['app1','null'],['app2','extend'] ] } ,
                  {'point':['back_0','back_b'], 'check':[ ['app2','null'] ] }  
            ]
case_24 =     [  
                  {'point':['app1_0','app1_a'], 'check':[ ['app1','main'] ] } ,
                  {'point':['home'],     'check':[ [ 'app1','pip' ]  ] } ,
                  
                  {'point':['home'],            'check':[ ['app1','main'] ] } ,
                  {'point':['back_0','back_a'], 'check':[ [ 'app1','null' ]  ] } 
            ]
case_25 =     [  
                  {'point':['app1_0','app1_a'], 'check':[ ['app1','main'] ] } ,
                  {'point':['home'],            'check':[ [ 'app1','pip' ]  ] } ,
                  
                  {'point':['back_0','back_a'], 'check':[ ['app1','pip'] ] } ,
                  {'point':['home'],            'check':[ [ 'app1','main' ]  ] } ,
                  {'point':['back_0','back_a'],'check':[ [ 'app1','null' ]  ] }  
            ]
case_26 =     [  
                  {'point':['app1_0','app1_a'],'check':[ ['app1','main'] ] } ,
                  {'point':['home'],'check':[ [ 'app1','pip' ]  ] } ,
                  
                  {'point':['back_0','back_b'],'check':[ ['app1','pip'] ] } ,
                  {'point':['home'],'check':[ [ 'app1','main' ]  ] } ,
                  {'point':['back_0','back_a'],'check':[ [ 'app1','null' ]  ] }  
            ]
case_27 =     [  
                  {'point':['home',],'check':[  ] } 
            ]
case_28 =     [  
                  {'point':['home',],'check':[  ] }  
            ]
case_29 =     [  
                  {'point':['back_0','back_a'],'check':[  ] } 
            ]
case_30 =     [  
                  {'point':['back_0','back_b'],'check':[  ] }  
            ]
case_31 =     [  
                  {'point':['app1_0','app1_b'],'check':[ ['app1','extend'] ] } ,
                  {'point':['back_0','back_b'],'check':[ [ 'app1','null' ]  ] } 
            ]
case_32 =     [  
                  {'point':['back_0','back_b'],'check':[  ] } 
            ]
case_0 =     [  
                  {'point':['back_0','back_b'],'check':[  ] } 
            ]
test_case = [case_0,case_1,case_2,case_3,case_4,case_5,case_6,case_7,case_8,case_9,\
             case_10,case_11,case_12,case_13,case_14,case_15,case_16,case_17,case_18,case_19,\
             case_20,case_21,case_22,case_23,case_24,case_25,case_26,case_27,case_28,case_29,\
             case_30,case_31,case_32]



class Android_lancher_unit_test :
    def __init__(self):
        print 'hello world'
        self.unit = autotestunit.AutoTestUnit()
    def Android_Lancher_Test_Unit(self,case):
        print test_case[ ( case ) ]
        action = 1;
        for unit in test_case[ ( case )] :   
            print '\ntest uint +++++++++ %d --> %s \n' %(action ,unit) 
            action = action +1          
            state  = self.unit.test_action(unit)
            if state == False :
                return 'FAIL'
        if state :
                return 'PASS'
        

if __name__ == '__main__':

    print 'hello'
    test =  Android_lancher_unit_test()
    test.Android_Lancher_Test_Unit(12)
