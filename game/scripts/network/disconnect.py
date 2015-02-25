def disconnectReaction():
	client.removeAllInterfaces()
	client.configure("cl_lockcontrols", 1)
	client.configure("cl_showmouse", 1)
	client.endGame()

Client.disconnectReaction = disconnectReaction