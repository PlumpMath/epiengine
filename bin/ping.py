import bge

ping = bge.logic.getCurrentController().owner

ping.resolution = 10

def drawPing(ip, port, ms):
    ping = bge.logic.globalDict["ping"]
    ping["Text"] = "Ping (%s, %i) %4ims" % (ip, port, ms)

def clearPing():
    ping = bge.logic.globalDict["ping"]
    ping["Text"] = ""

bge.logic.globalDict["ping"] = ping
  
clearPing()

bge.logic.globalDict["drawPing"] = drawPing
bge.logic.globalDict["clearPing"] = clearPing