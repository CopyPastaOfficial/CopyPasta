import requests


def send_text_scan(text):
    r = requests.post("http://127.0.0.1:21987/upload",json={"type" : "text", "content" : f"{text}"})
    print(r.text)


def send_file(file_path):
    files = {'files': open(file_path,'rb')}
    r = requests.post("http://127.0.0.1:21987/upload", files = files)
    print(r.text)


def send_keystrokes(text):
    r = requests.post("http://127.0.0.1:21987/upload",json={"type" : "keystrokes", "content" : {"text" : f"{text}"}})
    print(r.text)

def send_barcode(text):
    r = requests.post("http://127.0.0.1:21987/upload",json={"type" : "isbn", "content" : f"{text}"})
    print(r.text)


def send_wifi(ssid, encryption, key):
    r = requests.post("http://127.0.0.1:21987/upload",json={"type" : "wifi", "content" : {"ssid" : f"{ssid}", "encryption" : f"{encryption}", "key" : f"{key}"}})
    print(r.text) 


def send_email(dest_addr,subject,content):
    r = requests.post("http://127.0.0.1:21987/upload",json={"type" : "email", "content" : {"address" : f"{dest_addr}", "subject" : f"{subject}", "content" : f"{content}"}})
    print(r.text) 


#send_email("unrealsoft.dev@gmail.com","test","prout prout la vapeur")
send_barcode("test")
#send_file("qr.png")
#send_text_scan("test of text scan")
#send_wifi("ssid","wpa","password")