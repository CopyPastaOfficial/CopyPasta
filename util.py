import socket
from getpass import getuser
from random import randint
from json import *
from requests import get
from locale import getlocale
from os import mkdir, path
from xml.etree import ElementTree
from xml.sax.saxutils import escape
from multiprocessing import Process
from webbrowser import open as open_tab




def get_private_ip():
    """
    get all the private ips linked to your machine and return the one linked to your context
    :return: a string containing the private ip used on your machine

    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]



def make_qr_url():
    url = {"name" : getuser(),"ip" : get_private_ip(), "key" : str(randint(0,100000000000))}
    return dumps(url,indent=4)


def check_updates():
    with open("static/update.Blue","r") as f:
        n = int(f.read())
        if n == 10:
            download_templates()
        else:
            with open("static/update.Blue","w") as f:
                f.write(str(n+1))


def emergency_redownload():
    
    if not path.exists("templates/"):
        mkdir("templates")

    if not path.exists("static/"):
        mkdir("static")
        open("static/favicon.ico","w")

        with open("static/update.Blue","w") as f:
            f.write("1")

        mkdir("static/dist")
        mkdir("static/dist/css")
        mkdir("static/dist/js")
        mkdir("static/files_hist")

        init_history_file()


        
    download_templates()



    

def download_templates():
    locale = getlocale()[0][:2]

    #get supported languages list
    r = get(f"https://raw.githubusercontent.com/thaaoblues/copypasta/master/templates/supported_languages.Blue",allow_redirects=True).text
    r = r.replace("\n","").split("/")

    #check if the computer default language is supported
    if locale not in r:
        #if not, set to english
        locale = "en"


    #get the templates
    r = get(f"https://raw.githubusercontent.com/thaaoblues/copypasta/master/templates/{locale}/index.html",allow_redirects=True)
    with open("templates/index.html","wb") as f:
        f.write(r.content)

    r = get(f"https://raw.githubusercontent.com/thaaoblues/copypasta/master/templates/{locale}/scan_preview.html",allow_redirects=True)
    with open("templates/scan_preview.html","wb") as f:
        f.write(r.content)

    r = get(f"https://raw.githubusercontent.com/thaaoblues/copypasta/master/templates/{locale}/img_preview.html",allow_redirects=True)
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

    for file in history:
        store_to_history(file)


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