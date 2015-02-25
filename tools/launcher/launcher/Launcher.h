#ifndef LAUNCHER_H
#define LAUNCHER_H

#include <string>

using namespace std;

class Launcher
{
public:
	static void launchWindows();
	static void launchOSX();
	static void launchLinux();
private:
	static string winPath;
	static string osxPath;
	static string linuxPath;

	static string winIniPath;
	static string osxIniPath;
	static string linuxIniPath;

	static string getCommandLineArguments();
	static string getIniPath();
};

#endif