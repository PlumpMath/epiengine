import aud
from paths import SOUND_PATH, SOUND_EXT, LOCATIONS, MUSIC_EXT, MUSIC_PATH, DIALOG_EXT, DIALOG_PATH, VIDEO_PATH, GAME_PATH, TEXT_EXT
from outpipe import OutPipe
from contentreader import ContentReader
from subtitledrawer import SubtitleDrawer
from randomtools import oneOfList
from engineinterface import EngineInterface

class Sound():
    def __init__(self, engine, name, sound3D, resources):
        self.engine = engine
        self.name = name
        self.resources = resources
        self.Sound3D = sound3D
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def play(self):
        resource = oneOfList(self.resources)
        return self.engine.device.play(resource, False)

class SoundEngine():
    def __init__(self):
        self.oP = OutPipe("SoundEngine", 0)
        self.eI = EngineInterface()
        self.sD = SubtitleDrawer(self)
        
        self.subtitles = 1
        self.language = "en"
        
        self.device = aud.device()
        
        self.sounds = {}
        self.dialogs = {}
        
        self.music = None
        self.musicHandle = None
        
        self.playbacks = []
        self.dialogPlaybacks = []
        
        self.videoAudio = None
        
        self.masterVolume = 1.0
        self.dialogVolume = 1.0
        self.musicVolume = 1.0
        self.soundVolume = 1.0
        
        self.setMasterVolume(1.0)
        
        self.oP("Initialized.")
        
    def preLoadAudio(self):
        self.oP("Preloading audio files...")
        f = open(GAME_PATH+"preload_audio"+TEXT_EXT, "r")
        try:
            data = eval(f.read())
        except:
            pass
        f.close()
        
        for i in data:
            if i[1] == "sound":
                self.loadSound(i[0])
            if i[1] == "music":
                self.loadSound(i[0], music=True)
            if i[1] == "dialog":
                self.loadSound(i[0], dialog=True)
        
    def setMasterVolume(self, volume):
        self.masterVolume = volume*0.1
        self.device.volume = self.masterVolume
        
    def setDialogVolume(self, volume):
        self.dialogVolume = volume*0.1
        for key in self.dialogs.keys():
            self.sounds[key].volume = self.soundVolume
        for i in self.dialogPlaybacks:
            i.volume = self.soundVolume
    
    def setMusicVolume(self, volume):
        self.musicVolume = volume*0.1
        if self.music:
            self.music.volume = self.musicVolume
        if self.musicHandle:
            self.musicHandle.volume = self.musicVolume
            
    def setSoundVolume(self, volume):
        self.soundVolume = volume*0.1
        for key in self.sounds.keys():
            self.sounds[key].volume = self.soundVolume
        for i in self.playbacks:
            i.volume = self.soundVolume
        
    def loop(self):
        self.listener = self.eI.getMainScene().active_camera
        
        self.device.listener_location = self.listener.worldPosition
        self.device.listener_orientation = self.listener.worldOrientation.to_quaternion()
        self.device.listener_velocity = self.listener.getLinearVelocity()
        
        #Update 3D positioning
        for playback in self.playbacks + self.dialogPlaybacks:
            if playback[1].status == True:
                if playback[0]:
                    playback[1].relative = False
                    playback[1].location = playback[0].worldPosition
                    playback[1].orientation = playback[0].worldOrientation.to_quaternion()
                    playback[1].velocity = playback[0].getLinearVelocity()
                else:
                    playback[1].relative = False
                    playback[1].location = self.listener.worldPosition
                    playback[1].orientation = self.listener.worldOrientation.to_quaternion()
                    playback[1].velocity = self.listener.getLinearVelocity()
            #Garbage collection
            else:
                if playback in self.playbacks:
                    self.playbacks.remove(playback)
                break
                
        #Clear subtitles
        for playback in self.dialogPlaybacks:
            if playback[1].status == False:
                if self.sD.currentSubtitle == playback[2]:
                    self.sD.clearSubtitle()
                self.dialogPlaybacks.remove(playback)
                break
        
        #Music positioning and garbage collection
        if self.musicHandle and self.musicHandle.status == True:
            self.musicHandle.relative = False
            self.musicHandle.location = self.listener.worldPosition
            self.musicHandle.orientation = self.listener.worldOrientation.to_quaternion()
            self.musicHandle.velocity = self.listener.getLinearVelocity()
        elif self.musicHandle and self.musicHandle.status == False:
            self.musicHandle = None
        
    def load(self, location, name):
        path = LOCATIONS[location]
        if "Dialog" in path:
            path += self.language + "/"
        cR = ContentReader(path+name)
        return cR
        
    def loadSound(self, sound, music=False, dialog=False):
        if dialog:
            cR = self.load("Dialog", sound)
            EXT = DIALOG_EXT
            PATH = DIALOG_PATH+self.language+"/"
        elif not music:
            cR = self.load("Sound", sound)
            EXT = SOUND_EXT
            PATH = SOUND_PATH
        else:
            cR = self.load("Music", sound)
            EXT = MUSIC_EXT
            PATH = MUSIC_PATH
        
        name = cR.get("name")
        volume = cR.get("volume")
        loop = cR.get("loop")
        sound3D = cR.get("3D")
        resourceNames = cR.get("resources")
        resources = []
        
        for n in resourceNames:
            try:
                factory = aud.Factory.file(PATH+n+EXT)
                
                #Configure specific volumes
                if dialog:
                    factory = factory.volume(self.dialogVolume)
                elif not music:
                    factory = factory.volume(self.soundVolume)
                else:
                    factory = factory.volume(self.musicVolume)            

                if loop:
                    factory = factory.loop(-1)
                resources.append(factory)
                self.oP("Loaded sound resource %s." % (n+EXT))
            except:
                self.oP("Failed to load sound resource %s." % (n+EXT))
        
        self.oP("Loaded sound %s." % sound)
        
        if dialog:
            self.dialogs[name] = Sound(self, name, sound3D, resources)
        elif not music:
            self.sounds[name] = Sound(self, name, sound3D, resources)
        else:
            self.music = Sound(self, name, sound3D, resources)
        
    def playSound(self, sound, emitter=None):
        if not sound in self.sounds:
            self.loadSound(sound)
        
        if sound in self.sounds:
            soundObject = self.sounds[sound]
            handle = soundObject.play()
            self.playbacks.append([emitter, handle, sound])
        
        return handle
            
    def stopSound(self, handle):
        handle.stop()
        for playback in self.playbacks:
            if playback[1] == handle:
                self.playbacks.remove(playback)
                return playback[0].GUID, playback[2]
            
    def playDialog(self, dialog, emitter=None):
        if not dialog in self.dialogs:
            self.loadSound(dialog, dialog=True)
        
        if dialog in self.dialogs:
            dialogObject = self.dialogs[dialog]
            handle = dialogObject.play()
            self.dialogPlaybacks.append([emitter, handle, dialog])
            self.sD.drawSubtitle(dialog)
        
        return handle
    
    def stopDialog(self, handle):
        handle.stop()
        for playback in self.dialogPlaybacks:
            if playback[1] == handle:
                self.dialogPlaybacks.remove(playback)
                return playback[0].GUID, playback[2]
            
    def stopSoundByGUID(self, GUID, name):
        for playback in self.playbacks:
            if playback[0]["GUID"] == GUID and playback[2] == name:
                playback[1].stop()
                self.playbacks.remove(playback)
                
    def playMusic(self, music):
        if self.music:
            self.stopMusic()
        
        self.loadSound(music, music=True)
        self.musicHandle = self.music.play()
        self.oP("Started music %s." % music)
        
    def stopMusic(self):
        if self.music:
            self.music.stop()
            self.music = None
        self.oP("Stopped music.")
        
    def playVideoAudio(self, name):
        resource = aud.Factory.file(VIDEO_PATH+name+SOUND_EXT)
        resource = resource.volume(self.soundVolume)
        try:
            self.videoAudio = self.device.play(resource, False)
        except:
            pass
    
    def stopVideoAudio(self):
        if self.videoAudio:
            self.videoAudio.stop()
            self.videoAudio = None
        self.oP("Stopped video audio.")