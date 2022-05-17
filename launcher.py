from ast import literal_eval
from requests import get
from subprocess import Popen
from shutil import rmtree
from zipfile import  ZipFile
from os import path, chdir, remove,mkdir
import sys
from util import create_shortcut, emergency_redownload, notify_desktop


# to fix pyinstaller error
import pywintypes
import win32api



if getattr(sys, 'frozen', False):
    EXE_PATH = path.dirname(sys.executable)
elif __file__:
    EXE_PATH = path.dirname(__file__)

APP_PATH = "C:/Program Files/CopyPasta/copypasta"



def update_main_executable(version: str) -> None:
    
    # makes sure we go back to launcher's root
    chdir(EXE_PATH)

    if not literal_eval(get("https://api.github.com/repos/CopyPastaOfficial/CopyPasta/tags").text)[0]['name'] == version:
        
        notify_desktop("CopyPasta Installer","Donwloading CopyPasta components...")        
        
        
        #remove copypasta folder berfore downloading new version
        try:
            rmtree(APP_PATH)
        except:
            #not really an error if the folder have been deleted or folder already exists
            pass
        
        # create copypasta folder if not exists
        if not path.exists("C:/Program Files/CopyPasta"):
            mkdir("C:/Program Files/CopyPasta")
        
        
        #download zip file
        with open("copypasta.zip","wb") as f:
            f.write(get("https://github.com/CopyPastaOfficial/CopyPasta/releases/latest/download/copypasta_files.zip").content)
            f.close()

        #unzip file
        with ZipFile("copypasta.zip","r") as zip:
            
            
            for member in zip.namelist():
                if not (path.exists(APP_PATH + r'/' + member) or path.isfile(APP_PATH + r'/' + member)):
                    zip.extract(member,APP_PATH)
            

        #delete zipped file
        remove("copypasta.zip")


def is_installed() -> None:
    return path.exists(APP_PATH)



def get_current_version_and_check_update() -> None:

    try:

        with open("copypasta/version","r") as f:

            version = f.read()
            print(version)
            f.close()
            
        update_main_executable(version)
    except:
        update_main_executable("0")



def move_launcher():
    """
    - put launcher.exe in C:/Program Files/CopyPasta
    - create shortcut to launcher on Desktop and StartMenu
    - remove itself ?
    """
    
    # 1
    if not path.exists("C:/Program Files/CopyPasta/launcher.exe"):
        with open("launcher.exe","wb") as f:
                f.write(get("https://github.com/CopyPastaOfficial/CopyPasta/releases/latest/download/launcher.exe").content)
                f.close()
    
    # 2
    create_shortcut(path="C:\\Users\\Public\\Desktop\\CopyPasta.lnk",target="C:\\Program Files\\CopyPasta\\copypasta\\launcher.exe",wDir="C:\\Program Files\\CopyPasta\\",icon="C:\\Program Files\\CopyPasta\\copypasta\\static\\favicon.ico")       
       
    #3 ?         
    

if __name__ == "__main__":




    if is_installed():
        #make sure we work in the right directory
        chdir(APP_PATH)



    #install copypasta like if it is already installed by the same process as updating
    else:
        
        # download lastest version
        get_current_version_and_check_update()
        
        chdir(APP_PATH)
        
        move_launcher()
        
        
    #now, we can be sure to work in the copypasta app directory
    chdir(APP_PATH)

    #now that we have the lastest, we can start the app :D
    Popen(f"{APP_PATH}/copypasta/copypasta.exe")

