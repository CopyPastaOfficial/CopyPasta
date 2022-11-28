import socket
from getpass import getuser
from random import randint,choices
from json import *
from string import ascii_uppercase
from bs4 import BeautifulSoup
from requests import get as http_get
from os import mkdir, path, remove
from xml.etree import ElementTree
from xml.sax.saxutils import escape
from multiprocessing import Process
from webbrowser import open as open_tab
from ast import literal_eval
from functools import partial
from win10toast_click import ToastNotifier
from win32com.client import Dispatch
from time import sleep
from subprocess import Popen

def notify_desktop(title,text):
    # initialize 
    toaster = ToastNotifier()

    # showcase
    toaster.show_toast(
        title, # title
        text, # message 
        icon_path="static/favicon.ico", # 'icon_path' 
        duration=5, # for how many seconds toast should be visible; None = leave notification in Notification Center
        threaded=True, # True = run other code in parallel; False = code execution will wait till notification disappears 
        callback_on_click=partial(open_tab,"http://127.0.0.1:21987") # click notification to run function 
        )



def get_private_ip():
    """
    get all the private ips linked to your machine and return the one linked to your context
    :return: a string containing the private ip used on your machine

    """
    
    
    # check if online before, because some things I don't fully understand made
    # this request return the last private IP address sometimes when onffline
    if is_online():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    
    else:
        return "You are offline :/"


def make_qr_url():
    url = {"name" : getuser(),"ip" : get_private_ip(), "key" : str(randint(0,100000000000))}
    return dumps(url,indent=4)


def check_templates_update():
    
    
    
     
    # first, get a list of all templates available on github
    
    json_data = http_get("https://api.github.com/repos/copypastaofficial/copypasta/contents/templates").json()
    
    
    
    # check templates integrity
    for ele in json_data:
        if not path.exists(ele["path"]):
            download_templates()
            return
    
    
    # check 10 startup rule
    with open("static/update.Blue","r") as f:
        n = int(f.read())
        if n == 10:
            #download_templates()
            pass
        else:
            with open("static/update.Blue","w") as f:
                f.write(str(n+1))


def emergency_redownload():
    
    
    notify_desktop("CopyPasta update","CopyPasta is downloading its files, it can take some time...")
    
    if not path.exists("templates/"):
        mkdir("templates")

    if not path.exists("static/"):
        mkdir("static")
        
        f = open("static/favicon.ico","w")
        f.close()

        f = open("static/qr.jpeg","w")
        f.close()

        with open("static/update.Blue","w") as f:
            f.write("1")
            f.close()
            
            
        mkdir("static/files_hist")

        init_history_file()


        
    #download_templates()


def is_server_already_running():
    try:
        response = http_get("http://127.0.0.1:21987/api/ping").text
        
    except:
        response = "not pong lol"

    return True if response == "pong" else False
    

def download_templates():
    
    
    # first, get a list of all templates available on github
    
    json_data = http_get("https://api.github.com/repos/copypastaofficial/copypasta/contents/templates").json()
    
    
    """
        example :
        [ 
            {
                "name": "download_page.html",
                "path": "templates/download_page.html",
                "sha": "34d0f64b305c1798ec0b7aa9cc5cd192e3077368",
                "size": 3089,
                "url": "https://api.github.com/repos/ThaaoBlues/CopyPasta/contents/templates/download_page.html?ref=main",
                "html_url": "https://github.com/ThaaoBlues/CopyPasta/blob/main/templates/download_page.html",
                "git_url": "https://api.github.com/repos/ThaaoBlues/CopyPasta/git/blobs/34d0f64b305c1798ec0b7aa9cc5cd192e3077368",
                "download_url": "https://raw.githubusercontent.com/ThaaoBlues/CopyPasta/main/templates/download_page.html",
                "type": "file",
                "_links": {
                "self": "https://api.github.com/repos/ThaaoBlues/CopyPasta/contents/templates/download_page.html?ref=main",
                "git": "https://api.github.com/repos/ThaaoBlues/CopyPasta/git/blobs/34d0f64b305c1798ec0b7aa9cc5cd192e3077368",
                "html": "https://github.com/ThaaoBlues/CopyPasta/blob/main/templates/download_page.html"
                }
            }
            
        ]
    
    """
    
    #get the templates
    for ele in json_data:
        
        r = http_get(ele["download_url"],allow_redirects=True)
        
        with open(ele["path"],"wb") as f:
            f.write(r.content)

    with open("static/update.Blue","w") as f:
        f.write("1")



def update_main_executable(version):

    if not literal_eval(http_get("https://api.github.com/repos/CopyPastaOfficial/CopyPasta/tags").text)[0]['name'] == version:
        

        with open("copypasta(1).exe","wb") as f:
            f.write(http_get("https://github.com/CopyPastaOfficial/CopyPasta/releases/latest/download/copypasta.exe").content)
            f.close()

        Popen("copypasta(1).exe")
        
        remove("copypasta.exe")

        exit(1)


def store_to_history(json_data):
    json_data = dumps(json_data)
    tree = ElementTree.parse("static/history.xml")
    root = tree.getroot()
    new_ele = ElementTree.SubElement(root,"file")
    new_ele.text = escape(json_data)

    tree.write("static/history.xml")


def init_history_file(force=False):

    """
    initialize the history xml file

    """
    
    if (not path.exists("static/history.xml")) or (force):
        with open("static/history.xml","w") as f:
            f.write("<history>\n</history>")
            f.close()


def get_history_json()->dict:

    # using lists and join() to speed up
    history = {"history":[]}

    for element in ElementTree.parse("static/history.xml").getroot():
        history["history"].append(loads(element.text))

    return history

def get_history_file_last_id():
    return len(ElementTree.parse("static/history.xml").getroot()) -1
    
    
def get_history_file_by_id(file_id) -> dict:

    if file_id < len(ElementTree.parse("static/history.xml").getroot()):

        return loads(ElementTree.parse("static/history.xml").getroot()[file_id].text)


    else: # a file with this id does not exists
        return False
    

def delete_history_file_by_id(file_id):

    history = []

    for element in ElementTree.parse("static/history.xml").getroot():
        history.append(element.text)

    history.pop(file_id)
    
    init_history_file(force=True)

    tree = ElementTree.parse("static/history.xml")
    root = tree.getroot()
    for file in history:
        new_ele = ElementTree.SubElement(root,"file")
        new_ele.text = escape(file)
        tree.write("static/history.xml")


def append_to_scan_file(text):

    with open("static/scan.Blue","a") as f:
        f.write(text)
        f.close()

def wipe_scan_file():
    open("static/scan.Blue","w")


def open_link_process(url):
    open_tab(url)

def open_browser_if_settings_okay(url):
    
    if path.exists("static/tab"):
        Process(target=open_link_process,args=(url,)).start()
        
        
        
def create_shortcut(path, target='', wDir='', icon=''):    
 
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    if icon == '':
        pass
    else:
        shortcut.IconLocation = icon
    shortcut.save()



def is_online():
    try:
        socket.create_connection(("8.8.8.8",53))
        return True
    except OSError:
        return False

def get_server_version():
    
    
    if not path.exists("version"):
        return "version file not found :/"
    
    with open("version","r") as f:
        return f.read()

        
def is_image(file_type:str):
    
    return file_type in ["jpeg","jpg","png","ico","gif","apng","avif","gif","jfif","pjpeg","pjp","svg","webp"]



def identify_product(isbn:str):
    
    
    
    # edible product ?
    r = http_get(f"http://world.openfoodfacts.org/api/v0/product/{isbn}")
    r = loads(r.text)
    
    if "product" in r.keys():
        r = r["product"]
        
        return {"name":r["product_name"]+ " - "+r["brands"] if "brands" in r.keys() else r["product_name"] ,"url":f"https://world.openfoodfacts.org/product/{isbn}"}
    
    
    # book ?
    r = http_get(f"https://www.isbnsearcher.com/books/{isbn}",headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"})
    
    if r.status_code == 200:
        r = BeautifulSoup(r.text,"html.parser")
        
        return {"name":r.find("h1").get_text(),"url":f"https://www.isbnsearcher.com/books/{isbn}"}
    
    else:
        return {"name":isbn,"url":f"https://www.google.com/search?q={isbn}"}
    

def delete_ot_dl_proc(APP_PATH,file:str):
    
    sleep(30)
    # delete file after download as it is only a one timer
    remove(path.join(APP_PATH,"static","ot_upload",file))


def clear_tmp(filename:str):
    # wait the complete transfert
    sleep(10)
    #remove the temporary file
    remove(f"tmp/{filename}")


def gen_upload_code():

    return "".join(choices(ascii_uppercase,k=4))


def store_upload_code(APP_PATH:str,upload_code:str):

    with open(path.join(APP_PATH,"static/upload_code.cpasta"),"w") as f:
        f.write(upload_code)

def get_upload_code(APP_PATH:str):

    with open(path.join(APP_PATH,"static/upload_code.cpasta"),"r") as f:
        return f.read()

def is_upload_code_valid(APP_PATH:str,upload_code:str) -> bool:

    with open(path.join(APP_PATH,"static/upload_code.cpasta"),"r") as f:
        return f.read() == upload_code
