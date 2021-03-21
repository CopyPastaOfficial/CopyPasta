import socket
from getpass import getuser
from random import randint
from json import dumps
from requests import get
from locale import getlocale


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

    pass               
            

def download_templates():
    locale = getlocale()[1]

    if locale not in get(f"https://raw.githubusercontent.com/thaaoblues/copypasta/master/templates/supported_languages.Blue",allow_redirects=True).text.split("/")
        locale = "en_EN"


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
    with open("templates/favicon.ico","wb") as f:
        f.write(r.content)

    r = get("https://raw.githubusercontent.com/ThaaoBlues/CopyPasta/main/bootstrap/dist/css/bootstrap.min.css")
    with open("static/dist/css/bootstrap.min.css","wb") as f:
        f.write(r.content)

    r = get("https://raw.githubusercontent.com/ThaaoBlues/CopyPasta/main/bootstrap/dist/js/bootstrap.bundle.min.js")
    with open("static/dist/js/bootstrap.bundle.min.js","wb") as f:
        f.write(r.content)

    with open("static/update.Blue","w") as f:
        f.write("1")

