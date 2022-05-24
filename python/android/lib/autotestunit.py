import sys
import time as tm
import mouse
import check
import logging
import UserList
import os
import re
import math






points = {  'app1_0':[460,530],
            'app1_a':[440,490],
            'app1_b':[490,494],
            
            'app2_0':[580,515],
            'app2_a':[560,470],
            'app2_b':[610,480],
            
            'app3_0':[700,510],
            'app3_a':[680,470],
            'app3_b':[720,470],
            
            'app4_0':[820,510],
            'app4_a':[800,470],
            'app4_b':[840,470],
            
            'app5_0':[940,510],
            'app5_a':[920,470],
            'app5_b':[960,470],
            
            'home':[330,50],
        
            'back_0':[410,70],
            'back_a':[400,30],
            'back_b':[430,30],
            
            'pip':[],\
                  
          
          }




class AutoTestUnit():
    def __init__(self):
        self.click_num = 0
        self.check_num = 0
        self.click = []
        self.check = []
        self.click_handler = mouse.mouse()
        self.ob_check = check.Check('127.0.0.1',3333)  
        self.resoluton = self.get_screen_resolution()
        self.window = {'main':self.resoluton[0],\
                       'extend':self.resoluton[1],\
                       'pip':[280, 260, 10, 220] 
                       }
        print self.window
#        print self.resoluton
    def init_case_unit(self,data):
   
        self.click_num = len( data['point'] )
        self.check_num = len( data['check'])
        self.click = data['point']
        self.check = data['check']
#        print self.check_num
#        print self.click_num
#        print self.check
        print self.click
    def click_action(self):
        print('click action')
        if ( self.click_num == 1 ) :
            self.click_handler.mouse_click_xy(  points[ self.click[0] ] )
            str = "click 0 %d - %d" %( points[ self.click[0] ][0] ,points[ self.click[0] ][1])
            print str
        elif (self.click_num  == 2) :
            self.click_handler.mouse_click_xy(  points[ self.click[0] ] )
            str = "click 1 %d - %d" %( points[ self.click[0] ][0] ,points[ self.click[0] ][1]) 
            print str           
            tm.sleep(1)
            self.click_handler.mouse_click_xy(  points[ self.click[1] ] )
            str = "click 0 %d - %d" %( points[ self.click[1] ][0] ,points[ self.click[1] ][1])
            print str
        elif   (self.click_num  == 0 ):
            return True
        else :
            return False
        tm.sleep(2)
    def check_action(self):
        print('check action')
        print self.check
        print 'check action num - >%d ' %( len ( self.check )  )
        
        if self.check_num  == 0 :
            return True
        state = 0

        apps = self.ob_check.get_app_list() 
        print self.check
        
        for check in self.check :
            pid = self.get_pid_from_name( check[0] )
            if check[1] == 'null':                    
                if pid <0 :
                    state = state + 1
                    print '%s is closed'%(check[0])
                else :
                    return False
            else :            
                for app in apps :
                    if pid < 0 :
                        print 'query app -> %s  -> %d'%(check[0],pid)
                        return False
                    else :
                        print 'query app -> %s  -> %d'%(check[0],pid)
    #                        print check[1]
    #                        print self.window
    #                        print app['pid']
                        if ( app['pid'] == pid ) and  self.check_rect(app['rect'], self.window[ check[1] ]) :
                            print 'find target app -> %s  -> %d'%(check[0],pid)
                            state = state + 1

        #end loop
        print 'check result %d - %d'%(self.check_num,state)
        if self.check_num == state :
            print 'check pass'
            return True
        else :
            print 'check fail'
            return False
    def check_rect(self,rect0,rect1):
        print 'hello check rect'
        #return True
        #return True
        print 'rect 0 & rect 1 --> %s %s ' %(rect0 , rect1)
        #return True
        if ( math.fabs( rect0[0] - rect1 [0] ) < 10 ) and ( math.fabs( rect0[1] - rect1 [1] ) < 10 ) and ( math.fabs( rect0[2] - rect1 [2] ) < 10 ) and ( math.fabs( rect0[3] - rect1 [3] ) < 10 ):
            return True
        else :
            return False        
    def end_action(self):
        print('end action')
        return True;
    def prepare_acion(self):
        print 'prepare action'
        return
        cmd =  'ps'
        pids =  os.popen(cmd).readlines()
        print pids
        print len ( pids )
        for pid in pids :
            print pid
#        self.end =self.end
    def log_action(self,state):
        print('log action')
    
        
    def test_action(self,data):
        print('test_action')
        self.prepare_acion()
        self.init_case_unit(data)
        self.log_action(True);
        if( self.click_action() == False):
            self.log_action(False)
            return False
        if(self.check_action() == False ):
            self.log_action(False)
            return False     
        else :
            return True
        
    def get_pid_from_name(self,name):
        cmd =  'ps -C ' + name + ' -o pid'
        pid =  os.popen(cmd).readlines()
        #print cmd
        #print pid
        if len(pid) > 1 :
            return int (pid[1])
        else :
            return -1;
    def check_origin_state(self):
        print 'check origin state'
    def get_screen_resolution(self):
        cmd = 'xrandr'
        resolution =  os.popen(cmd).readlines()
        #print resolution
        result = []
        for str in resolution :
            index = str.find(' connected ')
            if index != -1 :
                tmp =  str.split()[2]
                tmp = tmp.replace('x',' ')
                tmp = tmp.replace('+',' ')
                tmp = tmp.split()
                tmp[0] = int (tmp[0])
                tmp[1] = int (tmp[1])
                tmp[2] = int (tmp[2])
                tmp[3] = int (tmp[3])
                result.append(tmp)
#        print result
        return result

        
                
        
        
        
    
    
if __name__ == '__main2__':
    #print len(test)

    
    unit = AutoTestUnit()
#    unit.prepare_acion()


    

    
    
        
        
        
    
   


