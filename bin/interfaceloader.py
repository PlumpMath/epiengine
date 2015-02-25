import bge
from engineinterface import EngineInterface
from paths import LOCATIONS

cont = bge.logic.getCurrentController()
own = cont.owner

if own["queue"] == "":
    own["queue"] = []
    own["eI"] = EngineInterface()
    
    def addToQueue(item, item1, item2):
        own["queue"].append([item, item1, item2])
        
    bge.logic.globalDict["addToQueue"] = addToQueue
    
for item in own["queue"]:
    own["eI"].loadLibrary(LOCATIONS["UI"]+item[0])
    obj = own["eI"].createInterface(item[1])
    item[2].gameObject = obj
    
own["queue"] = []
