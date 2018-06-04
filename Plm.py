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
import os
os.environ["PIPELINE_MANAGER"] = os.path.abspath(os.getcwd())                           # Set up environment variable

import sys, requests, ctypes
import qdarkgraystyle

# PyQt5
from PyQt5.QtCore import QCoreApplication, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon

# Plt
import appData as app

from appData import LocalCfg                                                          # Generate config info
LocalCfg = app.reload(LocalCfg)
preset1 = LocalCfg.LocalCfg()

from appData import MayaCfg                                                          # Generate config info
MayaCfg = app.reload(MayaCfg)
preset2 = MayaCfg.MayaCfg()

from utilities import localSQL as usql

from ui import (SignIn, SignUp, PipelineManager, SysTrayIcon)                       # Import ui
from ui import uirc as rc

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.set_log()

def str2bool(arg):
    return str(arg).lower() in ['true', 1, '1', 'ok', '2']

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PltConsole(QObject):

    updateAvatar = pyqtSignal(bool)

    def __init__(self):
        super(PltConsole, self).__init__()

        self.settings = app.appSetting

        mainApp = QApplication(sys.argv)
        mainApp.setApplicationName(app.__project__)
        QCoreApplication.setApplicationName(app.__appname__)
        QCoreApplication.setApplicationVersion(app.__version__)
        QCoreApplication.setOrganizationName(app.__organization__)
        QCoreApplication.setOrganizationDomain(app.__website__)

        mainApp.setWindowIcon(rc.AppIcon("Logo"))                                       # Set up task bar icon
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app.PLTAPPID)     # Change taskbar icon in system
        mainApp.setStyleSheet(qdarkgraystyle.load_stylesheet())                         # set them

        self.LoginUI = SignIn.SignIn()
        self.LoginUI.showPlt.connect(self.show_plt)
        self.LoginUI.showSignup.connect(self.show_signup)

        self.SignUpUI = SignUp.SignUp()
        self.SignUpUI.showSignup.connect(self.show_signup)

        self.MainUI = PipelineManager.PipelineManager()
        self.MainUI.showPlt.connect(self.show_plt)
        self.MainUI.loadLayout.connect(self.loadLayout)
        self.MainUI.execute.connect(self.execute)
        self.MainUI.timelogSig.connect(usql.TimeLog)
        self.updateAvatar.connect(self.MainUI.updateAvatar)
        self.SignUpUI.showPlt.connect(self.show_plt)

        self.SysTray = SysTrayIcon.SysTrayIcon()
        self.SysTray.showMin.connect(self.MainUI.showMinimized)
        self.SysTray.showMax.connect(self.MainUI.showMaximized)
        self.SysTray.showNor.connect(self.MainUI.showNormal)

        self.query = usql.QuerryDB()

        try:
            self.username, token, cookie, remember = self.query.query_table('curUser')
        except ValueError:
            self.show_login(True)
        else:
            if not str2bool(remember):
                self.show_login(True)
            else:
                r = requests.get(app.__serverCheck__, verify = False,
                                 headers={'Authorization': 'Bearer {token}'.format(token=token)},
                                 cookies={'connect.sid': cookie})

                if r.status_code == 200:
                    self.MainUI.showPlt.emit(True)
                    self.updateAvatar.emit(True)
                    if not QSystemTrayIcon.isSystemTrayAvailable():
                        QMessageBox.critical(None, app.SYSTRAY_UNAVAI)
                        sys.exit(1)
                else:
                    self.LoginUI.show()

        QApplication.setQuitOnLastWindowClosed(False)
        sys.exit(mainApp.exec_())

    def show_plt(self, param):
        if param:
            self.MainUI.show()
            self.SysTray.show()
            self.SysTray.log_in()
            self.show_login(not param)
        else:
            self.MainUI.hide()
            self.SysTray.hide()

        self.settings.setValue("showPlt", param)

    def show_signup(self, param):
        if param:
            self.SignUpUI.show()
            self.show_login(not param)
        else:
            self.SignUpUI.hide()

        self.settings.setValue("showSignUp", param)

    def show_login(self, param):
        if param:
            self.LoginUI.show()
            self.show_plt(not param)
            self.show_signup(not param)
        else:
            self.LoginUI.hide()

        self.settings.setValue("showSignIn", param)

    def loadLayout(self, param):
        print("get signal loadlayout: {0}".format(param))

    def execute(self, param):
        print("get signal execute: {0}".format(param))

if __name__ == '__main__':
    PltConsole()

# ----------------------------------------------------------------------------