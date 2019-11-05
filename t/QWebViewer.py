# -*- coding: utf-8 -*-
"""

Script Name: QWebViewer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebEngineWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()

        self.url = ""
        self.setWindowTitle("Teletext")
        self.setGeometry(0, 0, 800, 720)

        self.webView = QtWebEngineWidgets.QWebEngineView()
        self.webView.setUrl(QtCore.QUrl("about:blank"))

        self.setCentralWidget(self.webView)

        self.webView.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        self.webView.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.ShowScrollBars, False)
        self.webView.settings().setFontFamily(QtWebEngineWidgets.QWebEngineSettings.SansSerifFont, "Sans Serif")
        self.webView.settings().setFontSize(QtWebEngineWidgets.QWebEngineSettings.DefaultFontSize, 9)
        self.webView.loadFinished.connect(self.url_changed)

    def url_changed(self):
        self.setWindowTitle(self.webView.title())

    def go_back(self):
        self.webView.back()

    def load_url(self, path):
        print("loading HTML")
        self.url = path
        self.webView.load(QtCore.QUrl("file://" + self.url))


if __name__ == '__main__':

   import sys
   app = QtWidgets.QApplication(sys.argv)
   win = MainWindow()
   win.show()
   sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:15 AM
# © 2017 - 2018 DAMGteam. All rights reserved