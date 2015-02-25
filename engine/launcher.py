import bge
import traceback
import os

def systemReady():
    if not "isCollecting" in bge.logic.globalDict:
        return False
    if not "addToQueue" in bge.logic.globalDict:
        return False
    if not "drawSubtitle" in bge.logic.globalDict:
        return False
    if not "isVideoFinished" in bge.logic.globalDict:
        return False
    if not "addToWaypoints" in bge.logic.globalDict:
        return False
    if not "drawDisconnect" in bge.logic.globalDict:
        return False
    if not "drawPing" in bge.logic.globalDict:
        return False
    return True

if not "launcher" in bge.logic.globalDict and systemReady():
    from configreader import ConfigReader
    from outpipe import OutPipe
    from scriptexecuter import ScriptExecuter
    from soundengine import SoundEngine
    from client import Client
    from server import Server
    from engineinterface import loadLauncher, loadEpiArchive, EngineInterface
    from paths import ENGINE_PATH, TEXT_EXT, NET_PATH
    
    class Launcher():
        def __init__(self):
            #Remove engine log
            try:
                os.remove(ENGINE_PATH+"engine_log"+TEXT_EXT)
            except:
                pass
            
            #Remove net logs
            try:
                for i in os.listdir(NET_PATH):
                    os.remove(NET_PATH+i)
            except:
                pass
                
            #Create net path
            try:
                os.mkdir(NET_PATH)
            except:
                pass
            
            self.oP = OutPipe("Launcher", 0)
            for line in self.getSystemInfo():
                self.oP(line)
            self.cR = ConfigReader(ENGINE_PATH+"engine")
            self.sE = ScriptExecuter()
            self.eI = EngineInterface()
            self.eI.preLoad()
            self.eI.preLoadEpi()
            #Sloppy, removes the blacker that covers up starting glitches
            self.eI.getOverlayScene().objects["BlackScreen"].endObject()
            self.sound = SoundEngine()
            self.sound.preLoadAudio()
            
            self.s = None
            self.c = None
            self.output = True
            
            self.oP("Initialized.")
        
        def enableShader(self, index, text):
            self.oP("Activating shader pass #%i" % index)
            controller = bge.logic.getCurrentController()
            filterActuator = controller.actuators["filter"]
            
            filterActuator.mode = bge.logic.RAS_2DFILTER_CUSTOMFILTER
            filterActuator.passNumber = index
            filterActuator.shaderText = text
            
            controller.activate(filterActuator)
            controller.deactivate(filterActuator)
        
        def disableShader(self, index):
            self.oP("Deactivating shader pass #%i" % index)
            controller = bge.logic.getCurrentController()
            filterActuator = controller.actuators["filter"]
            
            filterActuator.mode = bge.logic.RAS_2DFILTER_DISABLED
            filterActuator.passNumber = index
            
            controller.activate(filterActuator)
            controller.deactivate(filterActuator)
            
        def bootSystem(self):
            self.output = int(self.cR.get("LAUNCHER", "la_output"))
            
            dedicated = int(self.cR.get("LAUNCHER", "la_dedicated"))
            
            if dedicated:
                lobby = int(self.cR.get("LAUNCHER", "la_dedicated_fast"))
                self.bootServer()
                self.s.configure("sv_game", lobby)
                self.s.configure("sv_dedicated", 1)
            else:
                self.bootClient()
        
        def getSystemInfo(self):
            f = open(ENGINE_PATH+"system"+TEXT_EXT, "r")
            
            try:
                data = eval(f.read())
                return ["EpiEngine v%.2f" % data["version"], "Built for BGE %.2f" % data["targetVersion"], "Running %s %.2f" % (data["game"], data["gameVersion"]), "Built %s" % data["date"],]
            except:
                return "EpiEngine launching."
            
            f.close()
            
        def bootClient(self):
            self.c = Client()
            #self.sE.addContext("Client", self.c)
            #self.sE.execute(bootScript)
            
            for option in self.cR.getAllOptions("CLIENT"):
                self.c.configure(option, self.cR.get("CLIENT", option))
            
        def bootServer(self):
            #bootScript = self.cR.get("SERVER", "sv_startscript")
            #addr = self.cR.get("SERVER", "sv_addr")
            #port = self.cR.get("SERVER", "sv_port")
            
            self.s = Server()
            
            #self.sE.addContext("Server", self.s)
            #self.sE.execute(bootScript)
            #
            #self.s.configure("sv_addr", addr)
            #self.s.configure("sv_port", int(port))
            
            for option in self.cR.getAllOptions("SERVER"):
                self.s.configure(option, self.cR.get("SERVER", option))
            
        def configureServer(self, level, gamemode):
            if self.s:
                self.s.configure("level", level)
                self.s.configure("gamemode", gamemode)
            
        def loop(self):
            self.sound.loop()
            
            try:
                if hasattr(self.c, "loop"):
                    self.c.loop()
            except:
                self.oP("Failure in client loop: %s" % str(traceback.format_exc()))
            
            try:
                if hasattr(self.s, "loop"):
                    self.s.loop()
            except:
                self.oP("Failure in server loop: %s" % str(traceback.format_exc()))
            
        def pushConsoleCommand(self, command):
            if hasattr(self, "s") and self.s:
                self.s.pushConsoleCommand(command)
            if hasattr(self, "c") and self.c:
                self.c.pushConsoleCommand(command)
    
    loadEpiArchive()
    l = Launcher()
    loadLauncher(l)
    l.bootSystem()
    
if "launcher" in bge.logic.globalDict:
    bge.logic.globalDict["launcher"].loop()