import hardware
def openDoorAction():
    return hardware.open()

def closeDoorAction():
    return hardware.close()

def stateDoorAction():
    return  hardware.state()
def checkUserPassword(username,password):
    if username== "admin" and password == "pass":
        return True
    else :
        return False

