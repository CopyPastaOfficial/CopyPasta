from subprocess import run
from os import chdir

chdir("main")
run(["start","main.exe"],shell=True)
