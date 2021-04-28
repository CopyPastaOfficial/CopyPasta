import socket
from flaskwebgui import FlaskUI
from flask import Flask, render_template, send_from_directory,send_file,request,redirect,flash
from multiprocessing import Process, freeze_support
from time import sleep
from sys import stdout
from datetime import date
import PIL.Image as Image
from random import randint
try:
    import win32clipboard
except ImportError:
    pass
from io import BytesIO
from os import remove, path
from pyperclip import copy
from webbrowser import open as display_website
from random import randint
from datetime import date


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

        #save the bytearray to a real image file and display the preview, 
        # also update the history
        image = Image.open(BytesIO(imgbytes))
        full_name = "imgscan"+str(randint(0,167645454))+'.jpeg'
        image.save("static/imgscan.jpeg")
        image.save("static/images_hist/"+full_name)

        with open("static/images_hist.Blue","a") as f:
            today = date.today()
            today = str(today.strftime("%d/%m/%Y"))
            f.write(f"{full_name}:{today}\n")
            f.close()


        cli.close()

        #display_website("http://127.0.0.1:21987/image_preview/[static=imgscan.jpeg]")

def start_image_proc():
    freeze_support()
    Process(target=image_process).start()