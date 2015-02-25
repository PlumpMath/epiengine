#EpiEngine Manual#  
  
##<S.01> Preamble##  
  
	Title:      EpiEngine Manual  
	Author: 	Asper Arctos  
	Version: 	1.9
	Date: 	    05/01/2014  
  
##<S.02> Introduction##  
  
	EpiEngine is an extension for the Blender Game Engine designed to make it behave like a “conventional” game engine. It was developed based on my experiences with the Source, Gamebyro and CryEngine systems mostly for internal use. EpiEngine focuses on providing automated loading and network synchronization so that developers can concentrate on development. It also enforces a strict file structure to help combat the file issues I have experienced with other systems in the past. EpiEngine was primarily developed to give me a development environment I could truly understand and because I have a preference for creating things as opposed to reading documentation (think of that what you will). I hope I'll be able to explain the functionality swiftly so you can have a similar comprehension of the engine.  
    
    EpiEngine is in active development, you can find more information on EpiEngine and new downloads here: (http://gadrial.net/epiengine/home)
  
##<S.03> Contents##  

    <S.01> Preamble  
    <S.02> Introduction  
    <S.03> Contents  
	<S.04> EPI File Structure  
	<S.05> BLEND File Structure  
	<S.06> Other Resource Files  
	<S.07> Controls  
	<S.08> Client Side Prediction  
	<S.09> Player Structure  
	<S.10> System Structure  
	<S.11> Preloading  
	<S.12> Entities  
	<S.13> Cameras and Lights  
	<S.14> Singleplayer, Multiplayer and Server Types  
    <S.15> Ending a Game
	<S.16> Lobbies, Gamemodes and Levels  
	<S.17> Network and Disconnection  
	<S.18> NetVars and Game Events  
	<S.19> Receiving Text  
	<S.20> Launch Scripts  
	<S.21> Saving  
	<S.22> Interfaces  
	<S.23> Waypoints  
	<S.24> Playing Videos  
	<S.25> Localization  
	<S.26> Shaders  
    <S.27> Standard Shaders  
	<S.28> Playing Sounds  
	<S.29> Console Variables  
	<S.30> Text Chat  
	<S.31> Server Passwords  
	<S.32> Playing Animations  
	<S.33> Detectors  
	<S.34> Changing Meshes  
    <S.35> The Launcher Application
	<S.36> System Configuration  
	<S.37> API Documentation  
	<S.38> Modifying the Engine  
	<S.39> Modifying Save Files  
	<S.40> Legal and Licensing  
	<S.41> Credits  

##<S.04> EPI File Structure##  

	EpiEngine operates primarily off .epi files. .epi files are python dictionaries in text files that define an asset. They always reside in the top level of their respective directory, for example Entities/example.epi. The exact contents of a .epi file vary from one application to another.  
  
	These are the available parameters for each type of .epi file.  
  
	Animation .epi  
  
		name – the name of the asset, should match the name of the .epi file (without the extension).  
		mode – [play, loop, frame] this decides if the animation will play once, or play until stopped. If set to frame the animation will display the single frame supplied. If frame is selected no start/end arguments are needed.  
		skeleton – if True the animation will be synced over network, should only be set to true for animations using an armature. Other animations are detected by the physics system anyway.  
		start – the frame to start the animation on.  
		end -  the frame to end the animation on.  
		layer – the animation layer this animation plays on, animations on the same layer may conflict if played together.  
		targetChild – if the animation affects a child of the main object for instance a skeleton, the name of the child object should be specified here.  
  
	Entity .epi  
  
		name – the name of the asset, should match the name of the .epi file (without the extension).  
		type – [Object, Light, Camera] used to specify when a special kind of Entity is required.  
		resourcePath – Points to the .blend file that contains the Entity's model (path starts in Entities).  
		scriptPath – Points to the .py file that contains the Entity's code (path starts in Scripts).  
		flags – Contains any properties of the Entity itself the developer wishes to change.  
			physicsTrack – If set to True the object will be synced over the network.  
			animTrack – If set to True the object will be animation synced over the network.  
		properties – Properties are attributes of the actual physics object created from your .blend file. This can be used for collision detection properties.  
  
	Level .epi  
  
		name – the name of the asset, should match the name of the .epi file (without the extension).  
		type – Always Object for levels.  
		resourcePath – Points to the .blend file that contains the Level's model (path starts in Levels).  
		scriptPath – Points to the .py file that contains the Level's code (path starts in Scripts).  
		properties – Properties are attributes of the actual physics object created from your .blend file. This can be used for collision detection properties.  
		sky – Sky is a level specific variable, it contains three sub variables r,g,b that control the color of the background when this level is loaded.  
  
	Mesh .epi  
  
		name – the name of the asset, should match the name of the .epi file (without the extension).  
		resourcePath – Points to the .blend file that contains the mesh (path starts in Meshes).  
  
	Sound .epi (This includes music, dialog and sound)  
  
		name – the name of the asset, should match the name of the .epi file (without the extension).  
		resources – the names of any sound files used, if multiple a random one will be selected each time. These can be paths. (Path starts in the relevant folder).  
		3D – If True the sound will be affected by distance from the emitter.  
		loop – The sound will play continuously until stopped by a script.  
		volume – The level of the sound.  
  
	UI .epi  
  
		name – the name of the asset, should match the name of the .epi file (without the extension).  
		type – Always Object for UIs.  
		resourcePath – Points to the .blend file that contains the Entity's model (path starts in Entities).  
		scriptPath – Points to the .py file that contains the Entity's code (path starts in Scripts).  

##<S.05> BLEND File Structure##  
  
	.blend files are used to provide a display and physics mesh to Entities and Levels. They are also used to store meshes for exchange mid game and animations that can be played on objects. .blend files must be set up in a particular way in order to be read correctly by the engine.  
  
	1: Everything in the file should be in layer 2.  
	2: When the file is saved, the active layer should be only layer 1.  
	3: The actual asset should be named the same thing as your entity.  
	4: Anything meant to be imported alongside the asset has to be parented to it. Several layers of parents is okay.  
  
	Recommended usage:  
  
	The recommended usage of .blend files in EpiEngine is to contain your meshes, their materials and textures, text objects, any armatures and animations associated with them all within one .blend file per asset. It is not recommended to assign properties to objects inside the .blend file, this should be done through the .epi file unless you require very specific property assignment. Additionally it is strongly advised not to use any logic bricks or scripts at all in the .blend file. It complicates matters significantly and is strongly against the EpiEngine style.  
  
	Text  
  
	There is an exception to the properties rule regarding Text objects. Text objects designed to be operable by scripts should be set up as follows. First a Text Game Property should be added to allow for the editing of the text in real time. Secondly if the text should be localized by the localization system another property should be added, this property should be called “localized” and the value inside should be the key for the localized string. Additionally the default text of the object should also read this string.  
  
	Shaders  
  
	If a special shader should be assigned to the object a property called “shader” should be added containing the name of the shader to be loaded. This should match the extensionless name of the shader files inside the Shaders folder. Never ever add a property for any reason called shaderLoaded as this is a special engine flag.  
  
	Technical explanation:  
  
	It's not necessary to read this to use the engine, but to have a full understanding of how it works it is recommended. .blend files are imported in their entirety into the engine when an asset is loaded. The game takes place on layer 1 and anything on layer 1 will appear in the scene as soon as the file is loaded. Additionally, anything on the active layer of the resource file will be loaded in, hence when the file is saved the active layer must be the empty layer 1. Once the blend has been loaded the engine uses the name it got from the .epi file to try to load the new object, hence the .epi file and the object in the .blend must have the same name. This is the only object that is created from the file so everything must be parented to it as it's children are also created.  
  
	The shaderLoaded property is created when the shader has been applied to inform the engine not to do it multiple times and adding it yourself will prevent the shader system from operating as intended.  
  
##<S.06> Other Resource Files##  
  
	.mp3 - .mp3 files are used to store music.  
  
	.wav - .wav files are used to store sounds and dialog.  
  
	.fsh - .fsh files are Fragment shaders written in GLSL.   
  
	.vsh - .vsh files are Vertex shaders written in GLSL.  
  
	.py - .py files are Python script files.  
  
	.mp4 – The recommended video format, other video formats may not be supported  
  
	.txt - .txt files are used for localization definitions and the engine descriptor file  
  
	.ini - .ini files are used for control and Cvar configuration files.  
  
##<S.07> Controls##  
  
	The control system in EpiEngine is a linear sequence of systems that transfer a command from the client to the server. We will go through the system relevant to development in order.  
  
	1: controls.ini  
	At the root of the Game folder is controls.ini. This file contains the pairings of keyboard keys and functions that handle their signals. The .ini file has one section [CONTROLS]. Inside this section are pairs of functionname = KEY. functionname refers to the name of the function called by that key in the next step while KEY refers to the keyboard key that triggers the function.  
  
	Keys:  
  
		LEFTMOUSE  
		MIDDLEMOUSE  
		RIGHTMOUSE   
		WHEELUPMOUSE   
		WHEELDOWNMOUSE   
		MOUSEX   
		MOUSEY  
		AKEY   
  
		BKEY   
		CKEY   
		DKEY   
		EKEY   
		FKEY   
		GKEY   
		HKEY   
		IKEY   
		JKEY   
		KKEY   
		LKEY   
		MKEY   
		NKEY   
		OKEY   
		PKEY   
		QKEY   
		RKEY   
		SKEY   
		TKEY   
		UKEY   
		VKEY   
		WKEY   
		XKEY   
		YKEY   
		ZKEY  
		ZEROKEY   
  
		ONEKEY   
		TWOKEY   
		THREEKEY   
		FOURKEY   
		FIVEKEY   
		SIXKEY   
		SEVENKEY   
		EIGHTKEY   
		NINEKEY  
		CAPSLOCKKEY   
  
		LEFTCTRLKEY   
		LEFTALTKEY   
		RIGHTALTKEY   
		RIGHTCTRLKEY   
		RIGHTSHIFTKEY   
		LEFTSHIFTKEY  
		LEFTARROWKEY   
  
		DOWNARROWKEY   
		RIGHTARROWKEY   
		UPARROWKEY  
		PAD0   
  
		PAD1   
		PAD2   
		PAD3   
		PAD4   
		PAD5   
		PAD6   
		PAD7   
		PAD8   
		PAD9   
		PADPERIOD   
		PADSLASHKEY   
		PADASTERKEY   
		PADMINUS   
		PADENTER   
		PADPLUSKEY  
		F1KEY   
  
		F2KEY   
		F3KEY   
		F4KEY   
		F5KEY   
		F6KEY   
		F7KEY   
		F8KEY   
		F9KEY   
		F10KEY   
		F11KEY   
		F12KEY   
		F13KEY   
		F14KEY   
		F15KEY   
		F16KEY   
		F17KEY   
		F18KEY   
		F19KEY  
		ACCENTGRAVEKEY   
  
		BACKSLASHKEY   
		BACKSPACEKEY   
		COMMAKEY   
		DELKEY   
		ENDKEY   
		EQUALKEY   
		ESCKEY   
		HOMEKEY   
		INSERTKEY   
		LEFTBRACKETKEY   
		LINEFEEDKEY   
		MINUSKEY   
		PAGEDOWNKEY   
		PAGEUPKEY   
		PAUSEKEY   
		PERIODKEY   
		QUOTEKEY   
		RIGHTBRACKETKEY   
		ENTERKEY   
		SEMICOLONKEY   
		SLASHKEY   
		SPACEKEY   
		TABKEY  
  
	2: input.py  
	Inside Game/Scripts/Input is input.py. In this file are stored the reaction functions for each of the keys you define in controls.ini. These need to have the same names you defined in the .ini file. The correct format for these functions is as follows. The functions should consist of a Python function sharing the name of the command in the .ini that takes one argument called state. This function should then be assigned to a variable on the global object Input of the same name.  
	  
	Example:  
	  
		def fire(state):  
			pass#Do something here  
			  
		Input.fire = fire  
		  
	Inside this function you can design the code to do whatever you want, here we'll cover the most common operation, sending a command to the server. the state argument can be one of the following values: "ACTIVATE", "DEACTIVATE", "ACTIVE". ACTIVE means the button is being held, ACTIVATE is sent once when the button is first pressed and DEACTIVATE is sent once when the button is released. Sending to the server can be done simply through the Input.addEvent(name) command. Just supply the name of your event to this function and it will be delivered to the server.  
	  
	Example:  
	  
		def fire(state):  
			if state == "ACTIVATE":  
				Input.addEvent("fire")  
				  
		Input.fire = fire  
		  
	There is one exception to this format. The keys MOUSEX and MOUSEY are both triggered when the mouse is moved. It doesn't matter which one you use, they are both always triggered when the mouse moves. Instead of being supplied with a state, any function attached to these keys will be supplied with a first argument that is the current on screen position of the cursor.  
	  
	3: player.py  
	Various subsystems and network modules transmit your command to the server (which might be a local one in the case of singleplayer games). Once it arrives at the server the name argument that was supplied to Input.addEvent(name) is passed to the pushCommand(name) method of your Player object. The Game/Scripts/input/player.py script defines the custom code of the Player object. The pushCommand function should be set up as follows:  
	  
	Example:  
		  
		def pushCommand(command):  
			pass#Do something here  
			  
		Player.pushCommand = pushCommand  
		  
##<S.08> Client Side Prediction##  
	  
	In order to smooth out network lag, EpiEngine supports client side prediction. Client side prediction is set up in a similar manner to keypress reactions. Inside the file Game/Scripts/Input/csp.py are the CSP reaction functions. These are need to be named the same as the reaction function in the input.py file but with the prefix "csp_" attached. They do not take any arguments and need to be assigned to the Input object the same as the key reactions.  
		  
	Example:  
	  
		def csp_fire():  
			pass  
			  
		Input.csp_fire = csp_fire  
		  
	In the case of mouse look (or any other functions operating on the MOUSEX and MOUSEY keys) a special CSP reaction is used, called "csp_look". Unlike other reactions this one takes one argument, the return value of the original reaction function. The CSP system only works when cl_predict is set to 1.  
	  
	In order to prevent client side prediction from interacting badly with messages from the server, you can disable rotation updates for certain entities using client.addToRotationBlacklist(GUID) where GUID is the GUID of the target Entity. This can be undone via client.removeFromRotationBlacklist(GUID)  
	  
##<S.09> Player Structure##  
  
	The player object is a core component of the EpiEngine system. One is created from the contents of Game/Scripts/Input/player.py for each player. The player runs code specific to that player and holds their game data. There are a number of named functions that need to be created for a Player object inside the player.py file:  
  
	destruct()  
  
		This is run when the player disconnects by any means from the server.  
  
	init()  
  
		This is run when the player object is created for the first time and not when they are restored from a save.  
  
	loop()  
  
		This is run for every frame.  
  
	pushCommand(command)  
  
		This is run when an input command is received from the specific client for this player.  
		  
	reInitPlayer()  
	  
		Called after the player has been resurrected from a save file, contains custom code to handle recovery from a save.  
		  
	reLinkPlayer()  
	  
		Called after the player has reconnected to their old avatar.  
		  
	To define these custom functions for a player, include an entry like this inside Game/Scripts/input/player.py  
	  
		def init():  
			Player.health = 100  
			  
		Player.init = init  
		  
##<S.10> System Structure##  
  
	The EpiEngine consists mainly of three parts, the first part, called the Launcher, is activated when the game engine is started up and loads the other two parts as well as hosting the sound system. The Launcher can launch either a Client object, a Server object or both. The Server and Client objects contain a lot of the useful functions developers need access to to operate the engine. To access any of these from any location in a script, another module called the EngineInterface is used. The EngineInterface is designed to allow access to inbuilt BGE functions adapted for EpiEngine. To access the Client object from inside a script use these commands:  
	  
		from engineinterface import EngineInterface  
		eI = EngineInterface()  
		client = eI.getGlobal("client")  
		  
	Of course you will only have to import and instance the EngineInterface module once. The client, server and launcher can all be accessed in this manner using the keys "client", "server" and "launcher" respectively. If the module cannot be retrieved the function will return None. You can use this to check for the existence of a server on the same machine for instance.   
	  
##<S.11> Preloading##  
  
	The main three items loaded into the engine are .epi files, .mp3/.wav audio files and .blend files. These three resources especially, due to the size of .blend/.wav/.mp3 files and the number of .epi files can produce a drain on the engine's speed, for instance the game will slow when character's fire their weapons for the first time in a session as their projectiles are loaded into the engine for the first time. To combat this problem, there are three special files which can be used to control the preloading system. The preloading system loads items into the engine when it boots that will definitely be used, regularly used weapons, vehicles, characters, etc. should be loaded in this way. This increases the load time at the start of the game (where it is acceptable) and decreases load times during the game (where it is not acceptable). The three files are Game/preload.txt, Game/preload_audio.txt and Game/preload_epi.txt. Inside each is a Python list, simply add the paths of .epi and .blend files (relative to Game/ and without their extensions) and they will be preloaded. The audio preload file contains a Python list of lists, each list contains first the name of the sound's .epi file to preload (this will also preload the sound resources) and the type of sound involved, either "sound", "dialog" or "music". Note that only one piece of music can be preloaded at a time.  
  
##<S.12> Entities##  
	  
	Entities represent all objects that are not directly part of the level in the game. Entities have their physical positions and attributes synced over the network. They can run custom code, play animations and sounds (which are also synced over the network) have waypoints track them and have detectors to react to certain physics situations such as collision.   
	  
	Entities are defined through a .epi file. This .epi file is read and the necessary resources loaded to create the Entity which is then created by the engine. The Entity acts as a wrapper around Blender's KX_GameObject for the most part. The actual gameObject can be found in Entity.gameObject. The game object used is taken from the referenced resource file in the .epi file. There is an important exception to this with regards to cameras and lights that is detailed in the next section.  
	  
	Entities have a number of specially named functions that can be used to extend their functionality:  
	  
	init(mode)  
	  
		This is run when the Entity is created, on both client and server. The mode argument contains either the string "client" or "server" depending on which the code is being executed on.  
		  
	destruct(mode)  
	  
		This is run when the Entity is removed, on both client and server. The mode argument contains either the string "client" or "server" depending on which the code is being executed on.  
		  
	loop(master, mode)  
	  
		This is run every frame, the master argument contains the client/server object and the mode argument contains either the string "client" or "server" depending on which the code is being executed on.  
		  
	To define these custom functions for a player, include an entry like this inside the specified script file named in the .epi file for your Entity:  
	  
		def init():  
			Entity.value = 10  
			  
		Entity.init = init  
	  
##<S.13> Cameras and Lights##  
	  
	Cameras and lights can be imported as entities or parts of entities the same as any other object. This allows you to have different cameras and lights with custom settings. While most if not all settings on cameras can be changed at runtime there are many settings on lights such as the shadow settings that must be set beforehand thus necessitating multiple lights. 
	Lights can be provided in one of three ways.
	
		Entity lights
			A lamp placed by itself in a .blend and used as an entity can be imported. This lamp will have been on layer 2 originally seen as it is an Entity. This means it will affect other entities and linked groups in the level that were originally on layer 2 in their files.
		Level lights
			Lamps can be included directly into the level file on layer 2. These will light up everything in the scene.
		Level Group Lights
			Lamps can also be placed inside linked groups used to build levels. This is not recommended due to their unusual behaviour. These lamps will not light anything unless they have been placed on layer 1 in their original file, in which case they will function as normal. (This is opposed to other linked groups which should usually be placed on layer 2).
	  
##<S.14> Singleplayer, Multiplayer and Server Types##  
	  
	In EpiEngine all games are essentially multiplayer games, all games run on a server and have at least one client connected to that server. Singleplayer games in EpiEngine consist of a client running locally connected to a local server, inside the same instance of the game. Multiplayer games can have this setup plus outside clients, or the server can be running in a completely separate instance as a "dedicated" server.   
	  
	Therefore, the three main configurations are as follows:  
	  
		Singleplayer 				- A local client and server connected together in the same instance, no outside clients.  
		  
		Multiplayer (listen server) - A local client and server connected together in the same instance, with outside clients.  
		  
		Multiplayer (dedicated server) - A server running by itself in a separate instance with clients.  
		  
	Starting each one of these configurations is a different affair and we will run through them one at a time.  
	  
	Singleplayer:  
		  
		To start a singleplayer game (it is presumed you wish to skip the lobby) call this function.  
		  
			client.startGameFast(levelname, gamemodename)  
			  
		The argument levelname is the name of the level to be loaded while gamemodename is the name of the gamemode to be loaded. If you want to launch into lobby mode for some reason use this command:  
		  
			client.startGameFull()  
			  
		You will need to find other means (likely UI buttons and scripts) of setting the level and gamemode and turning the game on.  
	  
	Multiplayer (listen server):  
	  
		client.startGameFull()  
	  
	Multiplayer (dedicated server):  
	  
		To start a dedicated server, set la_dedicated to 1 in engine.ini in the [LAUNCHER] section. If you wish to skip the lobby set la_dedicated_fast to 1. Then use either engine.ini or the script specified in sv_startscript to set your sv_level and sv_gamemode parameters.  
		  
	Multiplayer (remote):  
	  
		Multiplayer (remote) is when you are not hosting the server at all and are instead connecting to a server in a separate instance of the game. This is done using the following calls:  
		  
			client.configure("cl_addr", ip)  
			client.configure("cl_oport", oport)  
			client.configure("cl_iport", iport)  
			client.startGameRemote()  
			  
		The ip variable contains the string IP address of the server you wish to connect to. The oport variable contains the port on the server you wish to connect to and the iport variable contains the port you wish to receive messages on.  
	  
##<S.15> Ending a Game##  
	  
	Ending the game on the client can be performed with one simple call:  
	  
		client.endGame()  
	  
	Ending the game will have different effects depending on which kind of game you are running.  
	  
		Singleplayer  
			Ending the game will destruct the level, gamemode and everything to do with the game instance. You will have to use the inbuilt save features and any others you wish to add if you want to preserve data.  
		Multiplayer (listen server)  
			Ending the game will have the same effect as Singleplayer, except all other clients will also be disconnected.  
		Multiplayer (dedicated server)  
			This call does not apply to dedicated servers as they have no local client.  
		Multiplayer (remote)  
			This call will disconnect you from the server but the remote server will continue to function.  
			  
	The server has a similar function:  
	  
		server.endGame()  
		  
	This function ends the current game state. The level, entities, gamemode, etc. will be removed but the client connections will remain. This is usually used to return to the lobby or change levels.  
	  
	Additionally, quitting the client is done with this call:  
	  
		client.quitGame()  
		  
	Or on the server with the same call:  
	  
		server.quitGame()  
		  
	Calling either of these will completely shut down the engine.  
	  
##<S.16> Lobbies, Gamemodes and Levels##  
  
	The EpiEngine game server has two states, sv_game 1 and sv_game 0. In sv_game 0 the game is in what is known as "lobby" mode. This is used for lobbies and pre game rooms primarily but it can also be used for intermissions between games/missions/levels.  
	  
	When sv_game is set to 0, the level and gamemode aren't loaded and there are no entities.  
	When sv_game is set to 1, the level and gamemode are loaded and there can be entities.  
	  
	The Level is an Entity, that provides the static scenery around the players.   
	It is not recommended to integrate loose physics parts into the Level itself (as they will not undergo network sync) and instead load them later as Entities. Levels are set up in a similar fashion to Entities. It is suggested that to keep your level creation under control you save parts of levels into the Game/Objects folder and then use Blender's linking system to load them into your level as groups for use. Make sure these linked groups are on layer 2 within their own files as though they were entities or issues with lighting may occur (except if they are lights themselves, in which case they should be on layer 1). Consult the section on cameras and lights for more information. The Level to be used is set by the sv_level cVar which contains the string name of the .epi file inside of Game/Levels to load. Keep in mind that when the sv_level cVar is changed sv_game is quickly toggled off and on to cause the game to reload the level, this will delete all entities in the game at the time.  
	  
	Levels have the following specially named custom functions:  
	  
		init(mode)  
		  
			This is run when the Entity is created, on both client and server. The mode argument contains either the string "client" or "server" depending on which the code is being executed on.  
			  
		destruct(mode)  
		  
			This is run when the Entity is removed, on both client and server. The mode argument contains either the string "client" or "server" depending on which the code is being executed on.  
			  
		loop(master, mode)  
		  
			This is run every frame, the master argument contains the client/server object and the mode argument contains either the string "client" or "server" depending on which the code is being executed on.  
			  
	Levels are called Entity for the purpose of assigning functions, therefore the assignment looks like this:  
	  
		def init():  
			pass  
			  
		Entity.init = init  
	  
	The Gamemode is a non-physical object used to handle extra game functions such as declaring victory, scoring and instancing the player's Entity. The gamemode is a good way to handle any server side code that is global and not specific to any one level, entity or player. The Gamemode is selected through the contents of sv_gamemode which contains the string name of a script file inside of Game/Scripts/Gamemodes/. The gamemode only exists when sv_game 1 is set to one and is not saved when the game state is saved to disk.  
	  
	Gamemode code is different from most other custom code files, instead of binding functions to a pre-defined object, Gamemodes contain the entire definition of the object inside the script file. An example Gamemode file looks like this:  
	  
		class singleplayer():  
			def __init__(self, master):  
				self.master = master  
			  
			def kill(self):  
				pass  
			  
			def loop(self):  
				pass  
				  
			def pushGameEvent(self, mode, data):  
				pass  
				  
		Server.newGamemode = singleplayer  
				  
	The Gamemode has some special functions you need to pay attention to. First of all the __init__ function run when the object is created will be supplied with one argument containing the Server object. The loop function is run every frame, the kill function is run when the gamemode is destructed by shutting down the game or changing game mode and the pushGameEvent function takes the mode and data extracted from a game event message. It's important that the class inside the Gamemode script file has the same name as the file it is inside of, i.e. the class singleplayer above should be in singleplayer.py.  
  
##<S.17> Network and Disconnection##  
	  
	EpiEngine's network runs on a protocol implemented on top of UDP called EENP or EpiEngine Network Protocol. This protocol implements a number of reliability functions from TCP onto UDP and crucially provides the option to choose between two different methods of transmission for your packets. Packets can either be sent in RT mode or FAF mode.   
	RT stands for "Reliable Transmission" meaning that this packet will get there eventually, even if it has to be retransmitted, an acknowledgement is required for the packet to be considered sent. RT mode is used for things like text chat messages, level changes, other information that absolutely cannot be lost or a massive desync will occur.   
	FAF stands for "Fire And Forget" this means the packet will be sent and then ignored, no acknowledgement is required and the packet does not necessarily reach it's destination. This is used for physics and animation information which will be quickly made up for by the next packet and is too time dependent to bother retransmitting.  
	  
	Keep in mind there is an upper limit set on packet size by the NetCore.BUFFER setting. This can be changed using the following calls:  
	  
		server.nC.configure("BUFFER", 4096)  
	or  
		client.nC.configure("BUFFER", 4096)  
		  
	The default value is 2048 and it is recommended to use a number that it is a power of 2.   
	  
	Disconnection from the network is handled differently on the two different sides of the connection. On the server side the Player object's destruct function is called upon disconnection. On the client side, the script Game/Scripts/Network/disconnect.py is used to define a function that is called when the connection to the server is lost for whatever reason. An example file configuration is as follows:  
	  
		def disconnectReaction():  
			client.endGame()  
  
		Client.disconnectReaction = disconnectReaction  
		  
	On the server side, the Player objects player.destruct function is called when a player disconnects. Inside this function it is important to call Player.master.disconnectPlayer(Player.cli) like so:  
	  
		def destruct():  
			Player.master.disconnectPlayer(Player.cli)  
			  
		Player.destruct = destruct  
	  
##<S.18> NetVars and Game Events##  
	  
	NetVars are variables synced between the server and it's clients. They can be any value at all as long as it can be parsed into bytes for transmission over the network but limiting it to basic types (float, int, str, etc.) is recommended. NetVars come in two varieties, though these varieties are only noticable on the server. There are global NetVars, set using this command:  
	  
		server.configureNetVar(name, value)   
	  
	These are shared with all clients as opposed to personal NetVars, which are set using the following command:   
	  
		client.userProps["player"].configureNetVar(name, value)   
		  
	These are specific to that one client. On the client side NetVars from these two sources appear identical. NetVars are a dictation system, the server sets the NetVars for the clients and the clients cannot directly change them (of course their actions might change them).  
	  
	To send a custom message back to the server from the client use game events. Game events are messages sent from a client to the server which are passed by the server to the current Gamemode. To send one use this command:  
	  
		client.sendGameEvent(mode, data)  
		  
	Where mode is the string title of event and data is anything else needed for the message.  
	  
##<S.19> Receiving Text##  
  
	To create a text field, create a Text object with a Text Game Property called Text and another boolean property called TextEntry. When TextEntry is set to True and the cVar cl_lockcontrols is activated, text typed by the user will be entered into the Text property of that object. It is not currently possible to type special characters that require modifier keys or anything more complex to access.  
  
##<S.20> Launch Scripts##  
	  
	The cVars cl_startscript and sv_startscript can be used to command the client and server modules respectively to perform an action when they first start up. This only occurs when the client/server is first booted and not when transitioning from one level to the next or to/from the lobby. Client startup scripts are typically used to instance a main menu, while server ones can be used to load special features or configuration files.  
	  
##<S.21> Saving##  
  
	The EpiEngine save system is very easy to use but has a number of significant limitations. The save system can be invoked in the following ways. If you wish to save the game state, use this call:  
	  
		server.saveState()  
		  
	To recover the game state, use this call:  
	  
		server.loadState()  
		  
	These calls will automatically save and load from a singular save file called save.esf inside of EpiEngine/Saves.  
	  
	The state of all Entities in the engine is saved to disk when this is done and the state of all Player objects. Any information in the gameMode is discarded. Additionally no information about the level loaded is saved. If you require information on either of these it is suggested to save data manually alongside the automatic save, more information on doing this can be found in the section below on Modifying Save Files. When Entities are loaded, their ScriptExecuter, EngineInterface, detectors and gameObject are all reconstructed (as they are stripped off when the Entity is saved) and then the Entity is placed onto the Entity list. When players are reconstructed their pointer to the server object and ScriptExecuter are replaced and they are then put onto a list called server.unassignedPlayers. Here they sit until such as point as someone connects to the server with the same username as the last player to use the Player object, at which they will be given that Player object instead of a new one.  
	  
	It is important to note that when reviving a save Entities will not overwrite pre-existing entities, so if you load a level which spawns it's own entities such as physics props and then load a save of that level, it is likely that you will end up with two copies of each physics prop.  
  
##<S.22> Interfaces##  
  
	Interfaces are special objects spawned in the Overlay layer that provide menus, lobbies, HUDs and other interface elements. Interfaces are client side features that are not network synced, however the server can instruct the client to draw an interface to the screen. Creating an interface client side is done using the following call:  
	  
		client.addInterface(name)  
		  
	Where name is the name of the .epi file describing the UI element in Game/UI. Interfaces can be removed by name using this command:  
	  
		client.removeInterface(name)  
		  
	Servers can remotely get clients to call these functions using the following events passed to server.sendEvent(event):  
	  
		[client, ["SYSTEM", "INTERFACE_REMOVE", name1]])  
		[client, ["SYSTEM", "INTERFACE_CREATE", name2]])  
		  
	Where client is the client object of the desired client (or None for all clients) and name1/name2 is the name of the .epi file describing the interface. These events are passed to server.sendEvent(event) like so:  
	  
		server.sendEvent([client, ["SYSTEM", "INTERFACE_REMOVE", name1]]))  
		  
	Interfaces are one of the best ways of running custom client side code for the management of things such as waypoints and server commanded video playback.  
	  
	Interfaces support a special system designed to detect clicks on them. If you wish to make a part of the interface clickable give it the property "MouseOver". When this part of the interface is next clicked, the engine will attempt to call Interface.onClick(name). The name supplied to this function is the name of the KX_GameObject that collected the click. It's important to note that if this occurs and a click is collected by an interface the click will not be passed to any normal input handlers that may exist for it.  
	  
	Interfaces can have custom code the same as Entities and Players. These are the special custom functions for Interfaces:  
	  
	init()  
		Run when the interface is first created.  
		  
	loop()  
		Run every frame  
		  
	onClick(name)  
		Run when a part of the interface with the property "MouseOver" is clicked, takes that object's name as an argument.  
	  
##<S.23> Waypoints##  
  
	Waypoints are a special type of interface element. They are client side pointers that track the location of an Entity and position themselves on top of it. This can be used for health bars of characters, markers over squad mates, objective markers, etc. To add a waypoint call the following command on the client:  
	  
		client.addMarker(name, GUID)  
		  
	name refers to the name of the .epi file inside Game/UI describing the waypoint. The GUID refers to the GUID of the entity to be tracked by the waypoint. To remove a waypoint use this command, where GUID refers to the GUID of the tracked entity:  
	  
		client.removeMarker(GUID)  
		  
	Waypoints are not Interface objects and cannot run custom code, to do more complex tasks with them it is recommended you manage them from code running on another Interface.  
  
##<S.24> Playing Videos##  
  
	Playing videos in EpiEngine is done client-side by calling:  
	  
		client.playVideo(name)  
		  
	The name should match the name of the file inside Game/Videos. The server can instruct the client to play or stop videos through the netVar system. The following command can be used to stop a playing video.  
  
		client.stopVideo()  
  
	Only one video can be playing at any one time and the video will be removed automatically when it ends. Audio inside the video file will not be played for technical reasons. If you wish to play audio alongside your video, create a .wav file with the same name as your video in the video folder. The engine will automatically look for audio with the same name as the video file but with a .wav extension to play alongside the video.  
  
##<S.25> Localization##  
  
	The localization system consists of two parts. One of these parts is the dialog localization system. When a dialog line is requested the dialog localization system changes the subtitles and audio to match the specified language of the client.  
	  
		The audio file(s) loaded for a dialog will be the one located in Game/Dialog/languagecode/resourcename. languagecode is the code inside cl_langauge such as "en" for English. The subtitles are acquired by reading Game/Dialog/languagecode/dialogs.txt. Inside this file is a python dictionary formatted as follows:  
		  
		{  
			"key":"subtitletext",  
		}  
		  
		The "key" value is the name of the dialog .epi file.  
  
	The localization system's second part is the translating interface text and other text in the game world. Text that needs translating should be set up as follows: They should have a property called localized containing their pre localization string, this should be set as their default contents and then they should also have a Text Game Property called Text. The pre localization string is used as the key for the dictionary stored in Game/Localization/languagecode/strings.txt formatted in the same fasgion as the dictionary used for subtitles. The extracted string then replaces the key as the displayed text.  
  
##<S.26> Shaders##  
  
	In order to apply a shader to your object in EpiEngine you need to apply a blender game property to the object called shader containing the name of your .fsh and .vsh files. Your shaders should consist of two C code files shadername.vsh and shadername.fsh stored inside of the Game/Shaders folder. It is important you don't give the object a shaderLoaded value or that will prevent the shader system from working properly.  
  
	Example vertex shader:  
  
	   void main()  
	   {  
		  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;  
  
	   }  
	     
	Example fragment shader:  
	     
	   void main()  
	   {     
		  gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);  
	   }  
	     
    If you want to apply a shader to the entire screen in EpiEngine you'll need to use a Python script to call either of the two following methods:  
      
        server.enableShader(0, "shaderName", "fragment")  
        client.enableShader(0, "shaderName", "fragment")  
          
    This will activate the shader on the given pass. The pass indicates the order in which the shader is used. The last argument is used to specify the type of shader, this is simply used for file extensions, fragment shaders are expected to have .fsh extensions and vertex shaders are expected to have .vsh. Note that shaders are not synced over the network so the server function will only effect the server's viewport and vica versa. To disable a shader again use either of these two methods:  
         
        server.disableShader(0)  
        client.disableShader(0)  
         
	As shader programming is a wide topic I cannot cover here I suggest going here to learn more about GLSL shaders.  
	(https://en.wikibooks.org/wiki/GLSL_Programming/Blender)  
      
##<S.27> Standard Shaders##  
  
    EpiEngine comes with a set of shaders designed to improve the visual quality of games made within it. These shaders are generally focused around photo realism but there are a few edge shaders designed for cartoon effects. There's no requirement to use these shaders, they're simply provided for the convenience of anyone who doesn't wish to re-invent the wheel. These shaders are distributed under the same license as the engine as a whole and can be modified if you wish. To modify the operation of the shaders, you can find a set of variables at the top of the file that start with the name of the shader. These are the variables it is recommended to modify in order to control the shader.  
      
    The shaders are:  
      
        Depth of Field  
          
            The depth of field shader blurs background/foreground elements when the camera is looking at another item so as to simulate the limitations of camera focusing.  
          
        Bloom  
          
            The bloom shader causes bright objects to glow and their light to appear to "spill out" into the surrounding area.  
          
        Color Based Edge  
          
            This shader adds outlines to the scene based on sharp changes in color.  
          
        Depth Based Edge  
          
            This shader adds outlines to the scene based on sharp changes in depth.  
          
        High Dynamic Range  
          
            This shader implements a high dynamic range effect.  
          
        Lens Flare  
          
            This shader should not be used as it is experimental. It is supposed to create a lens flare effect around bright light sources.  
          
        Screen Space Ambient Occlusion  
          
            This shader simulates objects blocking the ambient light from reaching surfaces, resulting in the darkening of areas such as corners and enclosed spaces.  
          
        Vignette  
          
            This shader creates a vignette effect causing the edges of the screen to be slightly darker than the centre.  
          
        Volumetric Lighting  
          
            This shader creates a volumetric light scattering effect, simulating light being scattered by mist or fog. This creates the well known "god rays" effect when looking at light sources.

		Radial Blur
		
			Blurs the screen as you move away from the centre.
			
		Night
		
			Attempts to simulate human night vision by making low light areas grey while bright objects retain their color.
			
		Grayscale
		
			Drains all the color from the scene.
			
		Night Vision
		
			Attempts to simulate the effect of night vision goggles.
			
		Distortion
		
			A distortion effect intended for HUD failure.
          
##<S.28> Playing Sounds##  
  
	There are three different kinds of sound in EpiEngine and two subtypes. The three types are:  
	  
		Music - Music is always 2D sound, this refers to the soundtrack of the game layed over the game. Only one musical sound can be playing at once.  
		Dialog - Dialog can be either 2D (such as radio communications) or 3D sound. Dialog has localization built into it and the actual sound file being played can be changed depending on the language setting.  
		Sound - Sound is anything other than dialog and music. It can be interface pings, music playing from in the environment, ambient sound effects, explosions, weapon sounds, etc.  
		  
	The two subtypes are 2D sound and 3D sound.  
	  
		2D sound has no physical location and is played the same wherever you are. This is good for things like the soundtrack, radio dialogue and interface pings.  
		  
		3D sound is played from an object in the world such as a passing plane or the player. It is affected by the doppler effect, distance etc.  
		  
	Playing a sound on the server (which is automatically synced to the client) is done using one of the following commands:  
	  
		server.playSound(sound, emitter=None)  
		server.playDialog(dialog, emitter=None)  
		server.setMusic(music)  
		  
	In each case the sound/dialog/music refers to the name of the .epi file inside of the respective folder in Game/. The emitter argument, where applicable refers to the entity from which the sound eminates, if one is not supplied the sound will be 2D. These same functions exist on the client and can be used to play client only sounds, however client only music will be overriden if the server changes the track.  
	  
	Stopping sounds other than music is done through one of these two functions:  
	  
		server.stopSound(handle)  
		server.stopSoundByGUID(GUID, name)  
		server.stopDialog(handle)  
		server.stopDialogByGUID(GUID, name)  
		  
	The handle used to deactivate the sound through these is returned from the play functions above. Alternatively playback can be cancelled by specifying the GUID of the emitter (if one exists) and the name of the sound as supplied when the sound was started.  
	  
		server.stopMusic()  
		  
	Only one musical track can be played at once so the one to be stopped does not have to be specified.  
  
##<S.29> Console Variables##  
	Console variables, or cVars, are settings for the engine that can be modified via the console or the engine.ini settings file. Console variables exist in two types client and server.   
	Client cVars start with "cl_" and are local to one particular player or the server itself. Changing variables on one client or on the server does not affect the state of these variables on another client or on the server. The server can tell the client to change a cVar but this can be undone by the client.  
	Server cVars start with "sv_". Some Server cVars are local to the server itself while others are synced between all the clients and the server. The ones that are synced can be changed by one client defined as the host by the sv_master cVar.  
	  
	The console can be accessed by pressing your backslash key. It is built into the engine. You can use the console to change cVars on the fly during play. Doing this may have unintended consequences. You can also use the console to view the engine's reports while in the game. The console can be dismissed again with the backslash key.  
	  
	Server cVars:  
	  
		sv_addr						(STR)- The IP address of the server, used to specify if you want to run the server on a particular network.  
		sv_port						(INT)- The port of the server, used to specify which port the server receives messages on.  
		sv_level (C)				(STR)- The name of the map to load into the server, should match the name of the .epi in the Game/Levels folder.  
		sv_game (C)					(INT)- The state of the game, when set to 1 the game is running, when set to 0 the server is in lobby mode. In lobby mode the game mode does not function and the level is not loaded.  
		sv_singleplayer				(INT) - Whether or not more than one client is permitted. Used to seal off singleplayer games.  
		sv_gamemode (C)				(STR)- The name of the gamemode to load into the server, should match the name of the .py file in the in Game/Scripts/Gamemodes folder.  
		sv_startscript				(STR)- The name of the script to run when the server is launched (not the game) should match the name of the .py file in the Game/Scripts/Launch folder.  
		sv_master					(INT)- The IP of the client allowed to change server cVars remotely.  
		sv_dedicated				(INT)- This denotes the state of a server, a dedicated server does not have a client running in the same instance of the program.  
		sv_chat						(INT)- This flag controls if the inbuilt chat system is enabled.  
		sv_background_red (C)		(INT)- The red component of the background color.  
		sv_background_green (C)		(INT)- The green component of the background color.  
		sv_background_blue (C)		(INT)- The blue component of the background color.  
		sv_background_alpha (C)		(INT)- The alpha component of the background color.  
		sv_password					(STR)- The password required to access the server.  
		sv_netlog					(INT)- This flag turns on or off the detailed network logs the engine can record.  
	  
	Client cVars:  
	  
		cl_update					(INT)- This controls if the client will react to information it receives from the server, if 1 it will apply the changes, if 0 it will not. This is set 0 for clients of their own listen servers.  
		cl_synced					(INT)- This is set to 0 before connecting to a server, it is set to 1 once the client has performed the first time set up communications.  
		cl_addr						(STR)- The address of the server to connect to.  
		cl_oport					(INT)- The port of the server to connect to.  
		cl_iport					(INT)- The port to receive messages from the server on, should be different from cl_oport.  
		cl_game						(INT)- The client's game state, similar to sv_game  
		cl_startscript				(STR)- The start script started when the client starts up for the first time, typically used to load the main menu.  
		cl_master					(INT)- This flag denotes if the client is in control of the server it is connected to, as is the case with listen servers.  
		cl_predict					(INT)- This flag enables or disables client side prediction, keep in mind switching this off will undo any rotation blacklist entries you have.  
		cl_smooth					(INT)- Controls whether or not the physics smoothing system is on. This is experimental and it is recommended to keep it switched off.  
		cl_name						(STR)- The username of the client.  
		cl_password					(STR)- The password the client supplies to the server to gain access.  
		cl_camera					(STR)- The GUID of the player's assigned camera as dictated by the server.  
		cl_lockcontrols				(INT)- Whether or not commands other than clicks are accepted. When set to 1 all other commands are ignored, used for menus.  
		cl_showmouse				(INT)- Whether or not the cursor is drawn to the screen.  
		cl_xsens					(INT)- The x axis sensitivity of mouse look.  
		cl_ysens					(INT)- The y axis sensitivity of mouse look.  
		cl_inverted					(INT)- Controls if mouse look (if implemented) is inverted.  
		cl_language (S)				(STR)- Language code, this should match the name of the folders in Game/Dialog/ and Game/Localization/.  
		cl_subtitles (S)			(INT)- Toggles subtitles on and off.  
		cl_width (S)				(INT)- Controls the width of the window in pixels.  
		cl_height (S)				(INT)- Controls the height of the window in pixels.  
		cl_fullscreen (S)			(INT)- Toggles between fullscreen and windowed mode.  
		cl_motionblur (S)			(INT)- Toggles motion blur on and off.  
		cl_motionblur_amount (S)	(INT)- Controls the degree of motion blur.  
		cl_anisotropic (S)			(INT)- Controls the anisotropic filtering level.  
		cl_mipmap (S)				(STR)- Controls the mipmap mode.  
		cl_vsync (S)				(STR)- Toggles vertical sync on and off.  
		cl_musicvolume (S)			(INT)- The volume of music.  
		cl_dialogvolume (S)			(INT)- The volume of dialog.  
		cl_soundvolume (S)			(INT)- The volume of sound effects and general sound.  
		cl_mastervolume (S)			(INT)- The volume of the overall sound.  
		cl_netping		(S)			(INT)- This flag turns on or off the on screen ping counter  
		cl_netlog					(INT)- This flag turns on or off the detailed network logs the engine can record.  
		  
	There are a few extra cVars that can be used to control the behavior of the launcher, the device that starts the server and client.  
	  
	Launcher cVars:  
	  
		la_dedicated 				(INT)- If set to 1 the launcher will boot the server not the client.  
		la_dedicated_fast 			(INT)- If set to 1 and la_dedicated is also set to 1 it will launch the server directly into a game and ignore the lobby.  
		la_output					(INT)- If set to 1 there will be a console output and a log output. Warning, this may cause serious slowdown.  
        
        la_stereoscopy              (STR)- Can take on the following values: anaglyph, sidebyside, syncdoubling, 3dtvtopbottom, interlace, vinterlace, hwpageflip.
        la_dome                     (INT)- If set to 1 fisheye/dome lens will be enabled for the camera.
        la_domeangle                (INT)- Can take on a range of values representing the FOV in degrees.
        la_dometilt                 (INT)- Can take on a range of values representing the title angle in degrees.
        la_domewarpdata             (STR)- Contains the path for an image to use as the warp mapping for dome view.
        la_domemode                 (STR)- Can take on the following values: fisheye, truncatedfront, truncatedback, cubemap, sphericalpanoramic.
        la_antialiasing             (INT)- Can take on any value of 0, 2, 4, 8, 16, this will set the level of anti-aliasing for the renderer.
        la_console                  (INT)- If set to 1 the game will boot with the console open.
        la_debug                    (INT)- If set to 1 the game will boot with the debug flag. I don't know what this does.
        la_fixedtime                (INT)- If set to 1 this will cause video output to be smooth when running on 50Hz. It means the engine runs at 50Hz without frame skipping.
        la_nomipmap                 (INT)- If set to 1 mipmapping is disabled.
        la_fps                      (INT)- If set to 1 the FPS counter is displayed.
        la_properties               (INT)- If set to 1 any properties marked as debug will be displayed.
        la_profiler                 (INT)- If set to 1 the frame rate profiler will be displayed. This provides an overview of what is using up frame time.
		  
    Technical Note:
        All Launcher cVars except for la_dedicated, la_dedicated_fast and la_output are read by the Launcher executable and as a result changing these values after the game has been initialized will not have any effect on the system.
          
	If a cVar is marked with an S that means it's a client variable that also applies to the server, largely display settings so that the server's display can be configured.  
	If a cVar is marked with a C that means it's a server variable that is duplicated on clients, this means the master client can change the variable remotely.  
	(STR) or (INT) denotes if the value is a string, that can contain a series of characters, or an integer that can only contain a whole number.  
	  
	A few setting cVars have specific values they can take on.  
	  
	cl_vsync has to contain one of the following: on, off, adaptive.  
	cl_mipmap has to contain one of the following: none, nearest, linear.  
	  
	cVars can be set through the engine.ini config file. Server cVars have to go into the [SERVER] category, client in the [CLIENT] category and launcher in the [LAUNCHER] category.  
  
##<S.30> Text Chat##  
		  
	The system has in built global text chat that developers can avail of to make development of text chat systems faster. A chat message can be sent from a client like so:  
	  
		client.sendChatMessage(contents)  
		  
	This message will be received on the server and stored in server.chatMessages, it will also be sent back to all the clients where each client stores the message in their own client.chatMessages. It is up to the developer to interpret this these lists and provide a means of calling the command shown above. Additionally, servers can send chat messages to all the clients by calling this:  
	  
		server.sendChatMessage(contents)  
		  
	Or to a particular client like so:  
	  
		server.sendChatMessage(contents, client=clientObject)  
		  
##<S.31> Server Passwords##  
  
	A server can have a password enabled by filling in the sv_password cVar. If this cVar is left blank it will be interpreted as being a public server. Servers with passwords can receive and react to commands from a client that has not supplied the password, but will not send any data to that client until they receive the password. A client will automatically send the current contents of cl_password to a server upon connection. To change the values of these variables from the interface it is recommended you use the following calls from inside an interface.  
	  
		server.configure("sv_password", newPassword)  
		  
	and:  
	  
		client.configure("cl_password", newPassword)  
		  
##<S.32> Playing Animations##  
  
	To play an animation on an object, that object must be an entity. Once you have acquired the entity in a server side script you can call the following command to start an animation:  
	  
		Entity.playAction(name, onEnd=None)  
		  
	The name argument refers to the name of the .epi file in the Game/Animations folder that contains the play data for the animation. The onEnd argument is a function called when the animation ends by running out of frames and is automatically removed. Animations can be stopped by calling:  
	  
		Entity.stopAction(name)  
		  
	And supplying the same name used to start the animation. Animations can be played in the same manner on client side entities but this is not recommended unless you want to create an animation on only one client and may interfere with syncing.  
	  
	There is a special type of animation called a frame animation in EpiEngine. If the animation has it's mode property set to frame the animation can be controlled one frame at a time. This can be used for items like sliding parts where the player can stop them at any time. To do this this call is used:  
	  
		Entity.playActionFrame(name, frame)  
		  
	This will set the animation to display that frame in a stopped state. Simply call this again to change the frame and call Entity.stopAction(name) to remove the action entirely.  
  
##<S.33> Detectors##  
  
	Entities can react to their physical environment through objects called detectors. In order to add a detector one must first create a Detector instance like so:  
	  
		newDetector = Detector(Entity, type, function, {})  
	  
	The type field can be area, radar, sight or collision.   
	Collision is triggered whenever the mesh collides with another. Collision sensors have no special properties. The function pointed to by a collision detector should accept one argument that is the other object (a Blender KX_GameObject) that has been collided with.   
	Area detectors detect objects with a particular property in a particular area. An area sensor setup looks like this:  
	  
		newDetector = Detector(Entity, "near", Entity.enemyFound, {"range":10, "property":"enemy"})  
	  
	The range value decides the range of the detector and the property value decides the blender object property that will trigger the detector. The detector's function should take one argument which is a list of all objects in the range.  
	Radar detectors detect objects with a particular property in a particular cone of vision. They do not take obstructions into account when doing this. They have the following settings, the axis on which they scan, the angle of the cone, the range and the property to detect. A radar detector setup looks like this:  
	  
		newDetector = Detector(Entity, "radar", Entity.enemyFound, {"range":10, "axis":"+y", "angle":45, "property":"enemy"})  
		  
	Sight detectors are the same as radar detectors with one difference, they do an additional check to verify that the ray between the centre of your object and the detected one is clear. This is used to emulate sight so that obstructions such as walls will stop the detector from being triggered. A sight detector setup looks like this:  
	  
		newDetector = Detector(Entity, "sight", Entity.enemyFound, {"range":10, "axis":"+y", "angle":45, "property":"enemy"})  
	  
	Detectors are added to a entity using this method:  
	  
		Entity.addDetector(newDetector)  
		  
	Technical Note:  
	For complicated reasons Detectors are cleaned out of an entity when the entity is saved. Therefore you will need to put them in a particular point in your code so they are reconstructed with the object. Seen as an Entity script file is run every time the Entity is resurrected inserting your detectors at the end of that file can be a good way to ensure they are re-created each time. Actions are also cleared out and will have to be reconstructed.  
	  
	Additionally a detector must detect a property unless it is a collision detector. If a property is not supplied the detector will never trigger, even if the other requirements are met.  
  
##<S.34> Changing meshes##  
  
	If you change the mesh of an Entity through normal means the event will not be synced over the network and the Entity will look different on different machines. To perform a mesh change that will be synced over the network use the following call on the server:  
	  
		server.replaceMesh(entity, meshName)  
    
	entity is the Entity to replace the mesh of and meshName is the name of the .epi file in the Game/Meshes folder that describes the mesh.
	It can also be the name of the mesh itself, for instance when loading a crouch mesh you might have "crouchMesh" as the meshName, which refers to your crouch mesh inside the Meshes folder, however to return to the original mesh of the object (called "standMesh") you can have "standMesh" and even though it's not in your mesh folder the mesh will still change as that mesh was loaded when you first loaded your Entity.

##<S.35> The Launcher Application##

    The Launcher application is a special program written in C++ that starts the blenderplayer and supplies command line arguments to it based on the contents of the engine.ini file. This program's source can be found in the tools folder so you can recompile custom versions of it to suit your needs. The source is provided alongside project files for Visual Studio 2013 which can be used for compiling Windows versions of the application. Currently the launcher is only precompiled for Windows. This may change in the future.
    
##<S.36> System Configuration##  
  
	The system.txt file in the top directory of the engine contains some meta data about the game.  
	This is just used for people to check their game version and is displayed in the console on boot.  
	  
	version -			The version of the engine.  
	targetVersion - 	The version of the Blender Game Engine this is version is intended for.  
	game - 				The name of the game in the engine.  
	gameVersion - 		The version of the game in the engine.  
	date - 				The date this file was written on.  
	  
##<S.37> API Documentation##  
  
	This section details the behavior of the most important functions. Just because a function is listed doesn't mean it should be used. Only use these if you're sure you fully understand what they do.  
  
	Tools  
	  
		float d2r(d)  
			Turns a degree angle into a radian one.  
			  
		float r2d(r)  
			Turns a radian angle into a degree one.  
	  
		float getDistance3D(p1, p2)  
			Gets the distance between two points in 3D.  
			  
		float getDistance2D(p1, p2)  
			Gets the distance between two points in 2D (Z is ignored).  
			  
		isSpecialMethod(name)  
			Checks if a methods name starts and ends with "__" and thus is inbuilt.  
			  
		class LoopCounter()  
			This is a testing device used to count the number of items the network is looping per second.  
			  
			None loop()  
				Run this every cycle of your loop to use the LoopCounter.  
				  
		class OptiClock()  
			This is a testing device that counts the time taken to perform an action, used to optimize the system.  
			  
			None clockIn(name)  
				Run this after each action with the actions name to print the time since the last clockIn (or since the creation of the object in the case of the first clockIn).  
				  
		class Switch()  
			Used in SwitchPanel.  
			  
		class SwitchPanel()  
			Used to provide a delay system and to smooth keyboard inputs into a continous input. A SwitchPanel consists of a set of Switch objects in a SwitchPanel object that can be switched on for a period of time before switching themselves back off. This can be used to create cooldowns, to create gaps between firing, etc. It's also used to smooth keyboard inputs, for instance the forward command may just turn on a switch and then the switch's state will actually cause the motion.  
			  
			switches  
				A list of Switch objects.  
			  
			None loop()  
				Run this in your loop to use the SwitchPanel.  
			None addSwitch(name, cooldown)  
				Adds a switch with the given name and cooldown.  
			None tripSwitch(name)  
				Turns on the switch. If the switch is already on it refreshes the cooldown.  
			bool checkSwitch(name)  
				Gets the state of a given switch.  
		  
		class ToggleSwitch()  
			Used in ToggleSwitchPanel.  
			  
		class ToggleSwitchPanel()  
			Used to provide easy toggleable booleans, A ToggleSwitchPanel is the same as a SwitchPanel except that switches stay on permanently and tripping a switch changes it's state to the opposite one.  
			  
			switches  
				A list of ToggleSwitch objects  
				  
			None addSwitch(name, state)  
				Adds a switch with the given name and initial state.  
			None flipSwitch(name)  
				Changes the switch to the opposite of what it was before.  
			bool checkSwitch(name)  
				Gets the state of a given switch.  
		  
	class GameSide()  
	  
		None pushConsoleCommand(msg)  
			Takes a string command from the graphical console and sends gives it to the client/server cvars.  
			  
		None endLevel()  
			Destroys the current level and all physical objects.  
			  
		None setLevel(name)  
			Loads a level called name into the engine and sets the current level to be that level.  
			  
		Str/Int get(key)  
			Gets a cvar.  
			  
		str/int getNetVar(key)  
			Gets a netVar.  
			  
		None preload(l)  
			Preloads each .epi specified in the list l.  
			  
		ContentReader load(location, name)  
			Loads a .epi file name from location (location is a key for the locations stored in paths.py).  
		  
		bool loadLibrary(location, name, mesh=False)  
			Loads a .blend file name from location (location is a key for the locations stored in paths.py). In mesh mode it will just load the meshes, this is used for getting swappable meshes.  
			  
		tuple getBackgroundColor()  
			Converts the cvars containing background color data into a more easy to use format.  
			  
		Entity addEntity(name, GUID, pos, rot, sca)  
			Creates an entity from a .epi file called name at the specified position, rotation and scale. If a GUID is supplied the object will have that GUID, else one will be randomly generated.  
			  
		None removeEntity(GUID)  
			Removes an entity by it's GUID.  
			  
		None removeAllEntities()  
			Destroys all entities.  
			  
		None removeAllObjects()  
			Removes absolutely everything in the game world.  
			  
		Entity getEntityByGUID(GUID)  
			Gets an Entity by it's GUID  
			  
		None addPropertyTrack()  
			Adds a property to the track list for detectors.  
		  
		None updateDetectorIndex()  
			Updates the global index of items referenced by detectors.  
		  
	class Client(GameSide)  
	  
		mode  
			A string of "client" specifying that this is the client.  
		oP  
			The OutPipe used for printing.  
		eI  
			The EngineInterface used for controlling the engine.  
		vP  
			The VideoPlayer module.  
		sE  
			The ScriptExecuter used to run custom user scripts.  
		iR  
			The InputReceiver, used to receive presses from the keyboard and react accordingly.  
		l  
			The Localizer, this automatically finds and configures objects with localizable text.  
		pA  
			The PhysicsApplicator, this applies physical changes sent over the network.  
		sH  
			The ShaderHandler, this automatically finds and configures objects with shaders enabled.  
		nC  
			The NetCore used to communicate over the network.  
		cvars  
			The console variables of the client object.  
		netVars  
			Values synced over from the server through the netVar system.  
		chatMessages  
			Text chat messages synced from the server through the text chat system.  
		interfaces  
			The Interface objects representing UI elements.  
		entities  
			The Entity objects representing the objects in the game world.  
		level  
			The Entity object representing the static geometry of the world.  
		gameEvents  
			Game type events to be sent to the server.  
		keepAliveTicker  
			A counter to send KEEPALIVE messages to the server at regular intervals.  
		trackedProperties  
			Properties detectors are interested in.  
		  
		None forceUpdateCVars()  
			Forces all the cVars to update by configuring them all.  
			  
		None configure(key, val, fromServer=False, override=False)  
			Changes cVar key to val. fromServer and override are for internal usage.  
			  
		None connectGame()  
			Connects the client to a remote game.  
			  
		None disconnectGame()  
			Disconnects from a remote game.  
			  
		None updateGame(key)  
			Run whenever a cvar is changed.  
			  
		None updateNetwork()  
			Run when the network is changed.  
			  
		None purgeNetwork()  
			Completely destroys the current NetCore configuration.  
			  
		None startGameRemote()  
			Connects to a remote game as well as resetting cVars to the correct values for joining a game.  
			  
		None startGameFull()  
			Starts a listen server locally in sv_game 0 lobby mode.  
			  
		None startGameFast(level, gamemode, singleplayer=True)  
			Supply the name of a level and a gamemode to start a local listen server. The singleplayer argument decides if more clients beyond the first are permitted.  
			  
		None endGame()  
			Disconnects and shuts off the current game instance.  
			  
		None quitGame()  
			Completely closes the game.  
		  
		None setMusic(music)  
			Takes a string argument specifying the name of music resource to play.  
			  
		None stopMusic()  
			Stops the music if any is playing.  
			  
		None playSound(sound, emitter=None)  
			Plays the sound specified by the string argument sound. Optionally plays the sound in 3D emitting from the Entity specified in the emitter argument.  
			  
		None stopSound(handle)  
			Stops a sound from playing using the handle object generated by the sound starting.  
			  
		None stopSoundByGUID(GUID, name)  
			Stops a sound from playing using the name of the sound resource and the GUID of the sound's emitter.  
			  
		None playDialog(sound, emitter=None)  
			Plays the line specified by the string argument sound. Optionally plays the sound in 3D emitting from the Entity specified in the emitter argument.  
			  
		None stopDialog(handle)  
			Stops a line from playing using the handle object generated by the sound starting.  
			  
		None stopDialogByGUID(GUID, name)  
			Stops a dialog line from playing using the name of the sound resource and the GUID of the sound's emitter.  
			  
        None enableShader(index, shaderName, mode)  
            Enables a screen shader, index specifies the pass the shader should run on, shaderName corresponds to the name of the file and mode specifies the type of shader, either "fragment" or "vertex"  
          
        None disableShader(index)  
            Disables a screen shader on the specified pass.  
              
		None playVideo(video)  
			Plays the specified video resource.  
			  
		None stopVideo()  
			Stops any playing video.  
			  
		None replaceMesh(ent, meshName)  
			Replaces the mesh used by the specified Entity with the mesh resource with meshName.  
			  
		None addInterface(name)  
			Adds the interface resource called name to the UI overlay.   
			  
		None removeInterface(name)  
			Removes the interface with the specified name from the UI overlay.  
			  
		None removeAllInterfaces()  
			Removes every interface currently loaded.  
			  
		Interface getInterfaceByName(name)  
			Returns the interface specified by name.  
			  
		None addMarker(name, GUID)  
			Adds a marker resource by the specified name that tracks the Entity with the specified GUID.  
			  
		None removeMarker(GUID)  
			Removes any markers tracking the Entity with the specified GUID.  
			  
		bool inputClick(keyCode, pos)  
			Checks if a click hits any click receives interfaces.  
			  
		function getDisconnectReaction()  
			Loads the custom disconnection reaction from the disk.  
		  
		None addToRotationBlacklist(GUID)  
			Adds an entity to the rotation blacklist, preventing the server from modifying it's rotation.  
		  
		None removeFromRotationBlacklist(GUID)  
			Removes an entity from the rotation blacklist, allowing the server to modify it's rotation.  
		  
		None sendInterfaceEvent(event, aux=None)  
			Sends an input event consisting of a name event and any additional data, aux.  
			  
		None sendChatMessage(msg)  
			Sends a chat message containing the text msg.  
		  
		None sendGameEvent(mode, data)  
			Sends a game event named mode with data data.  
			  
		None sendEvent(event)  
			Sends any event supplied as event. Events usually take the form of a three item list, the general type, one of INPUT/KEEPALIVE/SYSTEM/GAME, a subtype and any extra data.  
			  
		None recvEvent(event)  
			Processes the specified event, intended for use on events coming off the network.  
		  
		None loop()  
			Run every frame, does everything that needs doing on the client.  
		  
	class Server(GameSide)  
	  
		mode  
			A string of "server" specifying that this is the server.  
		oP  
			The OutPipe used for printing.  
		eI  
			The EngineInterface used for controlling the engine.  
		sE  
			The ScriptExecuter used to run custom user scripts.  
		iR  
			The InputReceiver, used to receive presses from the keyboard and react accordingly.  
		l  
			The Localizer, this automatically finds and configures objects with localizable text.  
		pR  
			The PhysicsReader, this collects physics data to be sent over the network.  
		sH  
			The ShaderHandler, this automatically finds and configures objects with shaders enabled.  
		nC  
			The NetCore used to communicate over the network.  
		cvars  
			The console variables of the client object.  
		netVars  
			Values synced over from the server through the netVar system.  
		oldNetVars  
			The previous version of the NetVars, used to detect changes.  
		oldcvars  
			The previous version of the cvars, used to detect changes.  
		gameMode  
			The Gamemode object used by the server.  
		level  
			The Entity object containing the static geometry of the level.  
		unassignedPlayers  
			This contains the player objects of players who have disconnected so they can be reunited later.  
		entities  
			This contains the Entity objects in the game world.  
		events  
			A list of events to be sent over the network.  
		saveFile  
			This contains the save file object when one is open.  
		chatMessages  
			Contains a list of all text chat messages that have passed through the server.  
		keepAliveTicker  
			A counter to send KEEPALIVE messages to the server at regular intervals.  
		trackedProperties  
			Properties detectors are interested in.  
		  
		None forceUpdateCVars()  
			Forces all the cVars to update by configuring them all.  
			  
		None configure(key, val)  
			Changes cVar key to val.  
			  
		None configureNetVar(var, val)  
			Changes the NetVar var to val, also updates clients.  
			  
		None endGame()  
			Destroys the current level, entities and game mode.  
			  
		None endGameMode()  
			Destroys the current gamemode.  
			  
		None replaceMesh(ent, meshName)  
			Replaces the mesh used by the specified Entity with the mesh resource with meshName. Also tells all clients to copy this.  
			  
		None quitGame()  
			Destroys the current game instance and all network connections.  
			  
		None setGameMode(name)  
			Called by the cvar system to load a gamemode.  
			  
		None updateGame(key)  
			Run whenever a cvar is changed.  
			  
		None updateNetwork()  
			Run when the network is changed.  
			  
		None purgeNetwork()  
			Completely destroys the current NetCore configuration.  
			  
		None setMusic(music)  
			Takes a string argument specifying the name of music resource to play. Copied on clients.  
			  
		None stopMusic()  
			Stops the music if any is playing. Copied on clients.  
			  
		None playSound(sound, emitter=None)  
			Plays the sound specified by the string argument sound. Optionally plays the sound in 3D emitting from the Entity specified in the emitter argument. Copied on clients.  
			  
		None stopSound(handle)  
			Stops a sound from playing using the handle object generated by the sound starting. Copied on clients.  
			  
		None stopSoundByGUID(GUID, name)  
			Stops a sound from playing using the name of the sound resource and the GUID of the sound's emitter. Copied on clients.  
			  
		None playDialog(sound, emitter=None)  
			Plays the line specified by the string argument sound. Optionally plays the sound in 3D emitting from the Entity specified in the emitter argument. Copied on clients.  
			  
		None stopDialog(handle)  
			Stops a line from playing using the handle object generated by the sound starting. Copied on clients.  
			  
		None stopDialogByGUID(GUID, name)  
			Stops a dialog line from playing using the name of the sound resource and the GUID of the sound's emitter. Copied on clients.  
			  
        None enableShader(index, shaderName, mode)  
            Enables a screen shader, index specifies the pass the shader should run on, shaderName corresponds to the name of the file and mode specifies the type of shader, either "fragment" or "vertex"  
          
        None disableShader(index)  
            Disables a screen shader on the specified pass.  
              
		list getEmergencyUpdate(cli)  
			Gets all the cVar and netVar data needed to inform a client suffering from bad packet loss or a newly connected client in event format.  
			  
		list checkServer()  
			Gets any server events for sending to the client.  
			  
		None setPlayerCamera(cli, GUID)  
			Sets the camera of the specified Client object to be the camera specified by the GUID. On the client side this will cause the view to change to the new camera.  
			  
		None sendChatMessage(msg)  
			Sends a chat message containing the text msg.  
			  
		None sendEvent(event)  
			Sends any event supplied as event. Events usually take the form of a three item list, the general type, one of PHYSICS/KEEPALIVE/SYSTEM, a subtype and any extra data.  
			  
		None recvEvent(event)  
			Processes the specified event, intended for use on events coming off the network.  
		  
		None loop()  
			Run every frame, does everything that needs doing on the client.  
			  
		bool openSaveFile(name)  
			Opens the specified save file. The save file can be accessed at server.saveFile  
		  
		None closeSaveFile()  
			Closes the save file.  
		  
		None saveSaveFile()  
			Saves changes made to the save file.  
		  
		None saveState()  
			Saves the state of the Players and Entities to the disk.  
		  
		None loadState()  
			Loads the state of the Players and Entities from the disk.  
			  
		None saveEntity(ent, data)  
			Saves the given Entity into the given Sacrophagus.  
			  
		None loadEntity(entry)  
			Restores an Entity from a save file entry.  
			  
		None loadPlayer(player)  
			Restores a Player from a save file entry.  
			  
		Player/None getOldPlayer(name)  
			Checks if a username has had a Player object before.  
			  
		None removeOldPlayer(player)  
			Removes an old player that has been returned to it's user.  
			  
		None disconnectPlayer(cli)  
			Reacts to a clients disconnection by storing their player object in case they return.  
			  
	class Launcher()  
	  
		oP  
			The OutPipe used for printing.  
		s  
			The Server object.  
		c  
			The Client object.  
		sound  
			The SoundEngine object used to play sounds.  
		eI  
			The EngineInterface used to interact with the engine.  
		cR  
			The ConfigReaders used to read the engine.ini file.  
		sE  
			The ScriptExecuter used to run user scripts.  
		  
		None bootSystem()  
			Reads the engine.ini file and uses it to boot a client/server.  
		  
		str/list getSystemInfo()  
			Reads the system information file and returns it's contents.  
		  
		None bootClient()  
			Boots the client.  
		  
		None bootServer()  
			Boots the server.  
		  
		None configureServer(level, gamemode)  
			Configures the server with a level and gamemode.  
		  
		None loop()  
			Run every frame to run the client and/or server loops.  
		  
		None pushConsoleCommand(command)  
			Used to send a console command from the graphical console to the server/client.  
		  
	class EngineInterface()  
	  
		oP  
			The OutPipe used for printing.  
		worldCoreName  
			The name of the Empty object running the engine code.  
		overlayCoreName  
			The name of the Empty object running the overlay code.  
		waypointsCoreName  
			The name of the Emptu object running the waypoint code.  
		mainSceneName  
			The name of the main scene.  
		overlaySceneName  
			The name of the overlay scene.  
		waypointsSceneName  
			The name of the waypoints scene.  
		protected  
			The list of objects in the main scene that should never be deleted.  
		charset  
			The characters used to make GUIDs  
		l  
			The bge.logic module.  
		r  
			The bge.render module.  
		e  
			The bge.events module.  
		  
		None preLoad()  
			This is run when the engine starts. It preloads any .blend files from the preload file.  
		  
		None preLoadEpi()  
			This is run when the engine starts. It preloads any .epi files from the preload file.  
		  
		SCA_PythonMouse getMouse()  
			This returns the current mouse object.  
		  
		SCA_PythonKeyboard getKeyboard()  
			This returns the current keyboard object.  
		  
		various getGlobal()  
			Gets an item in the global dictionary.  
		  
		bool loadLibrary(name, mesh=False)  
			Loads the named .blend into the engine. If mesh is True it will be loaded as a mesh file and only the meshes will be extracted.  
		  
		bool unloadLibrary(name)  
			Unloads the named .blend from the engine. None of the content from this .blend will be usable once this is done.  
		  
		bool addScene(sceneName)  
			Adds the named scene. The scene must be already loaded.  
		  
		bool removeScene(sceneName)  
			Removes a scene from the engine.  
		  
		KX_Scene getMainScene()  
			Returns the main scene.  
		  
		KX_Scene getOverlayScene()  
			Returns the overlay scene.  
		  
		KX_Scene getWaypointsScene()  
			Returns the waypoints scene.  
		  
		None suspendMainScene()  
			Pauses the main scene. DO NOT EVER USE THIS IT DOES NOT WORK.  
		  
		None resumeMainScene()  
			Resumes the main scene. DO NOT EVER USE THIS IT DOES NOT WORK.  
		  
		KX_GameObject/bool createWaypoint(className)  
			Creates a waypoint based on the .epi in named in className.  
		  
		KX_GameObject/bool createObject(className, GUID, pos, rot, sca, scene=None)  
			Creates a KX_GameObject. The .epi is loaded using className, the GUID specifies the forced GUID to use if any is required, the pos, rot and sca arguments specify the position for the object to be created in and the scene variable states which scene this should occur in.  
		  
		KX_GameObject/bool createInterface(className)  
			Creates an Interface from the .epi named in className.  
		  
		None removeInterface(className)  
			Removes the named Interface.  
		  
		bool removeObject(GUID)  
			Removes the KX_GameObject by GUID.  
		  
		None removeAllObjects()  
			Removes all KX_GameObjects from the scene.  
		  
		None setMouseState(visible)  
			Sets the mouse cursor visible or invisible.  
		  
		None quitGame()  
			Exits the engine completely. That's it. That's all it does.  
		  
		KX_GameObject getBaseObjectByClassName(className)  
			Gets a base object (and inactive object in another layer used to create objects) by it's class name (i.e. the name from it's .epi file).  
		  
		KX_GameObject getTerminalParent(obj)  
			Gets the first parent of an obj that doesn't have a parent of it's own.  
		  
		KX_GameObject, KX_Scene getMouseOverObjectScene(pos)  
			Gets the object and scene detected at a particular screen position by a ray from the camera. Else returns none.  
		  
		list getObjectsByClassName(className)  
			Gets all objects from a particular class (i.e. that share the same .epi file).  
		  
		KX_GameObject getObjectByGUID(GUID)  
			Gets an object by the specified GUID.  
	  
		KX_Scene getSceneByName(name)  
			Gets a scene with the given name.  
		  
		None allocateGUIDs()  
			Allocates GUIDs to any objects that require them and are missing them.  
			  
		int getKeyCode(keyString)  
			Converts a keyString into a key code from bge.events.  
		  
		None setGUID(obj)  
			Generates a GUID for the given object.  
	  
		None setCamera(GUID)  
			Sets the current camera to be the Entity with the given GUID.  
	  
		KX_GameObject getWorldCommander(scene=None)  
			Gets the Empty object that runs the engine code.  
			  
		list getAllObjects()  
			Returns all objects in all scenes.  
		  
		list getAllObjectsInactive()  
			Returns all inactive objects (mainly base objects) in all scenes.  
		  
		None setResolution(width, height)  
			Sets the width and height of the render resolution.  
		  
		None setFullscreen(mode)  
			Sets the fullscreen status of the engine.  
		  
		None setMotionBlur(mode, level)  
			Sets the motion blur, the mode is a bool that toggles it on and off while the level is the degree of motion blur from 0.0 to 1.0.  
		  
		None setAnisotropic(level)  
			Sets the anisotropic filtering level, level can be of one the following: 1,2,4,8,16.  
		  
		None setMipmapping(mode)  
			Sets the mipmapping mode, mode can be either none, nearest or linear.  
		  
		None setVSync(mode)  
			Sets the vertical sync mode. Can be either, on, off or adaptive.  
		  
		None setBackgroundColor(color)  
			Sets the background sky color. color should be a four item tuple.  
		  
		list getIndexedObjectsByProperty(prop)  
			Gets all objects with a particular property if those objects have been indexed.  
	  
	class Player()  
	  
		oP  
			The OutPipe used for printing.  
		sE  
			The ScriptExecuter used to load custom code.  
		master  
			The server object.  
		username  
			The player's username.  
		confirmed  
			Set to True if the player has provided the correct password or there is no password.  
		cli  
			The network client object for the player.  
		entity  
			The player's physical entity in the game world.  
		netVars  
			Any netVars that should be synced to just this player.  
		  
		None initVolatileModules()  
			Initializes the players ScriptExecuter. This is done separately so it can be reapplied when the player is loaded from a save file.  
			  
		None installCustomCode()  
			Runs the player script and applies the custom code. This is done separately so it can be reapplied when the player is loaded from a save file.  
			  
		None configureNetVar(key, val)  
			Sets the specified netVar to have the specified value.  
			  
		None reconstructPlayer(server)  
			Re-initializes a player after they have been loaded from a save file.  
			  
	class Detector()  
	  
		master  
			The Entity this detector belongs to.  
		type  
			Either "sight", "area", "radar" or "collision". This specifies the type of detector  
		returnFunction  
			The function to call with the list of collided objects (or single collided object if collision detector).  
		trueDetector  
			If this bool is set to True the Detector will check every single object manually. Not recommended as it causes lag.  
		  
		bool isInCone(obj)  
			Returns true if the supplied objects is in the detectors cone of vision. Works on sight and radar detectors.  
			  
		bool isInSight(obj)  
			Returns true if the supplied object has a clear sight line to the object.  
			  
		bool isZeroLength(vector)  
			Returns true if the vector between two objects is zero length (i.e. the objects are on top of each other).  
			  
		list triggered()  
			Returns the objects that triggered the detector if it has been triggered.  
			  
		None addPropertyTrack(master)  
			Adds a property to the master (server/client) to be tracked.  
			  
	class Action()  
	  
		entity  
			The Entity this action belongs to.  
		action  
			The name of the action to play.  
		layer  
			The layer this action plays on.  
		targetChild  
			The name of the child object to play the action on.  
		obj  
			The object the action is playing on.  
		onEnd  
			A function to be called at the end of the action.  
		type  
			The type of the animation, either, "play", "frame", or "loop".  
		mode  
			The play mode, either KX_ACTION_MODE_PLAY or KX_ACTION_MODE_LOOP.  
		skeleton  
			If True the animation will be network synced as a skeletal animation. Use this for any animations applied to children.  
		start  
			The start frame number.  
		end  
			The end frame number.  
			  
		None play()  
			Plays the action.  
		  
		None stop()  
			Stops the action.  
	  
	class Entity()  
	  
		oP  
			The OutPipe used for printing.  
		eI  
			The EngineInterface used to interact with the engine.  
		sE  
			The ScriptExecuter used to run user scripts.  
		name  
			The name of the Entity.  
		gameObject  
			The KX_GameObject that is the Entity's physical representation.  
		GUID  
			The GUID of the Entity.  
		physicsTrack  
			If True the Entity physics will be synced over the network.  
		animTrack  
			If True the Entity animation will be synced over the network.  
		netVars  
			These values are netVars for an Entity. They will be synced from the server to all clients with the physics data. Keep in mind these values have to be transmitted over the network and should only contain base types, string, float, int, bool, etc.  
		actions  
			List of all the Action objects for this Entity.  
		detectors  
			List of all the Detector objects for this Entity.  
		scriptName  
			The name of the script containing the Entity's custom code.  
		  
		None initVolatileModules()  
			Initializes the ScriptExecuter and EngineInterface, used to restore these after the Entity has been loaded from the save file.  
		  
		None installCustomCode()  
			Installs the custom code functions for the Entity from an external script.  
		  
		None reconstructObject(objData)  
			Reconstructs an object after it has been recovered from a save file.  
		  
		None removeCustomCode()  
			Removes the custom code functions from an Entity so it can be saved.  
		  
		None createObject(objname, sourcename, GUID, pos, rot, sca, props, extra)  
			Creates the Entity's physical object. Normally objname and sourcename are the same, they're the from the .epi file. Occasionally the objname may change in the case of lights and cameras. The GUID can be supplied if the Entity already has one, otherwise one will be autogenerated and applied to both the Entity and the object. The pos, rot and sca argument describe where to spawn the object. The props argument contains any physics properties that should be applied to the Blender object. The extra section contains any extra data used for cameras and lights.  
		  
		None addDetector(detector)  
			Adds a detector supplied as the first argument to the Entity.  
		  
		None kill(side)  
			Destroys the Entity. The side argument specifies which side (server/client) the Entity is on.  
		  
		None processFlags(flags)  
			Run on start up to set the flags from the .epi file.  
		  
		None processProperties(props)  
			Run on start up to set the object's physical properties from the .epi file.  
		  
		ContentReader load(location, name)  
			Loads a .epi file called name. The location is a key for the locations in paths.py.  
		  
		None playAction(name, onEnd=None)  
			Plays the named action, the onEnd argument can contain a function to be run when the animation ends.  
		  
		None stopAction(name)  
			Stops the named action.  
		  
		Action getAction(name)  
			Returns the action with the given name.  
		  
		None playFrameAction(name, frame)  
			Plays a frame action with the specified name at the specified frame.  
		  
		None clearStances()  
			Clears any actions marked stance.  
		  
		None checkPhysics()  
			Run by the server/client at regular intervals to check the state of detectors.  
		  
		None checkAnimation()  
			Run by the server/client at regular intervals to check the state of animation.  
		  
		None configureCamera(extra)  
			Used during the init sequence to configure the Entity if it is a camera.  
		  
		None configureLight(extra)  
			Used during the init sequence to configure the Entity if it is a light.  
		  
		None trackTo(obj)  
			Points the objects +Y axis towards the object specified.  
		  
	class Interface()  
	  
		oP  
			The OutPipe used for printing.  
		eI  
			The EngineInterface used to interact with the engine.  
		sE  
			The ScriptExecuter used to run user scripts.  
		gameObject  
			The physical object of the interface in the overlay.  
			  
		None kill()  
			Removes the interface.  
		  
	class KX_Scene(PyObjectPlus)  
	  
		(http://www.blender.org/documentation/blender_python_api_2_71_6/bge.types.KX_Scene.html)  
	  
	class KX_GameObject(SCA_IObject)  
	  
		(http://www.blender.org/documentation/blender_python_api_2_71_6/bge.types.KX_GameObject.html)  
		  
	class SCA_PythonMouse(PyObjectPlus)  
		  
		(http://www.blender.org/documentation/blender_python_api_2_71_6/bge.types.SCA_PythonMouse.html)  
	  
	class SCA_PythonKeyboard(PyObjectPlus)  
		  
		(http://www.blender.org/documentation/blender_python_api_2_71_6/bge.types.SCA_PythonKeyboard.html)  
	  
	bge.logic  
	  
		(http://www.blender.org/documentation/blender_python_api_2_71_6/bge.logic.html)  
	  
	bge.render  
	  
		(http://www.blender.org/documentation/blender_python_api_2_71_6/bge.render.html)  
	  
	bge.events  
	  
		(http://www.blender.org/documentation/blender_python_api_2_71_6/bge.events.html)  
	  
##<S.38> Modifying the Engine##  
  
	I'm not going to provide a comprehensive guide to modifying the engine as it's inner workings get pretty complicated and difficult to describe without the aid of lengthy diagrams. I will however give an overview of the components and structure of the engine to aid anyone who wants to extend the engine.  
	  
	The engine's starting point is the .blend file Loader.blend. This file is specially constructed to support the engine's functions. Inside the file are the following components:  
	  
		MainScene 	- This is the scene where the "game" happens, this is where your level is loaded and your player spawned.  
			DefaultCamera - This camera sits at the world origin and helps to protect against a CTD bug. Don't delete it. It's okay to reposition it if you wish, keep in mind that if EpiEngine can find no other camera it will automatically fall back to this one.  
				RayTarget - An empty used to target rays coming directly out of the camera.  
			WorldCommander - This object runs our code for us. It also imports the other two scenes when the game is started and configures the paths prior to start.   
		Waypoints	- This layer exists for hovering markers over objects in the MainScene, it contains a camera that will mimic the actions of the camera in the MainScene so the waypoints appear in the correct locations.  
			MirrorCam - copies the exact position, rotation, etc. of the world camera.  
			WaypointsCore - runs the waypoints management script.  
		Overlay 	- This is a special layer which appears as a flat image over the top of the MainScene. It contains your menus, HUDs, it also plays videos, contains the console and displays subtitles.  
			BlackScreen - This object hides the game until all the scenes have initialized and the WorldCommander is ready to start running.  
			Camera - This watches the scene so it can be overlayed onto the MainScene.  
			InputText/Console/OutputText - This is the graphical representation of the console (avert your eyes from how disgusting this is).  
			OverlayCore - This runs the overlay management script.  
			Subtitle - A text object which displays the subtitles  
			VideoPlayer - A plane on which videos are displayed when the engine is asked to play them.  
			  
	Important Note: If you plan to add anything to layer 1 of the MainScene keep in mind you will have to add it to the protected list in engineinterface.py otherwise it will be destroyed when changing levels.  
			  
	The boot order:  
    1: When the Launcher application is launched, it reads the .ini file for information about the command line arguments to supply to the blenderplayer. The blenderplayer is run with these arguments loading up Loader.blend.
	2: startup.py is run, this file appends the system path with the EpiEngine/Engine directory where the code is kept.  
	3: The overlay and waypoint scenes are appended.  
	4: The Launcher is started. The Launcher is the first port of call for the engine boot sequence. The Launcher waits for all the other modules from the other layers to initialize and then runs itself. It initializes the SoundEngine, removes the black screen object, and then boots the system. If the system is test to boot as a dedicated server it will then boot the server, otherwise it will boot the client. In booting the client it reads all the client cVars from engine.ini and feeds them to the client object. It does the respective action when booting the server.  
	5:The server/client then runs it's boot script if one was provided by the relevant cVar, and initializes it's own system and cVars. What happens beyond this point depends on the game in question.  
	  
	Files:  
	  
		Loader Components:  
			  
			console.py 				- This script manages the input and output between the graphical console seen onscreen and the engine code itself.  
			interfaceloader.py 		- Loads interfaces into the engine when commanded to do so by the client.  
			videotexture.py 		- This script draws the video to the video plane.  
			subtitles.py 			- This script writes the subtitles to the screen and removes them.  
			waypointloader.py		- This script synchronizes the Waypoints layer with the MainScene  
			startup.py				- This script is run intiially to add the EpiEngine/Engine path to the system path.  
			  
		Engine Components:  
			  
			client.py				- This module runs the system on the client side of the engine.  
			configreader.py			- This module reads .ini files, it is primarily used to access the engine.ini file when the game is loaded and also for the controls.ini file.  
			contentreader.py		- This module reads .epi files and returns their contents, it is used in various other modules when loading content.  
			engineinterface.py		- This module is instanced by many other modules and used to get streamlined access to BGE functions.  
			entity.py				- This class represents entities, these are all objects in a game other than the level and parts thereof.  
			gameside.py				- This file contains functions shared between the client and server.  
			inputreceiver.py		- This module receives key presses and mouse events and triggers user defined code to react to them.  
			interface.py			- This class is represents interfaces such as HUDs and menus.  
			launcher.py				- This module starts the system, it loads the configs from the engine.ini file and boots the correct module (client/server) with their cVars.  
			level.py				- This class represents the level.  
			localizer.py			- This module automatically searches for unlocalized strings and localizes them to the language specified by the system.  
			network.py				- network.py is an implementation of the EpiEngine Network Protocol and handles all the low level transmission of data over the network.  
			outpipe.py				- The OutPipe module is a module instanced by a lot of other modules to provide them with swift access to the console and log file for printing to.  
			paths.py				- This file contains the default system paths for various resources.  
			physicsapplicator.py	- This module receives changes to the physical attributes of entities and mirrors them on the client.  
			physicsreader.py		- This module collects changes to the physical attributes of entities and for transmission over the network.  
			player.py				- This class is created for each player connected to the server and contains any custom code relating to them.  
			randomtools.py			- A collection of misc tools relating to random numbers.  
			sarcophagus.py			- This class is used to store the data in the save file without breaking pointers.  
			scriptexecuter.py		- This module is instanced by many other modules to run user scripts with.  
			server.py				- This module runs the system on the server side of the engine.  
			shaderhandler.py		- This module automatically searches for shaders to apply and applies them.  
			soundengine.py			- This module plays the sounds from the engine.  
			subtitledrawer.py		- This module acts as an interface between the subtitles.py module and the sound system.  
			tools.py				- A collection of misc tools not relating to random numbers.  
			typinghandler.py		- Converts keypresses into typed text for text entry fields.  
			videoplayer.py			- This module acts as an interface between the client module and the videotexture module running on the actual video plane.  
  
##<S.39> Modifying Save Files##  
  
	EpiEngine save files are written using Python's Pickle object serialization (more specifically using the shelve module). They have one main entry in the file called "data". Inside this entry is a Sacrophagus object that contains the saved data. The sarcophagus' data is stored in Sacrophagus.entities and Sacrophagus.players. Inside these lists are stripped down versions of Entity and Player objects designed to be stored inside the save file. If you extract the sacrophagus, modify the desired values and rewrite it to the "data" attribute of the file, you can edit a save file.   
	  
	If you wish to save additional data to the disk beyond what it is normally saved, simply perform the following operation:  
	  
		server.openSaveFile("save")#The default save name  
		server.saveFile["score"] = 15  
		server.saveSaveFile()  
		server.closeSaveFile()  
		  
	Using this method you can store extra data on the save file such as current level or score. To extract data stored through this method use the following calls:  
	  
		server.openSaveFile("save")  
		customData = server.saveFile["score"]  
		server.closeSaveFile()  
	  
##<S.40> Legal and Licensing##  
    
    Blender and the BlenderPlayer are licensed under the GNU GPL license. The text of this license can be read here: (http://www.gnu.org/copyleft/gpl.html)
    
	Almost everything included with the default download of EpiEngine is released under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license. The exception to this is the contents of the engine/blender/ directory, which are released under the GPL license to be compliant with Blender's GPL license.
	This license can be viewed here for humans:  
	(http://creativecommons.org/licenses/by-nc-sa/4.0/)  
	And here for whoever wants to subject themselves to legalese:  
	(http://creativecommons.org/licenses/by-nc-sa/4.0/legalcode)  
	  
    Any modifications made to Blender shipped with EpiEngine are available under the GPL.
      
	If you wish to use EpiEngine for commercial purposes you must acquire a separate license to this one that establishes compensation. This can be done by contacting me directly. I can be contacted for this purpose at enquires@gadrial.net. (Don't worry, I don't bite).
	  
##<S.41> Credits##  
  
    The Blender Foundation - Blender & it's documentation.
	Asper Arctos - Almost everything.