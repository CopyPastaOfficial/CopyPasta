import requests
from util import *

def send_text_scan(text:str,ip_addr:str,upload_code:str) -> bool:

    """
    sends the specified text
    to the instance of copypasta running on the specified address
    """
    r = requests.post(f"http://{ip_addr}:21987/upload",json={"type" : "text", "content" : f"{text}"})
    return r.status_code == 200


def send_file(file_path:str,ip_addr:str,upload_code:str):

    """
    sends the specified file
    to the instance of copypasta running on the specified address
    """

    files = {'files': open(file_path,'rb')}
    
    r = requests.post(f"http://{ip_addr}:21987/upload",files=files)
    return r.status_code == 200

def send_keystrokes(text:str,upload_code:str):
    r = requests.post("http://127.0.0.1:21987/upload",json={"type" : "keystrokes", "content" : {"text" : f"{text}"}})
    return r.status_code == 200

def send_barcode(text:str,upload_code:str):
    r = requests.post("http://127.0.0.1:21987/upload",json={"type" : "isbn", "content" : f"{text}"})
    return r.status_code == 200


def send_wifi(ssid:str, encryption:str, key:str,upload_code:str):
    r = requests.post("http://127.0.0.1:21987/upload",json={"type" : "wifi", "content" : {"ssid" : f"{ssid}", "encryption" : f"{encryption}", "key" : f"{key}"}})
    return r.status_code == 200


def send_email(dest_addr:str,subject:str,content:str,upload_code:str):
    r = requests.post("http://127.0.0.1:21987/upload",json={"type" : "email", "content" : {"address" : f"{dest_addr}", "subject" : f"{subject}", "content" : f"{content}"}})
    return r.status_code == 200

def send_url(url:str,upload_code:str):
    r = requests.post("http://127.0.0.1:21987/upload",json={"type" : "url", "content" : f"{url}"})
    return r.status_code == 200
