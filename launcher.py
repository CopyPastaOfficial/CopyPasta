from ast import literal_eval
from requests import get
from subprocess import Popen
from shutil import rmtree
from zipfile import  ZipFile
from os import path, chdir, remove

APP_PATH = path.abspath(__file__).replace("main.py","").replace("main.exe","").replace("copypasta.exe","").replace("copypasta.py","").replace("launcher.exe","").replace("launcher.py","")


def update_main_executable(version):

    if not literal_eval(get("https://api.github.com/repos/CopyPastaOfficial/CopyPasta/tags").text)[0]['name'] == version:
        

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


def is_installed():
    return path.exists("copypasta")

        
if __name__ == "__main__":

    #make sure we work in the right directory
    chdir(APP_PATH)
    
    #install copypasta like if it is not installed by the same process as updating
    if not is_installed():
        #is still 1.2 the lastest version ?
        update_main_executable("1.2")
    
    #now that we have the lastest, we can start the app :D
    Popen("copypasta/copypasta.exe")
