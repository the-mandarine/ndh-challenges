#!/usr/bin/env python

import os
import sys
import SocketServer
from threading import Thread
from time import sleep
from random import randint

from ai import calculate_words_scores

DATA_PATH = "data"
MIN_WAIT = 200
MAX_WAIT = 600


class WordScorer(Thread):
    """Just a thread that regularly scores each word according to the occs"""
    def __init__(self, path):
        Thread.__init__(self)
        self.path = path
        self.daemon = True
        
    def run(self):
        while True:
            calculate_words_scores(self.path)
            sys.stdout.write("Scored words\n")
            time_to_sleep = randint(MIN_WAIT, MAX_WAIT)
            sleep(time_to_sleep)

class RequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        from replyer import Replyer

        replyer = Replyer(self.client_address, DATA_PATH)

        for sentence in replyer.init_session():
            self.request.send(sentence)

        while not replyer.is_over():
            data = self.request.recv(1024)
            if not data:
                return
            response = replyer.reply(data)
            if response:
                self.request.sendall(response)

        for sentence in replyer.close_session():
            self.request.send(sentence)

        return

class Server(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    address = ('localhost', 4242)
    server = Server(address, RequestHandler)
    print "Listening on 4242"
    scorer = WordScorer(DATA_PATH)
    scorer.start()

    try:
        server.serve_forever()
    except:
        print "Terminating"
    finally:
        server.socket.close()

