from time import gmtime
import bge
from paths import ENGINE_PATH, TEXT_EXT
from tools import getFormattedTime

class OutPipe():
    def __init__(self, header, mode):
        self.HEADER = header
        self.mode = mode
        
        try:
            self.launcher = bge.logic.globalDict["launcher"]
        except:
            self.launcher = None
        
        self.log = True
        
    def __call__(self, msg, mode=100):
        if self.mode <= mode and (not self.launcher or self.launcher.output):
            msg = str(msg).replace(ENGINE_PATH, "")
            finalOut = "%-20s - %-8s - %-30s" % (self.HEADER, getFormattedTime(), str(msg))
            if "printToConsole" in bge.logic.globalDict:
                bge.logic.globalDict["printToConsole"](finalOut)
            print(finalOut)
            
            if self.log:
                try:
                    self.toFile(ENGINE_PATH+"engine_log"+TEXT_EXT, msg)
                except:
                    import traceback
                    print(traceback.format_exc())
            
    def toFile(self, name, data):
        f = open(name, "a")
        finalOut = "%-20s - %-8s - %-50s\n" % (self.HEADER, getFormattedTime(), str(data))
        f.write(finalOut)
        f.close()