try:
    from configparser import ConfigParser
except:
    from ConfigParser import ConfigParser
from outpipe import OutPipe
from paths import CONFIG_EXT

class ConfigReader():
    def __init__(self, fileName):
        self.oP = OutPipe("ConfigReader", 0)
        
        self.parser = ConfigParser()
        
        self.open(fileName+CONFIG_EXT)
        
        self.oP("Initialized.")
        
    def open(self, fileName):
        try:
            self.parser.read(fileName)
            self.oP("Opened config %s." % fileName)
        except:
            self.oP("Failed to open config %s." % fileName)
            
    def get(self, section, key):
        try:
            result = self.parser.get(section, key)
            self.oP("Retrieved %s - %s." % (section, key))
            return result
        except:
            self.oP("Failed to retrieve %s - %s." % (section, key))
            
    def set(self, section, key, value):
        try:
            result = self.parser.set(section, key, value)
            self.oP("set %s - %s." % (section, key))
            return result
        except:
            self.oP("Failed to set %s - %s." % (section, key))
            
    def getAllOptions(self, section):
        try:
            return self.parser.options(section)
        except:
            return []