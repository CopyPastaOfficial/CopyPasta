import socket
from flask import Flask, render_template, send_from_directory
from requests import get
import os
from multiprocessing import Process, freeze_support
import webbrowser
import sys
import PIL.Image as Image
import io
from array import array

app = Flask(__name__)
if not os.path.exists("static/"):
    os.mkdir("static")
app.config['UPLOAD FOLDER'] = "static/"

@app.route("/")
def home():

    return render_template("index.html")

@app.route("/image_preview")
def img_preview():
    
    return render_template("img_preview.html")

@app.route("/scan_preview")
def scan_preview():
    with open("static/scan.Blue","r") as f:
        return render_template("scan_preview.html",scan = f.read().replace("/n","<br>"))
        


@app.route("/process/<process_id>")
def process(process_id):

    if process_id == "[DOWNLOAD IMG]":
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename="imgscan.jpeg")

    if process_id == "[CLEAR SCAN]":
        open("static/scan.Blue","w")
        with open("static/scan.Blue","r") as f:
            return render_template("scan_preview.html",scan = f.read().replace("/n","<br>"))


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
        webbrowser.open("127.0.0.1/image_preview")

            


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
            else

                with open("static/scan.Blue","a") as f:
                    f.write(b.decode("UTF-8"))
    
                webbrowser.open("127.0.0.1/scan_preview")
            




if __name__ == "__main__":

    freeze_support()
    
    os.chdir(os.path.abspath(__file__).replace("test.py",""))
    r = get("https://chart.googleapis.com/chart?cht=qr&chs=150x150&chl="+str(socket.gethostbyname(socket.gethostname())),allow_redirects=True)
    


    with open("static/qr.jpeg","wb") as f:
        f.write(r.content)

    
    Process(target=listen_to_text_scan).start()
    Process(target=listen_to_file_scan).start()

    webbrowser.open("127.0.0.1")
    app.run(debug=True,host="0.0.0.0",port=80)
    