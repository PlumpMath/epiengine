#EpiEngine#

##Preamble##

    Title:      EpiEngine Readme  
    Author: 	Asper Arctos  
    Version: 	1.0  
    Date: 	    24/2/2015

##Introduction##

    EpiEngine is an extension of the blender game engine designed to make it behave more like a typical game engine. It was designed for internal use so that I could abstract myself from the functionalities of things like file loading and networking and focus on game development in a system I fully understood.
    
##Contents##

    Preamble  
    Introduction  
    Contents  
    Getting Started  
    Getting Help  
    Legal  
    Credits  
    
##Setup##

    Currently EpiEngine does not feature any modifications to Blender. For this reason it does not contain a copy of Blender internally. For EpiEngine's launcher application to function you will need to place a copy of Blender inside the engine/blender folder such that engine/blender/blenderplayer.exe is a valid path (or the equivalent for your OS).
    
##Getting started##

    EpiEngine can be opened via the .blend file in the bin directory. This blend file is used to launch the engine and should not be modified. Upon launching this file nothing will happen. This is because EpiEngine needs to know what to do when launched. For this reason a launch file is supplied via the cl_startscript console variable in the engine.ini file. This script will be run and will instruct the engine on what to do once it launches. Using this script you can load menus, levels or whatever else you want from the files. 

##Getting Help##

    Instructions on how to perform most actions in EpiEngine can be found in the EpiEngine manual, inside the docs folder. References to online help will be added later. For viewing the EpiEngine documentation I recommend using Notepad++ or another code editor with word wrap enabled.
    
##Helping##

    I'm not interested in taking on assistance with the project at the current time (you can read more about this in faq.md inside the docs folder). However if you'd like to donate to support or say thank you, you can go here: (http://gadrial.net/epiengine/donate)
    
##Legal##

    See the manual for license details.
    
##Credits##

    The Blender Foundation - Blender & it's documentation.  
    martinsh - Shader examples and SSAO/SSGI shader algorithm. 
    Microsoft - The consolas font provided as a font example.
    Asper Arctos - Almost everything.  
    Asper Aestus - Demo textures.
    Neev - Demo textures.
    Epsilon - Demo music.
    freesfx.co.uk - Demo sounds.