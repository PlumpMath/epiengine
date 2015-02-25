import bge

cont = bge.logic.getCurrentController()

toggle = cont.sensors["Console Toggle Key"]
enter = cont.sensors["Console Enter Key"]

inText = cont.owner
inText.resolution = 10

outText = inText.children["OutputText"]
outText.resolution = 10

if outText["items"] == "":
    outText["items"] = []

    def isCollecting():
        return own["toggleConsole"]

    def pushToLauncher(text):
        if "launcher" in bge.logic.globalDict:
            bge.logic.globalDict["launcher"].pushConsoleCommand(text)

    def printToConsole(text):
        outText["items"].append(text)
        outText["Text"] = "" 
        
        if len(outText["items"]) > 51:
            outText["items"] = outText["items"][1:]
        
        counter = 51 - len(outText["items"])
        
        while counter > 0:
            outText["Text"] += "\n"
            counter -= 1
            
        for i in outText["items"]:
            outText["Text"] += i + "\n"
            
    bge.logic.globalDict["printToConsole"] = printToConsole
    bge.logic.globalDict["isCollecting"] = isCollecting
    bge.logic.globalDict["pushToLauncher"] = pushToLauncher

if enter.getKeyStatus(enter.key) == 1:
    bge.logic.globalDict["printToConsole"](inText["Text"])
    bge.logic.globalDict["pushToLauncher"](inText["Text"])
        
    inText["Text"] = ""

if toggle.getKeyStatus(toggle.key) == 1:
    if inText["toggleConsole"]:
        inText["toggleConsole"] = False
    else:
        inText["toggleConsole"] = True
        
if inText["toggleConsole"]:
    inText.visible = True
    outText.visible = True
    inText.children["Console"].visible = True
else:
    inText.visible = False
    outText.visible = False
    inText.children["Console"].visible = False

