from shutil import rmtree
from os import remove
from getpass import getuser

try:
    remove("launcher.exe")
except:
    pass

try:
    rmtree("copypasta")
except Exception as e:
    print(e)

try:
    user = getuser()
    remove(f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\CopyPasta.lnk")
except Exception as e:
    print(e)

try:
    user = getuser()
    remove(f"C:\\Users\\{user}\\Desktop\\CopyPasta.lnk")
except Exception as e:
    print(e)

try:
    remove("unins000.exe")
except Exception as e:
    print(e)
    
