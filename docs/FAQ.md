#EpiEngine FAQ#  
  
##Preamble##  
  
	Title:      EpiEngine FAQ  
	Author: 	Asper Arctos    
	Version: 	1.1  
	Date: 	    05/01/2014    
  
##Introduction##  
  
    This FAQ will hopefully provide some useful information about EpiEngine and more specifically it's development. I have no idea if I'm actually gonna get asked these questions but they're just the questions I expect people to wonder about this project.  
  
##Q&A##  
  
    Q: Why shouldn't I just use another engine?  
    A: You probably should. If asked, I would say EpiEngine's strengths are in having a fully open source code base, a very simple clean structure and a strong separation between the game, the game engine and the render/physics components.  
      
    Q: Why did you make this?  
    A: I've tried working with a couple other engines before and I found they just never reached my standards in a few different areas. I felt I could never get a proper grasp of precisely how the whole thing worked (largely because I don't like reading documentation, not a good practice I agree). The engine didn't ever seem to clearly separated from the game within it and the way in which different functions of the engine were handled was very inconsistent. I decided I wanted to work within my own environment but I didn't particularly feel like spending hundreds of hours reinventing the wheel and writing a render engine so I built EpiEngine on top of Blender's pre-existing support for the really low level maths centric stuff.  
      
    Q: What exactly does EpiEngine do?  
    A: It does the following: automatically loads external resources such as shaders, sounds, music, models, etc. Enforces a standard file structure where important qualities of assets are described outside the data files in .epi files. Provides out of the box network synchronization for multiplayer games. Simplifies access to important settings into a more standard console variable configuration. Provides out of the box support for passworded servers, network text chat, subtitles, localization and much more.  
    
    Q: Why is it called EpiEngine?
    A: Not a clue. I had a vague idea to make an engine once and that was the particular name that sprung into my head. Feel free to dream up a funny story I can use to explain how I came up with the name because I feel this explanation is just disappointing.
      
    Q: This project is a stupid idea!  
    A: Yes, I agree. I'm a strange person.  
      
    Q: Can I help?  
    A: After being involved in a previous project where I felt other contributors slowed down my workflow considerably (through no fault of their own) I've decided that, at least to begin with, EpiEngine's development will not be publicly hosted. If you wish to contribute a fix/suggestion/addition however you can contact me privately and I will be very grateful. My position on this may change in the future, perhaps when the project is more mature, but right now I'm very hesitant to take a fully open source development approach.  
      
    Q: Can I donate/bribe you to work faster?  
    A: You sure can, you certainly don't have to and I'm not going to ask you to, but here's the link if you want to support the project: (http://gadrial.net/epiengine/donate).