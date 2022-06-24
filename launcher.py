from ast import literal_eval
from getpass import getuser
from importlib.util import find_spec
from requests import get
from subprocess import Popen
from shutil import move, rmtree
from zipfile import  ZipFile
from os import path, chdir, remove,mkdir,environ
import sys
from util import add_copypasta_port_redirect, add_copypasta_to_hosts_file, create_shortcut, is_hosts_file_modified, notify_desktop

# to fix pyinstaller error
import pywintypes
import win32api





        
#pyinstaller splash screen gestion


def update_splash_text():
    pass

def close_splash():
    pass

if '_PYIBoot_SPLASH' in environ and find_spec("pyi_splash"):
    from pyi_splash import update_text, close
    update_splash_text = update_text
    close_splash = close
    

# get all the pathes needed
if getattr(sys, 'frozen', False):
    EXE_PATH = path.dirname(sys.executable)
elif __file__:
    EXE_PATH = path.dirname(__file__)

APP_PATH = "C:/Program Files/CopyPasta"



def update_main_executable(version: str) -> None:
    
    # makes sure we go back to launcher's root
    chdir(EXE_PATH)

    if not literal_eval(get("https://api.github.com/repos/CopyPastaOfficial/CopyPasta/tags").text)[0]['name'] == version:
        
        notify_desktop("CopyPasta Installer","Donwloading CopyPasta components...")        
        
        
        try:
            # move static folder to keep history
            move(f"{APP_PATH}/copypasta/static",f"{EXE_PATH}/static")
        except:
            # just that the folder does not exists (installation case)
            pass
        
        
        #remove copypasta folder berfore downloading new version
        try:
            rmtree(APP_PATH)
        except:
            #not really an error if the folder have been deleted
            pass
        
        # create copypasta folder if not exists
        if not path.exists(APP_PATH):
            mkdir(APP_PATH)
        
        
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
        
        
        # re-put static folder in copypasta
        try:
            move(f"{EXE_PATH}/static",f"{APP_PATH}/copypasta/static")
        except:
            # folder does not exists 
            pass
        
        
        if not is_hosts_file_modified():
            
            try:
                add_copypasta_to_hosts_file()
            except:
                # launcher probably started without admin privileges, nothing to worry about
                pass


def is_installed() -> None:
    return path.exists(APP_PATH)



def get_current_version_and_check_update() -> None:

    try:

        with open(f"{APP_PATH}/copypasta/version","r") as f:

            version = f.read()
            f.close()
            
        update_main_executable(version)
    except:
        update_main_executable("0")



def move_launcher():
    """
    - put launcher.exe in C:/Program Files/CopyPasta
    - create shortcut to launcher on Desktop and StartMenu
    - create shortcut on start menu
    """
    
    # 1
    if not path.exists(f"{APP_PATH}/launcher.exe"):
        with open(f"{APP_PATH}/launcher.exe","wb") as f:
            f.write(get("https://github.com/CopyPastaOfficial/CopyPasta/releases/latest/download/launcher.exe").content)
            f.close()
    
    # 2
    create_shortcut(path="C:\\Users\\Public\\Desktop\\CopyPasta.lnk",target="C:\\Program Files\\CopyPasta\\launcher.exe",wDir="C:\\Program Files\\CopyPasta\\",icon="C:\\Program Files\\CopyPasta\\copypasta\\static\\favicon.ico")       
       
    #3
    create_shortcut(path=f"C:\\Users\\{getuser()}\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\CopyPasta.lnk",target="C:\\Program Files\\CopyPasta\\launcher.exe",wDir="C:\\Program Files\\CopyPasta\\",icon="C:\\Program Files\\CopyPasta\\copypasta\\static\\favicon.ico")
    

if __name__ == "__main__":


    if is_installed():
        #make sure we work in the right directory
        chdir(APP_PATH)
        # download lastest version
        get_current_version_and_check_update()
        
    else:
        # download lastest version like updates
        get_current_version_and_check_update()
        # create shortcuts and move launcher.exe to C:/Programs Files/CopyPasta/copypasta
        move_launcher()
    
    
    add_copypasta_port_redirect()
    
    chdir(APP_PATH)

    #now that we have the lastest, we can start the app :D
    Popen(f"{APP_PATH}/copypasta/copypasta.exe")