# -*- coding: utf-8 -*-
"""

Script Name: ui_browser.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    Browser hand made

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
print("Import from modules: {file}".format(file=__name__))
print("Directory: {path}".format(path=__file__.split(__name__)[0]))
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
import logging
import sys

# PtQt5
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QMainWindow, QToolBar, QLineEdit, QAction, QApplication, QLabel

# Plt tools
import appData as app
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain logs """
# -------------------------------------------------------------------------------------------------------------
logPth = os.path.join('appData', 'logs', 'browser.log')
logger = logging.getLogger('browser')
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
""" Declare variables """

HOMEPAGE = app.__homepage__

class WebBrowser(QMainWindow):

    def __init__(self, url=HOMEPAGE, *args, **kwargs):

        super(WebBrowser, self).__init__(*args, **kwargs)
        self.url = url
        self.setWindowTitle('Plt browser')
        self.setWindowIcon(QIcon(func.get_web_icon('Logo')))
        print(1)
        self.browser = QWebView()
        self.browser.setUrl(QUrl(self.url))
        print(2)
        self.buildUI()
        print(9)
        self.setCentralWidget(self.browser)
        print(10)

    def buildUI(self):
        print(3)
        navtb = QToolBar('Navigation')
        homeBtn, backBtn, forwardBtn, reloadBtn, stopBtn = self.tool_bar_btns()
        navtb.addAction(homeBtn)
        navtb.addAction(backBtn)
        navtb.addAction(forwardBtn)
        navtb.addAction(stopBtn)
        navtb.addAction(reloadBtn)
        print(4)
        urltb = QToolBar('URL')
        print(5)
        self.httpsicon = QLabel(" ")
        self.httpsicon.setPixmap(QPixmap(func.get_web_icon('Https')))
        self.httpsicon.resize(16, 16)
        urltb.addWidget(self.httpsicon)
        print(6)
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_url)
        urltb.addWidget(self.urlbar)
        print(7)
        self.addToolBar(navtb)
        self.addToolBar(urltb)
        print(8)
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

def main():
    app = QApplication(sys.argv)
    web = WebBrowser()
    web.show()
    app.exec_()

if __name__ == '__main__':

    main()
