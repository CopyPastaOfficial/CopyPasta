import socket
from getpass import getuser
from random import randint
from json import *
from requests import get
from locale import getlocale
from os import mkdir, path, remove
from xml.etree import ElementTree
from xml.sax.saxutils import escape
from multiprocessing import Process
from webbrowser import open as open_tab
from ast import literal_eval
import requests
from subprocess import Popen
from functools import partial
from win10toast_click import ToastNotifier
from win32com.client import Dispatch


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
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        # probably offline
        return "127.0.0.1"


def make_qr_url():
    url = {"name" : getuser(),"ip" : get_private_ip(), "key" : str(randint(0,100000000000))}
    return dumps(url,indent=4)


def check_templates_update():
    with open("static/update.Blue","r") as f:
        n = int(f.read())
        if n == 10:
            download_templates()
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

        mkdir("static/dist")
        mkdir("static/dist/css")
        mkdir("static/dist/js")
        mkdir("static/files_hist")

        init_history_file()


        
    download_templates()


def is_server_already_running():
    try:
        response = requests.get("http://127.0.0.1:21987/api/ping").text
        
    except:
        response = "not pong lol"

    return True if response == "pong" else False
    

def download_templates():

    #get the templates
    r = get(f"https://raw.githubusercontent.com/thaaoblues/copypasta/master/templates/index.html",allow_redirects=True)
    with open("templates/index.html","wb") as f:
        f.write(r.content)

    r = get(f"https://raw.githubusercontent.com/thaaoblues/copypasta/master/templates/scan_preview.html",allow_redirects=True)
    with open("templates/scan_preview.html","wb") as f:
        f.write(r.content)

    r = get(f"https://raw.githubusercontent.com/thaaoblues/copypasta/master/templates/img_preview.html",allow_redirects=True)
    with open("templates/img_preview.html","wb") as f:
        f.write(r.content)

    r = get(f"https://raw.githubusercontent.com/thaaoblues/copypasta/master/templates/favicon.ico",allow_redirects=True)
    with open("static/favicon.ico","wb") as f:
        f.write(r.content)

    r = get("https://raw.githubusercontent.com/ThaaoBlues/CopyPasta/main/bootstrap/dist/css/bootstrap.min.css")
    with open("static/dist/css/bootstrap.min.css","wb") as f:
        f.write(r.content)

    r = get("https://raw.githubusercontent.com/ThaaoBlues/CopyPasta/main/bootstrap/dist/js/bootstrap.bundle.min.js")
    with open("static/dist/js/bootstrap.bundle.min.js","wb") as f:
        f.write(r.content)

    with open("static/update.Blue","w") as f:
        f.write("1")



def update_main_executable(version):

    if not literal_eval(get("https://api.github.com/repos/CopyPastaOfficial/CopyPasta/tags").text)[0]['name'] == version:
        

        with open("copypasta(1).exe","wb") as f:
            f.write(get("https://github.com/CopyPastaOfficial/CopyPasta/releases/latest/download/copypasta.exe").content)
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


def init_history_file():

    """
    initialize the history xml file

    """
    
    if not path.exists("static/history.xml"):
        with open("static/history.xml","w") as f:
            f.write("<history>\n</history>")
            f.close()


def get_history():

    history = "{\"history\" : ["

    for element in ElementTree.parse("static/history.xml").getroot():
        history += element.text + ","

    history = history[:-1] + "]}" if history != "{\"history\" : [" else history +"]}"

    return history


def get_history_file_by_id(id):

    history = []

    for element in ElementTree.parse("static/history.xml").getroot():
        history.append(element.text)


    return loads(history[id])

def delete_history_file_by_id(id):

    history = []

    for element in ElementTree.parse("static/history.xml").getroot():
        history.append(element.text)

    history.pop(id)

    init_history_file()

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
    
    return get_private_ip() != "127.0.0.1"