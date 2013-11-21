from flask import Flask
app = Flask(__name__)
import actionlayer
@app.route('/open/<username>/<password>')
def openDoor(username,password):
    print "opendoor action"
    #action for open door
    if actionlayer.checkUserPassword(username, password) :
        return actionlayer.openDoorAction()
    else :
        return 'error username or pass\n'
@app.route('/close/<username>/<password>')
def closeDoor(username,password):
    print "closedoor action"
    #action for close door

    if actionlayer.checkUserPassword(username, password) :
        return actionlayer.closeDoorAction()
    else :
        return 'error username or pass\n'
@app.route('/state/<username>/<password>')

def stateDoor(username,password):
    print "statedoor action"
    #action for state door
    if actionlayer.checkUserPassword(username, password) :
        return actionlayer.stateDoorAction()
    else :
        return 'error username or pass\n'
if __name__ == '__main__':
    app.run()