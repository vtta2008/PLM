#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Plt.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Tool

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
# print("Import from modules: {file}".format(file=__name__))
# print("Directory: {path}".format(path=__file__.split(__name__)[0]))
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, logging, subprocess, webbrowser, requests
import sqlite3 as lite
from functools import partial

# PyQt5
from PyQt5.QtCore import Qt, QSize, QCoreApplication, QSettings, pyqtSignal, QByteArray
from PyQt5.QtGui import QIcon, QPixmap, QImage, QIntValidator, QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLineEdit, QLabel, QPushButton, QMessageBox, QGroupBox,
                             QCheckBox, QTabWidget, QSystemTrayIcon, QAction, QMenu, QFileDialog, QComboBox,
                             QDockWidget, QSlider, QSizePolicy, QStackedWidget, QStackedLayout)

# -------------------------------------------------------------------------------------------------------------
""" Set up env variable path """

__envKey__ = "PIPELINE_TOOL"
os.environ[__envKey__] = os.getcwd()

import appData as app

configPth = os.path.join(os.getenv(app.__envKey__), 'appData', 'config')
settingPth = os.path.join(os.getenv(app.__envKey__), 'appData', 'settings')
logPth = os.path.join(os.getenv(app.__envKey__), 'appData', 'logs')

for pth in [configPth, settingPth, logPth]:
    if not os.path.exists(pth):
        os.mkdir(pth)

# -------------------------------------------------------------------------------------------------------------
""" Stylesheet plugin """
import qdarkgraystyle

# -------------------------------------------------------------------------------------------------------------
""" Plt tools """
from ui import (SignIn, SignUp, PipelineTool, SysTrayIcon)

from utilities import utils as func
from utilities import sql_local as usql
from utilities import message as mess
from utilities import variables as var

func.preset_maya_intergrate()

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logPth = os.path.join(app.LOGPTH, 'master.log')
logger = logging.getLogger(__name__)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
""" Variables """


# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PltConsole():

    def __init__(self):

        super(PltConsole, self).__init__()

        usql.query_userData()

        QCoreApplication.setApplicationName(app.__appname__)
        QCoreApplication.setApplicationVersion(app.__version__)
        QCoreApplication.setOrganizationName(app.__organization__)
        QCoreApplication.setOrganizationDomain(app.__website__)

        mainApp = QApplication(sys.argv)
        # mainApp.setWindowIcon(QIcon(func.get_icon('Logo')))
        mainApp.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())

        username, token, cookie = usql.query_user_session()

        self.SignInUI = SignIn.SignIn()
        self.SignUpUI = SignUp.SignUp()
        self.MainUI = PipelineTool.PipelineTool()
        self.SysTrayIcon = SysTrayIcon.SysTrayIcon()

        showMainSig1 = self.SignInUI.showMainSig
        showSignUpSig = self.SignInUI.showSignUpSig
        showMainSig2 = self.SignUpUI.showMainSig
        showSignInSig = self.SignUpUI.showLoginSig
        showNorSig = self.SysTrayIcon.showNormalSig
        showMinSig = self.SysTrayIcon.showMinimizeSig
        showMaxSig = self.SysTrayIcon.showMaximizeSig

        showMainSig1.connect(self.show_hide_main)
        showMainSig2.connect(self.show_hide_main)
        showSignUpSig.connect(self.show_hide_signup)
        showSignInSig.connect(self.show_hide_signin)
        showNorSig.connect(self.MainUI.showNormal)
        showMinSig.connect(self.MainUI.hide)
        showMaxSig.connect(self.MainUI.showMaximized)

        if username is None or token is None or cookie is None:
            self.SignInUI.show()
        else:
            r = requests.get("https://pipeline.damgteam.com/check", verify = False,
                             headers={'Authorization': 'Bearer {token}'.format(token=token)},
                             cookies={'connect.sid': cookie})

            if r.status_code == 200:

                self.MainUI.show()
                self.SysTrayIcon.show()

                if not QSystemTrayIcon.isSystemTrayAvailable():
                    QMessageBox.critical(None, mess.SYSTRAY_UNAVAI)
                    sys.exit(1)

            else:
                self.SignInUI.show()

        QApplication.setQuitOnLastWindowClosed(False)
        sys.exit(mainApp.exec_())

    def show_hide_main(self, param):
        param = func.str2bool(param)
        if param:
            self.MainUI.show()
        else:
            self.MainUI.hide()

    def show_hide_signup(self, param):
        param = func.str2bool(param)
        if param:
            self.SignUpUI.show()
        else:
            self.SignUpUI.hide()

    def show_hide_signin(self, param):
        param = func.str2bool(param)
        if param:
            self.SignInUI.show()
        else:
            self.SignInUI.hide()

if __name__ == '__main__':
    PltConsole()

# ----------------------------------------------------------------------------