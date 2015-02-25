from tools import isSpecialMethod

class Sarcophagus():
    def __init__(self):
        self.records = {}
        self.playerRecords = {}
        self.entities = []
        self.players = []
        
        self.removeList = ["gameObject", "eI", "sE", "detectors", "actions"]
        self.removeListPlayer = ["master", "sE", "cli"]
        
    def deconstructEntity(self, ent):
        removedData = {}
        
        for i in self.removeList:
            removedData[i] = getattr(ent, i)
            #exec("del ent."+i)
            setattr(ent, i, None)
            
        for i in dir(ent):
            if "function" in str(type(getattr(ent, i))) and not isSpecialMethod(i):
                removedData[i] = getattr(ent, i)
                #exec("del ent."+i)
                setattr(ent, i, None)
        
        self.records[ent.GUID] = removedData
        
    def deconstructPlayer(self, player):
        removedData = {}
        
        for i in self.removeListPlayer:
            removedData[i] = getattr(player, i)
            #exec("del ent."+i)
            setattr(player, i, None)
            
        for i in dir(player):
            if "function" in str(type(getattr(player, i))) and not isSpecialMethod(i):
                removedData[i] = getattr(player, i)
                #exec("del ent."+i)
                setattr(player, i, None)
        
        self.playerRecords[player.username] = removedData
        
    def reconstructPlayer(self, player):
        removedData = self.playerRecords[player.username]
        
        for key in removedData.keys():
            setattr(player, key, removedData[key])
        
    def addEntity(self, ent, objData):
        self.entities.append([ent, objData])
        
        #for i in dir(ent):
        #    print(i, type(getattr(ent, i)))
        
    def addPlayer(self, player):
        self.players.append(player)
        
    def reconstructEntity(self, ent):
        removedData = self.records[ent.GUID]
        
        for key in removedData.keys():
            setattr(ent, key, removedData[key])
    
    def cleanUp(self):
        a = self.records
        self.records = None
        b = self.playerRecords
        self.playerRecords = None
        return a, b
    
    def restore(self, records, playerRecords):
        self.records = records
        self.playerRecords = playerRecords
    
    