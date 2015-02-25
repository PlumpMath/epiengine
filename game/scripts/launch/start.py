from engineinterface import EngineInterface

eI = EngineInterface()

client = eI.getGlobal("client")

client.configure("cl_showmouse", 1)

client.playVideo("intro")

client.addInterface("TitleScreen")