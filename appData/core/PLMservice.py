# -*- coding: utf-8 -*-
"""

Script Name: ping.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys,  subprocess, tempfile, random, time, re, shlex
from optparse import OptionGroup, OptionParser

# PyQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QApplication
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import *

# Plt
import appData as app
from ui import uirc as rc
from utilities import utils as func

width = 400
height = 100

cmd = "ping " + app.__serverUrl__ + " -t"
ping = subprocess.getoutput(cmd)
print(ping, type(ping))

def _get_match_groups(ping_output, regex):
    match = regex.search(ping_output)
    if not match:
        raise Exception("Invalid PING output:\n" + ping_output)
    return match.groups()

def parse(ping_output):
    matcher = re.compile(r'PING ([a-zA-Z0-9.\-]+) \(')
    host = _get_match_groups(ping_output, matcher)[0]

    matcher = re.compile(r'(\d+) packets transmitted, (\d+) received')
    sent, received = _get_match_groups(ping_output, matcher)

    try:
        matcher = re.compile(r'(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)')
        minping, avgping, maxping, jutter = _get_match_groups(ping_output, matcher)

    except:
        minping, avgping, maxping, jitter = ['NaN']*4

    return{'host': host, 'sent': sent, 'received': received,
            'minping': minping, 'avgping': avgping, 'maxping': maxping,
            'jitter': jitter}

def main(argv=sys.argv):
    ping_output = None
    if not sys.stdin.isatt():
        ping_output = sys.stdin.read()

    usage = 'Usage: %prog [OPTIONS] [+FORMAT]\n\n'\
            'Parses output from the system ping command piped in via stdin.'
    parser = OptionParser(usage=usage, version="%prog 0.1")

    format_group = OptionGroup(parser,

    """FORMAT controls the output. Interpreted sequences are:
    \t%h    host name or IP address
    \t%s    packets sent
    \t%r    packets received
    \t%m    minimum ping in milliseconds
    \t%a    average ping in milliseconds
    \t%M    maximum ping in milliseconds
    \t%j    jitter in milliseconds
    Default FORMAT is %h,%s,%r,%m,%a,%M,%j""")
    parser.add_option_group(format_group)

    (options, args) = parser.parse_args()

    if ping_output is None:
        parser.print_help()
        sys.exit(1)

    ping_result = parse(ping_output)

    format_replacements = [('%h', 'host'),
                           ('%s', 'sent'),
                           ('%r', 'received'),
                           ('%m', 'minping'),
                           ('%a', 'avgping'),
                           ('%M', 'maxping'),
                           ('%j', 'jitter')]
    format_replacements = [(fmt, ping_result[field]) for fmt, field in
                           format_replacements]

    if len(args) == 0:
        output = ','.join(fmt for (fmt, rep) in format_replacements)
    elif args[0].startswith('+'):
        args[0] = args[0].lstrip('+')
        output = ' '.join(args[0:])
    else:
        parser.print_help()

    for (fmt, rep) in format_replacements:
        output = output.replace(fmt, rep)

    sys.stdout.write(output)

    sys.exit(0)

# -------------------------------------------------------------------------------------------------------------
""" ping """

def ping(host):
    ping = subprocess.Popen(
        ["ping", "-c", "1", "-W", "1", host],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    out, error = ping.communicate()
    print(out, type(out))
    return parse(out)

# -------------------------------------------------------------------------------------------------------------
""" Ping thread """

class PingThread(QThread):

    pingNumber = pyqtSignal(int)
    connStatus = pyqtSignal(bool)
    networkStage = pyqtSignal(str)

    def __init__(self, host=app.__serverUrl__, parent=None):
        super(PingThread, self).__init__(parent)

        self.host = host

    def ping(self, host_name):
        # pings google.com and returns a dot . on success and an X on failure
        ping_command = "ping -i " + str(self.ping_timeout) + " -c 1 " + host_name
        process = subprocess.Popen(shlex.split(ping_command), stdout=subprocess.PIPE)
        output = process.stdout.read()
        matches = re.findall(r"time=[0-9]\w+", output)
        if len(matches):
            print(matches[0].split("=")[-1])
            return matches[0].split("=")[-1]
        else:
            return False

    def run(self):
        while self.isRunning():

            try:
                pingval = self.ping(self.host)
            except:
                pingval = 0
            else:
                pingval = 0
            finally:
                self.pingNumber.emit(pingval)

# -------------------------------------------------------------------------------------------------------------
""" PingService """

class PLMservice(QWidget):

    PLMserviceSig = pyqtSignal()
    console= pyqtSignal(bool)

    def __init__(self, parent=None):
        super(PLMservice, self).__init__(parent)

        self.network_icon = QPixmap(func.getAppIcon(16, "Unknown"))

        self.pingThread = PingThread()
        self.pingThread.pingNumber.connect(self.ping_number)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

        self.console.connect(self.thread_console)
        self.console.emit(True)

    def buildUI(self):

        self.pingLabel = rc.Label("0")

        self.pingIcon = QLabel()
        self.pingIcon.setPixmap(self.network_icon)

        self.layout.addWidget(self.pingIcon, 0, 0, 1, 1)
        self.layout.addWidget(self.pingLabel, 1, 0, 1, 1)

    @pyqtSlot(int)
    def ping_number(self, param):
        self.pingLabel.setText(str(param))
        self.pingLabel.update()

        if param < 100:
            self.network_quality("PingGood")
        elif param > 100 and param < 300:
            self.network_quality("PingNormal")
        elif param > 300 and param < 1000:
            self.network_quality("PingSlow")
        else:
            self.network_quality("PingLaggy")

    @pyqtSlot(bool)
    def network_stage(self, param):
        if param:
            self.pingIcon.setPixmap(self.connectIcon)
        else:
            self.pingIcon.setPixmap(self.disconnectIcon)

    @pyqtSlot(str)
    def network_quality(self, param):
        self.network_icon = QPixmap(func.getAppIcon(16, param))
        self.pingIcon.setPixmap(self.network_icon)
        self.pingIcon.update()

    @pyqtSlot(bool)
    def thread_console(self, param):
        if param:
            self.pingThread.start()
        else:
            self.pingThread.quit()


def main():
    plm = QApplication(sys.argv)
    plmService = PLMservice()
    plmService.show()
    plm.exec_()

if __name__ == '__main__':
    main()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 8:06 AM
# © 2017 - 2018 DAMGteam. All rights reserved