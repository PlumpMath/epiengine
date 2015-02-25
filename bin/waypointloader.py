import bge
from engineinterface import EngineInterface
from paths import LOCATIONS

cont = bge.logic.getCurrentController()
own = cont.owner

if own["queue"] == "":
    own["queue"] = []
    own["eI"] = EngineInterface()
    
    def addToWaypoints(item, item1, item2):
        own["queue"].append([item, item1, item2])
        
    bge.logic.globalDict["addToWaypoints"] = addToWaypoints
    
#Create waypoints
for item in own["queue"]:
    own["eI"].loadLibrary(LOCATIONS["UI"]+item[0])
    waypoint = own["eI"].createWaypoint(item[1])
    waypoint["targetGUID"] = item[2]
    
own["queue"] = []

#Update cam
mirrorCam = own["eI"].getWaypointsScene().objects["MirrorCam"]
referenceCam = own["eI"].getMainScene().active_camera

mirrorCam.worldPosition = referenceCam.worldPosition
mirrorCam.worldOrientation = referenceCam.worldOrientation
mirrorCam.fov = referenceCam.fov

#Update waypoints
for obj in own["eI"].getWaypointsScene().objects:
    if "targetGUID" in obj:
        targetObj = own["eI"].getObjectByGUID(obj["targetGUID"])
        
        if targetObj:
            obj.worldPosition = targetObj.worldPosition
            obj.worldOrientation = targetObj.worldOrientation
