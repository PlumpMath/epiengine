#Root Path
from sys import path

for i in path:
    if "epiengine\\bin" == i[len(i)-13:] or "epiengine\\com" == i[len(i)-13:] or "epiengine/bin" == i[len(i)-13:] or "epiengine/    com" == i[len(i)-13:]:
        break
   
i = i.replace("\\", "/") 
    
i+="/"

#Paths
ENGINE_PATH = i+"../"
BIN_PATH = i+""
GAME_PATH = ENGINE_PATH+"game/"
SAVE_PATH = ENGINE_PATH+"saves/"
NET_PATH = ENGINE_PATH+"netlogs/"
SCRIPTS_PATH = GAME_PATH+"scripts/"
SOUND_PATH = GAME_PATH+"sounds/"
MUSIC_PATH = GAME_PATH+"music/"
VIDEO_PATH = GAME_PATH+"videos/"
DIALOG_PATH = GAME_PATH+"dialog/"
LOCALIZATION_PATH = GAME_PATH+"localization/"
SHADER_PATH = GAME_PATH+"shaders/"

INPUT_PATH = "input/"
NETSCRIPT_PATH = "network/"
GAMEMODE_PATH = "gamemodes/"

#Locations
LOCATIONS = {
    "UI":GAME_PATH+"ui/",
    "Entity":GAME_PATH+"entities/",
    "Level":GAME_PATH+"levels/",
    "Sound":GAME_PATH+"sounds/",
    "Music":GAME_PATH+"music/",
    "Animation":GAME_PATH+"animations/",
    "Dialog":GAME_PATH+"dialog/",
    "Mesh":GAME_PATH+"meshes/"
}

#Extensions
MAIN_EXT = ".epi"
CONTENT_EXT = ".blend"
SCRIPT_EXT = ".py"
CONFIG_EXT = ".ini"
SOUND_EXT = ".wav"
MUSIC_EXT = ".mp3"
DIALOG_EXT = ".wav"
VIDEO_EXT = ".mp4"
TEXT_EXT = ".txt"
VSHADER_EXT = ".vsh"
FSHADER_EXT = ".fsh"
SAVE_EXT = ".esf"