#!/usr/bin/env python
import os
from time import sleep
import SocketServer

PORT = 3514
HOST = ''

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print self.client_address
        sleep(3)

if __name__ == "__main__":
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
