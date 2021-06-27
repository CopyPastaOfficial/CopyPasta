import json
import socket
from flask import Flask, render_template, abort ,send_from_directory,send_file,request,redirect,flash
from requests import get
from os import path, chdir, mkdir,remove,listdir, startfile
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
from util import *
from webbrowser import open as display_website
from multiprocessing import Process, freeze_support
from json import dumps
from werkzeug.utils import secure_filename
from datetime import date


#init flask app and secret key
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "CF3gNqD#%#MpSs=7J!VmM2KxWCWhGwjSP%pc*4G?XuUU4s6CC=2KcUba4WPA#EhhZ52gyU57_nF6cDM*_B9X7FpPH%^-c+c8naZSx2$atBwS?V"

APP_PATH = path.abspath(__file__).replace("main.py","").replace("main.exe","").replace("copypasta.exe","").replace("copypasta.py","")


#store_to_history("""{"file_type" : "text_scan","date" : "time","text" : "ahaha lol ça fonctionne un peu"}""")

#check if the necesarry files exists, if not download and/or create them.
if not path.exists("templates/"):
    emergency_redownload()


if not path.exists("static/"):
    emergency_redownload()



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

    if request.remote_addr == "127.0.0.1":

        #render the html with the history
        return render_template("index.html",hist = get_history(),ip=get_private_ip(),hostname=socket.gethostname(),tab=path.exists("static/tab"),)

    else:
        return abort(403)



@app.route("/hist/<i>")
def history(i):
    """
    :params: i is the index of the scan on the history list, given when and user click on a button

    """
    if request.remote_addr == "127.0.0.1":


        file_data = get_history_file_by_id(int(i))

        #rewrite the scan temporary file with the old scan
        with open("static/scan.Blue","w") as f:
            f.write(file_data['text'])

        #redirect to the usual scan preview
        return redirect("/scan_preview")

    else:
        return abort(403)



#image preview when the user send a picture
@app.route("/image_preview")
def img_preview():
    if request.remote_addr == "127.0.0.1":


        img_path = request.args.get("path")

        return render_template("img_preview.html",img_path=img_path)
    else:
        return abort(403)

#scan preview
@app.route("/scan_preview",methods=["GET", "POST"])
def scan_preview():

    if request.remote_addr == "127.0.0.1":


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
    
    else:
        return abort(403)


#processes
@app.route("/process/<process_id>")
def process(process_id):

    if request.remote_addr == "127.0.0.1":


        #delete a particular image from history table
        if "[DELETE_IMAGE_SCAN_FROM_HIST]" in process_id:

            img_path = request.args.get("path")
            img_id = int(request.args.get("image_id"))


            remove(img_path)
            delete_history_file_by_id(img_id)

            return redirect("/")

        #open an image preview from image history table
        if "[OPEN_IMAGE_SCAN_FROM_HIST]" in process_id:
            img_path = request.args.get("path")

            return redirect(f"/image_preview?path={img_path}")

        #copy scan from history page
        if "[COPY_SCAN_FROM_HIST]" in process_id:
            
            id = request.args.get("scan_id")

            text = get_history_file_by_id(int(id))['text']

            copy(text)

            return redirect("/")

        if "[DELETE_SCAN_FROM_HIST]" in process_id:
            id = request.args.get("scan_id")
            delete_history_file_by_id(int(id))

            return redirect("/")

        #download the image received
        if "[DOWNLOAD IMG]" in process_id:

            img_path = request.args.get("path")

            return send_file(img_path,
            attachment_filename=img_path.replace("static/files_hist/",""),
            as_attachment=True)

        #empty the scan temporary file
        if process_id == "[CLEAR SCAN]":
            open("static/scan.Blue","w")

            #redirect to the usual scan preview
            return redirect("/scan_preview")

        #copy the scan temporary file to clipboard
        if process_id == "[COPY SCAN]":

            with open("static/scan.Blue","r") as f:
                copy(f.read())
                f.close()

            flash("scan copied to clipboard :D")
            #redirect to the usual scan preview
            return redirect("/scan_preview")

        #copy an image to the clipboard with a win32 api
        if "[COPY IMG]" in process_id:

            img_path = request.args.get("path")


            try:
                output = BytesIO()
                image = Image.open(img_path)
                image.convert('RGB').save(output, 'BMP')
                data = output.getvalue()[14:]
                output.close()
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()

                flash("Image copied to clipboard :D")

                return redirect(f"/image_preview?path={img_path}")

            except ImportError:
                return redirect(f"/image_preview?path={img_path}")



        #empty the history files
        if process_id == "[DEL HISTORY]":
            init_history_file()
            return redirect("/")


        if process_id == "[HOME]":

            #redirect to homepage
            return redirect("/")


        if process_id == "[CHANGE TAB SETTINGS]":
            if path.exists("static/tab"):
                remove("static/tab")
            else:
                open("static/tab","w")

            return "OK"

        if process_id == "[OPEN FILES EXPLORER]":

            Process(target=startfile,args=(f"{APP_PATH}static/files_hist",)).start()
            return redirect("/")

        if process_id == "[OPEN FILE]":
            
            Process(target=startfile,args=("{}{}".format(APP_PATH,request.args.get("file_path")),)).start()

            return redirect("/")
    else:
        return abort(403)


#api url(s)

@app.route("/api/<api_req>")
def api(api_req):

    if request.remote_addr == "127.0.0.1":


        if api_req == "get_history":

            return get_history()
    else:
        return abort(403)



@app.route("/upload",methods=["POST"])

def upload():

    if request.method == "POST":

        r = request.get_json()

        time = date.today().strftime("%d/%m/%Y")

        if r != None:

            file_type = r['file_type']

            if file_type == "text_scan":
                
                file_content = r['text']
                time = r['date']

                append_to_scan_file(file_content)


                with open(f"{app.config['UPLOAD_FOLDER']}/scan.txt","w") as f:
                    f.write(file_content)
                    f.close()

                store_to_history("{"+f"\"file_type\" : \"{file_type}\",\"date\" : \"{time}\",\"text\" : \"{file_content}\""+"}")

                open_browser_if_settings_okay("http://127.0.0.1:21987/scan_preview")
                

                return "{\"upload_status\" : \"true\"}"

        else:


            files = request.files.getlist("file")

            for file in files :
                # If the user does not select a file, the browser submits an
                # empty file without a filename.
                if file.filename == '':

                    flash('No selected file')
                    return "{\"upload_status\" : \"false\"}"

                elif file :
                    filename = secure_filename(file.filename)
                    file_type = filename.split(".")[-1]
                    file.save(path.join(app.config['UPLOAD_FOLDER'],"files_hist", filename))
                    file_path = path.join(app.config['UPLOAD_FOLDER'],"files_hist", filename).replace("\\","/")
                    store_to_history("{"+f"\"file_name\" : \"{file.filename}\",\"file_type\" : \"{file_type}\",\"date\" : \"{time}\",\"path\" : \"{file_path}\""+"}")

                    open_browser_if_settings_okay(f"http://127.0.0.1:21987/image_preview?path={path}")
                    
            return "{\"upload_status\" : \"true\"}"





if __name__ == "__main__":

    freeze_support()
    
    #make sure we are in the right path
    chdir(APP_PATH)

    #create a qr code containing the ip with google chart api
    r = get("https://chart.googleapis.com/chart?cht=qr&chs=300x300&chl="+make_qr_url(),allow_redirects=True)
    

    #write it
    with open("static/qr.jpeg","wb") as f:
        f.write(r.content)


    #check if the templates are up-to-date
    check_updates()

    #open tab in web browser
    Process(target=open_link_process, args=("http://127.0.0.1:21987",)).start()


    #run flask web server
    app.run(host="0.0.0.0",port=21987)





    
    

