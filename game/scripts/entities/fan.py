def init(mode):
	if mode == "server":
		Entity.playAction("fan_spin")

Entity.init = init
    
def loop(master, mode):
    pass

Entity.loop = loop