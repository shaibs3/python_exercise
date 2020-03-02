import socket
import sys
import socket
import time
import random
import string
from socket import error as socket_error
from ClientBase import ClientBase
import errno
import os
from ClientBase import randomString

class ClientUdp(ClientBase):
    def __init__(self, _ip, _port, _numPings = 4, _payloadSize = 64, _timeout = 1):
        super().__init__( _ip, _port, socket.SOCK_DGRAM, _payloadSize, _numPings, _timeout)
    
    def errorHandler(self, error):
        self.pingPktsLost += 1
        if error.errno == 10035: #10035 is the error code recevied in windows os for a non blocking operation that could not complete
            print("timed out")
        else:
            print(error)
    
    def ping(self):
        self.prePingOps()
        with socket.socket(socket.AF_INET, self.protocol) as sock:
            #send the data to the server
            try:
                sock.settimeout(self.timeout)
                self.pingPktsTx += 1
                msg = randomString(self.payloadSize)
                sendData = bytes(msg + "\n", "utf-8")
                sock.sendto(sendData,(self.serverIp, self.serverPort))
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
    c1 = ClientUdp("127.0.0.1", 9000)
    c1.routine()

if __name__== "__main__":
  main()
