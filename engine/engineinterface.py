from outpipe import OutPipe
from paths import CONTENT_EXT, LOCATIONS, GAME_PATH, TEXT_EXT
from randomtools import oneOfList
from threading import Thread
from contentreader import ContentReader
import bge
import traceback

def loadLauncher(launcher):
    bge.logic.globalDict["launcher"] = launcher
        
def loadClient(client):
    bge.logic.globalDict["client"] = client
        
def loadServer(server):
    bge.logic.globalDict["server"] = server
    
def loadEpiArchive():
    bge.logic.globalDict["epiarchive"] = {}
    bge.logic.globalDict["detectorindex"] = {}

class EngineInterface():
    def __init__(self, objectMode=False):
        self.oP = OutPipe("EngineInterface", 0)
        
        self.worldCoreName = "WorldCommander"
        self.overlayCoreName = "OverlayCore"
        self.waypointsCoreName = "WaypointsCore"
        self.mainSceneName = "MainScene"
        self.overlaySceneName = "Overlay"
        self.waypointsSceneName = "Waypoints"
        
        self.protected = ["__default__cam__", "DefaultCamera", "WorldCommander"]
        
        self.charset = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        
        self.l = bge.logic
        self.r = bge.render
        self.e = bge.events
        
        if objectMode:
            pass
            #self.startLoop()
            
    def preLoad(self):
        self.oP("Preloading content.")
        f = open(GAME_PATH+"preload"+TEXT_EXT, "r")
        try:
            data = eval(f.read())
        except:
            pass
        f.close()
        
        for i in data:
            self.loadLibrary(GAME_PATH+i)
            
    def preLoadEpi(self):
        self.oP("Preloading .epi files...")
        f = open(GAME_PATH+"preload_epi"+TEXT_EXT, "r")
        try:
            data = eval(f.read())
        except:
            pass
        f.close()
        
        for i in data:
            cR = ContentReader(GAME_PATH+i)
        
    def getMouse(self):
        return self.l.mouse
    
    def getKeyboard(self):
        return self.l.keyboard
        
    def getGlobal(self, key):
        if key in self.l.globalDict:
            return self.l.globalDict[key]
        else:
            self.oP("No key in global %s." % key)
     
    def loadLibrary(self, name, mesh=False):
        try:
            if not mesh:
                self.l.LibLoad(name+CONTENT_EXT, "Scene", load_actions=True)
            else:
                self.l.LibLoad(name+CONTENT_EXT, "Mesh")
            self.oP("Loaded library %s." % name)
            return True
        except:
            if not name in str(self.l.LibList()).replace("\\", "/"):
                self.oP("Library %s already loaded." % (name+CONTENT_EXT))
            else:
                self.oP("Failed to load library %s." % (name+CONTENT_EXT))
            return False
        
    def unloadLibrary(self, name):
        try:
            self.l.LibFree(name)
            self.oP("Unloaded library %s." % name)
            return True
        except:
            self.oP("Failed to unload library %s." % name)
            return False
        
    def addScene(self, sceneName):
        try:
            self.l.addScene(sceneName)
            self.oP("Added scene %s." % sceneName)
            return True
        except:
            self.oP("Failed to add scene %s." % sceneName)
            return False
            
    def removeScene(self, sceneName):
        scenes = self.l.getSceneList()
        for scene in scenes:
            if scene.name == sceneName:
                scene.end()
                self.oP("Removed scene %s." % sceneName)
                return True
            
        self.oP("Failed to remove scene %s." % sceneName)
        return False
    
    def getMainScene(self):
        scenes = self.l.getSceneList()
        
        for scene in scenes:
            if scene.name == self.mainSceneName:
                return scene
            
    def getOverlayScene(self):
        scenes = self.l.getSceneList()
        
        for scene in scenes:
            if scene.name == self.overlaySceneName:
                return scene
            
    def getWaypointsScene(self):
        scenes = self.l.getSceneList()
        
        for scene in scenes:
            if scene.name == self.waypointsSceneName:
                return scene
    
    def suspendMainScene(self):
        scene = self.getMainScene()
        scene.suspend()
        self.oP("Suspended main scene.")
        
    def resumeMainScene(self):
        scene = self.getMainScene()
        scene.resume()
        self.oP("Resumed main scene.")
        
    def createWaypoint(self, className):
        scene = self.getWaypointsScene()
        
        worldCommander = self.getWorldCommander(scene)
        
        obj = self.getBaseObjectByClassName(className)
        
        try:
            waypoint = scene.addObject(obj, worldCommander)
            
            self.oP("Created waypoint.")
            return waypoint
        except:
            self.oP("Failed to create waypoint.")
            return False
        
    def createObject(self, className, GUID, pos, rot, sca, scene=None):
        if not scene:
            scene = self.getMainScene()
        
        worldCommander = self.getWorldCommander(scene)
        
        worldCommander.worldPosition = pos
        worldCommander.worldOrientation = rot
        worldCommander.worldScale = sca
        
        obj = self.getBaseObjectByClassName(className)
        
        try:
            newObj = scene.addObject(obj, worldCommander)
            
            if not GUID:
                self.allocateGUIDs()
            else:
                newObj["GUID"] = GUID
                
            self.oP("Created object %s." % className)
            return newObj
        except:
            print(traceback.format_exc())
            self.oP("Failed to create object %s!" % className)
            return False
        
    def createInterface(self, className):
        scene = self.getOverlayScene()
        
        obj = self.createObject(className, "", (0,0,0), (0,0,0), (1,1,1), scene)
        
        self.oP("Created interface %s." % className)
        
        return obj
        
    def removeInterface(self, className):
        GUID = ""
        
        for obj in self.getOverlayScene().objects:
            if obj.name == className:
                GUID = obj["GUID"]
        
        self.removeObject(GUID)
        
        self.oP("Removed interface %s." % className)
        
    def removeObject(self, GUID):
        for obj in self.getMainScene().objects + self.getOverlayScene().objects:
            if "GUID" in obj and obj["GUID"] == GUID:
                obj.endObject()
                self.oP("Removed object %s." % GUID)
                return True
            
        self.oP("Failed to remove object %s." % GUID)
        return False
    
    def removeAllObjects(self):
        for obj in self.getMainScene().objects:
            if not obj.name in self.protected:
                obj.endObject()
    
    def setMouseState(self, visible):
        self.r.showMouse(visible)
        
    def quitGame(self):
        self.l.endGame()
    
    def getBaseObjectByClassName(self, className):
        for obj in self.getAllObjectsInactive():
            if obj.name == className:
                return obj
    
    def getTerminalParent(self, obj):
        while 1:
            if obj.parent:
                obj = obj.parent
            else:
                break
            
        return obj
    
    def getMouseOverObjectScene(self, pos):
        for scene in self.l.getSceneList():
            camera = scene.active_camera
            obj = camera.getScreenRay(pos[0], pos[1], 100.0)
            if obj and "MouseOver" in obj:
                return obj, scene
            
        return None, None
    
    def getObjectsByClassName(self, className):
        objects = []
        for obj in self.getMainScene().objects:
            if obj.name == className:
                objects.append(obj)
        
        return objects
    
    def getObjectByGUID(self, GUID):
        for obj in self.getAllObjects():
            if "GUID" in obj and obj["GUID"] == GUID:
                return obj
    
    def getSceneByName(self, name):
        for scene in self.l.getSceneList():
            if scene.name == name:
                return scene
    
    def allocateGUIDs(self):
        for obj in self.getMainScene().objects + self.getOverlayScene().objects:
            if not "GUID" in obj:
                self.setGUID(obj)
                
    def getKeyCode(self, keyString):
        try:
            return getattr(self.e, keyString)
        except:
            self.oP("Incorrect key string %s." % keyString)
            return 0
                
    def setGUID(self, obj):
        GUID = ""
        
        counter = 0
        while counter < 32:
            GUID += oneOfList(self.charset)
            counter += 1
        
        obj["GUID"] = GUID
    
    def setCamera(self, GUID):
        obj = self.getObjectByGUID(GUID)
        
        if obj:
            self.getMainScene().active_camera = obj
    
    def getWorldCommander(self, scene=None):
        if not scene or scene == self.getMainScene():
            scene = self.getMainScene()
        
            for obj in scene.objects:
                if obj.name == self.worldCoreName:
                    return obj
        elif scene.name == "Overlay":
            for obj in scene.objects:
                if obj.name == self.overlayCoreName:
                    return obj
        elif scene.name == "Waypoints":
            for obj in scene.objects:
                if obj.name == self.waypointsCoreName:
                    return obj

    def getAllObjects(self):
        objects = []
        
        for scene in self.l.getSceneList():
            objects += scene.objects
            
        return objects
    
    def getAllObjectsInactive(self):
        objects = []
        
        for scene in self.l.getSceneList():
            objects += scene.objectsInactive
            
        return objects
            
    def setResolution(self, width, height):
        self.r.setWindowSize(width, height)
        
    def setFullscreen(self, mode):
        self.r.setFullScreen(mode)
    
    def setMotionBlur(self, mode, level):
        if mode:
            self.r.enableMotionBlur(level)
        else:
            self.r.disableMotionBlur()
    
    def setAnisotropic(self, level):
        if level in [1,2,4,8,16]:
            self.r.setAnisotropicFiltering(level)
        
    def setMipmapping(self, mode):
        modes = {
            "none":bge.render.RAS_MIPMAP_NONE,
            "nearest":bge.render.RAS_MIPMAP_NEAREST,
            "linear":bge.render.RAS_MIPMAP_LINEAR,
        }
        
        if mode in modes.keys():
            mode = modes[mode]
            self.r.setMipmapping(mode)
        
    def setVSync(self, mode):
        modes = {
            "off":bge.render.VSYNC_OFF,
            "on":bge.render.VSYNC_ON,
            "adaptive":bge.render.VSYNC_ADAPTIVE,
        }
        
        if mode in modes.keys():
            mode = modes[mode]
            self.r.setVsync(mode)
            
    def setBackgroundColor(self, color):
        self.r.setBackgroundColor(color)
        
    def getIndexedObjectsByProperty(self, prop):
        if prop in self.l.globalDict["detectorindex"].keys():
            return self.l.globalDict["detectorindex"][prop]