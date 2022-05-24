import serial
com = serial.Serial("/dev/ttyS0",115200)
while True :
    try :
        dat = com.readall()
        logger.info(dat)
        store_dat_mysql(dat)
    except :
        logger.err(dat)
