import socket
from getpass import getuser
from random import randint
from json import *
from requests import get
from os import mkdir, path, remove
from xml.etree import ElementTree
from xml.sax.saxutils import escape
from multiprocessing import Process
from webbrowser import open as open_tab
from ast import literal_eval
import requests
from subprocess import Popen, run
from functools import partial
from win10toast_click import ToastNotifier
from win32com.client import Dispatch
from platform import system


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
    r = get(f"https://raw.githubusercontent.com/copypastaofficial/copypasta/master/templates/index.html",allow_redirects=True)
    with open("templates/index.html","wb") as f:
        f.write(r.content)

    r = get(f"https://raw.githubusercontent.com/copypastaofficial/copypasta/master/templates/scan_preview.html",allow_redirects=True)
    with open("templates/scan_preview.html","wb") as f:
        f.write(r.content)

    r = get(f"https://raw.githubusercontent.com/copypastaofficial/copypasta/master/templates/img_preview.html",allow_redirects=True)
    with open("templates/img_preview.html","wb") as f:
        f.write(r.content)
        
    r = get(f"https://raw.githubusercontent.com/copypastaofficial/copypasta/master/templates/video_preview.html",allow_redirects=True)
    with open("templates/img_preview.html","wb") as f:
        f.write(r.content)

    r = get(f"https://raw.githubusercontent.com/copypastaofficial/copypasta/master/templates/favicon.ico",allow_redirects=True)
    with open("static/favicon.ico","wb") as f:
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


def init_history_file(force=False):

    """
    initialize the history xml file

    """
    
    if (not path.exists("static/history.xml")) or (force):
        with open("static/history.xml","w") as f:
            f.write("<history>\n</history>")
            f.close()


def get_history():

    history = "{\"history\" : ["

    for element in ElementTree.parse("static/history.xml").getroot():
        history += element.text + ","

    history = history[:-1] + "]}" if history != "{\"history\" : [" else history +"]}"

    return history

def get_history_file_last_id():
    return len(ElementTree.parse("static/history.xml").getroot()) -1
    
    
def get_history_file_by_id(file_id):

    history = []

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
    
    
def is_hosts_file_modified():
    
    hosts_file_path = "C:\Windows\System32\Drivers\etc\hosts" if system() == "Windows" else "/etc/hosts"
    
    with open(hosts_file_path,"r") as f:
        
        return True if "copypasta.me" in f.read() else False
    
    
def add_copypasta_to_hosts_file():
    
    hosts_file_path = "C:\Windows\System32\Drivers\etc\hosts" if system() == "Windows" else "/etc/hosts"
    
    with open(hosts_file_path,"a") as f:
        
        f.write("\n127.0.0.1:21987\tcopypasta")
        
        f.close()
        
    if system() == "Windows":
        
        # flush dns cache
        run("ipconfig /flushdns",shell=True)
        
        add_copypasta_port_redirect()

def get_server_version():
    
    
    if not path.exists("version"):
        return "version file not found :/"
    
    with open("version","r") as f:
        return f.read()




def add_copypasta_port_redirect():
    
    if system() == "Windows":
        
        # put port redirect from 127.0.0.1:21987 to 127.0.0.1:80
        try:
            run("netsh interface portproxy add v4tov4 listenport=80 listenaddress=127.0.0.1 connectport=21987 connectaddress=127.0.0.1")
        except:
            # feature that may crash sometimes, not essential
            pass
        
    
def remove_copypasta_port_redirect():
            
    if system() == "Windows":
        
        # re-put port redirect from 127.0.0.1:80 to 127.0.0.1:80
        try:
            run("netsh interface portproxy add v4tov4 listenport=80 listenaddress=127.0.0.1 connectport=80 connectaddress=127.0.0.1")
        except:
            # feature that may crash sometimes, not essential
            pass
        
        
def is_image(file_type:str):
    
    return file_type in ["jpeg","jpg","png","ico","gif","apng","avif","gif","jfif","pjpeg","pjp","svg","webp"]