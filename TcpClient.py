import socket
import sys
import socket
import time
import random
import string
import errno
from socket import error as socket_error
from ClientBase import ClientBase
from ClientBase import randomString

class tcpClient(ClientBase):
    def __init__(self, _ip, _port, _numPings = 4, _payloadSize = 64, _timeout = 1):
        super().__init__( _ip, _port, socket.SOCK_STREAM, _payloadSize, _numPings, _timeout)

    def ping(self):        
        self.prePingOps()
        with socket.socket(socket.AF_INET, self.protocol) as sock:
            # send the data to the server
            try:
                sock.settimeout(self.timeout)
                self.pingPktsTx += 1
                sock.connect((self.serverIp, self.serverPort))
                msg = randomString(self.payloadSize)
                sock.sendall(bytes(msg + "\n", "utf-8"))
            except socket.error as error:
                self.errorHandler(error)
                return
            # receive the data from the server
            try:
                received = str(sock.recv(self.rxBuffer), "utf-8")
            except socket.error as error:
                self.errorHandler(error)
                return
        self.postPingOps(received)

def main():
    c1 = tcpClient("127.0.0.1", 9000)
    c1.routine()

if __name__== "__main__":
  main()
