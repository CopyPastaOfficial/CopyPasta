import socket
from flask import Flask, render_template, send_from_directory,send_file,request,redirect
from requests import get
from os import path, chdir, mkdir,remove
from multiprocessing import Process, freeze_support
from sys import stdout
import PIL.Image as Image
from io import BytesIO
import win32clipboard
from array import array
from pyperclip import copy
from time import sleep
from random import randint
from flaskwebgui import FlaskUI
from subprocess import run
from datetime import date

app = Flask(__name__)
ui = FlaskUI(app)

if not path.exists("static/"):
    mkdir("static")
    open("static/hist.blue","w")
    open("static/dates.Blue","w")

app.config['UPLOAD_FOLDER'] = "static/"

@app.route("/")
def home():
    with open("static/hist.Blue","r",encoding="utf-8") as f:
        a = f.read()
        a = a.split("=")
        a.reverse()
        with open("static/dates.Blue","r") as f:
            dates=f.read().split("\n")
        
    return render_template("index.html",hist = a, len = len(a),dates=dates)



@app.route("/hist/<i>")
def history(i):
    with open("static/hist.Blue","r",encoding="utf-8") as f:
        a = f.read()
        a = a.split("=")
        a.reverse()
    text = a[int(i)]
    with open("static/scan.Blue","w",encoding="utf-8") as f:
        f.write(text)

    return redirect("/scan_preview")




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
        with open("static/scan.Blue","r",encoding="utf-8") as f:
            return render_template("scan_preview.html",scan = f.read().replace("/n","<br>"))

    if process_id == "[COPY SCAN]":
        with open("static/scan.Blue","r") as f:
            copy(f.read())
            return render_template("image_preview.html")
    
    if process_id == "[COPY IMG]":
        output = BytesIO()
        image = Image.open("static/imgscan.jpeg")
        image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        
        return render_template("img_preview.html")




def listen_to_file_scan():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("",8836))
    print("bound images")
    stdout.flush()
    while True:
        s.listen()
        cli,addr = s.accept()

        imgbytes = bytearray()
        while True:
            b = cli.recv(99999)
            imgbytes.extend(b)
            print(b)
            stdout.flush()
            if b == b"":
                cli.close()
                break
            elif path.exists("bool"):
                remove("bool")
                cli.close()
                break

        image = Image.open(BytesIO(imgbytes))
        image.save("static/imgscan.jpeg")
        run("start msedge \"127.0.0.1/image_preview\"",shell=True)
            




def listen_to_text_scan():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("",8835))
    print("bound text")
    stdout.flush()
    while True:
        s.listen()
        cli,addr = s.accept()
        print(addr)
        while True:
            b = cli.recv(99999)
            print(b.decode("utf-8"))
            stdout.flush()
            if b == b"":
               s.close()
               break
            elif b"[END FILE FLAG]" in b:
                open('bool',"w")
                pass

            else:

                with open("static/scan.Blue","a",encoding="utf-8") as f:
                    f.write(b.decode("UTF-8"))
                
                with open("static/hist.Blue","a",encoding="utf-8") as f:
                    
                    f.write("\n=\n"+b.decode("UTF-8"))
                    run("start msedge \"127.0.0.1/scan_preview\"",shell=True)
                with open("static/dates.Blue","a") as f:
                    today = date.today()
                    f.write(str(today.strftime("%d/%m/%Y"))+"\n")





if __name__ == "__main__":

    freeze_support()
    
    chdir(path.abspath(__file__).replace("test.py",""))
    r = get("https://chart.googleapis.com/chart?cht=qr&chs=150x150&chl="+str(socket.gethostbyname(socket.gethostname())),allow_redirects=True)
    


    with open("static/qr.jpeg","wb") as f:
        f.write(r.content)

    
    Process(target=listen_to_text_scan).start()
    Process(target=listen_to_file_scan).start()

    run("start msedge \"127.0.0.1/\"",shell=True)
    app.run(debug=True,host="0.0.0.0",port=80)
    