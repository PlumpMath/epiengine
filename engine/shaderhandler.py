from outpipe import OutPipe
from paths import SHADER_PATH, VSHADER_EXT, FSHADER_EXT
from engineinterface import EngineInterface

class ShaderHandler():
    def __init__(self):
        self.oP = OutPipe("ShaderHandler", 0)
        self.eI = EngineInterface()
        
        self.actionQueue = []
        self.actionCooldown = 0
        
        self.oldObjectCount = 0
        
        self.oP("Initialized.")
    
    def enableShader(self, index, name, mode):
        self.actionQueue.append(["enable", index, name, mode])
        
    def disableShader(self, index):
        self.actionQueue.append(["disable", index])
        
    def doShaderAction(self):
        if not self.actionQueue:
            return
            
        action = self.actionQueue.pop()
    
        if action[0] == "enable":
            index = action[1]
            name = action[2]
            mode = action[3]
        
            launcher = self.eI.getGlobal("launcher")
            
            text = ""
            
            if mode == "fragment":
                fsh = open(SHADER_PATH+name+FSHADER_EXT, "r")
                
                text = fsh.read()
                
                fsh.close()
            elif mode == "vertex":
                vsh = open(SHADER_PATH+name+VSHADER_EXT, "r")
                
                text = vsh.read()
                
                vsh.close()
            else:
                return
            
            launcher.enableShader(index, text)
            
        elif action[0] == "disable":
            index = action[1]
            
            launcher = self.eI.getGlobal("launcher")
            
            launcher.disableShader(index)
            
        self.actionCooldown = 120
        
    def loop(self):
        objects = self.eI.getAllObjects()
        
        if self.oldObjectCount != len(objects):
            for obj in objects:
                if "shader" in obj and not "shaderLoaded" in obj:
                    fsh = open(SHADER_PATH+obj["shader"]+FSHADER_EXT, "r")
                    
                    fShaderText = fsh.read()
                    
                    fsh.close()
                    
                    vsh = open(SHADER_PATH+obj["shader"]+VSHADER_EXT, "r")
                    
                    vShaderText = vsh.read()
                    
                    vsh.close()
                    
                    mesh = obj.meshes[0]
                    for mat in mesh.materials:
                        shader = mat.getShader()
                        if shader != None and not shader.isValid():
                            shader.setSource(vShaderText, fShaderText, 1)
                    
                    obj["shaderLoaded"] = True
            self.oldObjectCount = len(objects)
            
        if self.actionCooldown > 0:
            self.actionCooldown -= 1
        else:
            self.doShaderAction()