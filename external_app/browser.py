# -*- coding: utf-8 -*-
"""

Script Name: browser.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    Browser hand made

"""
__appname__ = "Pipeline Tool"
__module__ = "browser"
__version__ = "13.0.1"
__organization__ = "DAMG team"
__website__ = "www.dot.damgteam.com"
__email__ = "dot@damgteam.com"
__author__ = "Trinh Do, a.k.a: Jimmy"

# -------------------------------------------------------------------------------------------------------------
""" Import modules """
# -------------------------------------------------------------------------------------------------------------
# Python
import os
import logging
import sys

# PtQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWidgets import *

# Plt tools
from utilities import variables as var
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain logs """
# -------------------------------------------------------------------------------------------------------------
logPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'logs', 'browser.log')
logger = logging.getLogger('browser')
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
""" Declare variables """
# -------------------------------------------------------------------------------------------------------------
PACKAGE = var.PLT_PACKAGE
HOMEPAGE = var.PLT_URL['Home']

class Plt_browser(QMainWindow):

    def __init__(self, *args, **kwargs):

        super(Plt_browser, self).__init__(*args, **kwargs)

        self.setWindowTitle('Plt browser')
        self.setWindowIcon(QIcon(func.get_web_icon('Logo')))

        self.buildUI()

        self.setCentralWidget(self.browser)

        self.show()

    def buildUI(self):

        self.browser = QWebView()
        self.browser.setUrl(QUrl(HOMEPAGE))

        navtb = QToolBar('Navigation')
        homeBtn, backBtn, forwardBtn, reloadBtn, stopBtn = self.tool_bar_btns()
        navtb.addAction(homeBtn)
        navtb.addAction(backBtn)
        navtb.addAction(forwardBtn)
        navtb.addAction(stopBtn)
        navtb.addAction(reloadBtn)

        urltb = QToolBar('URL')

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(func.get_web_icon('Https')))
        self.httpsicon.resize(16, 16)
        urltb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_url)
        urltb.addWidget(self.urlbar)

        self.addToolBar(navtb)
        self.addToolBar(urltb)

        self.browser.urlChanged.connect(self.update_url_bar)

    def tool_bar_btns(self):

        homeBtn = QAction(QIcon(func.get_web_icon('Home')), 'Home', self)
        homeBtn.setToolTip('Go to homepage')
        homeBtn.triggered.connect(self.homepage)

        backBtn = QAction(QIcon(func.get_web_icon('Back')), 'Back', self)
        backBtn.setToolTip('Back to previous page')
        backBtn.triggered.connect(self.browser.back)

        forwardBtn = QAction(QIcon(func.get_web_icon('Forward')), 'Forward', self)
        forwardBtn.setToolTip('Forward to next page')
        forwardBtn.triggered.connect(self.browser.forward)

        reloadBtn = QAction(QIcon(func.get_web_icon('Refresh')), 'Reload', self)
        reloadBtn.setToolTip('Reload the current page')
        reloadBtn.triggered.connect(self.browser.reload)

        stopBtn = QAction(QIcon(func.get_web_icon('Stop')), 'Stop', self)
        stopBtn.setToolTip('Stop loading page')
        stopBtn.triggered.connect(self.browser.stop)

        return homeBtn, backBtn, forwardBtn, reloadBtn, stopBtn

    def update_url_bar(self, q):

        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(func.get_web_icon('Https')))
        else:
            self.httpsicon.setPixmap(QPixmap(func.get_web_icon('Http')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def navigate_url(self):

        q = QUrl(self.urlbar.text())

        if q.scheme() == '':
            q.setScheme('https')

        self.browser.setUrl(QUrl(q))

    def homepage(self):
        self.browser.setUrl(QUrl('https://www.google.com.vn'))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    web = Plt_browser()
    app.exec_()
