from outpipe import OutPipe
from tools import getDistance3D
from time import time

class Archive():
    def __init__(self):
        self.records = []

    def store(self, GUID, mode, currValue, newValue):
        self.records.append({"GUID":GUID, "mode":mode, "last":currValue, "new":newValue, "time":time()})
        
    def check(self, ent):
        GUID = ent.GUID
        
        for record in self.records:
            if record["GUID"] == GUID:
                if time() > record["time"] + 1:
                    if record["mode"] == "pos":
                        if ent.gameObject.worldPosition == record["last"]:
                            ent.gameObject.worldPosition = record["new"]
                    elif record["mode"] == "rot":
                        if ent.gameObject.worldOrientation.to_euler() == record["last"]:
                            ent.gameObject.worldOrientation = record["new"]
                    elif record["mode"] == "sca":
                        if ent.gameObject.worldScale == record["last"]:
                            ent.gameObject.worldScale = record["new"]
                    elif record["mode"] == "linV":
                        if ent.gameObject.getLinearVelocity() == record["last"]:
                            ent.gameObject.setLinearVelocity(record["new"])
                    elif record["mode"] == "angV":
                        if ent.gameObject.getAngularVelocity() == record["last"]:
                            ent.gameObject.setAngularVelocity(record["new"])
                            
                    self.records.remove(record)

class PhysicsApplicator():
    def __init__(self, client):
        self.oP = OutPipe("PhysicsApplicator", 0)
        
        self.c = client
        
        #self.scene = bge.logic.getCurrentScene()
        
        self.archive = Archive()
        self.blacklistedGUIDs = []
        
        self.smooth = False
        self.maxLocationDisparity = 0.2
        self.maxRotationDisparity = 10.0
        self.maxScaleDisparity = 0.1
        self.maxVelocityDisparity = 0.5
        
        self.oP("Initialized.")
    
    def isAlreadyPlaying(self, ent, action):
        for action in ent.actions:
            if action.action == action:
                return True
            
        return False
    
    def isStillPlaying(self, anims, action):
        found = False
        for a in anims:
            if type(a) == type([]) and action == a[0]:
                found = True
                
        return action in anims or found
    
    def update(self, event):
        if event[1] == "CREATE" and not self.c.getEntityByGUID(event[2]["GUID"]):
            self.c.addEntity(event[2]["name"], event[2]["GUID"], event[2]["pos"], event[2]["rot"], event[2]["sca"])
        elif event[1] == "DELETE":
            self.c.removeEntity(event[2])
        elif event[1] == "MESH":
            for ent in self.c.entities:
                if ent.GUID == event[2][0]:
                    self.c.replaceMesh(ent, event[2][1])
        elif event[1] == "ANIMATION":
            for ent in self.c.entities:
                if ent.GUID == event[2]["GUID"]:
                    
                    #Start new anims
                    for action in event[2]["anim"]:
                        if type(action) == type(""):
                            if not self.isAlreadyPlaying(ent, action):
                                ent.playAction(action)
                        #Do frame anims
                        else:
                            ent.playFrameAction(action[0], action[1])
                            
                    #Remove stopped anims
                    for action in ent.actions:
                        if not self.isStillPlaying(event[2]["anim"], action.action):
                            ent.stopAction(action.action)
        else:
            for ent in self.c.entities:
                self.archive.check(ent)
                if ent.GUID == event[2]["GUID"]:
                    obj = ent.gameObject
                    
                    if event[1] == "UPDATE":
                        if self.locationDisparity(obj, event[2]) > self.maxLocationDisparity or not self.smooth:
                            obj.worldPosition = event[2]["pos"]
                        elif self.locationDisparity(obj, event[2]) != 0:
                            self.archive.store(ent.GUID, "pos", obj.worldPosition, event[2]["pos"])
                            
                        if self.rotationDisparity(obj, event[2]) > self.maxRotationDisparity or not self.smooth:
                            if not ent.GUID in self.blacklistedGUIDs:
                                obj.worldOrientation = event[2]["rot"]
                        elif self.rotationDisparity(obj, event[2]) != 0:
                            self.archive.store(ent.GUID, "rot", obj.worldOrientation.to_euler(), event[2]["rot"])
                            
                        if self.scaleDisparity(obj, event[2]) > self.maxScaleDisparity or not self.smooth:
                            obj.worldScale = event[2]["sca"]
                        elif self.scaleDisparity(obj, event[2]) != 0:
                            self.archive.store(ent.GUID, "sca", obj.worldScale, event[2]["sca"])
                            
                        if self.velocityDisparity(obj, event[2]) > self.maxVelocityDisparity or not self.smooth:
                            obj.setLinearVelocity(event[2]["linV"])
                            obj.setAngularVelocity(event[2]["angV"])
                        elif self.velocityDisparity(obj, event[2]) != 0:
                            self.archive.store(ent.GUID, "linV", obj.getLinearVelocity(), event[2]["linV"])
                            self.archive.store(ent.GUID, "angV", obj.getAngularVelocity(), event[2]["angV"])
                            
                        ent.netVars = event[2]["vars"]
                            
                        if event[2]["par"]:                                
                            for ent in self.c.entities:
                                #Find parent
                                if ent.GUID == event[2]["par"]:
                                    #Check if this is a new thing
                                    if obj.parent == None or not "GUID" in self.getTerminalParent(obj) or self.getTerminalParent(obj)["GUID"] != event[2]["par"] or obj.parent.name != event[2]["pars"]:
                                        #Apply parent, sub parent or otherwise
                                        if event[2]["pars"] == ent.gameObject.name:#True parent
                                            obj.setParent(ent.gameObject)
                                        else:#Sub parent
                                            obj.setParent(ent.gameObject.childrenRecursive[event[2]["pars"]])
                        #Remove any decommisioned parents
                        elif obj.parent:
                            obj.removeParent()

    def getTerminalParent(self, obj):
        while 1:
            if obj.parent:
                obj = obj.parent
            else:
                break
            
        return obj

    def locationDisparity(self, obj, update):
        disparity = 0
        
        disparity += getDistance3D(obj.worldPosition, update["pos"])
        
        return disparity
    
    def rotationDisparity(self, obj, update):
        disparity = 0
        
        currPos = obj.worldOrientation.to_euler()
        currPos = [currPos[0], currPos[1], currPos[2]]
        newPos = update["pos"]
        
        disparity += abs(currPos[0]-newPos[0])
        disparity += abs(currPos[1]-newPos[1])
        disparity += abs(currPos[2]-newPos[2])
        
        return disparity
    
    def scaleDisparity(self, obj, update):
        disparity = 0
        
        disparity += abs(obj.worldScale[0] - update["sca"][0])
        disparity += abs(obj.worldScale[1] - update["sca"][1])
        disparity += abs(obj.worldScale[2] - update["sca"][2])
        
        return disparity
    
    def velocityDisparity(self, obj, update):
        disparity = 0
        
        disparity += abs(obj.getLinearVelocity()[0] - update["linV"][0])
        disparity += abs(obj.getLinearVelocity()[1] - update["linV"][1])
        disparity += abs(obj.getLinearVelocity()[2] - update["linV"][2])
        
        disparity += abs(obj.getAngularVelocity()[0] - update["angV"][0])
        disparity += abs(obj.getAngularVelocity()[1] - update["angV"][1])
        disparity += abs(obj.getAngularVelocity()[2] - update["angV"][2])
        
        return disparity