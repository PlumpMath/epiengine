from tools import SwitchPanel
from outpipe import OutPipe
import time

class PhysicsReader():
    def __init__(self, server):
        self.oP = OutPipe("PhysicsReader", 0)
        
        self.server = server
        self.oldPositions = {}
        self.oldActions = {}
        
        self.recent = {}
        
        self.maxMessages = 30
        self.updateCount = 0
        self.switchPanel = SwitchPanel()
        self.switchPanel.addSwitch("skipTicks", 0.0333)
        
        self.oP("Initialized.")
    
    def addEvent(self, events, event, GUID):
        self.updateCount += 1
        
        if not GUID in self.switchPanel.switches.keys():
            self.switchPanel.addSwitch(GUID, 0.0333)
        
        if not self.switchPanel.checkSwitch(GUID):
            events.append(event)
            
            self.switchPanel.tripSwitch(GUID)
    
    def roundList(self, l):
        newList = []
        
        if l == [] or type(l[0]) != type(0.0):
            return l
        
        for i in l:
            newList.append(round(i, 2))
        
        return newList
    
    def getAnimData(self, ent):
        data = {"GUID":ent.GUID, "anim":[]}
        
        for action in ent.actions:
            if action.skeleton:
                #currFrame = action.obj.getActionFrame(action.layer)
                if action.type != "frame":
                    data["anim"].append(action.action) #([action.action, currFrame])
                else:
                    data["anim"].append([action.action, action.start])
                
        return data
        
    def getTerminalParent(self, obj):
        while 1:
            if obj.parent:
                obj = obj.parent
            else:
                break
            
        return obj
        
    def getObjectData(self, ent):
        obj = ent.gameObject
        
        try:
            obj.worldPosition
        except:
            self.oP("%s has failed to load, PhysicsReader cannot function!" % ent.name)
            return
        
        pos = obj.worldPosition
        rot = obj.worldOrientation.to_euler()
        sca = obj.worldScale
        linV = obj.getLinearVelocity()
        angV = obj.getAngularVelocity()
        
        variables = ent.netVars
        
        GUID = obj["GUID"]
        
        if obj.parent:
            terminus = self.getTerminalParent(obj)
            
            if "GUID" in terminus:
                parGUID = terminus["GUID"]
                
            pars = obj.parent.name
        else:
            parGUID = ""
            pars = ""
        
        data = {
            "name":ent.name,
            "GUID":GUID,
            "par":parGUID,
            "pars":pars,
            "pos":[pos[0], pos[1], pos[2]],
            "rot":[rot[0], rot[1], rot[2]],
            "sca":[sca[0], sca[1], sca[2]],
            "linV":[linV[0], linV[1], linV[2]],
            "angV":[angV[0], angV[1], angV[2]],
            "vars":variables,
        }
        
        for key in data.keys():
            if type(data[key]) == type([]):
                data[key] = self.roundList(data[key])
        
        return data
        
    def loop(self, cli=None, override=None):
        events = []
        
        if override != None:
            old = override
            oldanim = override
        else:
            old = self.oldPositions
            oldanim = self.oldActions
        
        self.updateCount = 0
        
        self.switchPanel.loop()
        
        for ent in self.server.entities:
            if ent.physicsTrack and not ent.GUID in old.keys():
                self.addEvent(events, [cli, ["PHYSICS", "CREATE", self.getObjectData(ent)]], ent.GUID)
                self.oldPositions[ent.GUID] = self.getObjectData(ent)
                
            elif ent.physicsTrack and ent.GUID in old.keys() and self.getObjectData(ent) != old[ent.GUID]:
                
                if not ent.GUID in self.recent.keys():
                    self.addEvent(events, [cli, ["PHYSICS", "UPDATE", self.getObjectData(ent)]], ent.GUID)
                    
                    self.recent[ent.GUID] = time.time()
                
                self.oldPositions[ent.GUID] = self.getObjectData(ent)
            
            if not ent.GUID in oldanim or (ent.animTrack and self.getAnimData(ent) != oldanim[ent.GUID]):
                self.addEvent(events, [cli, ["PHYSICS", "ANIMATION", self.getAnimData(ent)]], ent.GUID)
                self.oldActions[ent.GUID] = self.getAnimData(ent)
                
        for GUID in old.keys():
            if not self.server.getEntityByGUID(GUID):
                self.addEvent(events, [cli, ["PHYSICS", "DELETE", GUID]], GUID)
                del self.oldPositions[GUID]
                break
                
        #Handle the "recent" spam blocker
        if not override:
            keys = self.recent.keys()
            for key in keys:
                if abs(self.recent[key] - time.time()) > 0.05:
                    del self.recent[key]
                    break
                
            #Handle the "massive update" spam blocker
            if self.updateCount > self.maxMessages:
                self.switchPanel.switches["skipTicks"].cooldown = ((updateCount - 30)/30) * 0.0333
                self.switchPanel.tripSwitch("skipTicks")
                
        return events
            
    def getEmergencyUpdate(self, cli):
        return self.loop(cli, override={})