import sys
import subprocess
from objs import App, Pac_ser

if (__name__ == "__main__"):
    result: subprocess.CompletedProcess = subprocess.run([sys.executable,
                                                          "launcher.py"])
    if (result.returncode != 1):
        game: App = Pac_ser.app_init()
        game.run()
