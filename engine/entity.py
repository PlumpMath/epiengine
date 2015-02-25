from mathutils import Vector
from outpipe import OutPipe
from engineinterface import EngineInterface
from scriptexecuter import ScriptExecuter
from contentreader import ContentReader
from paths import LOCATIONS
from tools import d2r, r2d
from math import atan

class Detector():
    def __init__(self, master, t, returnFunc, settings):
        self.master = master
        self.type = t
        self.returnFunction = returnFunc
        self.trueDetector = False
        
        if "property" in settings:
            self.targetProperty = settings["property"]
            
            #Set property to be searched by main search
            server = self.master.eI.getGlobal("server")
            
            if server:
                self.addPropertyTrack(server)
            else:
                self.addPropertyTrack(self.master.eI.getGlobal("client"))
            
        if "range" in settings:
            self.range = settings["range"]
        
        #Cone angle
        if "angle" in settings:
            self.angle = settings["angle"]
        else:
            self.angle = 45
        
        #Directional axis
        if "axis" in settings:
            self.axis = settings["axis"]
        else:
            self.axis = "+y"
            
        #Special consideration for collision
        if t == "collision":
            self.master.gameObject.collisionCallbacks.append(self.returnFunction)
            
        if self.axis == "+y":
            self.axis = Vector((0, -1, 0))
        elif self.axis == "-y":
            self.axis = Vector((0, 1, 0))
        elif self.axis == "+x":
            self.axis = Vector((-1, 0, 0))
        elif self.axis == "-x":
            self.axis = Vector((1, 0, 0))
        elif self.axis == "+z":
            self.axis = Vector((0, 0, -1))
        elif self.axis == "-z":
            self.axis = Vector((0, 0, 1))
        
    def isInCone(self, obj):
        vector = self.master.gameObject.getVectTo(obj)[2]
        
        if not self.isZeroLength(vector):
            return self.axis.angle(vector) <= self.angle
        else:
            return False
        
    def isInSight(self, obj):
        hitObj = self.master.gameObject.rayCast(obj, self.master.gameObject, self.range, self.targetProperty, 1, 0, 0)[0]
        return obj == hitObj 
        
    def isZeroLength(self, vector):
        return vector[0] == 0 and vector[1] == 0 and vector[2] == 0
        
    def triggered(self):
        objects = []
        
        if self.trueDetector:
            if self.type == "area":
                for obj in self.master.eI.getMainScene().objects:
                    if self.master.gameObject.getDistanceTo(obj) <= self.range and (self.targetProperty in obj or self.targetProperty == None):
                        objects.append(obj)
                    
            elif self.type == "radar":
                for obj in self.master.eI.getMainScene().objects:
                    if self.master.gameObject.getDistanceTo(obj) <= self.range and (self.targetProperty in obj or self.targetProperty == None):
                        if self.isInCone(obj):
                            objects.append(obj)
                            
            elif self.type == "sight":
                for obj in self.master.eI.getMainScene().objects:
                    if self.master.gameObject.getDistanceTo(obj) <= self.range and (self.targetProperty in obj or self.targetProperty == None):
                        if self.isInCone(obj):
                            if self.isInSight(obj):
                                objects.append(obj)
                            
            elif self.type == "collision":
                pass
        else:
            if self.type == "area":
                if self.targetProperty in self.master.eI.getGlobal("detectorindex").keys():
                    for obj in self.master.eI.getGlobal("detectorindex")[self.targetProperty]:
                        if self.master.gameObject.getDistanceTo(obj) <= self.range:
                            objects.append(obj)
                    
            elif self.type == "radar":
                if self.targetProperty in self.master.eI.getGlobal("detectorindex").keys():
                    for obj in self.master.eI.getGlobal("detectorindex")[self.targetProperty]:
                        if self.master.gameObject.getDistanceTo(obj) <= self.range:
                            if self.isInCone(obj):
                                objects.append(obj)
                            
            elif self.type == "sight":
                if self.targetProperty in self.master.eI.getGlobal("detectorindex").keys():
                    for obj in self.master.eI.getGlobal("detectorindex")[self.targetProperty]:
                        if self.master.gameObject.getDistanceTo(obj) <= self.range:
                            if self.isInCone(obj):
                                if self.isInSight(obj):
                                    objects.append(obj)
                            
            elif self.type == "collision":
                pass
        
        return objects
    
    def addPropertyTrack(self, master):
        master.addPropertyTrack(self.targetProperty)

class Action():
    def __init__(self, entity, action, mode, times, layer, targetChild=None):
        self.entity = entity
        self.action = action
        self.layer = layer
        self.targetChild = targetChild
        self.obj = None
        
        self.onEnd = None
        
        self.type = mode[0]
        self.skeleton = mode[1]
        
        self.start = times[0]
        self.end = times[1]
        
        if mode[0] == "play" or mode[0] == "frame":
            self.mode = self.entity.eI.l.KX_ACTION_MODE_PLAY
        elif mode[0] == "loop":
            self.mode = self.entity.eI.l.KX_ACTION_MODE_LOOP
            
    def play(self):
        if not self.targetChild:
            self.entity.gameObject.playAction(self.action, self.start, self.end, self.layer, self.layer, play_mode=self.mode)
            self.obj = self.entity.gameObject
        else:
            self.entity.gameObject.childrenRecursive[self.targetChild].playAction(self.action, self.start, self.end, self.layer, self.layer, play_mode=self.mode)
            self.obj = self.entity.gameObject.childrenRecursive[self.targetChild]
        
    def stop(self):
        self.obj.stopAction(self.layer)
        
    def __str__(self):
        return "Action - %s" % (self.action)
    
    def __repr__(self):
        return "Action - %s" % (self.action)
            
class Entity():
    def __init__(self, sourcename, objname, GUID, scriptName, flags, props, pos=(0,0,0), rot=(0,0,0), sca=(1,1,1), extra=None, side="SERVER"):
        #Tools
        self.oP = OutPipe("Entity - "+sourcename, 0)
        self.initVolatileModules()
        
        #Basic values
        self.name = sourcename
        self.GUID = ""
        
        #Extra
        if not extra:
            extra = {}
        
        #Basic Flags
        self.physicsTrack = False
        self.animTrack = False
        self.netVars = {}
        
        self.actions = []
        
        self.detectors = []
        
        self.scriptName = scriptName
        
        #Handle Flags
        self.processFlags(flags)
        
        #Create Object
        self.createObject(objname, sourcename, GUID, pos, rot, sca, props, extra)
                
        #Install custom code
        self.installCustomCode()
                
        if hasattr(self, "init"):
            self.init(side)
            
    def initVolatileModules(self):
        self.eI = EngineInterface(objectMode=False)
        self.sE = ScriptExecuter()
        self.detectors = []
        self.sE.addContext("Entity", self)
        self.sE.addContext("Detector", Detector)
        
    def installCustomCode(self):
        if self.scriptName:
            self.sE.execute(self.scriptName)
            
    def reconstructObject(self, objData):
        self.initVolatileModules()
        path = LOCATIONS["Entity"]
        cR = ContentReader(path+objData["name"])
        
        objectType = cR.get("type")
        
        sourcename = cR.get("name")
        objname = sourcename
        resource = cR.get("resourcePath")
        scriptName = cR.get("scriptPath")
        flags = cR.get("flags")
        props = cR.get("properties")
        
        if objectType == "Object":
            self.eI.loadLibrary(path+resource, False)
            extra = {}
        #elif objectType == "Light":
        #    extra = cR.get("lightSettings")
        #    if extra["type"] == "SUN":
        #        objname = "SunBase"
        #    elif extra["type"] == "SPOT":
        #        objname = "SpotBase"
        #    elif extra["type"] == "NORMAL":
        #        objname = "LightBase"
        #elif objectType == "Camera":
        #    objname = "CameraBase"
        #    extra = cR.get("cameraSettings")
            
        self.createObject(objname, sourcename, self.GUID, objData["pos"], objData["rot"], objData["sca"], props, extra)
        
        #Install custom code
        self.installCustomCode()
    
    def removeCustomCode(self):
        for i in dir(self):
            if "function" in type(getattr(self, i)):
                setattr(self, i, None)
            
    def createObject(self, objname, sourcename, GUID, pos, rot, sca, props, extra):
        self.gameObject = self.eI.createObject(objname, GUID, pos, rot, sca)
        
        if self.gameObject:
            self.GUID = self.gameObject["GUID"]
            self.oP("Added entity %s." % sourcename)
        else:
            self.oP("Failed to add entity %s." % sourcename)
            
        if self.gameObject:
            self.processProperties(props)
            
        #    if objname == "CameraBase":
        #        self.configureCamera(extra)
        #    elif objname in ["LightBase", "SpotBase", "SunBase"]:
        #        self.configureLight(extra)
            
    def __str__(self):
        return self.name + " - " + self.GUID
    
    def __repr__(self):
        return self.name + " - " + self.GUID
            
    def addDetector(self, detector):
        self.detectors.append(detector)
            
    def kill(self, side):
        if hasattr(self, "destruct"):
            self.destruct(side)
        self.eI.removeObject(self.GUID)
        
    def processFlags(self, flags):
        for flag in flags:
            if hasattr(self, flag):
                setattr(self, flag, flags[flag])
                
    def processProperties(self, props):
        for prop in props.keys():
            self.gameObject[prop] = props[prop]
                
    def load(self, location, name):
        path = LOCATIONS[location]
        cR = ContentReader(path+name)
        return cR
                
    def playAction(self, name, onEnd=None):
        action = self.getAction(name)
        
        if not action:
            cR = self.load("Animation", name)
            
            name = cR.get("name")
            mode = cR.get("mode")
            skeleton = cR.get("skeleton")
            times = [cR.get("start"), cR.get("end")]
            layer = cR.get("layer")
            targetChild = cR.get("targetChild")
            
            action = Action(self, name, [mode, skeleton], times, layer, targetChild)
            
            action.onEnd = onEnd
            
            action.play()
            
            self.actions.append(action)
        
    def stopAction(self, name):
        for action in self.actions:
            if action.action == name:
                action.stop()
                self.actions.remove(action)
                return
            
    def getAction(self, name):
        for action in self.actions:
            if action.action == name:
                return action
            
    def playFrameAction(self, name, frame):
        action = self.getAction(name)
        
        if not action:
            cR = self.load("Animation", name)
            
            name = cR.get("name")
            mode = cR.get("mode")
            skeleton = cR.get("skeleton")
            times = [frame, frame+1]
            layer = cR.get("layer")
            targetChild = cR.get("targetChild")
            
            action = Action(self, name, [mode, skeleton], times, layer, targetChild)
            
            action.play()
            
            self.actions.append(action)
        else:
            action.start = frame
            action.end = frame+1
            action.play()
            
    def clearStances(self):
        for action in self.actions:
            if action.action[:len(action.action)-7] == "_stance":
                self.stopAction(action.action)
            
    def checkPhysics(self):
        for detector in self.detectors:
            result = detector.triggered()
            if result and hasattr(detector, "returnFunction"):
                detector.returnFunction(result)
                
    def checkAnimation(self):
        for action in self.actions:
             isOver = action.obj.getActionFrame(action.layer) == action.end
             isPlay = action.mode == 0
             isStance = "_stance" == action.action[:len(action.action)-7]
             
             if isOver and isPlay and not isStance:
                self.stopAction(action.action)
                if action.onEnd:
                    action.onEnd()
                
    #def configureCamera(self, extra):
    #    self.gameObject.fov = extra["fov"]
    #    self.gameObject.near = extra["near"]
    #    self.gameObject.far = extra["far"]
    
    #def configureLight(self, extra):
    #    self.gameObject.color = (extra["r"], extra["g"], extra["b"])
    #    self.gameObject.type = getattr(self.gameObject, extra["type"])
    #    self.gameObject.energy = float(extra["energy"])
    #    self.gameObject.spotsize = float(extra["spotsize"])
        
    def trackTo(self, obj):
        #vector = self.gameObject.getVectTo(obj)[1]
        #
        #self.gameObject.alignAxisToVect(vector, 1)
        #ori = self.gameObject.worldOrientation.to_euler()
        
        x = self.gameObject.worldPosition[0] - obj.worldPosition[0]
        y = self.gameObject.worldPosition[1] - obj.worldPosition[1]
        
        if self.gameObject.worldPosition[0] > obj.worldPosition[0]:
            adjustment = 90
        else:
            adjustment = 270
            
        try:
            self.gameObject.worldOrientation = (0, 0, d2r(r2d(atan(y/x))+adjustment))
        except:
            if y > 0:
                self.gameObject.worldOrientation = (0, 0, d2r(180))
            else:
                self.gameObject.worldOrientation = (0, 0, d2r(0))