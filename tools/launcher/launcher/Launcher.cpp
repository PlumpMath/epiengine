#include "Launcher.h"

#include <iostream>
#include <string>

#include "SimpleIni.h"

using namespace std;

#define WIN 0
#define LINUX 1
#define OSX 2

#define OS WIN

#define LOADER "Loader.blend"

string Launcher::winPath = "..\\engine\\blender\\blenderplayer.exe ";
string Launcher::osxPath = "../engine/blender/blenderplayer.app ";
string Launcher::linuxPath = "../engine/blender/blenderplayer ";

string Launcher::winIniPath = "..\\engine.ini";
string Launcher::osxIniPath = "../engine.ini";
string Launcher::linuxIniPath = "../engine.ini";

string Launcher::getIniPath()
{
	if (OS == WIN)
	{
		return Launcher::winIniPath;
	}
	else if (OS == LINUX)
	{
		return Launcher::linuxIniPath;
	}
	else if (OS == OSX)
	{
		return Launcher::osxIniPath;
	}
}

string Launcher::getCommandLineArguments()
{
	string args = "";

	CSimpleIniA ini;
	ini.SetUnicode();
	ini.LoadFile(Launcher::getIniPath().c_str());

	string pVal;

	//STEREO//////////////////////////////////////////
	pVal = ini.GetValue("LAUNCHER", "la_stereoscopy", "nostereo");

	if (pVal != "nostereo")
	{
		args += "-s " + pVal + " ";
	}

	//DOME////////////////////////////////////////////
	bool dome = false;

	pVal = ini.GetValue("LAUNCHER", "la_dome", "0");

	if (pVal != "0")
	{
		args += "-D ";
		dome = true;
	}

	pVal = ini.GetValue("LAUNCHER", "la_domeangle", "0");

	if (dome)
	{
		args += pVal + " ";
	}

	pVal = ini.GetValue("LAUNCHER", "la_dometilt", "0");

	if (dome)
	{
		args += pVal + " ";
	}

	pVal = ini.GetValue("LAUNCHER", "la_domewarpdata", "");

	if (dome)
	{
		args += pVal + " ";
	}

	pVal = ini.GetValue("LAUNCHER", "la_domemode", "fisheye");

	if (dome)
	{
		args += pVal + " ";
	}

	//ANTI-ALIASING/////////////////////////////////////////
	pVal = ini.GetValue("LAUNCHER", "la_antialiasing", "0");

	if (pVal != "0")
	{
		args += "-m " + pVal + " ";
	}

	//CONSOLE//////////////////////////////////////////////
	pVal = ini.GetValue("LAUNCHER", "la_console", "0");

	if (pVal != "0")
	{
		args += "-c ";
	}

	//DEBUG///////////////////////////////////////////////
	pVal = ini.GetValue("LAUNCHER", "la_debug", "0");

	if (pVal != "0")
	{
		args += "-d ";
	}

	bool gameOption = false;

	//FIXEDTIME//////////////////////////////////////////
	pVal = ini.GetValue("LAUNCHER", "la_fixedtime", "0");

	if (!gameOption && pVal != "0")
	{
		args += "-g ";
		gameOption = true;
	}

	if (pVal != "0")
	{
		args += "fixedtime ";
	}

	//NOMIPMAP////////////////////////////////////////////
	pVal = ini.GetValue("LAUNCHER", "la_nomipmap", "0");

	if (!gameOption && pVal != "0")
	{
		args += "-g ";
		gameOption = true;
	}

	if (pVal != "0")
	{
		args += "nomipmap ";
	}

	//FPS////////////////////////////////////////////////
	pVal = ini.GetValue("LAUNCHER", "la_fps", "0");

	if (!gameOption && pVal != "0")
	{
		args += "-g ";
		gameOption = true;
	}

	if (pVal != "0")
	{
		args += "show_framerate ";
	}

	//PROPERTIES////////////////////////////////////////
	pVal = ini.GetValue("LAUNCHER", "la_properties", "0");

	if (!gameOption && pVal != "0")
	{
		args += "-g ";
		gameOption = true;
	}

	if (pVal != "0")
	{
		args += "show_properties ";
	}

	//PROFILER////////////////////////////////////////
	pVal = ini.GetValue("LAUNCHER", "la_profiler", "0");

	if (!gameOption && pVal != "0")
	{
		args += "-g ";
		gameOption = true;
	}

	if (pVal != "0")
	{
		args += " show_profile ";
	}

	return args;
}

void Launcher::launchWindows()
{
	winPath += Launcher::getCommandLineArguments();
	winPath += LOADER;
	printf("%s\n\n", winPath);
	system(winPath.c_str());
}

void Launcher::launchOSX()
{
	osxPath += Launcher::getCommandLineArguments();
	osxPath += LOADER;
	system(osxPath.c_str());
}

void Launcher::launchLinux()
{
	linuxPath += Launcher::getCommandLineArguments();
	linuxPath += LOADER;
	system(linuxPath.c_str());
}

void main()
{
	if (OS == WIN)
	{
		Launcher::launchWindows();
	}
	else if (OS == LINUX)
	{
		Launcher::launchLinux();
	}
	else if (OS == OSX)
	{
		Launcher::launchOSX();
	}
}