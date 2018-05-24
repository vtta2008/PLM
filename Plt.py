#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Plt.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Tool

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, logging, requests

# PyQt5
from PyQt5.QtCore import QCoreApplication, QObject, QSettings
from PyQt5.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon

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

from utilities import utils as func
from utilities import sql_local as usql
from utilities import message as mess
from utilities import variables as var

func.Collect_info()
func.preset_maya_intergrate()

from ui import (SignIn, SignUp, PipelineTool, SysTrayIcon)

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logPth = os.path.join(app.LOGPTH)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PltConsole(QObject):

    def __init__(self):
        super(PltConsole, self).__init__()

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        usql.query_userData()

        QCoreApplication.setApplicationName(app.__appname__)
        QCoreApplication.setApplicationVersion(app.__version__)
        QCoreApplication.setOrganizationName(app.__organization__)
        QCoreApplication.setOrganizationDomain(app.__website__)

        mainApp = QApplication(sys.argv)
        mainApp.setApplicationDisplayName(app.__slogan__)
        mainApp.setStyleSheet(qdarkgraystyle.load_stylesheet())

        username, token, cookie = usql.query_user_session()

        self.SignInUI = SignIn.SignIn()

        self.SignUpUI = SignUp.SignUp()

        self.MainUI = PipelineTool.PipelineTool()

        self.SysTray = SysTrayIcon.SysTrayIcon()

        showSignUpSig = self.SignInUI.showSignUpSig
        showSignUpSig.connect(self.show_hide_signup)

        showMainSig1 = self.SignInUI.showMainSig
        showMainSig2 = self.SignUpUI.showMainSig2
        showMainSig3 = self.MainUI.showMainSig

        showMainSig1.connect(self.show_hide_main)
        showMainSig2.connect(self.show_hide_main)
        showMainSig3.connect(self.show_hide_main)

        showSignInSig1 = self.MainUI.showLoginSig1
        showSignInSig2 = self.SignUpUI.showLoginSig2
        showSignInSig1.connect(self.show_hide_signin)
        showSignInSig2.connect(self.show_hide_signin)

        showNorSig = self.SysTray.showNormalSig
        showMinSig = self.SysTray.showMinimizeSig
        showMaxSig = self.SysTray.showMaximizeSig
        closeMessSig = self.MainUI.closeMessSig
        showNorSig.connect(self.MainUI.showNormal)
        showMinSig.connect(self.MainUI.hide)
        showMaxSig.connect(self.MainUI.showMaximized)
        closeMessSig.connect(self.closeMess)

        if username is None or token is None or cookie is None:
            self.SignInUI.show()
        else:
            r = requests.get("https://pipeline.damgteam.com/check", verify = False,
                             headers={'Authorization': 'Bearer {token}'.format(token=token)},
                             cookies={'connect.sid': cookie})

            if r.status_code == 200:

                self.MainUI.show()
                self.SysTray.show()
                self.SysTray.loginMess()

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
            self.SysTray.show()
        else:
            self.MainUI.hide()
            self.SysTray.hide()

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

    def closeMess(self, param):
        if param:
            self.SysTray.closeMess()

if __name__ == '__main__':
    PltConsole()

# ----------------------------------------------------------------------------