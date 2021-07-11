from shutil import rmtree
from os import remove


try:
    remove("launcher.exe")
except:
    pass

try:
    rmtree("copypasta")
except:
    pass