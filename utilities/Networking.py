#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Networking.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, logging, socket, subprocess
from urllib.request import urlopen
from time import sleep



# Plt
import appData as app

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logPth = os.path.join(app.LOGPTH)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
""" Connection checker """

try:
    from urllib2 import urlopen, URLError
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
    from urllib.request import urlopen, URLError

class CheckNetworkCollection(object):

    con_url = app.__server__

    def __init__(self):
        pass

    def check_url1(self):
        try:
            data = urlopen(self.con_url, timeout=5)
        except URLError:
            return False

        try:
            host = data.fp._sock.fp._sock.getpeername()
        except AttributeError:
            host = data.fp.raw._sock.getpeername()

        self.conn_url = 'https://' + (host[0] if len(host) == 2 else socket.gethostbyname(urlparse(data.geturl()).hostname))
        return True

    def check_url2(self, url=app.__server__):
        nboftrials =0
        answer = 'NO'

        while answer=='NO' and nboftrials<10:
            try:
                urlopen(url)
                answer='YES'
            except:
                answer='NO'
                nboftrials += 1
                sleep(30)

    def check_ip1(self):

        ipaddress = socket.gethostbyname(socket.gethostname())

        print(ipaddress)

        if ipaddress == "127.0.0.1":
            return False
        else:
            return True

    def check_ip2(self, url=app.__server__):

        while True:
            print(socket.gethostbyname(url))
            if socket.gethostbyname(url) == "92.242.140.2":
                return False
            else:
                socket.gethostbyname(url)
                return True

    def check_online(self, timeout):

        try:
            return subprocess.run(['wget', '-q', '--spider', app.__server__], timeout=timeout).returncode == 0
        except subprocess.TimeoutExpired:
            return False

# -------------------------------------------------------------------------------------------------------------
""" Data request """
@coroutine
def handle_request(request):
    data = yield get_more_data(request)
    return make_response(data)


@coroutine
def get_mode_data(request):
    data = yield make_db_query(request.user_id)
    return data

def processrequest(request):
    data = get_more_data(request)
    return data



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018