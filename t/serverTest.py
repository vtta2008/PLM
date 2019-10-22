# -*- coding: utf-8 -*-
"""

Script Name: serverTest.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import socket
import threading
import socketserver

# MyAwesomelyNamedServerScript.py

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        def func1(scr1):
            # put code that does something here.
            print('func1 : %s' % scr1)
            return scr1

        def func2(scr2):
            # put code that does something here.
            print('func2 : %s' % scr2)
            return scr2

        # self.request is the TCP socket connected to the client
        cur_thread = threading.current_thread()
        data = self.request.recv(1024)

        # In the data package the IP from client.
        # Extract and add to an IP list (e.g. max 2 connection.)
        # if/else statement: if max connection reached than report back "cannot connect... waiting in queue or something".
        # limiting the request also prevent DDos attacks from the start.

        data_proc = func1(data)  # do something once
        data = func2(data_proc)  # do something twice

        response = "{}: {}".format(cur_thread.name, data)
        self.request.sendall(response
                             )

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def setupServer(ip = None, port = None, message = None):
    # Ip, port, message can be linked to below code if you want exernal input via GUI
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 0

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print("Received: {}".format(response))
    finally:
        sock.close()

def test_main():

        #client(ip, port, "Hello World 1")
        #client(ip, port, "Hello World 2")
        #client(ip, port, "Hello World 3")

        client(message = "Hello World 1")
        client(message = "Hello World 2")
        client(message = "Hello World 3")

        server.shutdown()
        server.server_close()

if __name__ == "__main__":

    test_main()  #runs the main test

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/10/2019 - 4:56 AM
# © 2017 - 2018 DAMGteam. All rights reserved