def init(mode):
    server = Entity.eI.getGlobal("server")
    if server:
        server.enableShader(0, "vignette", "fragment")
        server.enableShader(1, "bloom", "fragment")
        server.enableShader(2, "dof", "fragment")
        server.enableShader(3, "hdr", "fragment")
        server.enableShader(4, "volumetric", "fragment")
        server.enableShader(5, "ssao", "fragment")
	
        server.setMusic("intro")
        server.playSound("ambience")
    
        sP = Entity.gameObject.children["fan_spawn"]
        server.addEntity("fan", "", sP.worldPosition, sP.worldOrientation, sP.worldScale)
	
        #sP = Entity.gameObject.children["sun_spawn"]
        #server.addEntity("sun", "", sP.worldPosition, sP.worldOrientation, sP.worldScale)
        
        sP = Entity.gameObject.children["barrel_spawn"]
        server.addEntity("barrel", "", sP.worldPosition, sP.worldOrientation, sP.worldScale)
        
        sP = Entity.gameObject.children["plank_spawn_1"]
        server.addEntity("breakableplank", "", sP.worldPosition, sP.worldOrientation, sP.worldScale)
        
        sP = Entity.gameObject.children["plank_spawn_2"]
        server.addEntity("breakableplank", "", sP.worldPosition, sP.worldOrientation, sP.worldScale)
        
        sP = Entity.gameObject.children["plank_spawn_3"]
        server.addEntity("breakableplank", "", sP.worldPosition, sP.worldOrientation, sP.worldScale)

Entity.init = init
    
def loop(master, mode):
    pass

Entity.loop = loop