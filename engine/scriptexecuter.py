from paths import SCRIPTS_PATH, SCRIPT_EXT
from outpipe import OutPipe
from traceback import format_exc
import sys

class ScriptExecuter():
    def __init__(self):
        self.oP = OutPipe("ScriptExecuter", 0)
        
        self.context = {}
        
        self.oP("Initialized.")
        
    def addContext(self, key, obj):
        self.context[key] = obj
        
    def execute(self, scriptName):
        finalPath = SCRIPTS_PATH+scriptName+SCRIPT_EXT
        self.enableImport(finalPath)
        try:
            f = open(finalPath, "r")
            self.oP("Opened script %s." % finalPath)
        except:
            self.oP("Failed to open script %s." % finalPath)
            return
            
        raw = f.read()
        f.close()
        
        try:
            exec(raw, self.context)
            self.oP("Script %s executed." % finalPath)
        except:
            self.oP("Error occured during execution of %s: %s." % (finalPath, str(format_exc())))
            
        self.disableImport(finalPath)
        
    def enableImport(self, path):
        counter = len(path)-1
        while counter != 0:
            if path[counter] == "/":
                path = path[:counter]
                break
            counter -= 1
            
        sys.path.append(path)
        
    def disableImport(self, path):
        counter = len(path)-1
        while counter != 0:
            if path[counter] == "/":
                path = path[:counter]
                break
            counter -= 1
            
        sys.path.remove(path)