from outpipe import OutPipe
from engineinterface import EngineInterface
from scriptexecuter import ScriptExecuter

class Interface():
    def __init__(self, name, resource, scriptName):
        self.oP = OutPipe("Interface - "+name, 0)
        self.eI = EngineInterface(objectMode=False)
        self.sE = ScriptExecuter()
        
        self.name = name
        
        self.gameObject = None
        
        self.sE.addContext("Interface", self)
        self.sE.execute(scriptName)
        
        self.eI.getGlobal("addToQueue")(resource, name, self)
        
        if hasattr(self, "init"):
            self.init()
        
        self.oP("Added interface %s." % name)
            
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
            
    def kill(self):
        self.eI.removeInterface(self.name)