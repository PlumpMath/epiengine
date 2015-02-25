import bge
from outpipe import OutPipe
from paths import MAIN_EXT

class ContentReader():
    def __init__(self, fileName):
        self.oP = OutPipe("ContentReader", 0)
        
        self.val = None
        self.load(fileName)
        
        self.oP("Initialized.")
        
    def load(self, fileName):
        finalName = fileName+MAIN_EXT
        
        if not finalName in bge.logic.globalDict["epiarchive"].keys():
            try:
                f = open(finalName, "r")
                self.oP("Opened file %s." % (finalName))
            except:
                self.oP("Failed to open file %s." % (finalName))
                return
            
            text = f.read()
            
            try:
                val = eval(text)
                self.oP("Evaluated file.")
            except:
                self.oP("Failed to evaluate file.")
                return
            
            self.val = val
            bge.logic.globalDict["epiarchive"][finalName] = val
            
            f.close()
        else:
            self.oP("Recovered %s from epiarchive." % (finalName))
            data = bge.logic.globalDict["epiarchive"][finalName]
            self.val = data
        
    def get(self, *keys):
        currentLayer = self.val
        
        for key in keys:
            try:
                currentLayer = currentLayer[key]
            except:
                self.oP("Failed to load key %s from file." % str(keys))
                return ""
            
        return currentLayer