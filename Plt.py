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
import os, sys, requests
import qdarkgraystyle

# PyQt5
from PyQt5.QtCore import QCoreApplication, QObject
from PyQt5.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon

# Plt
import appData as app

os.environ[app.__envKey__] = os.getcwd()        # Set up environment variable

from utilities import utils as func
from utilities import message as mess

func.preset_setup_config_data()         # Set up config data
func.preset_implement_maya_tanker()     # Implement maya tankers
func.Collect_info()                     # Generate config info

from utilities import localdb as usql

# Import ui
from ui import (SignIn, SignUp, PipelineTool, SysTrayIcon)

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.set_log()

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PltConsole(QObject):

    def __init__(self):
        super(PltConsole, self).__init__()

        self.settings = app.APPSETTING

        QCoreApplication.setApplicationName(app.__appname__)
        QCoreApplication.setApplicationVersion(app.__version__)
        QCoreApplication.setOrganizationName(app.__organization__)
        QCoreApplication.setOrganizationDomain(app.__website__)

        mainApp = QApplication(sys.argv)
        mainApp.setApplicationDisplayName(app.__appname__)
        mainApp.setStyleSheet(qdarkgraystyle.load_stylesheet())

        self.username, token, cookie = usql.query_user_session()

        self.SignInUI = SignIn.SignIn()
        self.SignUpUI = SignUp.SignUp()
        self.MainUI = PipelineTool.PipelineTool()
        self.SysTray = SysTrayIcon.SysTrayIcon()

        self.SignInUI.greetingSig.connect(self.loginMess)
        self.SignInUI.showSignUpSig.connect(self.show_hide_signup)
        self.SignInUI.showMainSig.connect(self.show_hide_main)

        self.MainUI.showMainSig.connect(self.show_hide_main)
        self.MainUI.showLoginSig.connect(self.show_hide_signin)
        self.SignUpUI.showLoginSig.connect(self.show_hide_signin)

        self.SysTray.showNormalSig.connect(self.MainUI.showNormal)
        self.SysTray.showMinimizeSig.connect(self.MainUI.hide)
        self.SysTray.showMaximizeSig.connect(self.MainUI.showMaximized)
        # self.MainUI.closeMessSig.connect(self.closeMess)

        if self.username is None or token is None or cookie is None:
            self.SignInUI.show()
        else:
            r = requests.get(app.__serverCheck__, verify = False,
                             headers={'Authorization': 'Bearer {token}'.format(token=token)},
                             cookies={'connect.sid': cookie})
            if r.status_code == 200:

                self.SysTray.show()
                self.SysTray.loginMess()
                self.MainUI.show()

                if not QSystemTrayIcon.isSystemTrayAvailable():
                    QMessageBox.critical(None, mess.SYSTRAY_UNAVAI)
                    sys.exit(1)
            else:
                self.SignInUI.show()

        QApplication.setQuitOnLastWindowClosed(False)
        sys.exit(mainApp.exec_())

    def show_hide_main(self, param):
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

    def loginMess(self, param):
        if param:
            self.SysTray.loginMess()

    def closeMess(self, param):
        if param:
            self.SysTray.closeMess()

if __name__ == '__main__':
    PltConsole()

# ----------------------------------------------------------------------------