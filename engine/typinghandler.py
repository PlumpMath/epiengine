from engineinterface import EngineInterface
from outpipe import OutPipe

class TypingHandler():
    def __init__(self, keyboard):
        self.oP = OutPipe("TypingHandler", 0)
        self.eI = EngineInterface()
        self.keyboard = keyboard
        
        self.letters = {
            self.eI.e.AKEY:"a",
            self.eI.e.BKEY:"b",
            self.eI.e.CKEY:"c",
            self.eI.e.DKEY:"d",
            self.eI.e.EKEY:"e",
            self.eI.e.FKEY:"f",
            self.eI.e.GKEY:"g",
            self.eI.e.HKEY:"h",
            self.eI.e.IKEY:"i",
            self.eI.e.JKEY:"j",
            self.eI.e.KKEY:"k",
            self.eI.e.LKEY:"l",
            self.eI.e.MKEY:"m",
            self.eI.e.NKEY:"n",
            self.eI.e.OKEY:"o",
            self.eI.e.PKEY:"p",
            self.eI.e.QKEY:"q",
            self.eI.e.RKEY:"r",
            self.eI.e.SKEY:"s",
            self.eI.e.TKEY:"t",
            self.eI.e.UKEY:"u",
            self.eI.e.VKEY:"v",
            self.eI.e.WKEY:"w",
            self.eI.e.XKEY:"x",
            self.eI.e.YKEY:"y",
            self.eI.e.ZKEY:"z",
        }
        
        self.specials = {
            self.eI.e.ZEROKEY:"0",
            self.eI.e.ONEKEY:"1",
            self.eI.e.TWOKEY:"2",
            self.eI.e.THREEKEY:"3",
            self.eI.e.FOURKEY:"4",
            self.eI.e.FIVEKEY:"5",
            self.eI.e.SIXKEY:"6",
            self.eI.e.SEVENKEY:"7",
            self.eI.e.EIGHTKEY:"8",
            self.eI.e.NINEKEY:"9",
            self.eI.e.ACCENTGRAVEKEY:"`",
            self.eI.e.BACKSLASHKEY:"\\",
            self.eI.e.COMMAKEY:",",
            self.eI.e.EQUALKEY:"=",
            self.eI.e.LEFTBRACKETKEY:"[",
            self.eI.e.MINUSKEY:"-",
            self.eI.e.PERIODKEY:".",
            self.eI.e.QUOTEKEY:"'",
            self.eI.e.RIGHTBRACKETKEY:"]",
            self.eI.e.SEMICOLONKEY:";",
            self.eI.e.SLASHKEY:"/",
            self.eI.e.SPACEKEY:" ",
        }
        
        
        
        self.oP("Initialized.")
        
    def process(self):
        scene = self.eI.getOverlayScene()
        
        for obj in scene.objects:
            if "Text" in obj and "TextEntry" in obj:
                if obj["TextEntry"]:
                    self.enterText(obj)
                    
    def enterText(self, obj):
        oldText = obj["Text"]
        
        newText = oldText
        
        for keycode in self.keyboard.active_events.keys():
            if self.keyboard.active_events[keycode] == self.eI.l.KX_INPUT_JUST_ACTIVATED:
                if keycode in self.letters.keys():
                    letter = self.letters[keycode]
                    if self.caps():
                        letter = letter.upper()
                    newText += letter
                elif keycode in self.specials.keys():
                    letter = self.specials[keycode]
                    
                    newText += letter
                elif keycode == self.eI.e.BACKSPACEKEY:
                    newText = newText[:len(newText)-1]
        
        obj["Text"] = newText
        
    def caps(self):
        return self.eI.e.RIGHTSHIFTKEY in self.keyboard.active_events.keys() or self.eI.e.LEFTSHIFTKEY in self.keyboard.active_events.keys() or self.eI.e.CAPSLOCKKEY in self.keyboard.active_events.keys()