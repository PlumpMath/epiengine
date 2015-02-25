from sys import path

for i in path:
    if "EpiEngine" in i:
        break
   
i = i.replace("\\", "/") 
    
i+="/"

GAME_PATH = "../../Game/"