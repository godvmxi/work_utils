__author__ = 'bluebird'

import logging
import sys
import  time

logger = logging.getLogger("endlesscode")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
#file_handler = logging.FileHandler("test.log")
file_handler = logging.StreamHandler()
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler(sys.stderr)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

import pyinotify
import threading
class EventHandler(pyinotify.ProcessEvent):
        def setLogger(self,log):
            self.logger = log
        def process_default(self, event):
            logger.debug('Event -> %s %s  %s %s '%(event.name,event.maskname,type(event.name),type(event.maskname)))

        #def process_IN_MOVED_FROM(self, event):
        #    logger.debug('Event comming-> %s %s'%(event.name,event.maskname))
        #
        #
        #def process_IN_MOVED_TO(self, event):
        #    self.logger()
        #    logger.debug('Event comming-> %s %s'%(event.name,event.maskname))
        #
        #
        #def process_IN_CLOSE_WRITE(self, event):
        #    self.logger()
        #    logger.debug('Event comming-> %s %s'%(event.name,event.maskname))
def hello():
    print 'I am handler'

def inotify_dir() :
    wfile = '/tmp/inotify/'
    wm = pyinotify.WatchManager()  # Watch Manager
    mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM | pyinotify.IN_DELETE
    #mask = pyinotify.ALL_EVENTS
    handler = EventHandler()
    handler.setLogger(hello)
    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch(wfile, mask, rec=True,auto_add=True)
    notifier.loop()
def add_threading():
    test = threading.Thread(target =inotify_dir )
    test.start()
    print 'add threading ok'

if __name__ == '__main__':
    logger.debug('hello debug')
    #inotify_dir()
    #exit()
    add_threading()
    while True :
        time.sleep(10)
        #logger.debug('I am here!!')




