from socket import *
from requests import get
from json import loads

PORT = 21988

#print(get("http://127.0.0.1:21987/api/ping").text)

HTTP_REQ = b"GET /api/ping HTTP/1.1\r\nHost:www.example.com\r\n\r\n"

def t1():
    s = socket(AF_INET,SOCK_DGRAM)

    s.bind(('',0))
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    s.sendto(HTTP_REQ,('<broadcast>',PORT))
    print("packet sent")
    print(s.recv(10))

def t2():
    with socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP) as sock:
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        sock.sendto(b"ping", ("255.255.255.255", PORT))

        resp = sock.recv(1024).decode("utf-8")

        if resp.startswith("[PONG FLAG]"):
            resp = loads(resp.replace("[PONG_FLAG]",""))
            print(resp["ip_addr"])
            


t2()