from configreader import ConfigReader
from outpipe import OutPipe
from scriptexecuter import ScriptExecuter
from engineinterface import EngineInterface
from typinghandler import TypingHandler
from paths import GAME_PATH, SCRIPTS_PATH, INPUT_PATH
import time

class InputReceiver():
    def __init__(self):
        self.oP = OutPipe("InputReceiver", 0)
        self.cR = ConfigReader(GAME_PATH+"controls")
        self.sE = ScriptExecuter()
        self.eI = EngineInterface(objectMode=False)
        self.keyboard = self.eI.getKeyboard()
        self.mouse = self.eI.getMouse()
        self.tH = TypingHandler(self.keyboard)
        self.pairs = {}
        self.responses = {}
        self.oldKeyboard = self.keyboard.events
        self.oldMouse = self.mouse.events
        
        self.sE.addContext("Input", self)
        self.sE.execute(INPUT_PATH+"csp")
        self.sE.execute(INPUT_PATH+"input")
        
        self.keyEvents = []
        
        self.readControls()
        
        self.locked = False
        self.xsens = 50
        self.ysens = 50
        self.inverted = 0
        self.predict = False
        
        self.recent = {}
        
        self.oP("Initialized.")
        
    def addEvent(self, event):
        if not event in self.recent.keys():
            self.keyEvents.append(["INPUT", "COMMAND", event])
            
            if not type(event) == type(tuple()):
                self.recent[event] = time.time()
            
            if self.predict:
                self.callClientSidePrediction(event)
        
    def callClientSidePrediction(self, event):
        if not type(event) == type(tuple()):
            if hasattr(self, "csp_"+event):
                getattr(self, "csp_"+event)()
        else:
            if hasattr(self, "csp_look"):
                getattr(self, "csp_look")(event)
        
    def readControls(self):
        keys = self.cR.getAllOptions("CONTROLS")
        
        for key in keys:
            keyString = self.cR.get("CONTROLS", key)
            keyCode = self.eI.getKeyCode(keyString)
            try:
                self.pairs[keyCode] = getattr(self, key)
                self.oP("Read in key response %s successfully." % key)
            except:
                self.oP("Failed to read in key response %s successfully." % key)
                
    def checkControls(self):
        for keyCode in self.pairs.keys():
            if keyCode in self.keyboard.events and not self.locked:
                if self.keyboard.events[keyCode] == self.eI.l.KX_INPUT_ACTIVE:
                    self.callCommand("KEYBOARD", keyCode)
                elif self.keyboard.events[keyCode] == self.eI.l.KX_INPUT_JUST_ACTIVATED:
                    self.callCommand("KEYBOARD", keyCode)
                elif self.keyboard.events[keyCode] == self.eI.l.KX_INPUT_JUST_RELEASED:
                    self.callCommand("KEYBOARD", keyCode)
                    
            elif keyCode in self.mouse.events:
                if self.mouse.events[keyCode] == self.eI.l.KX_INPUT_ACTIVE:
                    self.callCommand("MOUSE", keyCode)
                elif self.mouse.events[keyCode] == self.eI.l.KX_INPUT_JUST_ACTIVATED:
                    self.callCommand("MOUSE", keyCode)
                elif self.mouse.events[keyCode] == self.eI.l.KX_INPUT_JUST_RELEASED:
                    self.callCommand("MOUSE", keyCode)
                    
        self.oldKeyboard = self.keyboard.events
        self.oldMouse = self.mouse.events
        
        #Handle the "recent" spam blocker
        keys = self.recent.keys()
        for key in keys:
            if abs(self.recent[key] - time.time()) > 0.1:
                del self.recent[key]
                break
            
        if self.locked:
            self.tH.process()
        
    def callCommand(self, mode, keyCode):
        if mode == "KEYBOARD":
            state = self.getState(self.keyboard.events[keyCode], self.oldKeyboard[keyCode])
        elif mode == "MOUSE":
            state = self.getState(self.mouse.events[keyCode], self.oldMouse[keyCode])
        
        consumed = False
        
        if state == "DEACTIVATE" and keyCode in [self.eI.e.LEFTMOUSE, self.eI.e.RIGHTMOUSE]:
            consumed = self.checkInterfaceClick(keyCode, self.mouse.position)
            
        if not consumed and not keyCode in [self.eI.e.MOUSEX, self.eI.e.MOUSEY]:
            self.pairs[keyCode](state)
        elif keyCode in [self.eI.e.MOUSEX, self.eI.e.MOUSEY]:
            pos = self.mouse.position
            self.pairs[keyCode](pos)
        
    def checkInterfaceClick(self, keyCode, pos):
        return self.eI.getGlobal("client").inputClick(keyCode, pos)
        
    def getState(self, newstate, oldstate):
        if newstate == self.eI.l.KX_INPUT_ACTIVE:
            if oldstate == self.eI.l.KX_INPUT_ACTIVE:
                return "ACTIVE"
            elif oldstate == self.eI.l.KX_INPUT_NONE:
                return "ACTIVATE"
            elif oldstate == self.eI.l.KX_INPUT_JUST_ACTIVATED:
                return "ACTIVATE"
            elif oldstate == self.eI.l.KX_INPUT_JUST_RELEASED:
                return "ACTIVATE"
            
        if newstate == self.eI.l.KX_INPUT_NONE:
            if oldstate == self.eI.l.KX_INPUT_ACTIVE:
                return "DEACTIVATE"
            elif oldstate == self.eI.l.KX_INPUT_NONE:
                return "INACTIVE"
            elif oldstate == self.eI.l.KX_INPUT_JUST_ACTIVATED:
                return "DEACTIVATE"
            elif oldstate == self.eI.l.KX_INPUT_JUST_RELEASED:
                return "DEACTIVATE"
            
        if newstate == self.eI.l.KX_INPUT_JUST_ACTIVATED:
            if oldstate == self.eI.l.KX_INPUT_ACTIVE:
                return "ACTIVATE"
            elif oldstate == self.eI.l.KX_INPUT_NONE:
                return "ACTIVATE"
            elif oldstate == self.eI.l.KX_INPUT_JUST_ACTIVATED:
                return "ACTIVATE"
            elif oldstate == self.eI.l.KX_INPUT_JUST_RELEASED:
                return "ACTIVATE"
            
        if newstate == self.eI.l.KX_INPUT_JUST_RELEASED:
            if oldstate == self.eI.l.KX_INPUT_ACTIVE:
                return "DEACTIVATE"
            elif oldstate == self.eI.l.KX_INPUT_NONE:
                return "DEACTIVATE"
            elif oldstate == self.eI.l.KX_INPUT_JUST_ACTIVATED:
                return "DEACTIVATE"
            elif oldstate == self.eI.l.KX_INPUT_JUST_RELEASED:
                return "DEACTIVATE"
    