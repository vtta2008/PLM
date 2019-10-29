# -*- coding: utf-8 -*-
"""

Script Name: PLM.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is master file of Pipeline Manager

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

""" Set up environment variable """

__envKey__ = "DAMGTEAM"

import os, sys

ROOT = os.path.abspath(os.getcwd())

from appData import Configurations
configurations = Configurations(__envKey__, os.path.join(ROOT))

from cores.EnvVariableManager import EnvVariableManager

try:
    os.getenv(__envKey__)
except KeyError:
    cfgable                     = False
    EnvVariableManager(__envKey__, ROOT)
else:
    if os.getenv(__envKey__)   != ROOT:
        EnvVariableManager(__envKey__, ROOT)
    cfgable                     = True

if not cfgable:
    print("CONFIGERROR: environment variable not set.")
    sys.exit()
else:
    if not configurations.cfgs:
        print("CONFIGERROR: configurations have not done yet.")
        sys.exit()
    else:
        print('Configurations has been completed.')

# -------------------------------------------------------------------------------------------------------------
""" import """

# Python
import sys, requests, ctypes

# PyQt5
from PyQt5.QtCore                   import pyqtSlot, QCoreApplication
from PyQt5.QtWidgets                import QApplication

# Plm
from appData                        import (__localServer__, PLMAPPID, __organization__,
                                            __appname__, __version__, __website__, SETTING_FILEPTH,
                                            ST_FORMAT, SYSTRAY_UNAVAI)

from cores.StyleSheets              import StyleSheets
from cores.ThreadManager            import ThreadManager
from utils                          import str2bool, clean_file_ext, QuerryDB
from cores.Loggers                  import Loggers
from cores.Settings                 import Settings
from ui.uikits.Icon                 import LogoIcon
from ui.Web.Browser                 import Browser
from ui.LayoutManager               import LayoutManager

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PLM(QApplication):

    key = 'PLM'

    def __init__(self):
        super(PLM, self).__init__(sys.argv)

        # Run all neccessary configuration to start PLM

        self.configs                = configurations

        self.logger                 = Loggers(self.__class__.__name__)
        self.settings               = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self._login                 = False

        self.appInfo                = self.configs.appInfo  # Configuration data

        # Multithreading.
        self.thread_manager         = ThreadManager()
        self.database               = QuerryDB()                                    # Database tool
        self.browser                = Browser()

        QCoreApplication.setOrganizationName(__organization__)
        QCoreApplication.setApplicationName(__appname__)
        QCoreApplication.setOrganizationDomain(__website__)
        QCoreApplication.setApplicationVersion(__version__)

        self.set_styleSheet('darkstyle')                                            # Layout style
        self.setWindowIcon(LogoIcon("Logo"))                                         # Set up task bar icon
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(PLMAPPID)     # Change taskbar icon

        self.layoutManager          = LayoutManager(self)
        self.layoutManager.buildLayouts()

        for layout in self.layoutManager.values():
            layout.signals.showLayout.connect(self.showLayout)
            layout.signals.executing.connect(self.executing)
            layout.signals.openBrowser.connect(self.openBrowser)

        try:
            self.username, token, cookie, remember = self.database.query_table('curUser')
        except (ValueError, IndexError):
            self.logger.info("Error occur, can not query data")
            self.showLayout('SignIn', "show")
        else:
            if not str2bool(remember):
                self.showLayout('SignIn', "show")
            else:
                r = requests.get(__localServer__, verify = False, headers = {'Authorization': 'Bearer {0}'.format(token)}, cookies = {'connect.sid': cookie})
                if r.status_code == 200:
                    if not self.layoutManager.sysTray.isSystemTrayAvailable():
                        self.logger.report(SYSTRAY_UNAVAI)
                        sys.exit(1)
                    self._login = True
                    self.showLayout('PipelineManager', "show")
                else:
                    self.showLayout('SignIn', "show")

        self.setQuitOnLastWindowClosed(False)
        sys.exit(self.exec_())

    @property
    def registerUI(self):
        return self.layout_manager

    @property
    def loginState(self):
        return self._login

    @loginState.setter
    def loginState(self, newVal):
        self._login = newVal

    @pyqtSlot(bool)
    def loginChanged(self, newVal):
        self._login = newVal

    @pyqtSlot(str)
    def openBrowser(self, url):
        self.webBrowser.setUrl(url)
        self.webBrowser.update()
        self.webBrowser.show()

    @pyqtSlot(str, str, str)
    def setSetting(self, key=None, value=None, grp=None):
        # print("receive setting: configKey: {0}, to value: {1}, in group {2}".format(configKey, value, grp))
        self.settings.initSetValue(key, value, grp)

    @pyqtSlot(str)
    def executing(self, cmd):
        if cmd in self.layout_manager.keys():
            self.signals.showLayout.emit(cmd, 'show')
        elif os.path.isdir(cmd):
            os.startfile(cmd)
        elif cmd in self.configs.appInfo.keys():
            os.system(self.appInfo[cmd])
        elif cmd == 'Debug':
            from ui.Debugger import Debugger
            debugger = Debugger()
            return debugger
        elif cmd == 'open_cmd':
            os.system('start /wait cmd')
        elif cmd == 'CleanPyc':
            clean_file_ext('.pyc')
        elif cmd == 'ReConfig':
            self.configs.cfg_mainPkgs()
        elif cmd == 'appExit':
            self.exit()
        else:
            print("This command is not regiested yet: {0}".format(cmd))

    @pyqtSlot(str, str)
    def showLayout(self, name, mode):
        if name == 'app':
            layout = self.parent
        elif name in self.layoutManager.keys():
            layout = self.layoutManager[name]
        else:
            print("Layout: '{0}' is not registerred yet.".format(name))
            layout = None
        if mode == "hide":
            # print('hide: {}'.format(layout))
            layout.hide()
            layout.setValue('showLayout', 'hide')
        elif mode == "show":
            # print('show: {}'.format(layout))
            try:
                layout.show()
            except AttributeError:
                pass
            else:
                layout.setValue('showLayout', 'show')

        elif mode == 'showNor':
            layout.showNormal()
            layout.setValue('state', 'showNormal')
        elif mode == 'showMin':
            layout.showMinimized()
            layout.setValue('state', 'showMinimized')
        elif mode == 'showMax':
            layout.showMaximized()
            layout.setValue('state', 'showMaximized')
        elif mode == 'quit' or mode == 'exit':
            layout.quit()

    @pyqtSlot(str)
    def get_report(self, param):
        self.logger.report(param)

    def set_styleSheet(self, style):
        stylesheet = dict(darkstyle=StyleSheets('dark').changeStylesheet, stylesheet=StyleSheets('bright').changeStylesheet, )
        self.setStyleSheet(stylesheet[style])
        self.settings.initSetValue('styleSheet', 'dark')



if __name__ == '__main__':
    PLM()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved