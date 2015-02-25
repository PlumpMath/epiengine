import sys
import platform

if platform.system() == "Windows":
	paths = ["epiengine\\bin", "epiengine\\com"]
else:
	paths = ["epiengine/bin", "epiengine/com"]

for i in sys.path:
    if paths[0] == i[len(i)-13:].lower() or paths[1] == i[len(i)-13:].lower():
        sys.path.append(i[:len(i)-3]+"Engine")
        break