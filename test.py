import socket
from flask import Flask, render_template, send_from_directory,send_file,request
from requests import get
import os
from multiprocessing import Process, freeze_support
import webbrowser
import sys
import PIL.Image as Image
import io
from array import array
from pyperclip import copy
from time import sleep
from random import randint
from flaskwebgui import FlaskUI
from subprocess import run

app = Flask(__name__)
ui = FlaskUI(app)

if not os.path.exists("static/"):
    os.mkdir("static")
app.config['UPLOAD_FOLDER'] = "static/"

@app.route("/")
def home():

    return render_template("index.html")

@app.route("/image_preview")
def img_preview():
    
    return render_template("img_preview.html")

@app.route("/scan_preview",methods=["GET", "POST"])
def scan_preview():
    with open("static/scan.Blue","r") as f:

        if request.method == 'POST':
            title = request.form.get("title")
            return send_file('static/scan.Blue',attachment_filename=title+".txt",as_attachment=True)
        else:
            a = f.read()
            leng = len(a.split("\n"))
            return render_template("scan_preview.html",scan = a.replace("/n","<br>"),len=leng)
        


@app.route("/process/<process_id>")
def process(process_id):

    if process_id == "[DOWNLOAD IMG]":
        return send_file('static/imgscan.jpeg',
                     attachment_filename='imgscan'+str(randint(0,167645454))+'.jpeg',
                     as_attachment=True)

    if process_id == "[CLEAR SCAN]":
        open("static/scan.Blue","w")
        with open("static/scan.Blue","r") as f:
            return render_template("scan_preview.html",scan = f.read().replace("/n","<br>"))

    if process_id == "[COPY SCAN]":
        with open("static/scan.Blue","r") as f:
            copy(f.read())




def listen_to_file_scan():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("",8836))
    print("bound images")
    sys.stdout.flush()
    while True:
        s.listen()
        cli,addr = s.accept()

        imgbytes = bytearray()
        while True:
            b = cli.recv(99999)
            imgbytes.extend(b)
            print(b)
            sys.stdout.flush()
            if b == b"":
                cli.close()
                break
            elif os.path.exists("bool"):
                os.remove("bool")
                cli.close()
                break

        image = Image.open(io.BytesIO(imgbytes))
        image.save("static/imgscan.jpeg")
        run("start msedge \"127.0.0.1/image_preview\"",shell=True)
            


def listen_to_text_scan():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("",8835))
    print("bound text")
    sys.stdout.flush()
    while True:
        s.listen()
        cli,addr = s.accept()
        print(addr)
        while True:
            b = cli.recv(1024)
            print(b.decode("utf-8"))
            sys.stdout.flush()
            if b == b"":
               s.close()
               break
            elif b"[END FILE FLAG]" in b:
                pass

            else:

                with open("static/scan.Blue","a") as f:
                    f.write(b.decode("UTF-8"))
    
                    run("start msedge \"127.0.0.1/scan_preview\"",shell=True)
            




if __name__ == "__main__":

    freeze_support()
    
    os.chdir(os.path.abspath(__file__).replace("test.py",""))
    r = get("https://chart.googleapis.com/chart?cht=qr&chs=150x150&chl="+str(socket.gethostbyname(socket.gethostname())),allow_redirects=True)
    


    with open("static/qr.jpeg","wb") as f:
        f.write(r.content)

    
    Process(target=listen_to_text_scan).start()
    Process(target=listen_to_file_scan).start()

    run("start msedge \"127.0.0.1/\"",shell=True)
    app.run(debug=True,host="0.0.0.0",port=80)
    