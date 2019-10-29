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

from cores.base                     import DAMGDICT
from cores.StyleSheets              import StyleSheets
from cores.ThreadManager            import ThreadManager
from utils                          import str2bool, clean_file_ext, QuerryDB
from cores.Loggers                  import Loggers
from cores.Settings                 import Settings
from ui.uikits.Icon                 import LogoIcon
from ui.Web.Browser                 import Browser
# from ui.LayoutManager               import LayoutManager

# -------------------------------------------------------------------------------------------------------------
""" Operation """

print(1)
from ui                                 import PipelineManager, SysTray
print(11)
from ui.Funcs                           import SignIn, SignUp, ForgotPassword
print(12)
from ui.Settings                        import UserSetting, SettingUI
print(13)
from ui.Projects                        import NewProject
print(2)
from ui.Tools                           import (Screenshot, NoteReminder, ImageViewer, FindFiles, EnglishDictionary,
                                                Calendar, Calculator)
from ui.Tools.NodeGraph                 import NodeGraph
from ui.Tools.TextEditor                import TextEditor
print(3)
from ui.Menus.config                    import Configuration, Preferences
print(4)
from ui.Info.InfoWidget                 import InfoWidget

class LayoutManager(DAMGDICT):

    key = 'LayoutManager'

    def __init__(self, parent=None):
        super(LayoutManager, self).__init__(parent)

        self.parent = parent

        self.mains      = self.mainLayouts()
        self.funcs      = self.functionLayouts()

        self.infos      = self.infoLayouts()
        self.setts      = self.settingLayouts()
        self.tools      = self.toolLayouts()
        self.prjs       = self.projectLayouts()

    def functionLayouts(self):
        self.signin     = SignIn.SignIn()
        self.forgotPW   = ForgotPassword.ForgotPassword()
        self.signup     = SignUp.SignUp()

        for layout in [self.signin, self.signup, self.forgotPW]:
            self.regisLayout(layout)

    def mainLayouts(self):
        self.mainUI     = PipelineManager.PipelineManager()
        self.sysTray    = SysTray.SysTray()

        layouts = [self.mainUI, self.sysTray]

        for layout in layouts:
            self.regisLayout(layout)

        for layout in self.mainUI.mainUI_layouts:
            self.regisLayout(layout)

        for layout in self.mainUI.topTabUI.tabLst:
            key = layout.key
            if not key in self.keys():
                self[key] = layout

        return layouts

    def infoLayouts(self):
        self.about          = InfoWidget('About')
        self.codeConduct    = InfoWidget('CodeOfConduct')
        self.contributing   = InfoWidget('Contributing')
        self.credit         = InfoWidget("Credit")
        self.licence        = InfoWidget('Licence')
        self.reference      = InfoWidget('Reference')
        self.version        = InfoWidget('Verion')

        layouts = [self.about, self.codeConduct, self.contributing, self.credit, self.licence,
                       self. reference, self.version]

        for layout in layouts:
            self.regisLayout(layout)

        return layouts

    def settingLayouts(self):
        self.settingUI      = SettingUI.SettingUI(self)
        self.userSetting    = UserSetting.UserSetting()

        layouts = [self.settingUI, self.userSetting]

        for layout in layouts:
            self.regisLayout(layout)

        return layouts

    def toolLayouts(self):
        self.calculator     = Calculator.Calculator()
        self.calendar       = Calendar.Calendar()
        self.configuration  = Configuration.Configuration()
        self.engDict        = EnglishDictionary.EnglishDictionary()
        self.findFile       = FindFiles.FindFiles()
        self.imageViewer    = ImageViewer.ImageViewer()
        self.nodeGraph      = NodeGraph.NodeGraph()
        self.noteReminder   = NoteReminder.NoteReminder()
        self.preferences    = Preferences.Preferences()
        self.screenShot     = Screenshot.Screenshot()
        self.textEditor     = TextEditor.TextEditor()

        layouts     = [self.calculator, self.calendar, self.configuration, self.engDict, self.findFile,
                       self.imageViewer, self.nodeGraph, self.noteReminder, self.preferences, self.screenShot,
                       self.textEditor]

        for layout in layouts:
            self.regisLayout(layout)

        return layouts

    def projectLayouts(self):
        self.newProject     = NewProject.NewProject()

        for layout in [self.newProject, ]:
            self.regisLayout(layout)

    @pyqtSlot(object)
    def regisLayout(self, layout):
        key = layout.key
        if not key in self.keys():
            # self.logger.report("Registing layout: {0} \n {1}".format(configKey, layout))
            self[key] = layout
            layout.signals.showLayout.connect(self.showLayout)
        else:
            print("Already registered: {0}".format(key))

    @pyqtSlot(str, str)
    def showLayout(self, name, mode):
        if name == 'app':
            layout = self.parent
        elif name in self.keys():
            layout = self[name]
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

        self.signin                 = self.layoutManager.signin
        self.forgotPW               = self.layoutManager.forgotPW
        self.signup                 = self.layoutManager.signup
        self.mainUI                 = self.layoutManager.mainUI
        self.sysTray                = self.layoutManager.sysTray

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
                    if not self.appCore.sysTray.isSystemTrayAvailable():
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

    @pyqtSlot(str)
    def get_report(self, param):
        self.logger.report(param)

    def set_styleSheet(self, style):
        stylesheet = dict(darkstyle=StyleSheets('dark').changeStylesheet, stylesheet=StyleSheets('bright').changeStylesheet, )
        self.setStyleSheet(stylesheet[style])
        self.settings.initSetValue('styleSheet', 'dark')

    pyqtSlot()
    def closeEvent(self, event):
        self._closing = True
        self.thread_manager.waitForDone()


if __name__ == '__main__':
    PLM()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved