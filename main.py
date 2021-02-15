import socket
from flask import Flask, render_template, send_from_directory,send_file,request,redirect,flash
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
from datetime import date
from subprocess import run
from webbrowser import open as open_website
from platform import system
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
from OpenSSL import crypto, SSL

#init flask app and secret key
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = b"6{#~@873gJHGZ@sfa54ZZEd^\\@#'"



#check if the necesarry files exists, if not download and/or create them.
if not path.exists("static/"):
    mkdir("static")
    open("static/hist.blue","w")
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
    return render_template("index.html",hist = a, len = len(a),dates=dates)



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
    
    return render_template("img_preview.html")


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


#funtion run by another process to receive images
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
        open_browser("127.0.0.1/image_preview")


        cli.close()



#funtion run by another process to receive text scan
def listen_to_text_scan():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("",8835))
    print("bound text")
    stdout.flush()

    #receive text scanned and put it to scan temporary file and history files
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
                    open_browser("127.0.0.1/scan_preview")
                
                #history file to store dates
                with open("static/dates.Blue","a") as f:
                    today = date.today()
                    f.write(str(today.strftime("%d/%m/%Y"))+"\n")

def open_browser(url):
    #run(["rundll32","url.dll,FileProtocolHandler " + url],shell=True)
    if system() == "Windows":
        run(["start","msedge",url],shell=True)
        print("open")
    else:
        open_website(url)



def cert_gen(
    emailAddress="thaaoblues81@gmail.com",
    commonName="commonName",
    countryName="France",
    localityName="France",
    stateOrProvinceName="France",
    organizationName="Blue",
    organizationUnitName="inc",
    serialNumber=0,
    validityStartInSeconds=0,
    validityEndInSeconds=10*365*24*60*60,
    KEY_FILE = "private.key",
    CERT_FILE="selfsigned.crt"):
    #can look at generated file using openssl:
    #openssl x509 -inform pem -in selfsigned.crt -noout -text
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = countryName
    cert.get_subject().ST = stateOrProvinceName
    cert.get_subject().L = localityName
    cert.get_subject().O = organizationName
    cert.get_subject().OU = organizationUnitName
    cert.get_subject().CN = commonName
    cert.get_subject().emailAddress = emailAddress
    cert.set_serial_number(serialNumber)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(validityEndInSeconds)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha512')
    with open(CERT_FILE, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    with open(KEY_FILE, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))




if __name__ == "__main__":

    #suppport multiprocessing
    freeze_support()
    
    #make sure we are in the right path
    chdir(path.abspath(__file__).replace("main.py",""))
    #get the ip (pray that this is the right one and not some virutal machines)
    ip = str(socket.gethostbyname(socket.gethostname()))

    #create a qr code containing the ip with google chart api
    r = get("https://chart.googleapis.com/chart?cht=qr&chs=150x150&chl="+ip,allow_redirects=True)
    
    

    #write it
    with open("static/qr.jpeg","wb") as f:
        f.write(r.content)

    #start text scan server
    Process(target=listen_to_text_scan).start()

    #start images scan server
    Process(target=listen_to_file_scan).start()

    #generate ssl certificate
    #cert_gen()

    open_browser("127.0.0.1")

    #run flask web server
    app.run(host="127.0.0.1",port=80)
    

