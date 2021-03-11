import socket
from flask import Flask, render_template, send_from_directory,send_file,request,redirect,flash
from requests import get
from os import path, chdir, mkdir,remove
import PIL.Image as Image
from io import BytesIO
try:
    import win32clipboard
except ImportError:
    pass
from array import array
from pyperclip import copy
from time import sleep
from random import randint
from platform import system
#from flaskwebgui import FlaskUI
from image_proc import start_image_proc
from text_proc import start_text_proc
from util import make_qr_url
from webbrowser import open as display_website
from multiprocessing import Process, freeze_support
from time import sleep


#init flask app and secret key
app = Flask(__name__)
#ui = FlaskUI(app,port=21053)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = b"6{#~@873gJHGZ@sfa54ZZEd^\\@#'"



#check if the necesarry files exists, if not download and/or create them.
if not path.exists("static/"):
    mkdir("static")
    open("static/hist.Blue","w")
    open("static/dates.Blue","w")



if not path.exists("templates/"):
    mkdir("templates")

    r = get("https://raw.githubusercontent.com/thaaoblues/copypasta/master/templates/index.html",allow_redirects=True)
    with open("templates/index.html","wb") as f:
        f.write(r.content)

    r = get("https://raw.githubusercontent.com/thaaoblues/copypasta/master/templates/scan_preview.html",allow_redirects=True)
    with open("templates/scan_preview.html","wb") as f:
        f.write(r.content)

    r = get("https://raw.githubusercontent.com/thaaoblues/copypasta/master/templates/settings.html",allow_redirects=True)
    with open("templates/settings.html","wb") as f:
        f.write(r.content)

    r = get("https://raw.githubusercontent.com/thaaoblues/copypasta/master/templates/favicon.ico",allow_redirects=True)
    with open("templates/favicon.ico","wb") as f:
        f.write(r.content)



#specify the folder where the scan are uploaded
app.config['UPLOAD_FOLDER'] = "static/"



#necessary to update images (stack overflow)
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response



#home
@app.route("/")
def home():
    #read history files, convert it to an array and reverse it to have the most recent first
    with open("static/hist.Blue","r") as f:
        a = f.read()
        a = a.split("=")
        a.reverse()

        with open("static/dates.Blue","r") as f:
            dates=f.read().split("\n")
            dates.reverse()
        
            #render the html with the history
            qr_url = "static/qr.jpeg"
            return render_template("index.html",hist = a, len = len(a),dates=dates,qr_url = qr_url)



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

#settings page
@app.route("/[SETTINGS]")
def settings():

    return render_template("settings.html")

#image preview when the user send a picture
@app.route("/image_preview")
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
            f.close()
        with open("static/scan.Blue","r") as f:
            return render_template("scan_preview.html",scan = f.read().replace("/n","<br>"))
    
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


def open_tab():
    sleep(1)
    display_website("http://127.0.0.1:21987")




if __name__ == "__main__":

    freeze_support()
    
    #make sure we are in the right path
    chdir(path.abspath(__file__).replace("main.py","").replace("main.exe","").replace("copypasta.exe","").replace("copypasta.py",""))

    #create a qr code containing the ip with google chart api
    r = get("https://chart.googleapis.com/chart?cht=qr&chs=300x300&chl="+make_qr_url(),allow_redirects=True)
    

    #write it
    with open("static/qr.jpeg","wb") as f:
        f.write(r.content)


    start_image_proc()
    start_text_proc()

    #open tab in web browser
    Process(target=open_tab).start()


    #run flask web server
    app.run(host="127.0.0.1",port=21987)





    
    

