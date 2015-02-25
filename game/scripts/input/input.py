def leftclick(state):
	if state == "ACTIVATE":
		Input.addEvent("click")
	
Input.leftclick = leftclick
    
def forward(state):
	if state == "ACTIVE" or state == "ACTIVATE":
		Input.addEvent("forward")
		
Input.forward = forward
		
def backward(state):
	if state == "ACTIVE" or state == "ACTIVATE":
		Input.addEvent("backward")
		
Input.backward = backward
		
def left(state):
	if state == "ACTIVE" or state == "ACTIVATE":
		Input.addEvent("left")
		
Input.left = left
		
def right(state):
	if state == "ACTIVE" or state == "ACTIVATE":
		Input.addEvent("right")
		
Input.right = right
		
def jump(state):
	if state == "ACTIVATE":
		Input.addEvent("jump")
		
Input.jump = jump

#MOUSE LOOK
def lookx(pos):
	if not Input.locked:
		Input.mouse.position = (0.5, 0.5)
		
		width = Input.eI.r.getWindowWidth()
		height = Input.eI.r.getWindowHeight()
		
		if width % 2 == 0:
			w = 0.5
		else:
			w = ((width/2)-1)/float(width)
		
		if height % 2 == 0:
			h = 0.5
		else:
			h = ((height/2)-1)/float(height)
			
		standardPos = (w, h)
		
		if abs(pos[0] - standardPos[0]) > 0.001 or abs(pos[1] - standardPos[1]) > 0.001:
			adj = (pos[0]-0.5, pos[1]-0.5)
			
			if Input.inverted:
				adj = (adj[0], adj[1]*-1)
			
			result = (adj[0]*-Input.xsens, adj[1]*-Input.ysens)
			Input.addEvent(result)

Input.lookx = lookx