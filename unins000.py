from shutil import rmtree
from os import remove
from getpass import getuser
from sys import argv
# for pyinstaller
import pywintypes

APP_PATH = "C:/Program Files/CopyPasta"

try:
    remove(f"{APP_PATH}/launcher.exe")
except:
    pass

try:
    rmtree(f"{APP_PATH}/copypasta",ignore_errors=True)
except Exception as e:
    print(e)


try:
    user = getuser()
    remove(f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\CopyPasta.lnk")
    del user
except Exception as e:
    print(e)

try:
    remove(f"C:\\Users\\Public\\Desktop\\CopyPasta.lnk")
except Exception as e:
    print(e)

try:
    remove(argv[0])
except Exception as e:
    print(e)
    
    


