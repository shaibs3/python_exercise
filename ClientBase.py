import socket
import sys
import socket
import time
import random
import string
from socket import error as socket_error
import errno

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class ClientBase:
    def __init__(self, ip = "127.0.0.1", port = 9000, proto = socket.SOCK_STREAM, payloadSize = 64, numPings = 4, timeout = 3):
        self.serverIp = ip
        self.serverPort = port
        self.protocol = proto
        self.t0 = 0
        self.t1 = 0
        self.pingPktsRx = 0
        self.pingPktsTx = 0
        self.pingPktsLost = 0
        self.payloadSize = payloadSize
        self.bytesReceived = 0
        self.numPings = numPings
        self.timeout = timeout
        self.rxBuffer = 1024

    def errorHandler(self, error):
        print(error)
        self.pingPktsLost += 1

    def prePingOps(self):
        self.t0 = int(round(time.time() * 1000))

    def postPingOps(self, bytesRx):
        self.pingPktsRx += 1
        self.bytesReceived = len(bytesRx)
        self.t1 = int(round(time.time() * 1000))

    def getRoundTripTimeMs(self):
        return self.t1 - self.t0

    def getPayload(self):
        return self.payloadSize

    def getNumPings(self):
        return self.numPings

    def getNumBytesReceived(self):
        return self.bytesReceived

    def getServerPort(self):
        return self.serverPort

    def getServerIp(self):
        return self.serverIp

    def printSummary(self):
        receiveStr = "Packets: Sent= " + str(self.pingPktsTx) + ", Received=" + str(self.pingPktsRx) +\
        " ,Lost=" + str(self.pingPktsLost) + "(" + str(self.pingPktsLost / self.numPings * 100) + "% loss)"
        print(receiveStr)

    def printReply(self):
        receiveStr = "Reply from " + str(self.getServerIp()) + ":" + str(self.getServerPort()) +  " bytes=" + str(self.getNumBytesReceived()) + " time=" + str(self.getRoundTripTimeMs()) +"ms"
        print(receiveStr)

    def printRequest(self):
        sendStr = "pinging " + str(self.serverIp) + ":" + str(self.serverPort) +  " with  " + str(self.getPayload()) + " bytes of data"
        print(sendStr)

    def routine(self):
        numPings = self.getNumPings()
        self.printRequest()
        while numPings > 0:
            self.ping()
            if self.getNumBytesReceived() != 0:
                self.printReply()
            numPings -= 1
        self.printSummary()