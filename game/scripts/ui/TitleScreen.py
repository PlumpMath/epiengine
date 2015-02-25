def loop():
    pass
    
Interface.loop = loop

def onClick(name):
    if name == "Background":
        client = Interface.eI.getGlobal("client")
        client.removeInterface("TitleScreen")
        client.configure("cl_showmouse", 0)
        client.configure("cl_lockcontrols", 0)
        client.startGameFast("desolation", "sandbox", singleplayer=True)
        
Interface.onClick = onClick