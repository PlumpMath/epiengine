from mathutils import Vector
from tools import d2r, r2d, SwitchPanel, ToggleSwitchPanel, getDistance3D

def destruct():  
	'''This is run when the player disconnects by any means from the server.'''
	Player.master.disconnectPlayer(Player.cli)

Player.destruct = destruct
	
def init():
	'''This is run when the player object is created for the first time and not when they are restored from a save.'''
	Player.look = 90
	
	Player.initGameValues()
	
	Player.master.gameMode.initPlayer(Player)
	
Player.init = init
	
def loop():
	'''This is run for every frame.'''
	Player.switchPanel.loop()
	
	if Player.switchPanel.checkSwitch("forward"):
		Player.move("forward")
	if Player.switchPanel.checkSwitch("backward"):
		Player.move("backward")
	if Player.switchPanel.checkSwitch("left"):
		Player.move("left")
	if Player.switchPanel.checkSwitch("right"):
		Player.move("right")
		
	Player.camera.gameObject.localOrientation = (d2r(Player.look),0,0)
	
Player.loop = loop
	
def pushCommand(command):
	'''This is run when an input command is received from the specific client for this player.''' 
	if Player.master.get("sv_game"):
		if command == "forward":
			Player.switchPanel.tripSwitch("forward")
		elif command == "backward":
			Player.switchPanel.tripSwitch("backward")
		elif command == "left":
			Player.switchPanel.tripSwitch("left")
		elif command == "right":
			Player.switchPanel.tripSwitch("right")
		elif command == "jump":
			Player.jump()
		elif type(command) == type(tuple()):
			Player.look += command[1]
			
			if Player.look <= 0:
				Player.look = 0
			elif Player.look >= 180:
				Player.look = 180
				
			ori = Player.entity.gameObject.localOrientation.to_euler()
			Player.entity.gameObject.localOrientation = (ori[0], ori[1], ori[2]+d2r(command[0]))
	
Player.pushCommand = pushCommand
	
def reInitPlayer():  
	'''Called after the player has been resurrected from a save file, contains custom code to handle recovery from a save.'''  
	Player.master.gameMode.reInitPlayer(Player)
	
Player.reInitPlayer = reInitPlayer
	
def reLinkPlayer():  
	'''Called after the player has reconnected to their old avatar.'''  
	if Player.camera:
		Player.master.setPlayerCamera(Player.cli, Player.camera.GUID)
	
Player.reLinkPlayer = reLinkPlayer

#Specialized commands
def initGameValues():
	Player.switchPanel = SwitchPanel()
	Player.switchPanel.addSwitch("forward", 0.20)
	Player.switchPanel.addSwitch("backward", 0.20)
	Player.switchPanel.addSwitch("left", 0.20)
	Player.switchPanel.addSwitch("right", 0.20)
	
Player.initGameValues = initGameValues

def jump():
	'''Used to make the player jump.'''
	Player.entity.gameObject.applyMovement(Vector((0, 0, 1.5)), 1)
	
Player.jump = jump

def move(direction):
	if direction == "forward":
		Player.entity.gameObject.applyMovement(Vector((0, 0.05, 0)), 1)
	if direction == "backward":
		Player.entity.gameObject.applyMovement(Vector((0, -0.05, 0)), 1)
	if direction == "left":
		Player.entity.gameObject.applyMovement(Vector((-0.05, 0, 0)), 1)
	if direction == "right":
		Player.entity.gameObject.applyMovement(Vector((0.05, 0, 0)), 1)
	
Player.move = move