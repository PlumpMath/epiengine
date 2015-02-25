from outpipe import OutPipe
from engineinterface import EngineInterface, loadServer
from scriptexecuter import ScriptExecuter
from physicsreader import PhysicsReader
from network import NetCore
from gameside import GameSide
from paths import LOCATIONS, SAVE_PATH, SAVE_EXT, GAMEMODE_PATH
from entity import Entity
from player import Player
from shaderhandler import ShaderHandler
from localizer import Localizer
from sarcophagus import Sarcophagus
from tools import OptiClock
import time
import shelve

class Server(GameSide):
    def __init__(self):
        '''Initializes the server.'''
        self.mode = "server"
        
        self.oP = OutPipe("Server", 0)
        self.nC = None
        
        self.cvars = {
            "sv_addr":"0.0.0.0",
            "sv_port":7777,
            "sv_netlog":0,
            "sv_level":"",
            "sv_game":0,
            "sv_singleplayer":0,
            "sv_gamemode":"singleplayer",
            "sv_startscript":"",
            "sv_master":"",
            "sv_dedicated":0,
            
            "sv_chat":1,
            
            "sv_background_red":0,
            "sv_background_green":0,
            "sv_background_blue":0,
            "sv_background_alpha":0,
            
            "sv_password":"",
            
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
            
            "cl_netping":0,
        }
        
        self.netVars = {
            
        }
        
        self.oldNetVars = self.netVars
        self.oldcvars = self.cvars
        
        self.gameMode = None
        self.level = None
        
        self.unassignedPlayers = []
        
        self.entities = []
        
        self.events = []
        
        self.saveFile = None
        
        self.chatMessages = []
        
        self.eI = EngineInterface(True)
        self.sE = ScriptExecuter()
        self.pR = PhysicsReader(self)
        self.sH = ShaderHandler()
        self.l = Localizer(self)
        
        self.updateNetwork()
        
        self.forceUpdateCVars()
        
        self.keepAliveTicker = 0
        self.trackedProperties = []
        
        loadServer(self)
        
        self.oP("Initialized.")
    
    def forceUpdateCVars(self):
        '''Forces all the cVars to run their updaters as though they had just been set.'''
        for key in self.cvars.keys():
            if not "cl_" == key[:3]:
                self.configure(key, self.get(key), override=True)
        self.oP("Force updated cVars.")

    def configureNetVar(self, var, val):
        '''Configures a NetVar and updates clients about it.'''
        self.netVars[var] = val
        self.events.append([None, ["SYSTEM", "NETVARS", [var, val]]])
        self.oP("Configured netVar %s to %s." % (str(var), str(val)))
    
    def configure(self, key, val, override=False):
        '''Configure a cvar.'''
        changed = False
        
        if key in self.cvars.keys():
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
                    self.sendEvent([None, ["SYSTEM", "CVARS", [key, val]]])
                    self.oP("CVar %s configured to %s (%s)." % (key, val, str(type(val)).replace("<class '", "").replace("'>", "")))
        else:
            self.oP("CVar %s not present." % key)
            
        if changed:
            self.updateGame(key)
    
    def endGame(self):
        '''Ends the game instance.'''
        self.oP("Ending game instance.")
        self.endGameMode()
        self.endLevel()
        
    def endGameMode(self):
        '''Ends the game mode.'''
        if hasattr(self.gameMode, "kill"):
            self.gameMode.kill()
        self.gameMode = None
        
    def replaceMesh(self, ent, meshName):
        '''Replaces the mesh of an entity.'''
        cR = self.load("Mesh", meshName)
        
        name = cR.get("name")
        resourcePath = cR.get("resourcePath")
        
        self.loadLibrary("Mesh", resourcePath, mesh=True)
        
        for obj in self.eI.getMainScene().objectsInactive:
            if obj.name == meshName:
                meshName = obj.meshes[0]
                break
        
        ent.gameObject.replaceMesh(meshName, True, True)
        self.sendEvent([None, ["PHYSICS", "MESH", [ent.GUID, meshName]]])
        self.oP("Replaced mesh of %s with %s." % (ent.GUID, meshName))
    
    def quitGame(self):
        '''Ends the game and kills network connections.'''
        self.oP("Shutting down...")
        self.endGame()
        self.purgeNetwork()
    
    def setGameMode(self, name):
        '''Load a gamemode into the engine.'''
        self.sE.addContext("Server", self)
        self.sE.execute(GAMEMODE_PATH+name)
        self.gameMode = self.newGamemode(self)
        
    def updateNetwork(self):
        '''Update the network module for changes to port or addr'''
        self.purgeNetwork()
        
        self.nC = NetCore()
        if self.get("sv_netlog"):
            self.nC.configure("DEBUG", True)
            self.nC.configure("VERBOSE", True)
        else:
            self.nC.configure("DEBUG", False)
            self.nC.configure("VERBOSE", False)
            
        self.nC.pingcount = self.get("cl_netping")
            
        self.nC.configure("NAME", "Server")
        self.nC.setProtocol("UDP")
        self.nC.configure("HOST", self.get("sv_addr"))
        self.nC.configure("PORT", self.get("sv_port"))
        self.nC.initialize()
        
    def purgeNetwork(self):
        '''Destroys the NetCore once and for all.'''
        if self.nC:
            self.nC.clear()
            self.nC.destroy()
            self.nC = None
    
    def setMusic(self, music):
        '''Sets the music track.'''
        launcher = self.eI.getGlobal("launcher")
        
        launcher.sound.playMusic(music)
        self.events.append([None, ["SYSTEM", "MUSIC_PLAY", [music, 0.0]]])
        self.oP("Set music to %s." % music)
        
    def stopMusic(self):
        '''Stops the music track.'''
        launcher = self.eI.getGlobal("launcher")
        
        launcher.sound.stopMusic()
        self.events.append([None, ["SYSTEM", "MUSIC_STOP", None]])
        
    def playSound(self, sound, emitter=None):
        '''Plays a sound.'''
        launcher = self.eI.getGlobal("launcher")
        
        if emitter:
            launcher.sound.playSound(sound, emitter.gameObject)
            self.events.append([None, ["SYSTEM", "SOUND_PLAY", [emitter.GUID, sound]]])
        else:
            launcher.sound.playSound(sound)
            self.events.append([None, ["SYSTEM", "SOUND_PLAY", [None, sound]]])
        
        self.oP("Started sound %s." % sound)
        
    def stopSound(self, handle):
        '''Stops a sound.'''
        launcher = self.eI.getGlobal("launcher")
        
        GUID, sound = launcher.sound.stopSound(handle)
        
        self.events.append(["SYSTEM", "SOUND_STOP", [emitter.GUID, sound]])
        self.oP("Stopped sound %s." % sound)
        
    def stopSoundByGUID(self, GUID, name):
        '''Stops a sound.'''
        launcher = self.eI.getGlobal("launcher")
        
        GUID, sound = launcher.sound.stopSoundByGUID(GUID, name)
        self.oP("Stopped sound %s." % sound)
        
        self.events.append(["SYSTEM", "SOUND_STOP", [emitter.GUID, sound]])
        self.oP("Stopped sound %s." % sound)
        
    def playDialog(self, sound, emitter=None):
        '''Plays a dialog line.'''
        launcher = self.eI.getGlobal("launcher")
    
        if emitter:
            launcher.sound.playDialog(sound, emitter.gameObject)
            self.events.append([None, ["SYSTEM", "DIALOG_PLAY", [emitter.GUID, sound]]])
        else:
            launcher.sound.playDialog(sound)
            self.events.append([None, ["SYSTEM", "DIALOG_PLAY", [None, sound]]])
            
        self.oP("Started dialog %s." % sound)
        
    def stopDialog(self, handle):
        '''Stops a dialog line.'''
        launcher = self.eI.getGlobal("launcher")
        
        GUID, sound = launcher.sound.stopDialog(handle)
        
        self.events.append(["SYSTEM", "DIALOG_STOP", [emitter.GUID, sound]])
        self.oP("Stopped dialog %s." % sound)
        
    def stopDialogByGUID(self, GUID, name):
        '''Stops a dialog line.'''
        launcher = self.eI.getGlobal("launcher")
        
        GUID, sound = launcher.sound.stopDialogByGUID(GUID, name)
        self.oP("Stopped dialog %s." % sound)
        
        self.events.append(["SYSTEM", "DIALOG_STOP", [emitter.GUID, sound]])
        self.oP("Stopped dialog %s." % sound)
        
    def enableShader(self, index, name, mode):
        '''Enables a shader as a filter for the entire screen.'''
        self.sH.enableShader(index, name, mode)
    
    def disableShader(self, index):
        '''Disables a shader that was filtering the entire screen.'''
        self.sH.disableShader(index)
        
    def updateGame(self, key):
        '''Reacts to changes to the cVars.'''
        if key == "sv_gamemode" and self.get("sv_game"):
            self.setGameMode(self.get("sv_gamemode"))
        elif key == "sv_level" and self.get("sv_game"):
            self.configure("sv_game", 0)
            self.configure("sv_game", 1)
        elif key == "sv_game":
            if self.get("sv_game"):
                self.setGameMode(self.get("sv_gamemode"))
                self.setLevel(self.get("sv_level"))
            else:
                self.endGame()
        elif key == "sv_port" or key == "sv_addr":
            self.updateNetwork()
        elif key == "sv_startscript":
            self.sE.addContext("Server", self)
            self.sE.execute(self.get("sv_startscript"))
            
        elif key in ["sv_background_red", "sv_background_green", "sv_background_blue", "sv_background_alpha"] and not self.get("cl_master"):
            self.eI.setBackgroundColor((self.getBackgroundColor()))
            
        elif key == "sv_netlog":
            if self.get("sv_netlog"):
                self.nC.configure("DEBUG", True)
                self.nC.configure("VERBOSE", True)
            else:
                self.nC.configure("DEBUG", False)
                self.nC.configure("VERBOSE", False)
            
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
                
        elif key == "cl_netping":
            self.nC.pingcount = self.get("cl_netping")
            
    def getEmergencyUpdate(self, cli):
        '''Gets a special update to repair desynced clients.'''
        events = []
        
        for var in self.cvars:
            if not "cl_" == var[:3]:
                events.append([cli, ["SYSTEM", "CVARS", [var, self.cvars[var]]]])
            
        for var in self.netVars:
            events.append([cli, ["SYSTEM", "NETVARS", [var, self.netVars[var]]]])
            
        return events
            
    def setPlayerCamera(self, cli, GUID):
        '''Set a client's current camera.'''
        self.events.append([cli, ["SYSTEM", "SET_CAMERA", GUID]])
        if cli:
            self.oP("Set client %s camera to be %s" % (str(cli.addr), GUID))
        else:
            self.oP("Set all client cameras to be %s" % GUID)
            
    def checkServer(self):
        '''Runs server loops and checks for events.'''
        events = []
        
        #CVar based events
        for key in self.cvars.keys():
            if not key in self.oldcvars or self.cvars[key] != self.oldcvars[key]:
                events.append(["SYSTEM", "CVARS", [key, self.cvars[key]]])
            
        self.oldcvars = self.cvars
        
        if self.gameMode:
            self.gameMode.loop()
        
        #Other game events
        events += self.events
        self.events = []
        
        return events
    
    def sendChatMessage(self, msg, client=None):
        '''Sends a chat message to the client(s).'''
        self.sendEvent([client, ["SYSTEM", "CHAT", msg]])
        self.chatMessages.append(msg)
     
    def sendEvent(self, event):
        '''Sends an event to the client(s).'''
        if (event[1][0] == "PHYSICS" and  not event[1][1] in ["CREATE", "DELETE"]) or event[1] == "KEEPALIVE":
            mode = "FAF"
        else:
            mode = "RT"
        
        #Send global events
        if event[0] == None:
            for cli in self.nC.clients:
                if cli.userProps["confirmed"] or not self.get("sv_password"):
                    cli.send(event[1], mode)
        #Send one user events
        else:
            if event[0].userProps["confirmed"] or not self.get("sv_password"):
                event[0].send(event[1], mode)
    
    def recvEvent(self, cli, event):
        '''Handles an event from a client.'''
        if type(event) == type([]) and len(event) >= 3:
            if event[0] == "INPUT":
                
                if event[1] == "COMMAND" or event[1] == "INTERFACE":
                    if cli.userProps["player"]:
                        cli.userProps["player"].pushCommand(event[2])
                    
            elif event[0] == "SYSTEM":
                
                if event[1] == "PHYSICS":
                    if event[2] == "FORCEUPDATE" and not cli.userProps["synced"]:
                        events = self.pR.getEmergencyUpdate(cli)
                        events += self.getEmergencyUpdate(cli)
                        for event in events:
                            self.sendEvent(event)
                        cli.userProps["synced"] = True
                        
                elif event[1] == "CVARS":
                    if cli.addr[0] == self.get("sv_master"):
                        self.configure(event[2][0], event[2][1])
                        
                elif event[1] == "CHAT" and self.get("sv_chat"):
                    self.chatMessages.append(event[2])
                    self.sendEvent([None, event])
                    
                elif event[1] == "NAME":
                    if cli.userProps["player"]:
                        cli.userProps["player"].username = event[2]
                    cli.userProps["username"] = event[2]
                    
                elif event[1] == "PASSWORD":
                    if event[2] == self.get("sv_password"):
                        cli.userProps["confirmed"] = True
                        
            elif event[0] == "GAME":
                self.gameMode.pushGameEvent([event[1], event[2]])
    
    def openSaveFile(self, name):
        '''Opens the save file.'''
        try:
            self.saveFile = shelve.open(SAVE_PATH+name+SAVE_EXT)
            self.oP("Opened save file %s." % (SAVE_PATH+name+SAVE_EXT))
            return True
        except:
            self.saveFile = None
            self.oP("Failed to open save file %s." % (SAVE_PAT+name+SAVE_EXT))
            return False
        
    def closeSaveFile(self):
        '''Closes the save file.'''
        if self.saveFile != None:
            self.saveFile.close()
            self.oP("Closed the save file.")
            self.saveFile = None
    
    def saveSaveFile(self):
        '''Saves the save file.'''
        if self.saveFile != None:
            self.oP("Saved the save file.")
            self.saveFile.sync()
    
    def saveState(self):
        '''Saves the game state.'''
        self.oP("Saving entity state.")
        self.openSaveFile("save")
        
        if self.saveFile != None:
            data = Sarcophagus()
            
            for ent in self.entities:
                #if ent.name != "avatar":
                self.saveEntity(ent, data)
                
            for cli in self.nC.clients:
                if cli.userProps["player"]:
                    self.savePlayer(cli.userProps["player"], data)
                    
            for player in self.unassignedPlayers:
                self.savePlayer(player, data)
            
            records, playerRecords = data.cleanUp()
            
            try:
                self.saveFile["data"] = data
                self.oP("Saved data to save file.")
            except:
                self.oP("Failed to save data to save file.")
            
            self.saveSaveFile()
        
        self.closeSaveFile()
        
        data.restore(records, playerRecords)
        
        for ent in self.entities:
            #if ent.name != "avatar":
            data.reconstructEntity(ent)
            
        for cli in self.nC.clients:
            if cli.userProps["player"]:
                data.reconstructPlayer(cli.userProps["player"])
                
        for player in self.unassignedPlayers:
            data.reconstructPlayer(player)
    
    def loadState(self):
        '''Loads the game state.'''
        self.oP("Loading entity state.")
        self.openSaveFile("save")
        
        if self.saveFile != None:
            if "data" in self.saveFile.keys():
                container = self.saveFile["data"]
                for entry in container.entities:
                    self.loadEntity(entry)
                for player in container.players:
                    self.loadPlayer(player)
                        
        self.closeSaveFile()
    
    def saveEntity(self, ent, data):
        '''Saves an Entity to the sarcophagus.'''
        objData = self.pR.getObjectData(ent)
        data.deconstructEntity(ent)
        data.addEntity(ent, objData)
        
    def savePlayer(self, player, data):
        '''Saves a Player to the sarcophagus.'''
        data.deconstructPlayer(player)
        data.addPlayer(player)
    
    def loadEntity(self, entry):
        '''Reconstructs an Entity.'''
        ent = entry[0]
        
        ent.reconstructObject(entry[1])
        
        self.oP("Retrieved entity %s from save file." % ent.GUID)
        
        self.entities.append(ent)
        
    def loadPlayer(self, player):
        '''Reconstructs a player.'''
        player.reconstructPlayer(self)
        
        self.oP("Retrieved player %s from save file." % player.username)
        
        self.unassignedPlayers.append(player)
        
    def getOldPlayer(self, name):
        '''Checks for an unassigned player.'''
        for player in self.unassignedPlayers:
            if player.username == name:
                return player
            
    def removeOldPlayer(self, player):
        '''Removes a player from the unassigned list.'''
        self.unassignedPlayers.remove(player)
        
    def disconnectPlayer(self, cli):
        '''Handles the disconnection of a player.'''
        if cli.userProps["player"]:
            cli.userProps["player"].cli = None
            self.unassignedPlayers.append(cli.userProps["player"])
    
    def loop(self):
        '''Does everything basically.'''
        
        #cl = OptiClock()
        
        #Detector Index
        self.updateDetectorIndex()
            
        #cl.clockIn("DetectorIndex")
            
        #KEEP ALIVE
        self.keepAliveTicker += 1
        if self.keepAliveTicker % 600 == 0:
            self.sendEvent([None, "KEEPALIVE"])
        
        #cl.clockIn("KeepAlive")
        
        #RECV THINGS###############################################
        
        for cli in self.nC.clients:
            #Make sure only one client gets through on singleplayer
            if not self.get("sv_singleplayer") or len(self.nC.clients) <= 1:
                #Create a player once the username is collected
                if not cli.userProps["player"] and "username" in cli.userProps:
                    player = self.getOldPlayer(cli.userProps["username"])
                    if player:
                        self.oP("Client's previous avatar found, reassigning.")
                        cli.userProps["player"] = player
                        player.cli = cli
                        player.reLinkPlayer()
                        self.removeOldPlayer(cli.userProps["player"])
                    else:
                        self.oP("Client gets a new avatar.")
                        cli.userProps["player"] = Player(self, cli)
                    cli.disconnectFunc = cli.userProps["player"].destruct
                #If a player has been created
                elif cli.userProps["player"]:
                    cli.userProps["player"].loop()
            
            packet = cli.recv()
            
            if packet:
                payload = packet.getPayload()
                
                try:
                    data = eval(payload)
                except:
                    data = None
                
                if data:
                    self.recvEvent(cli, data)
                    
        #cl.clockIn("RecvLoop")
                    
        #CHANGE THINGS###########################################
        
        #Apply Shaders
        self.sH.loop()
        
        #cl.clockIn("Shaders")
        
        #Localize text
        self.l.loop()
        
        #cl.clockIn("Localization")
            
        #Entities loop
        for ent in self.entities:
            ent.checkPhysics()
            ent.checkAnimation()
            
            if hasattr(ent, "loop"):
                #print(ent)
                ent.loop(self, "server")
                
        #cl.clockIn("Entities")
        
        #Physics Read Loop
        events = self.pR.loop()
        
        #cl.clockIn("Physics")
        
        #Self Read Loop
        
        events += self.checkServer()
                
        #cl.clockIn("GameEvents")
                
        #Gamerules Loop
        if hasattr(self.gameMode, "loop"):
            self.gameMode.loop()
        
        #cl.clockIn("GameMode")
        
        #Level loop
        if self.level and hasattr(self.level, "loop"):
            self.level.loop(self, "server")
        
        #cl.clockIn("Level")
        
        #SEND THINGS###############################################
          
        #Send Events
        for event in events:
            self.sendEvent(event)
            
        #cl.clockIn("SendLoop")
            
        #KILL THINGS###################################################
        kill = self.nC.pullKillQueue()
        
        if kill and self.gameMode:
            kill()
            
        #cl.clockIn("Kill")
        
        self.nC.loop()
        
        #cl.clockIn("Network")