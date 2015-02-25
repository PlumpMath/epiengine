def init(mode):
	server = Entity.eI.getGlobal("server")
	server.replaceMesh(Entity, "testbox2")

Entity.init = init
    
def loop(master, mode):
	pass
	
Entity.loop = loop