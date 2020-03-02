import socketserver
import time

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9000
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()