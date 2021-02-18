import socket
from flaskwebgui import FlaskUI
from flask import Flask, render_template, send_from_directory,send_file,request,redirect,flash
from multiprocessing import Process, freeze_support
from time import sleep
from sys import stdout
from datetime import date
import PIL.Image as Image
from random import randint
import win32clipboard
from io import BytesIO


app = Flask(__name__)

def init_flask():
    #init flask app and secret key
    ui = FlaskUI(app,port=8838)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    #specify the folder where the scan are uploaded
    app.config['UPLOAD_FOLDER'] = "static/"
    app.secret_key = b"6{#~@873gJHGZ@sfa54ZZEd^\\@#'"
    #open the gui
    ui.run()



#image preview when the user send a picture
@app.route("/")
def img_preview():
    return render_template("img_preview.html")


#processes
@app.route("/process/<process_id>")
def process(process_id):

    #download the image received
    if process_id == "[DOWNLOAD IMG]":
        return send_file('static/imgscan.jpeg',
                     attachment_filename='imgscan'+str(randint(0,167645454))+'.jpeg',
                     as_attachment=True)

    #empty the scan temporary file
    if process_id == "[CLEAR SCAN]":
        open("static/scan.Blue","w")
        with open("static/scan.Blue","r") as f:
            return render_template("scan_preview.html",scan = f.read().replace("/n","<br>"))

    #copy the scan temporary file to clipboard
    if process_id == "[COPY SCAN]":
        with open("static/scan.Blue","r") as f:
            copy(f.read())
        
            flash("Scan copied in your clipboard :D")

        with open("static/scan.Blue","r") as f:
            return render_template("scan_preview.html",scan = f.read().replace("/n","<br>"))    
    
    #copy an image to the clipboard with a win32 api
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

    #empty the history files
    if process_id == "[DEL HISTORY]":
        open("static/hist.Blue","w")
        open("static/dates.Blue","w")
        flash("Your scan History has been deleted :D")
        return redirect("/[SETTINGS]")


def image_process():
    #funtion run by another process to receive images
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("",8836))
    print("bound images")
    stdout.flush()
    while True:
        s.listen()
        cli,addr = s.accept()
        imgbytes = bytearray()
        print(addr)

        #make sure there is no old pic file
        if path.exists("static/imgscan.jpeg"):
            remove("static/imgscan.jpeg")

        #receive the image and store it to bytearray
        while True:
            b = cli.recv(1024)
            
            print(b)
            stdout.flush()

            if (b == b""):
                print("[OUICECIESTUNEFINFLAG]")
                stdout.flush()

                break
            else:
                imgbytes.extend(b)

        #save the bytearray to a real image file and display the preview
        image = Image.open(BytesIO(imgbytes))
        image.save("static/imgscan.jpeg")
        cli.close()
        Process(target=init_flask).start()

def start_image_proc():
    freeze_support()
    Process(target=image_process).start()