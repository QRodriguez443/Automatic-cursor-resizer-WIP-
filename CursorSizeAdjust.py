import os
import subprocess

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ModifyCursorSize", "Debug", "ModifyCursorSize.exe")
    subprocess.call(file_path)
    #print("CALLED:", file_path)