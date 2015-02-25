from time import time, gmtime
from math import sqrt

pi = 3.14159

def d2r(d):
    return d * (pi/180)

def r2d(r):
    return r / (pi/180)

def getDistance3D(p1, p2):
    return abs(sqrt(pow((p1[0]-p2[0]), 2) + pow((p1[1]-p2[1]), 2) + pow((p1[2]-p2[2]), 2)))

def getDistance2D(p1, p2):
    return abs(sqrt(pow((p1[0]-p2[0]), 2) + pow((p1[1]-p2[1]), 2)))

def isSpecialMethod(string):
    if len(string) > 4:
        return "__" == string[:2] and "__" == string[len(string)-2:]
    else:
        return False
    
def getFormattedTime():
    return "%02i:%02i:%02i" % (gmtime()[3], gmtime()[4], gmtime()[5])

class LoopCounter():
    def __init__(self):
        self.loopCount = 0
        self.currentSecond = 0
    
    def loop(self):
        
        if time() - self.currentSecond < 1:
            self.loopCount += 1
        else:
            self.currentSecond = time()
            self.loopCount = 0
            
        print(self.loopCount)

class OptiClock():
    def __init__(self):
        self.time = time()
        
    def clockIn(self, name):
        elapsed = time() - self.time
        self.time = time()
        print("%s: %ims" % (name, int(elapsed*1000)))

class Switch():
    def __init__(self, name, cooldown):
        self.name = name
        self.cooldown = cooldown
        self.state = False
        self.lastTriggered = 0.0

    def get(self):
        return self.state
    
    def set(self):
        self.state = True
        self.lastTriggered = time()
        
    def check(self):
        if self.lastTriggered + self.cooldown <= time():
            self.state = False
            
class SwitchPanel():
    def __init__(self):
        self.switches = {}
        
    def loop(self):
        for key in self.switches.keys():
            self.switches[key].check()
            
    def addSwitch(self, name, cooldown):
        self.switches[name] = Switch(name, cooldown)
        
    def tripSwitch(self, name):
        self.switches[name].set()
        
    def checkSwitch(self, name):
        return self.switches[name].get()
        
class ToggleSwitch():
    def __init__(self, name, state):
        self.name = name
        self.state = state

    def get(self):
        return self.state
    
    def set(self):
        if self.state:
            self.state = False
        else:
            self.state = True
        
class ToggleSwitchPanel():
    def __init__(self):
        self.switches = {}
            
    def addSwitch(self, name, state):
        self.switches[name] = ToggleSwitch(name, state)
        
    def flipSwitch(self, name):
        self.switches[name].set()
        
    def checkSwitch(self, name):
        return self.switches[name].get()