from util import get_private_ip
import socket
from json import loads
from multiprocessing import Process


class Server():





    def __init__(self) -> None:
        """
        a simple server responding to udb ping on port 21988
        and sending ping requests to discover others copypasta instances on the local network
        """

        self.port = 21987

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)



    def response_loop(self,PORT:int,sock:socket.socket):



        msg = ("[PONG FLAG]{ip_addr:\""+get_private_ip() +"\"}").encode("utf-8")

        PORT = 21988
        sock.bind(('',21988))

        while True:
            if sock.recv(1024) == b"ping":
                sock.sendto(msg, ("255.255.255.255", PORT))


    def start(self):

        Process(target=self.response_loop,args=(self.port,self.sock)).start()


    def discover_instances(self) -> set:
        """
        returns a set of tuples (ip_addr,hostname)
        that corresponds to all copypasta instances running on the local network 
        """

        ret = set()

        self.sock.sendto(b"ping", ("255.255.255.255", self.port))

        resp = self.sock.recv(1024).decode("utf-8")

        if resp.startswith("[PONG FLAG]"):
            resp = loads(resp.replace("[PONG_FLAG]",""))
            ret.add((resp["ip_addr"],socket.gethostbyaddr(resp["ip_addr"])))


        return ret

        






