from tools import d2r

class sandbox():
	def __init__(self, master):
		self.master = master
		
		self.respawnTime = 60*10
		self.loaded = False
		
	def kill(self):
		pass

	def loop(self):
		if not self.loaded:
			self.loaded = True
		
	def pushGameEvent(self, mode, data):
		pass
		
	def initPlayer(self, playerObject):
		if playerObject.master.level.gameObject:
			server = playerObject.master
			
			sP = server.level.gameObject.children["player_spawn"]
			playerObject.entity = server.addEntity("avatar", "", sP.worldPosition, sP.worldOrientation, sP.worldScale)
			camera = server.addEntity("playercamera", "", sP.worldPosition, sP.worldOrientation, sP.worldScale)
			camera.gameObject.setParent(playerObject.entity.gameObject)
			
			camera.gameObject.localPosition = (0, 0.45, 0.5)
			camera.gameObject.localOrientation = (d2r(90),0,0)
			
			playerObject.camera = camera
			server.setPlayerCamera(playerObject.cli, camera.GUID)
			
	def reInitPlayer(self, playerObject):
		server = playerObject.master
		
		playerObject.camera.gameObject.setParent(playerObject.entity.gameObject)
		
		camera.gameObject.localPosition = (0, 0, 0)
		playerObject.camera.gameObject.localOrientation = (d2r(90),0,0)

Server.newGamemode = sandbox