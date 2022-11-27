import sys
import socket
from flask import Flask, after_this_request, render_template, abort,jsonify,send_file,request,redirect,flash
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from requests import get
from os import path,remove, startfile, rename,chdir
import PIL.Image as Image
from io import BytesIO
from shutil import copyfile
from urllib.parse import quote as url_encode
import client as pc_client
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


# socket io for real time speeeeeed
from flask_socketio import SocketIO
# necessary to compile -__(°-°)__-
from engineio.async_drivers import gevent


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


# init socketio
socketio = SocketIO(app,async_mode="gevent")


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
        return render_template("index.html",copypasta_url=COPYPASTA_URL,server_version=get_server_version(),hist = get_history_json(),ip=get_private_ip(),hostname=socket.gethostname(),tab=path.exists("static/tab"),upload_code=get_upload_code(APP_PATH))


    else:
        return abort(403)



@app.route("/hist/<i>")
def history(i):
    """
    :params: i is the index of the scan on the history list, given when and user click on a button

    """
    if request.remote_addr == "127.0.0.1":

        try:
            i = int(i)
        except ValueError:
            return jsonify({"Error","Invalid url variable. Here, it must be an integer."})
            
            
        file_data = get_history_file_by_id(i)
        
        if not file_data:
            return jsonify({"Error":"This scan id does not exists."})

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
        except ValueError:
            return jsonify({"Error":"wrong image_id argument type/no argument passed"})

        image_path = get_history_file_by_id(image_id)
        
        
        if not image_path:
            return jsonify({"Error":"this id does not belongs to any file"})
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
    
    
    
# real time processes (socketio)
@socketio.on("[DELETE_FILE_FROM_HIST]")
def delete_file_from_hist(json):
    
    file_info = get_history_file_by_id(json["file_id"])
    
    # this id doest not belongs to any file
    if not file_info:
        return
    
    # check if file haven't been deleted by another process (we never know ^^)
    if path.exists(file_info["path"]):
        remove(file_info["path"])

    delete_history_file_by_id(json["file_id"])
    
    
    # now tell the page to refresh its history content
    socketio.emit("fill_history_tab",get_history_json())
    
    
    
#copy scan from history page
@socketio.on("[COPY_SCAN_FROM_HIST]")
def copy_scan_from_hist(json_data:dict):


    text = get_history_file_by_id(json_data["scan_id"])
    
    if not text:
        return jsonify({"Error":"this id does not belongs to any sacn"})
    
    copy(text["text"])
    
    socketio.emit("[NOTIFY_USER]",{"msg":"Scan copied !"})


@socketio.on("[DELETE_SCAN_FROM_HIST]")
def delete_scan_from_hist(json_data:dict):
    
    
    delete_history_file_by_id(json_data["scan_id"])
    
    # now tell the page to refresh its history content
    socketio.emit("fill_history_tab",get_history_json())
    
    # and notify user ;)
    socketio.emit("[NOTIFY_USER]",{"msg":"File deleted from history"})

#empty the history files
@socketio.on("[DEL_HISTORY]")
def del_history(json_data:dict):
 

    init_history_file(force=True)
    
    # now tell the page to refresh its history content
    socketio.emit("fill_history_tab",get_history_json())
    
    
    socketio.emit(["NOTIFY_USER"] ,{"msg" : "History deleted !"})
    
    
#open new tab on scan received or not
@socketio.on("[CHANGE_TAB_SETTINGS]")
def change_tab_settings(json_data:dict):
    
    if path.exists("static/tab"):
        remove("static/tab")
    else:
        open("static/tab","w")

    socketio.emit("[NOTIFY_USER]",{"msg":"Settings changed !"})


# open files explorer into the the copypasta directory
socketio.on("[OPEN_FILES_EXPLORER]")
def open_files_explorer(json_data:dict):
    
    Process(target=startfile,args=(f"{APP_PATH}/static/files_hist",)).start()
    
    socketio.emit("[NOTIFY_USER]",{"msg":"Opening your files explorer..."})


# open a file with default app
socketio.on("[OPEN_FILE]")
def open_file(json_data:dict):
    
            

    json_dict = get_history_file_by_id(json_data["file_id"])
    
    if not json_dict: # id does not exists
        socketio.emit("[NOTIFY_USER]",{"msg":"This file does not exists."})
        return
    
    Process(target=startfile,args=("{}/{}".format(APP_PATH,json_dict["path"]),)).start()
    
    socketio.emit("[NOTIFY_USER]",{"msg":"Opening your file in the default app..."})



socketio.on("[COPY_WIFI_PW]")
def copy_wifi_pw(json_data:dict):
            

    json_dict = get_history_file_by_id(json_data["scan_id"])
    
    if not "content" in json_dict.keys():
        socketio.emit("[NOTIFY_USER]",{"msg":"this kind of scan cannot be copied to clipboard"})
        
        return
            
    copy(json_dict['password'])

    socketio.emit("[NOTIFY_USER]",{"msg":"Wifi password copied to clipboard !"})

    

# copy text scan content
socketio.on("[COPY_CONTENT]")
def copy_text_scan_content(json_data:dict):
            
            
    json_dict = get_history_file_by_id(json_data["scan_id"])
    
    if not "content" in json_dict.keys():
        
        socketio.emit("[NOTIFY_USER]",{"msg":"this kind of scan cannot be copied to clipboard"})
        return
        
    # finally, if nothing is wrong, copy the scan content
    copy(json_dict["content"])
    socketio.emit("[NOTIFY_USER]",{"msg":"Scan copied to clipboard !"})
    
    
@socketio.on("[SHUTDOWN_SERVER]")
def shutdown_server(json_data:dict):
    
    socketio.emit("[NOTIFY_USER]",{"msg":"CopyPasta server is now off. You may close this tab."})
    
    socketio.stop()
    


#empty the scan temporary file
@socketio.on("[CLEAR_LAST_SCAN]")
def clear_last_scan(json_data:dict):
    
    # overwrite the temp scan file
    with open("static/scan.Blue","w") as f:
        f.close()
    
    socketio.emit("[CLEAR_LAST_SCAN]")

#copy the scan temporary file to clipboard
@socketio.on("[COPY_LAST_SCAN]")
def copy_last_scan(json_data:dict):

    with open("static/scan.Blue","r") as f:
        copy(f.read())
        f.close()

    notify_desktop("CopyPasta","scan copied to clipboard :D")
                




#processes
@app.route("/process/<process_id>")
def process(process_id):

    if request.remote_addr == "127.0.0.1":

        #open an image preview from image history table
        if "[OPEN_IMAGE_SCAN_FROM_HIST]" in process_id:
            
            try:
                image_id = request.args.get("image_id",type=int)
            except ValueError:
                return jsonify({"Error":"wrong image_id argument type/no argument passed"})

            return redirect(f"/image_preview?image_id={image_id}")

        

        #download the image received
        if "[DOWNLOAD_IMG]" in process_id:


            try:
                image_id = request.args.get("image_id",type=int)
            except ValueError:
                return jsonify({"Error":"wrong image_id argument type/no argument passed"})
            
            image_path = get_history_file_by_id(image_id)
            
            
            if not image_path:
                return jsonify({"Error":"this id does not belongs to any file"})
            
            image_path = image_path["path"]

            return send_file(image_path,
            download_name=secure_filename(image_path.replace("static/files_hist/","")),
            as_attachment=True)


        
        

        #copy an image to the clipboard with a win32 api
        if "[COPY_IMG]" in process_id:

            try:
                image_id = request.args.get("image_id",type=int)
            except:
                return jsonify({"Error":"wrong image_id argument type/no argument passed"})
            
            image_path = get_history_file_by_id(image_id)
            
            if not image_path:
                return jsonify({"Error":"this id does not belongs to any file"})
            
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

        if process_id == "[HOME]":

            #redirect to homepage
            return redirect("/")
        
        if process_id == "[OPEN_VIDEO]":
            
            try:
                video_id = request.args.get('video_id',type=int)
            except ValueError:
                return jsonify({"Error":"invalid url argument"})
            
            if video_id <= get_history_file_last_id():
                file_path = get_history_file_by_id(video_id)["path"]
                
            else: # id does not exists
                return jsonify({"Error":"invalid url argument"})
            
            
            return render_template("video_preview.html",file_path=file_path)
    else:
        return abort(403)




#api url(s)

@app.route("/api/<api_req>")
@cross_origin()
def api(api_req):
    
    if request.remote_addr == "127.0.0.1":

        if api_req == "ping":

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
        
        
        elif api_req == "gen_otdl_url":
            
            # keep main window hidden
            root = Tk()
            root.attributes("-topmost", True)
            root.withdraw()
            # open file dialog
            file_path = askopenfilename(parent=root)
            
            if not file_path:
                return jsonify({"Error":"no file selected"})
                
            
            if not path.exists("static/ot_upload"):
                mkdir("static/ot_upload")
            
            #move file in a downloadable directory
            copyfile(file_path,path.join(APP_PATH,f"static/ot_upload/{path.basename(file_path)}"))
            
            # return url to javascript for qr code generation and notification
            safe_arg = url_encode(url_encode(path.basename(file_path))) # twice because google charts api will transform it once before qr generation
            return f"http://{get_private_ip()}:21987/download/main_page?file={safe_arg}"
        else:
            return jsonify({"Error" : "wrong api call"})
        
    else:

        if api_req == "ping":

            return "pong"

        else:
            return abort(403)


@app.route("/download/<action>",methods=["GET"])

def download(action):
    
    try:
        file = request.args.get("file",type=str)
    except:
        return jsonify({"Error":"Invalid url parameter"})
    
    if action == "main_page":
        return render_template("download_page.html",file=url_encode(file))
    
    elif action == "send_file":
        @after_this_request
        def delete_ot_dl(response):
            
            if path.exists(path.join(APP_PATH,"static","ot_upload",file)):
                Process(target=delete_ot_dl_proc,args=(APP_PATH,file,)).start()

            return response
        
        
        file_path = path.join(APP_PATH,"static","ot_upload",file)
        if path.exists(file_path):
            return send_file(file_path,as_attachment=True)
        else:
            return jsonify({"Error":"This file does not exists or have already been downloaded one time."})
        
    else:
        return jsonify({""})


@app.route("/upload",methods=["POST"])

def upload():

    if request.method == "POST":
        

        r = request.get_json(silent=True)
        time = date.today().strftime("%d/%m/%Y")

        # check upload code validity
        """upload_code = request.args.get("code",default="[NO CODE]",type=str)
        if not is_upload_code_valid(APP_PATH,upload_code):
            return jsonify({"Error":"Invalid upload code"}),403"""

        notify_desktop("New scan Incoming !", "Click to open CopyPasta")
        
        socketio.emit("[NOTIFY_USER]",{"msg":"New scan Incoming !"})
        socketio.emit("fill_history_tab",get_history_json())


        if r != None:

            try:
                file_type = r['type']
                r = r['content']
            except:
                return jsonify({"upload_status" : "false","Error":"malformed json"}), 400

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

                return jsonify({"upload_status" : "false","Error" : "unknown type"}), 400


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



# new feature, pc-to-pc
@app.route("/client",methods=["GET","POST"])

def client():
    
    # obviously only allowed from the current computer
    if request.remote_addr == "127.0.0.1":
        msg = ""

        if request.method == "POST":
            
            msg = "Document sent !"

            try:
                scan_type = request.form.get("type",type=str)
                ip_addr = request.form.get("pc_ip_addr",type=str)
                upload_code = request.form.get("upload_code",type=str)
            except ValueError:
                return render_template("send_client.html",msg="erreur, champs non remplis")



            if scan_type == "text":
                try:
                    scan_ctt = request.form.get("text_content",type=str)
                except ValueError:
                    return render_template("send_client.html",msg="ValueError")

                if not pc_client.send_text_scan(scan_ctt,ip_addr,upload_code):
                    msg = "/!\ Invalid upload code or client offline /!\\"



            elif scan_type == "file":
                files = request.files.getlist("files_input")

                #go and store each files
                for file in files :
                    
                    # If the user does not select a file, the browser submits an
                    # empty file without a filename.
                    if file.filename == '':
                        flash('No selected file')
                        return jsonify({"upload_status" : "false"})

                    #store file in temporary folder and delete after request
                    elif file :
                        filename = secure_filename(file.filename)
                        
                        # create temp folder if it does not exists

                        if not path.exists("tmp"):
                            mkdir("tmp")
                            
                        # save the file into it
                        file.save(f"tmp/{filename}")

                        if not pc_client.send_file(f"tmp/{filename}",ip_addr,upload_code):
                            msg = " /!\ Invalid upload code or client offline /!\\"


                        # clear temporary file in 10s, but we don't sleep on main thread ^^
                        Process(target=clear_tmp,args=(filename,)).start()

        # finally, render the same page with a little message ;)
        return render_template("send_client.html",msg=msg)
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



    # code needed for another pc to upload on this machine
    upload_code = gen_upload_code()
    store_upload_code(APP_PATH,upload_code)

    
    Process(target=open_link_process, args=(COPYPASTA_URL,)).start()

    if not is_server_already_running():
        
        socketio.run(app,host="0.0.0.0",port=21987)
        


