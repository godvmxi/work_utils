import Queue #导入FIFO库
msgBuf = Queue.Queue()
def inQueue(dat):
    msgBuf.put(dat)
def outQueue():
    if msgBuf.empty() == False:
        return msgBuf.get()
    else :
        return None
    
import MySQLdb
def openMySQL(host,user,password,db,port): #获取数据库操作句柄
    try:
        conn=MySQLdb.connect(host,user,password,db,port)
        cur=conn.cursor()
        return cur
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def insertMysql(cur,dat):
     SQL = creatInsertSqlCmd(dat)
     error = cur.execute(SQL)
     return error
def updateMysql(cur,dat):
     SQL = creatUpdateSqlCmd(dat)
     error = cur.execute(SQL)
     return error
     
def stortDatIntoMysql(cur,dat):
    if updateMySql(cur,dat) == True :#
        return True
    else :
        return insertMysql(cur,dat)
    
def isRfidValid(rfid):
    if queryRfid() == False :
        print "无效的用户卡"
    else :
        return True
def CheckInMode():#用户注册车位
    if queryPacks() != False :
        print "车位已满，无法进入"
        return False
    else :
        packId = mallocPack() #申请车位
    if updatePackMySql(cur,dat,packID) == True :#
        pass
    else :
        insertMysql(cur,dat,packId)
    
def CheckOutMode():#用户结帐车位
    if queryRfid() == False :
        print "该ID账户不存在"
        return False
    timelong = queryPackTime()
    return timelong
    
    
    
SPI = spi.spi()    
def readSpiDat(address):
    dat = SPI.readall()
    return dat

def writeSpiCmd(address,cmd):
    SPI.write(address,cmd)
    time.sleep(0.02)
def readDatFromRC522():
    writeSpiCmd(RC522_reg1,0x23)
    writeSpiCmd(RC522_reg2,0x23)
    dat = SPI.write(address,cmd)
    return dat
    

    pass

 
