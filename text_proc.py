import socket
from flaskwebgui import FlaskUI
from flask import Flask, render_template, send_from_directory,send_file,request,redirect,flash
from multiprocessing import Process, freeze_support
from time import sleep
from sys import stdout
from datetime import date
from random import randint
from pyperclip import copy


app = Flask(__name__)

def init_flask():
    #init flask app and secret key
    ui = FlaskUI(app,port=8837)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    #specify the folder where the scan are uploaded
    app.config['UPLOAD_FOLDER'] = "static/"
    app.secret_key = b"6{#~@873gJHGZ@sfa54ZZEd^\\@#'"
    #open the gui
    ui.run()



#scan preview
@app.route("/",methods=["GET", "POST"])
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
            return render_template("scan_preview.html")
    
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




#funtion run by another process to receive text scan
def text_process():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("",8835))
    print("bound text")
    stdout.flush()

    #receive text scanned and put it to scan temporary file and h
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

            else:

                #scan temporary file
                with open("static/scan.Blue","a") as f:
                    f.write(b.decode("UTF-8"))
                
                #history file to store scans
                with open("static/hist.Blue","a") as f:
                    
                    f.write("\n=\n"+b.decode("UTF-8"))

                #history file to store dates
                with open("static/dates.Blue","a") as f:
                    today = date.today()
                    f.write(str(today.strftime("%d/%m/%Y"))+"\n")

            Process(target=init_flask).start()
            s.close()


def start_text_proc():

    freeze_support()
    Process(target=text_process).start()