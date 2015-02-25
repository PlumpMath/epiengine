from engineinterface import EngineInterface
from outpipe import OutPipe
from paths import DIALOG_PATH, TEXT_EXT
from traceback import format_exc

class SubtitleDrawer():
    def __init__(self, master):
        self.oP = OutPipe("SubtitleDrawer", 0)
        self.eI = EngineInterface()
        self.master = master
        
        self.currentSubtitle = None
        
        self.oP("Initialized.")
        
    def drawSubtitle(self, subtitle):
        if self.master.subtitles:
            drawSubtitle = self.eI.getGlobal("drawSubtitle")
            
            subtitlesFile = open(DIALOG_PATH+self.master.language+"/"+"dialogs"+TEXT_EXT, "r")
            
            self.currentSubtitle = subtitle
            
            try:
                subtitles = eval(subtitlesFile.read())
                drawSubtitle(subtitles[subtitle])
            except:
                self.oP("Failed to read subtitles.")
                drawSubtitle(subtitle)
            
            subtitlesFile.close()
            
    def clearSubtitle(self):
        clearSubtitle = self.eI.getGlobal("clearSubtitle")
        
        clearSubtitle()