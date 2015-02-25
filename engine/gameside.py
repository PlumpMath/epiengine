from paths import LOCATIONS
from contentreader import ContentReader
from entity import Entity
from engineinterface import EngineInterface

class GameSide():
    
    def pushConsoleCommand(self, msg):
        '''Used to send a cvar command from the graphical console to the client/server.'''
        msg = msg.split(" ")
        
        command = msg[0]
        
        if len(msg) > 1:
            arg = msg[1]
        else:
            arg = ""
        
        self.configure(command, arg)
        
    def endLevel(self):
        '''Destroys the current level and any physical objects.'''
        if self.level:
            self.level.kill(self.mode)
            self.level = None
        self.removeAllEntities()
        self.removeAllObjects()
        
    def setLevel(self, name):
        '''Load a level into the engine.'''
        
        cR = self.load("Level", name)
        
        name = cR.get("name")
        resource = cR.get("resourcePath")
        scriptName = cR.get("scriptPath")
        flags = cR.get("flags")
        props = cR.get("properties")
        sky = cR.get("sky")
        #preload = cR.get("preload")
        
        self.configure("sv_background_red", sky["r"])
        self.configure("sv_background_green", sky["g"])
        self.configure("sv_background_blue", sky["b"])
        self.configure("sv_background_alpha", 100)
        
        self.loadLibrary("Level", resource)
        #self.preload(preload)
        self.level = Entity(name, name, None, scriptName, flags, props, side=self.mode)
        
    def get(self, key):
        '''Retrieve cvar.'''
        try:
            return self.cvars[key]
        except:
            self.oP("No CVar %s exists." % key)
            return None
        
    def getNetVar(self, key):
        '''Retrieve netVar.'''
        try:
            return self.netVars[key]
        except:
            #self.oP("No netVar %s exists." % key)
            return None
    
    def preload(self, l):
        '''Loads assets to be spawned by another asset so the system doesn't fuck up.'''
        if l:
            for i in l:
                self.load("Entity", i)
    
    def load(self, location, name):
        '''Loads an epi file.'''
        path = LOCATIONS[location]
        cR = ContentReader(path+name)
        return cR
        
    def loadLibrary(self, location, name, mesh=False):
        '''Loads a blend file.'''
        path = LOCATIONS[location]
        
        return self.eI.loadLibrary(path+name, mesh)

    def getBackgroundColor(self):
        '''Reformats the background color.'''
        return (self.get("sv_background_red")*0.01, self.get("sv_background_green")*0.01, self.get("sv_background_blue")*0.01, self.get("sv_background_alpha")*0.01)
        
    def addEntity(self, name, GUID, pos, rot, sca):
        '''Adds an Entity.'''
        cR = self.load("Entity", name)
        
        objectType = cR.get("type")
        
        sourcename = cR.get("name")
        objname = sourcename
        resource = cR.get("resourcePath")
        scriptName = cR.get("scriptPath")
        flags = cR.get("flags")
        props = cR.get("properties")
        
        if objectType == "Object":
            self.loadLibrary("Entity", resource)
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
        
        ent = Entity(sourcename, objname, GUID, scriptName, flags, props, pos, rot, sca, extra=extra, side=self.mode)
        
        self.entities.append(ent)
        return ent
        
    def removeEntity(self, GUID):
        '''Removes an Entity.'''
        entity = self.getEntityByGUID(GUID)
        
        if entity:
            if self.eI.getMainScene().active_camera == entity.gameObject:
                self.eI.getMainScene().active_camera = "DefaultCamera"
            
            self.entities.remove(entity)
            entity.kill(self.mode)
            
    def removeAllEntities(self):
        '''Removes all entities.'''
        while self.entities:
            self.removeEntity(self.entities[0].GUID)
            
    def removeAllObjects(self):
        '''Removes all objects.'''
        self.eI.removeAllObjects()
            
    def getEntityByGUID(self, GUID):
        '''Gets the specified Entity.'''
        for entity in self.entities:
            if entity.GUID == GUID:
                return entity
    
    def addPropertyTrack(self, prop):
        '''Adds a property for tracking by detectors.'''
        self.trackedProperties.append(prop)
            
    def updateDetectorIndex(self):
        '''Updates the global catalog of objects.'''
        
        self.eI.l.globalDict["detectorindex"] = {}
        
        for obj in self.eI.getMainScene().objects:
            for prop in self.trackedProperties:
                if prop in obj:
                    if prop in self.eI.l.globalDict["detectorindex"].keys():
                        self.eI.l.globalDict["detectorindex"][prop].append(obj)
                    else:
                        self.eI.l.globalDict["detectorindex"][prop] = [obj]