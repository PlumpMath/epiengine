def init(mode):
	server = Entity.eI.getGlobal("server")
	Entity.broken = False

Entity.init = init
    
def loop(master, mode):
	pass
	
Entity.loop = loop

def onCollision(other):
	if "player" in other and not Entity.broken:
		Entity.broken = True
		server = Entity.eI.getGlobal("server")
		server.replaceMesh(Entity, "breakableplankbroken")
	
Entity.onCollision = onCollision

Entity.addDetector(Detector(Entity, "collision", Entity.onCollision, {}))