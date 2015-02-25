from random import randrange
from time import time

def oneOfList(l):
    return l[randrange(0, len(l))]

def onceEveryX(x):
    return int(time()) % x == 0
	
def randomOnceEveryX(x):
	return randrange(0, x*60) == 0;

def randomDegree(maxDeg):
    
    maxDeg = int(maxDeg*100)
    
    result = randrange(-maxDeg, maxDeg)
    
    return result/100.0