import bge
from outpipe import OutPipe
from time import time

cont = bge.logic.getCurrentController()
own = cont.owner

if not "oP" in own:
    own["oP"] = OutPipe("VideoTexture", 0)
    own["starttime"] = 0.0
    own["executions"] = 0

def playVideo(video):
    materialID = bge.texture.materialID(own, "IMblank.tif")
    own["video"] = bge.texture.Texture(own, materialID)
    try:
        own["video"].source = bge.texture.VideoFFmpeg(video)
        own["video"].source.scale = True
        own["video"].source.play()
        own.setVisible(True)
        own["starttime"] = time()
        own["executions"] = 0
        own["oP"]("Loaded video %s." % video)
    except:
        own["oP"]("Failed to load video %s." % video)

def stopVideo():
    own.setVisible(False)
    if "video" in own:
        bge.logic.globalDict["launcher"].sound.stopVideoAudio()
        own["video"].close()
        del own["video"]
    own["oP"]("Stopped video play back.")
    
def isVideoFinished():
    if "video" in own:
        length = own["video"].source.range[1]
        #if (length + own["starttime"]) <= time() and own["executions"] >= (length * 60):
        if own["executions"] >= (length * 60):
            return True
        else:
            return False

if not "playVideo" in bge.logic.globalDict:
    bge.logic.globalDict["playVideo"] = playVideo
    bge.logic.globalDict["stopVideo"] = stopVideo
    bge.logic.globalDict["isVideoFinished"] = isVideoFinished

if "video" in own:
    own["video"].refresh(True)
    own["executions"] += 1
