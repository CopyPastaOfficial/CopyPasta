from ast import literal_eval
from requests import get
from subprocess import Popen
from shutil import rmtree
from zipfile import  ZipFile
from os import path, chdir, remove
import sys

if getattr(sys, 'frozen', False):
    APP_PATH = path.dirname(sys.executable)
elif __file__:
    APP_PATH = path.dirname(__file__)


def update_main_executable(version: str) -> None:

    if not literal_eval(get("https://api.github.com/repos/CopyPastaOfficial/CopyPasta/tags").text)[0]['name'] == version:
        
        print("NOT UP TO DATE")
        #remove copypasta folder berfore downloading new version
        try:
            rmtree("copypasta")
        except:
            #not really an error if the folder have been deleted
            pass

        #download zip file
        with open("copypasta.zip","wb") as f:
            f.write(get("https://github.com/CopyPastaOfficial/CopyPasta/releases/latest/download/copypasta_files.zip").content)
            f.close()

        #unzip file
        with ZipFile("copypasta.zip","r") as zip_ref:
            zip_ref.extractall()

        #delete zipped file
        remove("copypasta.zip")


def is_installed() -> None:
    return path.exists("copypasta")


def get_current_version_and_check_update() -> None:

    try:

        with open("copypasta/version","r") as f:
            version = f.read()
            print(version)
            f.close()
            
        update_main_executable(version)
    except:
        update_main_executable("0")


if __name__ == "__main__":

    #make sure we work in the right directory
    chdir(APP_PATH)
    print(APP_PATH)
    
    #install copypasta like if it is not installed by the same process as updating
    if not is_installed():
        #is still the lastest version ?
        get_current_version_and_check_update()

    print("starting copypasta...")
    #now that we have the lastest, we can start the app :D
    Popen("copypasta/copypasta.exe")
