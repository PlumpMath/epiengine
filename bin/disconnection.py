import bge

disconnect = bge.logic.getCurrentController().owner

disconnect.resolution = 10

def drawDisconnect(ip, port, time):
    disconnect = bge.logic.globalDict["discon"]
    disconnect["Text"] = "Disconnecting (%s, %i)... %.2fs" % (ip, port, time)

def clearDisconnect():
    disconnect = bge.logic.globalDict["discon"]
    disconnect["Text"] = ""

bge.logic.globalDict["discon"] = disconnect
  
clearDisconnect()

bge.logic.globalDict["drawDisconnect"] = drawDisconnect
bge.logic.globalDict["clearDisconnect"] = clearDisconnect