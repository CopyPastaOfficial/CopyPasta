import socket
from flask import Flask, render_template, send_from_directory,send_file,request,redirect,flash
from multiprocessing import Process, freeze_support
from time import sleep
from sys import stdout
from datetime import date
from random import randint
from pyperclip import copy
from webbrowser import open as display_website


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
                display_website("http://127.0.0.1:21987/scan_preview")

                break

            else:

                #scan temporary file
                with open("static/scan.Blue","a") as f:
                    f.write(b.decode("UTF-8"))
                
                #history file to store scans
                with open("static/hist.Blue","a") as f:
                    
                    f.write(b.decode("UTF-8")+"\n=\n")

                #history file to store dates
                with open("static/dates.Blue","a") as f:
                    today = date.today()
                    f.write(str(today.strftime("%d/%m/%Y"))+"\n")

            display_website("http://127.0.0.1:21987/scan_preview")
            break

        cli.close()

        
            
            


def start_text_proc():

    freeze_support()
    Process(target=text_process).start()
