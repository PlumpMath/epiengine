from outpipe import OutPipe
from engineinterface import EngineInterface
from scriptexecuter import ScriptExecuter
from entity import Detector
from paths import INPUT_PATH

class Player():
    def __init__(self, master, cli):
        #Tools
        self.oP = OutPipe("Player - "+str(cli.addr), 0)
        self.master = master
        self.initVolatileModules()
        
        self.username = cli.userProps["username"]
        self.confirmed = False
        
        #Basic values
        self.cli = cli
        self.entity = None

        self.installCustomCode()
        
        self.netVars = {}
        
        self.init()
        
        self.oP("Initialized player.")
    
    def sendPlayerEvent(self, event):
        self.master.sendEvent([self.cli, event])
    
    def initVolatileModules(self):
        self.sE = ScriptExecuter()
        self.sE.addContext("Player", self)
        self.sE.addContext("Detector", Detector)
    
    def installCustomCode(self):
        self.sE.execute(INPUT_PATH+"player")
        
    def configureNetVar(self, key, val):
        if not key in self.netVars.keys() or val != self.netVars[key]:
            self.netVars[key] = val
            self.master.sendEvent([self.cli, ["SYSTEM", "NETVARS", [key, val]]])
            
    def reconstructPlayer(self, server):
        self.master = server
        self.initVolatileModules()
        self.installCustomCode()
        self.reInitPlayer()