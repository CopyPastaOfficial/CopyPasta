import socket
from flask import Flask, render_template, send_from_directory,send_file,request,redirect,flash
from requests import get
from os import path, chdir, mkdir,remove,listdir
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
from image_proc import start_image_proc
from text_proc import start_text_proc
from util import make_qr_url, get_private_ip, download_templates, check_updates, emergency_redownload
from webbrowser import open as display_website
from multiprocessing import Process, freeze_support
from time import sleep



#init flask app and secret key
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = b"6{#~@873gJHGZ@sfa54ZZEd^\\@#'"


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
    #read history files, convert it to an array and reverse it to have the most recent first
    with open("static/hist.Blue","r") as f:
        a = f.read()
        a = a.split("=")
        a.reverse()
        f.close()

    with open("static/dates.Blue","r") as f:
        dates=f.read().split("\n")
        dates.reverse()
        f.close()
    
    with open("static/images_hist.Blue") as f:
        images_dates = []
        images_hist = []
        for ele in f.read().split("\n")[:-1]:
            print(ele)
            ele = ele.split(":")
            images_dates.append(ele[1])
            images_hist.append(ele[0])
            f.close()
            

        
    #render the html with the history
    return render_template("index.html",hist = a, len1 = len(a),dates=dates,hostname=socket.gethostname(),ip=get_private_ip(),images_hist = images_hist,images_dates = images_dates,len2=len(images_dates))





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

#image preview when the user send a picture
@app.route("/image_preview/<img_path>")
def img_preview(img_path):
    
    return render_template("img_preview.html",img_path=img_path.strip("[").strip("]").replace("=","/"),img_path_formated=img_path)


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


    #wipe the images scan history
    if process_id == "[DEL_IMAGE HISTORY]":
        for file in listdir("static/images_hist/"):
            remove(file)

        return redirect("/")

    #delete a particular image from history table
    if "[DELETE_IMAGE_SCAN_FROM_HIST]" in process_id:
        process_id = process_id.replace("[DELETE_IMAGE_SCAN_FROM_HIST]","")
        with open("static/images_hist.Blue","r") as f:
            file_ctt = f.read()
            for line in file_ctt.splitlines():
                if process_id == line.split(":")[0]:
                    line_to_remove = line + "\n"

            f.close()

        
        with open("static/images_hist.Blue","w") as f:
            f.write(file_ctt.replace(line_to_remove,"",1))
            f.close()

        remove("static/images_hist/"+process_id)
        
        return redirect("/")

    #open an image preview from image history table
    if "[OPEN_IMAGE_SCAN_FROM_HIST]" in process_id:
        process_id = process_id.replace("[OPEN_IMAGE_SCAN_FROM_HIST]","")

        return redirect("/image_preview/[static=images_hist="+process_id.replace("/","=")+"]")

    #copy scan from history page
    if "[COPY_SCAN_FROM_HIST]" in process_id:
        process_id = process_id.replace("[COPY_SCAN_FROM_HIST]","")
        with open("static/hist.Blue","r") as f:
            a = f.read()
            a = a.split("=")
            a.reverse()
            text = a[int(process_id)]
            copy(text)
            f.close()
        flash("scan copied to clipboard :D")
        return redirect("/")

    if "[DELETE_SCAN_FROM_HIST]" in process_id:
        process_id = process_id.replace("[DELETE_SCAN_FROM_HIST]","")
        with open("static/hist.Blue","r") as f:
            a = f.read()
            a = a.split("=")
            a.reverse()
            text = "="+a[int(process_id)]
            f.close()
        
        with open("static/hist.Blue","r") as f:
            a = f.read()
            f.close()

        with open("static/hist.Blue","w") as f:
            f.write(a.replace(text,"",1))
            f.close()

        return redirect("/")

    #download the image received
    if "[DOWNLOAD IMG]" in process_id:
        process_id = process_id.replace("[DOWNLOAD IMG]","")
        return send_file(process_id.strip("[").strip("]").replace("=","/"),
                     attachment_filename=process_id.strip("[").strip("]").replace("=","/").replace("static/images_hist/",""),
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
            flash("Scan copied in your clipboard :D")
            f.close()

        flash("scan copied to clipboard :D")
        #redirect to the usual scan preview
        return redirect("/scan_preview")
    
    #copy an image to the clipboard with a win32 api
    if "[COPY IMG]" in process_id:
        process_id = process_id.replace("[COPY IMG]","")
        try:
            output = BytesIO()
            image = Image.open(process_id.strip("[").strip("]").replace("=","/"))
            image.convert('RGB').save(output, 'BMP')
            data = output.getvalue()[14:]
            output.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()

            flash("Image copied to clipboard :D")

            return redirect("/image_preview/"+process_id)
            
        except ImportError:
            return redirect("/image_preview/"+process_id)



    #empty the history files
    if process_id == "[DEL HISTORY]":
        open("static/hist.Blue","w")
        open("static/dates.Blue","w")
        flash("Your scan History has been deleted :D")
        return redirect("/[SETTINGS]")


    if process_id == "[HOME]":

        #redirect to homepage
        return redirect("/")


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

    #check if the templates are up-to-date
    check_updates()

    #open tab in web browser
    Process(target=open_tab).start()


    #run flask web server
    app.run(host="127.0.0.1",port=21987)





    
    

