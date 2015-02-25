import bge

cont = bge.logic.getCurrentController()

own = cont.owner

own.resolution = 10

def drawSubtitle(text):
    own.worldPosition = (0-((len(text)*0.054)/2), own.worldPosition[1], own.worldPosition[2])
    own["Text"] = text
    
def clearSubtitle():
    drawSubtitle("")
    
if not "drawSubtitle" in bge.logic.globalDict:
    bge.logic.globalDict["drawSubtitle"] = drawSubtitle
    bge.logic.globalDict["clearSubtitle"] = clearSubtitle
    own["Text"] = ""
