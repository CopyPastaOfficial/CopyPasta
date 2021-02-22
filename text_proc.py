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


    #empty the scan temporary file
    if process_id == "[CLEAR SCAN]":
        open("static/scan.Blue","w")
        with open("static/scan.Blue","r") as f:
            a = f.read()
            leng = len(a.split("\n"))
            return render_template("scan_preview.html",scan = a.replace("/n","<br>"),len=leng)

    #copy the scan temporary file to clipboard
    if process_id == "[COPY SCAN]":
        with open("static/scan.Blue","r") as f:
            copy(f.read())
            flash("Scan copied in your clipboard :D")

        with open("static/scan.Blue","r") as f:
            a = f.read()
            leng = len(a.split("\n"))
            return render_template("scan_preview.html",scan = a.replace("/n","<br>"),len=leng)
    

    #empty the history files
    if process_id == "[DEL HISTORY]":
        open("static/hist.Blue","w")
        open("static/dates.Blue","w")
        flash("Your scan History has been deleted :D")
        return redirect("/[SETTINGS]")

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



#settings page
@app.route("/[SETTINGS]")
def settings():

    return render_template("settings.html")



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
