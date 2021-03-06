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
from os import remove, path
from pyperclip import copy


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
    return render_template("img_preview.html",img_url="static\imgscan.jpeg")



#scan preview
@app.route("/scan_preview",methods=["GET", "POST"])
def scan_preview():

    #download file is post request
    if request.method == 'POST':
        #get the file title
        title = request.form.get("title")
        #send file
        return send_file('static/scan.Blue',attachment_filename=title+".txt",as_attachment=True)

    else:
        #read scan temp file, split it by lines and return it to the template
        with open("static/scan.Blue","r") as f:
            a = f.read()
            leng = len(a.split("\n"))
            return render_template("scan_preview.html",scan = a.replace("/n","<br>"),len=leng)


#settings page
@app.route("/[SETTINGS]")
def settings():

    return render_template("settings.html")




@app.route("/hist/<i>")
def history(i):
    """
    :params: i is the index of the scan on the history list, given when and user click on a button

    """

    #read scan history file, convert it to an array and get the specified scan
    with open("static/hist.Blue","r") as f:
        a = f.read()
        a = a.split("=")
        a.reverse()
    text = a[int(i)]

    #rewrite the scan temporary file with the old scan
    with open("static/scan.Blue","w") as f:
        f.write(text)

    #redirect to the usual scan preview
    return redirect("/scan_preview")




#processes
@app.route("/process/<process_id>")
def process(process_id):

    #download the image received
    if process_id == "[DOWNLOAD IMG]":
        return send_file('static/imgscan.jpeg',
                     attachment_filename='imgscan'+str(randint(0,167645454))+'.jpeg',
                     as_attachment=True)




    if process_id == "[HOME]":
        #read history files, convert it to an array and reverse it to have the most recent first
        with open("static/hist.Blue","r") as f:
            a = f.read()
            a = a.split("=")
            a.reverse()
            with open("static/dates.Blue","r") as f:
                dates=f.read().split("\n")
                dates.reverse()

                #render the html with the history
                qr_url = "../static/qr.jpeg"
                return render_template("index.html",hist = a, len = len(a),dates=dates,qr_url = qr_url)



    #copy an image to the clipboard with a win32 api
    if process_id == "[COPY IMG]":
        try:
            output = BytesIO()
            image = Image.open("static/imgscan.jpeg")
            image.convert('RGB').save(output, 'BMP')
            data = output.getvalue()[14:]
            output.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()

            return render_template("img_preview.html",img_url="..\static\imgscan.jpeg")
        except ImportError:
            pass 
        



        return render_template("img_preview.html",img_url="..\static\imgscan.jpeg")

    #empty the history files
    if process_id == "[DEL HISTORY]":
        open("static/hist.Blue","w")
        open("static/dates.Blue","w")
        flash("Your scan History has been deleted :D")
        return redirect("/[SETTINGS]")


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
            f.close()
        with open("static/scan.Blue","r") as f:
            return render_template("scan_preview.html",scan = f.read().replace("/n","<br>"))

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
            b = cli.recv(9999)
            
            if (b == b""):
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