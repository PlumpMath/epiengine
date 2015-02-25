import os
from paths import GAME_PATH

class Controller():
    #Initialization
    def __init__(self):
        self.i = None
    
    def setI(self, i):
        '''Assigns the interface.'''
        self.i = i
        
    #Disk access
    def getItems(self, mode):
        '''Gets all the items in a particular directory.'''
        items = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(GAME_PATH+mode+"/")) for f in fn]
        
        truncItems = []
        
        for item in items:
            if item[len(item)-4:] == ".epi":
                truncItems.append(item[:len(item)-4].replace(GAME_PATH+mode+"/", "").replace("\\", "/"))
        
        return truncItems
    
    #Readin
    def readEpi(self, path):
        '''Reads a .epi in.'''
        with open(path, "r") as f:
            data = eval(f.read())
            
        return data
    
    def readSystem(self):
        '''Reads the system.txt in.'''
        with open(GAME_PATH+"/../system.txt", "r") as f:
            data = eval(f.read())
            
        return data
    
    def readCVars(self):
        '''Reads the engine.ini in.'''
        
        data = 
        
        return data
        
    def readLocalization(self):
        '''Reads the localization files in.'''
        
        data = 
        
        return data
    
    #Update
    def openUpdateItem(self, item):
        '''Updates an item in the .epi list.'''
        path = GAME_PATH+self.i.mode+"/"+item+".epi"
        
        data = self.readEpi(path)
        
        self.i.constructUpdateWindow(data)
        
    #Configuration
    def openConfigureCVars(self):
        '''Opens the cvar configuration window.'''
        
        data = self.readCVars()
        
        self.i.constructCVarWindow(data)
        
    def openConfigureLocalization(self):
        '''Opens the localization configuration window.'''
        
        data = self.readLocalization()
        
        self.i.constructLocalizationWindow(data)
    
    def openConfigureSystem(self):
        '''Opens the system configuration window.'''
        
        data = self.readSystem()
        
        self.i.constructSystemWindow(data)
    
    #Delete
    def deleteItem(self, item):
        '''Removes an item from the disk.'''
        path = GAME_PATH+self.i.mode+"/"+item+".epi"
        
        if self.i.confirm("Are you sure you wish to delete this item?"):
            if self.i.confirm("Do you want to remove all referenced files?"):
                paths = []
                data = self.readEpi(path)
                
                if self.i.mode == "Entities":
                    paths.append(GAME_PATH+"Entities/"+data["resourcePath"])
                    paths.append(GAME_PATH+"Scripts/"+data["scriptPath"])
                elif self.i.mode == "Meshes":
                    paths.append(GAME_PATH+"Meshes/"+data["resourcePath"])
                elif self.i.mode == "Sounds":
                    for i in data["resources"]:
                        paths.append(GAME_PATH+"Sounds/"+i)
                elif self.i.mode == "Levels":
                    paths.append(GAME_PATH+"Levels/"+data["resourcePath"])
                    paths.append(GAME_PATH+"Scripts/"+data["scriptPath"])
                elif self.i.mode == "UI":
                    paths.append(GAME_PATH+"UI/"+data["resourcePath"])
                    paths.append(GAME_PATH+"Scripts/"+data["scriptPath"])
                elif self.i.mode == "Dialog":
                    for i in data["resources"]:
                        paths.append(GAME_PATH+"Dialog/"+i)
                elif self.i.mode == "Music":
                    for i in data["resources"]:
                        paths.append(GAME_PATH+"Music/"+i)
                
                #Remove referenced resources
                for i in paths:
                    os.remove(i)
                
            os.remove(path)
            
        self.i.updateRoot()