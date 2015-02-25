from engineinterface import EngineInterface
from tools import *

eI = EngineInterface()

def csp_look(command):
	client = eI.getGlobal("client")
	if client:
		cameraObj = eI.getMainScene().active_camera
		
		if "GUID" in cameraObj:
			camera = client.getEntityByGUID(cameraObj["GUID"])
			
			if camera and camera.name == "playercamera":
			
				player = client.getEntityByGUID(eI.getTerminalParent(cameraObj)["GUID"])
				
				#client.addToRotationBlacklist(player.GUID)
					
Input.csp_look = csp_look