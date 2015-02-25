from engineinterface import EngineInterface
from outpipe import OutPipe
from paths import VIDEO_PATH, VIDEO_EXT

class VideoPlayer():
    def __init__(self):
        self.oP = OutPipe("VideoPlayer", 0)
        self.eI = EngineInterface()
        
        self.oP("Initialized.")
        
    def playVideo(self, video):
        playVideo = self.eI.getGlobal("playVideo")
        
        if playVideo:
            self.eI.l.globalDict["launcher"].sound.playVideoAudio(video)
            playVideo(VIDEO_PATH+video+VIDEO_EXT)
            
            self.oP("Requested video playback.")
    
    def stopVideo(self):
        stopVideo = self.eI.getGlobal("stopVideo")
        
        if stopVideo:
            self.eI.l.globalDict["launcher"].sound.stopVideoAudio()
            stopVideo()
            
            self.oP("Stopped video playback.")
    
    def loop(self):
        isVideoFinished = self.eI.getGlobal("isVideoFinished")
        
        if isVideoFinished:
            if isVideoFinished():
                self.oP("Video end detected, stopping video.")
                self.stopVideo()