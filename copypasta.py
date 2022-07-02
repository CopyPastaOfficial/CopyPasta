import sys
import socket
from flask import Flask, render_template, abort,jsonify,send_file,request,redirect,flash
from itsdangerous import json
from requests import get
from os import path,remove, startfile, rename,chdir
import PIL.Image as Image
from io import BytesIO
try:
    import win32clipboard
except ImportError:
    pass
from pyperclip import copy
from util import *
from multiprocessing import Process, freeze_support
from werkzeug.utils import secure_filename
from datetime import date
from pyautogui import write as send_keystrokes
from flask_cors import CORS, cross_origin
from re import findall

#waitress wsgi server

from waitress import serve
from webtest.http import StopableWSGIServer

# to generate app secret key
from random import choice
from string import printable

#init flask app and secret key
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, support_credentials=True, resources={r"/": {"origins": ["http://127.0.0.1:21987","http://copypasta.me"]}})

app.secret_key = "".join([choice(printable) for _ in range(256)])



# init waitress wsgi server
webserv = StopableWSGIServer(app)



if getattr(sys, 'frozen', False):
    APP_PATH = path.dirname(sys.executable)
elif __file__:
    APP_PATH = path.dirname(__file__)


chdir(APP_PATH)

#check if the necesarry files exists, if not download and/or create them.
if not path.exists("templates/"):
    emergency_redownload()


if not path.exists("static/"):
    emergency_redownload()


def check_exe_name():
    if path.basename(__file__).replace(".py",".exe") != "copypasta.exe":
        rename(path.basename(__file__).replace(".py",".exe"),"copypasta.exe")


#specify the folder where the scan are uploaded
app.config['UPLOAD_FOLDER'] = "static/"



# copypasta url

if is_hosts_file_modified():
    
    COPYPASTA_URL = "http://copypasta.me" if system() == "Windows" else "http://copypasta.me:21987"
    
else:
    
    COPYPASTA_URL = "http://127.0.0.1:21987"

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
@cross_origin()
def home():

    if request.remote_addr == "127.0.0.1":


        if not path.exists("static/history.xml"):
            
            init_history_file()
            
            
        #render the html with the history
        return render_template("index.html",copypasta_url=COPYPASTA_URL,server_version=get_server_version(),hist = get_history(),ip=get_private_ip(),hostname=socket.gethostname(),tab=path.exists("static/tab"))

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

        try:
            image_id = request.args.get("image_id",type=int)
        except:
            return jsonify({"error":"wrong image_id argument type/no argument passed"})

        image_path = get_history_file_by_id(image_id)
        
        
        if not image_path:
            return jsonify({"error":"this id does not belongs to any file"})
        else:
            image_path = image_path["path"]

        return render_template("img_preview.html",image_path=image_path,image_id=image_id)
    
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
            return send_file('static/scan.Blue',download_name=title+".txt",as_attachment=True)        
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
        if "[DELETE_FILE_FROM_HIST]" in process_id:

            try:
                file_id = request.args.get("file_id",type=int)
            except:
                return jsonify({"error":"wrong file_id argument type/no argument passed"})
            
            file_path = get_history_file_by_id(file_id)
            
            if not file_path:
                
                return jsonify({"error":"this id does not belongs to any file"})

            remove(file_path['path'])

            delete_history_file_by_id(file_id)

            return redirect("/")

        #open an image preview from image history table
        if "[OPEN_IMAGE_SCAN_FROM_HIST]" in process_id:
            
            try:
                image_id = request.args.get("image_id",type=int)
            except:
                return jsonify({"error":"wrong image_id argument type/no argument passed"})
            
            image_path = get_history_file_by_id(image_id)
        
            if not image_path:
                return jsonify({"error":"this id does not belongs to any file"})
            
            else:
                
                image_path = image_path["path"]
            
            # try to secure the image path
            # if suspicious path, just go home
            if (not path.exists(image_path)) or (not image_path.startswith("static/files_hist/")) or (".." in image_path):
                return redirect("/")

            return redirect(f"/image_preview?image_id={image_id}")

        #copy scan from history page
        if "[COPY_SCAN_FROM_HIST]" in process_id:
            
            try:
                scan_id = request.args.get("scan_id",type=int)
            except:
                return jsonify({"error":"wrong scan_id argument type/no argument passed"})

            text = get_history_file_by_id(scan_id)
            
            if not text:
                return jsonify({"error":"this id does not belongs to any sacn"})
            
            text = text["text"]

            copy(text)

            return redirect("/")

        if "[DELETE_SCAN_FROM_HIST]" in process_id:
            
            try:
                scan_id = request.args.get("scan_id",type=int)
            except:
                return jsonify({"error":"wrong scan_id argument type/no argument passed"})
            
            delete_history_file_by_id(scan_id)

            return redirect("/")

        #download the image received
        if "[DOWNLOAD IMG]" in process_id:


            try:
                image_id = request.args.get("image_id",type=int)
            except:
                return jsonify({"error":"wrong image_id argument type/no argument passed"})
            
            image_path = get_history_file_by_id(image_id)
            
            
            if not image_path:
                return jsonify({"error":"this id does not belongs to any file"})
            
            else:
                
                image_path = image_path["path"]
            
            # try to secure the image path
            # if suspicious path, just go home
            if (not path.exists(image_path)) or (not image_path.startswith("static/files_hist/")) or (".." in image_path):
                return redirect("/")

            return send_file(image_path,
            download_name=secure_filename(image_path.replace("static/files_hist/","")),
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

            notify_desktop("CopyPasta","scan copied to clipboard :D")
            #redirect to the usual scan preview
            return redirect("/scan_preview")

        #copy an image to the clipboard with a win32 api
        if "[COPY IMG]" in process_id:

            try:
                image_id = request.args.get("image_id",type=int)
            except:
                return jsonify({"error":"wrong image_id argument type/no argument passed"})
            
            image_path = get_history_file_by_id(image_id)
            
            if not image_path:
                return jsonify({"error":"this id does not belongs to any file"})
            
            else:
                
                image_path = image_path["path"]
            

            # try to secure the image path
            # if suspicious path, just go home
            if (not path.exists(image_path)) or (not image_path.startswith("static/files_hist/")) or (".." in image_path):
                return redirect("/")

            try:
                output = BytesIO()
                image = Image.open(image_path)
                image.convert('RGB').save(output, 'BMP')
                data = output.getvalue()[14:]
                output.close()
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()

                return redirect(f"/image_preview?image_id={image_id}")

            except ImportError:
                return redirect(f"/image_preview?image_id={image_id}")



        #empty the history files
        if process_id == "[DEL HISTORY]":
            init_history_file(force=True)
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

            Process(target=startfile,args=(f"{APP_PATH}/static/files_hist",)).start()
            return redirect("/")

        if process_id == "[OPEN FILE]":
            
            Process(target=startfile,args=("{}/{}".format(APP_PATH,request.args.get("file_path")),)).start()

            return redirect("/")


        if process_id == "[COPY WIFI PW]":

            copy(get_history_file_by_id(int(request.args.get("scan_id")))['password'])

            return redirect("/")


        if process_id == "[COPY CONTENT]":
            
            copy(get_history_file_by_id(int(request.args.get("scan_id")))['content'])

        
        if process_id == "[OPEN VIDEO]":
            file_path = request.args.get('file_path')
            
            
            # try to secure the file path
            # if suspicious path, just go home
            if (not path.exists(file_path)) or (not file_path.startswith("static/files_hist/")) or (".." in file_path):
                return redirect("/")
            
            
            return render_template("video_preview.html",file_path=file_path)
    else:
        return abort(403)







#api url(s)

@app.route("/api/<api_req>")
@cross_origin()
def api(api_req):
    
    if request.remote_addr == "127.0.0.1":


        if api_req == "get_history":

            return get_history()

        elif api_req == "ping":

            return "pong"

        elif api_req == "get_private_ip":

            return get_private_ip()

        elif api_req == "update_ip":
            
            
            if not is_online():
                return "You are offline :/"
            
            #create a qr code containing the ip with google chart api
            r = get("https://chart.googleapis.com/chart?cht=qr&chs=300x300&chl="+make_qr_url(),allow_redirects=True)
                
            
            try:
                remove("static/qr.jpeg")
            except:
                pass
            #write it
            with open("static/qr.jpeg","wb") as f:
                f.write(r.content)
                f.close()

            notify_desktop("Network change detected !","Updating you qr code, you need to rescan it ;)")
            return jsonify({"new_ip" : "updating qr code and private ip"})
        
        elif api_req == "shutdown_server": 
            webserv.shutdown()
            
            remove_copypasta_port_redirect()
                      
            return jsonify({"success":"shutting down CopyPasta server..."})
        
        else:
            return jsonify({"error" : "wrong api call"})
        
        
    else:

        if api_req == "ping":

            return "pong"

        else:
            return abort(403)







@app.route("/upload",methods=["POST"])

def upload():

    if request.method == "POST":
        
        notify_desktop("New scan Incoming !", "Click to open CopyPasta")

        r = request.get_json()

        time = date.today().strftime("%d/%m/%Y")

        if r != None:

            try:
                file_type = r['type']
                r = r['content']
            except:
                return jsonify({"upload_status" : "false","error":"malformed json"}), 400

            if file_type == "text":
                
                file_content = r
        
                
                #detect urls in text scan
                regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                urls = findall(regex,str(file_content))

                #detect email in text scan
                emails =  findall(r'[\w\.-]+@[\w\.-]+', file_content)
                
                rest = str(file_content)
                
                for url in urls:
                    store_to_history({"file_type" : "url","url" : f"{url[0]}", "date" : f"{time}"})
                    rest = rest.replace(url[0],"",1)

                for email in emails:

                    store_to_history({"file_type" : "email","addr" : f"{email}", "subject" : f"", "content" : f"", "date" : f"{time}"})




                #after url detection, store the whole text as scan
                if rest != "":
                    with open(f"{app.config['UPLOAD_FOLDER']}/scan.Blue","w") as f:
                        f.write(file_content)
                        f.close()

                    store_to_history({ "file_type" : f"{file_type}", "date" : f"{time}","text" : f"{file_content}"})


                    open_browser_if_settings_okay("http://127.0.0.1:21987/scan_preview")
                

                return jsonify({"upload_status" : "true"})

            elif file_type == "keystrokes":


                keystrokes = r['text']
                send_keystrokes(keystrokes)

                return jsonify({"upload_status" : "true"})

            elif file_type == "wifi":

                ssid = r['ssid']
                enctype = r['encryption']
                password = r['key']

                store_to_history({"file_type" : "wifi", "ssid" : f"{ssid}","password" : f"{password}", "enctype" : f"{enctype}", "date" : f"{time}"})

                return jsonify({"upload_status" : "true"})


            elif file_type == "isbn":

                isbn = r
                
                store_to_history({"file_type" : "isbn", "content" : f"{isbn}", "date" :f"{time}","isbn_lookup":identify_product(isbn)})
                
                return jsonify({"upload_status" : "true"})


            elif file_type == "email":

                store_to_history({"file_type" : "email","addr" : f"{r['address']}", "subject" : f"{r['subject']}", "content" : f"{r['content']}", "date" : f"{time}"})

                return jsonify({"upload_status" : "true"})


            elif file_type == "url":

                store_to_history({"file_type" : "url","url" : f"{r}", "date" : f"{time}"})

                return jsonify({"upload_status" : "true"})

            elif file_type == "phone":

                store_to_history({"file_type" : "phone","phone_number" : f"{r}", "date" : f"{time}"})

                return jsonify({"upload_status" : "true"})

            elif file_type == "sms":

                store_to_history({"file_type" : "sms","phone_number" : f"{r['number']}", "content": f"{r['content']}", "date" : f"{time}"})

                return jsonify({"upload_status" : "true"})

            elif file_type == "location":
                lat = r['lattitude']
                long = r['longitude']

                store_to_history({"file_type" : "location", "lat" : f"{lat}", "long" : f"{long}", "date" : f"{time}"})            
            
            elif file_type == "contact":
                
                store_to_history({"file_type" : "contact", "first_name" : f"{r['firstName']}", "name" : f"{r['name']}", "organization" : f"{r['organization']}", "job" : f"{r['title']}"})


            else:

                return jsonify({"upload_status" : "false","error" : "unknown type"}), 400


        #multipart request (files)
        else:


            files = request.files.getlist("files")


            #go and store each files
            for file in files :
                # If the user does not select a file, the browser submits an
                # empty file without a filename.
                if file.filename == '':

                    flash('No selected file')
                    return jsonify({"upload_status" : "false"})

                #store file to static/files_hist and metadata to history
                elif file :
                    filename = secure_filename(file.filename)
                    file_type = filename.split(".")[-1]
                    full_path = "{}{}/{}".format(app.config['UPLOAD_FOLDER'],"files_hist",filename)
                    
                    #rename file if one has already its name
                    i = 0
                    while(path.exists(full_path)):
                        full_path = "{}{}/{}".format(app.config['UPLOAD_FOLDER'],"files_hist", path.splitext(filename)[0]+str(i)+"."+filename.split(".")[-1])
                        i += 1
                    
                    file.save(full_path)
                    store_to_history({"file_name" : f"{file.filename}","file_type" : f"{file_type}","date" : f"{time}","path" : f"{full_path}"})

                    if is_image(file_type):
                        open_browser_if_settings_okay(f"{COPYPASTA_URL}/image_preview?image_id={get_history_file_last_id()}")
                        
            return jsonify({"upload_status" : "true"})

    else:
        return abort(403)



if __name__ == "__main__":

    freeze_support()

    chdir(APP_PATH)

    #make sure we are in the right path


    if not is_server_already_running():
        
        
        if is_online():
            #create a qr code containing the ip with google chart api
            r = get("https://chart.googleapis.com/chart?cht=qr&chs=300x300&chl="+make_qr_url(),allow_redirects=True)
            

            #write it
            with open("static/qr.jpeg","wb") as f:
                f.write(r.content)
                f.close()

            #check if the templates are up-to-date
            check_templates_update()

    #open tab in web browser
    
    
    Process(target=open_link_process, args=(COPYPASTA_URL,)).start()

    if not is_server_already_running():
        
        #run waitress web server
        webserv.create(app,host="0.0.0.0",port=21987)
        webserv.run()
        
