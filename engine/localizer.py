from engineinterface import EngineInterface
from outpipe import OutPipe
from paths import LOCALIZATION_PATH, TEXT_EXT

class Localizer():
    def __init__(self, master):
        self.oP = OutPipe("Localizer", 0)
        self.eI = EngineInterface()
        self.master = master
        self.oldLanguage = ""
        self.oldObjectCount = 0
        self.oP("Initialized.")
    
    def getLocalization(self, msg):
        localizationFile = open(LOCALIZATION_PATH+self.master.get("cl_language")+"/"+"strings"+TEXT_EXT, "r")
        
        try:
            strings = eval(localizationFile.read())
            return strings[msg]
        except:
            return msg
        
    def loop(self):
        
        if self.oldLanguage != self.master.get("cl_language"):
            for obj in self.eI.getAllObjects():
                if "localized" in obj:
                    localized = self.getLocalization(obj["localized"])
                    if obj["Text"] != localized:
                        obj["Text"] = localized
            self.oldLanguage = self.master.get("cl_language")
            
        objects = self.eI.getAllObjects()
            
        if self.oldObjectCount != len(objects):
            for obj in objects:
                if hasattr(obj, "resolution"):
                    obj.resolution = 10
                    
                if "localized" in obj and obj["Text"] in ["", "Text", obj["localized"]]:
                    localized = self.getLocalization(obj["localized"])
                    if obj["Text"] != localized:
                        obj["Text"] = localized
            self.oldObjectCount = len(objects)