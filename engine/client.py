from outpipe import OutPipe
from engineinterface import EngineInterface, loadClient
from contentreader import ContentReader
from scriptexecuter import ScriptExecuter
from inputreceiver import InputReceiver
from network import NetCore
from interface import Interface
from paths import LOCATIONS, NETSCRIPT_PATH
from threading import Thread
from time import sleep
from gameside import GameSide
from videoplayer import VideoPlayer
from physicsapplicator import PhysicsApplicator
from localizer import Localizer
from shaderhandler import ShaderHandler
from tools import OptiClock, LoopCounter
import time

class Client(GameSide):
    def __init__(self):
        '''Initializes the client.'''
        
        self.mode = "client"
        
        self.oP = OutPipe("Client", 0)
        
        self.eI = EngineInterface(objectMode=True)
        self.vP = VideoPlayer()
        self.sE = ScriptExecuter()
        self.iR = InputReceiver()
        self.l = Localizer(self)
        self.pA = PhysicsApplicator(self)
        self.sH = ShaderHandler()
        self.nC = None
        
        self.sE.addContext("Client", self)
        
        self.cvars = {
            #Low level settings
            "cl_update":1,
            "cl_synced":0,
            "cl_addr":"0.0.0.0",
            "cl_oport":7777,
            "cl_iport":7778,
            "cl_netlog":0,
            "cl_game":0,
            "cl_startscript":"",
            "cl_master":0,
            "cl_predict":1,
            "cl_smooth":0,
            
            "cl_name":"Player",
            "cl_password":"",
            
            "cl_camera":"",
            
            "cl_lockcontrols":1,
            "cl_showmouse":1,
            
            "cl_xsens":50,
            "cl_ysens":50,
            "cl_inverted":0,
            
            "cl_netping":0,
            
            #High level settings
            "cl_language":"en",
            "cl_subtitles":1,
            
            "cl_width":1280,
            "cl_height":720,
            "cl_fullscreen":0,
            
            "cl_motionblur":0,
            "cl_motionblur_amount":0,
            
            "cl_anisotropic":1,
            
            "cl_mipmap":"none",
            
            "cl_vsync":"off",
            
            "cl_musicvolume":10,
            "cl_dialogvolume":10,
            "cl_soundvolume":10,
            "cl_mastervolume":10,
            
            #Server shared settings
            "sv_level":"",
            "sv_gamemode":"",
            "sv_game":0,
            
            "sv_background_red":0,
            "sv_background_green":0,
            "sv_background_blue":0,
            "sv_background_alpha":0,
        }
        
        self.netVars = {
            
        }
        
        self.chatMessages = []
        
        self.interfaces = []
        self.entities = []
        self.level = None
        
        self.gameEvents = []
        self.updateNetwork()
        
        #self.startLoop()
        self.forceUpdateCVars()
        
        self.keepAliveTicker = 0
        self.trackedProperties = []
        
        loadClient(self)
        
        self.oP("Initialized.")
        
    def forceUpdateCVars(self):
        '''Forces all the cVars to run their updaters as though they had just been set.'''
        for key in self.cvars.keys():
            if not "sv_" == key[:3]:
                self.configure(key, self.get(key), override=True)
        self.oP("Force updated cVars.")
    
    def configure(self, key, val, fromServer=False, override=False):
        '''Configure a cVar.'''
        changed = False
        
        if key in self.cvars.keys() and (not "sv_" == key[:3] or fromServer):
            #Switch for int
            if type(self.cvars[key]) == type(0):
                val = int(val)
            
            #Used for functions    
            if type(self.cvars[key]) == type(self.configure):
                self.cvars[key](val)
                self.oP("CVar %s executed." % key)
            else:
                if val != self.cvars[key] or override:
                    changed = True
                    self.cvars[key] = val
                    self.oP("CVar %s configured to %s (%s)." % (key, val, str(type(val)).replace("<class '", "").replace("'>", "")))
        elif "sv_" == key[:3] and not fromServer and key in self.cvars.keys() and self.cvars[key] != val:
            self.sendEvent(["SYSTEM", "CVARS", [key, val]])
            self.oP("Asking server to change CVar %s." % key)
        else:
            self.oP("CVar %s not present." % key)
            
        if changed:
            self.updateGame(key)
    
    def connectGame(self):
        '''Connects to a game.'''
        self.oP("Connecting to game.")
        self.nC.connect((self.get("cl_addr"), self.get("cl_oport")))
        self.configure("cl_game", 1)
        self.configure("cl_synced", 0)
        
    def disconnectGame(self):
        '''Disconnects from a game.'''
        self.oP("Disconnecting from a game.")
        self.updateNetwork()
        self.configure("cl_game", 0)
        self.configure("cl_synced", 0)
        self.configure("cl_update", 1)
        self.oP("Disconnected from game.")
        
    def updateGame(self, key):
        '''Reacts to changes to the cVars.'''
        if key == "cl_startscript":
            self.sE.addContext("Client", self)
            self.sE.execute(self.get("cl_startscript"))
            
        elif key in ["cl_iport"]:
            self.updateNetwork()
            
        elif key == "cl_addr":
            if self.get("cl_addr") == "0.0.0.0":
                self.configure("cl_addr", "127.0.0.1")
            
        elif key == "cl_name":
            self.sendEvent(["SYSTEM", "NAME", self.get("cl_name")])
            
        elif key == "sv_level" and not self.get("cl_master"):
            if self.get("sv_game"):
                self.setLevel(self.get("sv_level"))
            
        elif key == "sv_game" and not self.get("cl_master"):
            if self.get("sv_game"):
                self.setLevel(self.get("sv_level"))
            else:
                self.endLevel()
            
        elif key in ["sv_background_red", "sv_background_green", "sv_background_blue", "sv_background_alpha"] and not self.get("cl_master"):
            self.eI.setBackgroundColor((self.getBackgroundColor()))
            
        elif key == "cl_width" or key == "cl_height":
            self.eI.setResolution(self.get("cl_width"), self.get("cl_height"))
        elif key == "cl_fullscreen":
            self.eI.setFullscreen(self.get("cl_fullscreen"))
        elif key == "cl_motionblur" or key == "cl_motionblur_amount":
            self.eI.setMotionBlur(self.get("cl_motionblur"), self.get("cl_motionblur_amount"))
        elif key == "cl_anisotropic":
            self.eI.setAnisotropic(self.get("cl_anisotropic"))
        elif key == "cl_mipmap":
            self.eI.setMipmapping(self.get("cl_mipmap"))
        elif key == "cl_vsync":
            self.eI.setVSync(self.get("cl_vsync"))
        elif key == "cl_camera" and self.get("cl_camera") != "":
            self.eI.setCamera(self.get("cl_camera"))
            
        elif key == "cl_mastervolume":
            launcher = self.eI.getGlobal("launcher")
            
            if launcher:
                launcher.sound.setMasterVolume(self.get("cl_mastervolume"))
                
        elif key == "cl_musicvolume":
            launcher = self.eI.getGlobal("launcher")
            
            if launcher:
                launcher.sound.setMusicVolume(self.get("cl_musicvolume"))
                
        elif key == "cl_dialogvolume":
            launcher = self.eI.getGlobal("launcher")
            
            if launcher:
                launcher.sound.setDialogVolume(self.get("cl_dialogvolume"))
                
        elif key == "cl_soundvolume":
            launcher = self.eI.getGlobal("launcher")
            
            if launcher:
                launcher.sound.setSoundVolume(self.get("cl_soundvolume"))
                
        elif key == "cl_subtitles":
            launcher = self.eI.getGlobal("launcher")
            
            if launcher:
                launcher.sound.subtitles = self.get("cl_subtitles")
        
        elif key == "cl_language":
            launcher = self.eI.getGlobal("launcher")
            
            if launcher:
                launcher.sound.language = self.get("cl_language")
                
        elif key == "cl_lockcontrols":
            self.iR.locked = self.get("cl_lockcontrols")
            
        elif key == "cl_showmouse":
            self.eI.setMouseState(self.get("cl_showmouse"))
                
        elif key == "cl_xsens":
            self.iR.xsens = self.get("cl_xsens")
        
        elif key == "cl_ysens":
            self.iR.ysens = self.get("cl_ysens")
               
        elif key == "cl_inverted":
            self.iR.inverted = self.get("cl_inverted")
            
        elif key == "cl_predict":
            self.iR.predict = self.get("cl_predict")
            
            if not self.get("cl_predict"):
                for GUID in self.pA.blacklistedGUIDs:
                    self.removeFromRotationBlacklist(GUID)
                    
        elif key == "cl_smooth":
            self.pA.smooth = self.get("cl_smooth")
            
        elif key == "cl_netlog":
            if self.get("cl_netlog"):
                self.nC.configure("DEBUG", True)
                self.nC.configure("VERBOSE", True)
            else:
                self.nC.configure("DEBUG", False)
                self.nC.configure("VERBOSE", False)
                
        elif key == "cl_netping":
            self.nC.pingcount = self.get("cl_netping")
            
    def updateNetwork(self):
        '''Update the network module for changes to port or addr'''
        self.purgeNetwork()
        
        self.nC = NetCore()
        if self.get("cl_netlog"):
            self.nC.configure("DEBUG", True)
            self.nC.configure("VERBOSE", True)
        else:
            self.nC.configure("DEBUG", False)
            self.nC.configure("VERBOSE", False)
        
        self.nC.pingcount = self.get("cl_netping")
            
        self.nC.configure("NAME", "Client")
        self.nC.setProtocol("UDP")
        self.nC.configure("PORT", self.get("cl_iport"))
        self.nC.initialize()
        
    def purgeNetwork(self):
        '''Destroys the NetCore once and for all.'''
        if self.nC:
            self.nC.clear()
            self.nC.destroy()
            self.nC = None
    
    def startGameRemote(self):
        '''Used to connect to another person's game.'''
        self.oP("Starting game (remote)...")
        self.configure("cl_master", 0)
        self.configure("cl_update", 1)
        self.configure("cl_predict", 1)
        
        self.connectGame()
        
    def startGameFull(self):
        '''Used if you want the lobby when you start up a game.'''
        self.oP("Starting game (full)...")
        self.configure("cl_master", 1)
        self.configure("cl_update", 0)
        self.configure("cl_predict", 0)
        
        launcher = self.eI.getGlobal("launcher")
        
        if launcher:
            launcher.bootServer()
            self.oP("Booted server from client (Full).")
            self.configure("cl_addr", launcher.s.get("sv_addr"))
            self.connectGame()
        
    def startGameFast(self, level, gamemode, singleplayer=True):
        '''Used if you want to go straight to the game, usually used for singleplayer.'''
        self.oP("Starting game (fast)...")
        self.configure("cl_master", 1)
        self.configure("cl_update", 0)
        self.configure("cl_predict", 0)
        self.configure("cl_game", 1)
        
        self.updateNetwork()
        
        launcher = self.eI.getGlobal("launcher")
        
        if launcher:
            launcher.bootServer()
            self.oP("Booted server from client (Fast).")
            launcher.s.configure("sv_level", level)
            launcher.s.configure("sv_gamemode", gamemode)
            launcher.s.configure("sv_game", 1)
            if singleplayer:
                launcher.s.configure("sv_singleplayer", 1)
            else:
                launcher.s.configure("sv_singleplayer", 0)
            self.configure("cl_addr", launcher.s.get("sv_addr"))
            self.connectGame()
            
    def endGame(self):
        '''Ends the game instance and disconnects.'''
        self.oP("Ending game session...")
        self.disconnectGame()
        
        self.endLevel()
        
        launcher = self.eI.getGlobal("launcher")
        
        if launcher and self.get("cl_master") and launcher.s:
            launcher.s.quitGame()
            launcher.s = None
    
    def quitGame(self):
        '''Quits the game completely.'''
        self.oP("Shutting down...")
        self.endGame()
        self.purgeNetwork()
        self.eI.quitGame()
    
    def setMusic(self, music):
        '''Sets the music track.'''
        launcher = self.eI.getGlobal("launcher")
        
        launcher.sound.playMusic(music)
        self.oP("Set music to %s." % music)
        
    def stopMusic(self):
        '''Stops the music track.'''
        launcher = self.eI.getGlobal("launcher")
        
        launcher.sound.stopMusic()
        self.oP("Stopped music.")
        
    def playSound(self, sound, emitter=None):
        '''Plays the sound.'''
        launcher = self.eI.getGlobal("launcher")
        
        if emitter:
            launcher.sound.playSound(sound, emitter.gameObject)
        else:
            launcher.sound.playSound(sound)
            
        self.oP("Started playing sound %s." % sound)
        
    def stopSound(self, handle):
        '''Stops a sound.'''
        launcher = self.eI.getGlobal("launcher")
        
        GUID, name = launcher.sound.stopSound(handle)
        
        self.oP("Stopped sound %s." % name)
        
    def stopSoundByGUID(self, GUID, name):
        '''Stops a sound.'''
        launcher = self.eI.getGlobal("launcher")
        
        launcher.sound.stopSoundByGUID(GUID, name)
        self.oP("Stopped sound %s." % name)
        
    def playDialog(self, sound, emitter):
        '''Plays a dialog line.'''
        launcher = self.eI.getGlobal("launcher")
        
        if emitter:
            launcher.sound.playDialog(sound, emitter.gameObject)
        else:
            launcher.sound.playDialog(sound)
            
        self.oP("Playing dialog %s." % sound)
        
    def stopDialog(self, handle):
        '''Stops a dialog line.'''
        launcher = self.eI.getGlobal("launcher")
        
        GUID, name = launcher.sound.stopDialog(handle)
        
        self.oP("Stopped dialog %s." % name)
        
    def stopDialogByGUID(self, GUID, name):
        '''Stops a dialog line.'''
        launcher = self.eI.getGlobal("launcher")
        
        launcher.sound.stopDialogByGUID(GUID, name)
        
        self.oP("Stopped dialog %s." % name)
        
    def enableShader(self, index, name, mode):
        '''Enables a shader as a filter for the entire screen.'''
        self.sH.enableShader(index, name, mode)
    
    def disableShader(self, index):
        '''Disables a shader that was filtering the entire screen.'''
        self.sH.disableShader(index)
        
    def playVideo(self, video):
        '''Plays a video.'''
        self.vP.playVideo(video)
        self.oP("Started video %s." % video)
        
    def stopVideo(self):
        '''Stops a video.'''
        self.vP.stopVideo()
        self.oP("Stopped video.")
        
    def replaceMesh(self, ent, meshName):
        '''Replaces the mesh of an Entity.'''
        cR = self.load("Mesh", meshName)
        
        name = cR.get("name")
        resourcePath = cR.get("resourcePath")
        
        self.loadLibrary("Mesh", resourcePath, mesh=True)
        
        ent.gameObject.replaceMesh(meshName, True, True)
        self.oP("Replaced mesh of %s with %s." % (ent.GUID, meshName))
        
    def addInterface(self, name):
        '''Adds an interface.'''
        if not self.getInterfaceByName(name):
            cR = self.load("UI", name)
            
            name = cR.get("name")
            resource = cR.get("resourcePath")
            scriptName = cR.get("scriptPath")
            
            #self.loadLibrary("UI", resource)
            
            self.oP("Creating interface %s." % name)
            self.interfaces.append(Interface(name, resource, scriptName))
        else:
            self.oP("Interface %s already exists, not created." % name)
        
    def removeInterface(self, name):
        '''Removes an interface.'''
        interface = self.getInterfaceByName(name)
            
        if interface:
            self.oP("Removing interface %s." % name)
            self.interfaces.remove(interface)
            interface.kill()
        
    def removeAllInterfaces(self):
        '''Removes all interfaces.'''
        self.oP("Removing all interfaces.")
        names = []
        for interface in self.interfaces:
            names.append(interface.name)
            
        for name in names:
            self.removeInterface(name)
        
    def getInterfaceByName(self, name):
        '''Gets an interface by name.'''
        for interface in self.interfaces:
            if interface.name == name:
                return interface
        
    def addMarker(self, name, GUID):
        '''Adds a marker tracking the specified Entity.'''
        cR = self.load("UI", name)
        
        name = cR.get("name")
        resource = cR.get("resourcePath")
        
        self.eI.getGlobal("addToWaypoints")(resource, name, GUID)
        
        self.oP("Added waypoint %s tracking %s." % (name, GUID))
    
    def removeMarker(self, GUID):
        '''Removes all markers tracking an Entity.'''
        for obj in self.eI.getWaypointsScene().objects:
            if "targetGUID" in obj and obj["targetGUID"] == GUID:
                obj.endObject()
                
        self.oP("Removed waypoints tracking %s." % GUID)
    
    def inputClick(self, keyCode, pos):
        '''Checks for the interface clicks.'''
        obj, scene = self.eI.getMouseOverObjectScene(pos)
        
        if obj and scene:
            for interface in self.interfaces:
                if interface.name == self.eI.getTerminalParent(obj).name:
                    interface.onClick(obj.name)
                    return True
                
            for i in self.entities:
                if obj == i.gameObject or obj in i.gameObject.childrenRecursive:
                    i.onClick(obj.name)
                    return True
            
        return False
    
    def getDisconnectReaction(self):
        '''Gets the reaction function for disconnecting from the server.'''
        self.sE.execute(NETSCRIPT_PATH+"disconnect")
        return self.disconnectReaction
    
    def addToRotationBlacklist(self, GUID):
        '''Adds a GUID to the rotation blacklist.'''
        if not GUID in self.pA.blacklistedGUIDs:
            self.pA.blacklistedGUIDs.append(GUID)
            
    def removeFromRotationBlacklist(self, GUID):
        '''Removes a GUID from the rotation blacklist.'''
        if GUID in self.pA.blacklistedGUIDs:
            self.pA.blacklistedGUIDs.remove(GUID)
    
    def sendInterfaceEvent(self, event, aux=None):
        '''Sends an interface event.'''
        self.sendEvent(["INPUT", "INTERFACE", [event, aux]])
    
    def sendChatMessage(self, msg):
        '''Sends a chat message.'''
        self.sendEvent(["SYSTEM", "CHAT", msg])
        
    def sendGameEvent(self, mode, data):
        '''Sends a game event.'''
        self.sendEvent(["GAME", mode, data])
    
    def sendEvent(self, event):
        '''Sends an event to the server.'''
        if event[0] == "INPUT" or event == "KEEPALIVE":
            mode = "FAF"
        elif event[0] in ["SYSTEM", "GAME", "NETWORK"]:
            mode = "RT"
        
        if self.nC.clients:
            server = self.nC.clients[0]
            server.send(event, mode)
    
    def recvEvent(self, event):
        '''Handles an event from the server.'''
        if event[0] == "PHYSICS" and self.get("cl_update"):
            self.pA.update(event)
        if event[0] == "SYSTEM":
            if event[1] == "CVARS":
                self.configure(event[2][0], event[2][1], fromServer=True)
            elif event[1] == "NETVARS":
                self.netVars[event[2][0]] = event[2][1]
                
            elif event[1] == "SOUND_PLAY" and self.get("cl_update"):
                entity = self.getEntityByGUID(event[2][0])
                self.playSound(event[2][1], entity)
            elif event[1] == "SOUND_STOP" and self.get("cl_update"):
                self.stopSoundByGUID(event[2][0], event[2][1])
                
            elif event[1] == "DIALOG_PLAY" and self.get("cl_update"):
                entity = self.getEntityByGUID(event[2][0])
                self.playDialog(event[2][1], entity)
            elif event[1] == "DIALOG_STOP" and self.get("cl_update"):
                self.stopDialogByGUID(event[2][0], event[2][1])
                
            elif event[1] == "MUSIC_PLAY" and self.get("cl_update"):
                self.setMusic(event[2][0])
            elif event[1] == "MUSIC_STOP" and self.get("cl_update"):
                self.stopMusic()
                
            elif event[1] == "SET_CAMERA":
                self.configure("cl_camera", event[2])
                
            elif event[1] == "INTERFACE_CREATE":
                self.addInterface(event[2])
            elif event[1] == "INTERFACE_REMOVE":
                self.removeInterface(event[2])
                
            elif event[1] == "CHAT":
                self.chatMessages.append(event[2])
                
    def loop(self):
        '''Does everything basically.'''
        
        #cl = OptiClock()
        
        #Detector Index
        if not self.get("cl_master"):
            self.updateDetectorIndex()
            
        #cl.clockIn("DetectorIndex")
        
        #KEEP ALIVE
        self.keepAliveTicker += 1
        if self.keepAliveTicker % 600 == 0:
            self.sendEvent("KEEPALIVE")
            
        #cl.clockIn("KeepAlive")
        
        #Do Things#######################
        
        #Read in controls
        
        self.iR.checkControls()
        
        #cl.clockIn("Input")
        
        #Update Video Player
        
        self.vP.loop()
        
        #cl.clockIn("VideoPlayer")
        
        if self.get("cl_update"):
            #Update localization
            self.l.loop()
            
            #cl.clockIn("Localization")
            #Apply shaders
            self.sH.loop()
        
        #cl.clockIn("Shaders")
        #Run object code
        
        for ent in self.entities:
            if hasattr(ent, "loop"):
                ent.checkAnimation()
                ent.loop(self, "client")
        #Run interface code
        
        #cl.clockIn("Entities")
        
        if self.level:
            if hasattr(self.level, "loop"):
                self.level.loop(self, "client")
        
        #cl.clockIn("Level")
        
        for interface in self.interfaces:
            if hasattr(interface, "loop"):
                try:
                    interface.loop()
                except:
                    pass
        
        #cl.clockIn("Interface")
        
        if self.nC:
            #Send Things#####################
            for key in self.iR.keyEvents:
                self.sendEvent(key)
            
            for event in self.gameEvents:
                self.sendEvent(event)
            
            self.gameEvents = []
            self.iR.keyEvents = []
            
            #cl.clockIn("SendLoop")
            
            #Recv Things#####################
            
            if self.nC.clients:
                server = self.nC.clients[0]
                
                packet = server.recv()
                
                if packet:
                    payload = packet.getPayload()
                    
                    try:
                        data = eval(payload)
                    except:
                        data = None
                    
                    if data:
                        self.recvEvent(data)
                        
            #cl.clockIn("RecvLoop")
            
            #Initial sync
            if self.nC.clients:
                server = self.nC.clients[0]
                
                if not self.get("cl_synced"):
                    server.disconnectFunc = self.getDisconnectReaction()
                    self.sendEvent(["SYSTEM", "NAME", self.get("cl_name")])
                    self.sendEvent(["SYSTEM", "PASSWORD", self.get("cl_password")])
                    self.sendEvent(["SYSTEM", "PHYSICS", "FORCEUPDATE"])
                    self.configure("cl_synced", 1)
                    
            #cl.clockIn("Sync")
                
            #KILL THINGS###################################################
            kill = self.nC.pullKillQueue()
            
            if kill:
                kill()
                
            #cl.clockIn("Kill")
            
            self.nC.loop()
            
            #cl.clockIn("Network")