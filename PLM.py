# -*- coding: utf-8 -*-
"""

Script Name: PLM.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is master file of Pipeline Manager

"""
# -------------------------------------------------------------------------------------------------------------
""" Set up environment variable """

# Python
import os, sys, subprocess, requests, ctypes, pkg_resources
from core.Loggers import SetLogger
logger = SetLogger()
report = logger.report

key = "PIPELINE_MANAGER"
ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)))
requirements = ['deprecate', 'msgpack', 'winshell', 'pandas', 'wheel', 'argparse', 'green']
envKeys = [k for k in os.environ.keys()]
program86 = os.getenv('PROGRAMFILES(X86)')
program64 = os.getenv('PROGRAMW6432')

try:
    os.getenv(key)
except KeyError:
    os.environ[key] = ROOT
else:
    if os.getenv(key) != ROOT:
        os.environ[key] = ROOT

class Configurations(object):

    checkList = dict()

    def __init__(self):
        super(Configurations, self).__init__()

        self.install_packages = []
        self.packages = []
        self.versions = []
        self.cfgs = True
        self.pyVersion = float(sys.version[:3])
        pyRoot, pyFolder = self.get_installed_pyPth()
        pyPth = os.path.join(pyRoot, pyFolder)

        self.cfgPyVer = True
        self.cfgPyPth = self.add_python_into_path(pyPth)
        self.cfgPip = self.config_pip()
        self.cfgFree = self.config_deepFreeze()
        self.cfgReqs = self.check_pkg_required()

        self.checkList['python version'] = self.cfgPyVer
        self.checkList['python path'] = self.cfgPyPth
        self.checkList['config pip'] = self.cfgPip
        self.checkList['config deepFreeze'] = self.cfgFree
        self.checkList['python requirement'] = self.cfgReqs

        for key in self.checkList.keys():
            value = self.checkList[key]
            if value is True:
                continue
            else:
                self.cfgs = False

        from pprint import pprint
        pprint(self.checkList)

        if not self.cfgs:
            print('configurations is not completed!')
        else:
            print('configuration completed!')


    def config_pip(self):
        pipVer = self.get_pkg_version('pip')
        if pipVer is None:
            subprocess.Popen('python -m pip install --user --upgrade pip', shell=True).wait()
        else:
            if pipVer < 18.0:
                subprocess.Popen('python -m pip install --user --upgrade pip', shell=True).wait()
        return True

    def config_deepFreeze(self):
        try:
            import cx_Freeze
        except ImportError:
            subprocess.Popen('python -m pip install --user --upgrade cx_Freeze', shell=True).wait()
        finally:
            return True

    def check_pkg_install(self, pkg):
        self.install_packages = self.get_installed_pkgs()
        self.packages = [p[0] for p in self.install_packages]
        self.versions = [v[1] for v in self.install_packages]
        if pkg in self.packages:
            return True
        else:
            return False

    def check_pkg_required(self):
        for pkg in requirements:
            check = self.check_pkg_install(pkg)
            print('check package: {0}'.format(pkg))
            if not check:
                subprocess.Popen('python -m pip install --user --upgrade {0}'.format(pkg), shell=True).wait()
        return True

    def add_python_into_path(self, pyPth):
        sysPths = self.get_system_path()
        addPyPath = False
        for pth in sysPths:
            if pth == pyPth:
                continue
            else:
                addPyPath = True

        if addPyPath:
            return True
        else:
            os.environ['PATH'] = os.getenv('PATH') + pyPth
            return True

    def get_pkg_version(self, pkg):
        check = self.check_pkg_install(pkg)
        if check:
            return float(self.versions[self.packages.index(pkg)][:4])
        else:
            return None

    def get_system_path(self):
        return os.getenv('PATH').split(';')[0:-1]

    def get_installed_pkgs(self):
        return [(d.project_name, d.version) for d in pkg_resources.working_set]

    def get_installed_pyPth(self):

        if 'Anaconda' in sys.version:
            pyRoot = os.getenv('PROGRAMDATA')
            if self.pyVersion > 2:
                pyFolder = 'Anaconda3'
            else:
                pyFolder = 'Anaconda2'
        else:
            pyOrgDefault = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'Python')
            if not os.path.exists(pyOrgDefault):
                folder86 = self.get_folder_path(program86)
                folder64 = self.get_folder_path(program64)
                paths = folder86 + folder64
                pyFolder = None
                pyRoot = None
                for pth in paths:
                    if 'python' in pth:
                        pyFolder = os.path.basename(pth)
                        pyRoot = pth.split(pyFolder)[0]
                        break
            else:
                pyRoot = pyOrgDefault
                pyFolder = self.get_folder_path(pyRoot)[0]

        return pyRoot, pyFolder

    def get_all_path_from_dir(self, directory):
        filePths = []                                                       # List which will store all file paths.
        dirPths = []                                                        # List which will store all folder paths.
        for root, directories, files in os.walk(directory, topdown=False):  # Walk the tree.
            for filename in files:
                filePths.append(os.path.join(root, filename))               # Add to file list.
            for folder in directories:
                dirPths.append(os.path.join(root, folder))                  # Add to folder list.
        return [filePths, dirPths]

    def get_folder_path(self, directory):
        self.handle_path_error(directory)
        return self.get_all_path_from_dir(directory)[1]

    def handle_path_error(self, directory=None):
        if not os.path.exists(directory) or directory is None:
            try:
                raise IsADirectoryError("Path is not exists: {directory}".format(directory=directory))
            except IsADirectoryError as error:
                raise ('Caught error: ' + repr(error))

cfg = Configurations()
print(cfg.cfgs)

# PyQt5
from ui.Web.PLMBrowser import PLMBrowser
from PyQt5.QtCore import QThreadPool, pyqtSlot, pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QApplication

# Plm
from appData import (APPINFO, __serverCheck__, PLMAPPID, SYSTRAY_UNAVAI, SETTING_FILEPTH, ST_FORMAT, __appname__,
                     __version__, __organization__, __website__)

from core.Settings import Settings
from core.Cores import AppCores
from core.Specs import Specs
from utilities import Worker
from utilities.localSQL import QuerryDB
from utilities.utils import str2bool, clean_file_ext
from ui.uikits.UiPreset import AppIcon

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PLM(QApplication):

    key = 'console'
    returnValue = pyqtSignal(str, str)

    def __init__(self):
        super(PLM, self).__init__(sys.argv)

        self.organization = __organization__
        self.appName = __appname__
        self.version = __version__
        self.website = __website__
        self.core = QCoreApplication
        self.core.setOrganizationName(self.organization)
        self.core.setApplicationName(self.appName)
        self.core.setOrganizationDomain(self.website)
        self.core.setApplicationVersion(self.version)
        self.layouts = dict()

        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.appInfo = APPINFO
        self.specs = Specs(self.key, self)
        self.cores = AppCores(self)                                                          # Core metadata

        self.logger = SetLogger(self)
        self.threadpool = QThreadPool()                                                     # Thread pool
        self.numOfThread = self.threadpool.maxThreadCount()                                 # Maximum threads available

        self.setWindowIcon(AppIcon("Logo"))                                                 # Set up task bar icon
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(PLMAPPID)             # Change taskbar icon

        from ui.Settings.SettingUI import SettingUI
        self.settingUI = SettingUI()
        self.cores.addLayout.connect(self.addLayout)
        self.addLayout(self.settingUI)
        self.db = QuerryDB()                                                                # Query local database
        self.webBrowser = PLMBrowser()                                                      # Webbrowser
        self.addLayout(self.webBrowser)
        self.login, self.forgotPW, self.signup, self.mainUI, self.sysTray = self.cores.import_uiSet1()
        self.uiSet1 = [self.login, self.forgotPW, self.signup, self.mainUI, self.sysTray]
        self.mainUI.settings = self.settings
        self.setupConn1()

        try:
            self.username, token, cookie, remember = self.db.query_table('curUser')
        except ValueError:
            self.showLayout('login', "show")
        else:
            if not str2bool(remember):
                self.showLayout('login', "show")
            else:
                r = requests.get(__serverCheck__, verify = False, headers = {'Authorization': 'Bearer {0}'.format(token)}, cookies = {'connect.sid': cookie})
                if r.status_code == 200:
                    if not self.cores.sysTray.isSystemTrayAvailable():
                        self.logger.critical(SYSTRAY_UNAVAI)
                        sys.exit(1)
                    self.showLayout('mainUI', "show")
                else:
                    self.showLayout('login', "show")

        self.sysTray.showLayout.connect(self.showLayout)
        self.sysTray.executing.connect(self.executing)

        self.uiSet2 = [self.about, self.calculator, self.calendar, self.codeConduct, self.configuration, self.contributing,
                       self.credit, self.engDict, self.findFile, self.imageViewer, self.licence, self.newProj,
                       self.nodeGraph, self.noteReminder, self.preferences, self.reference, self.screenShot,
                       self.textEditor, self.userSetting, self.version] = self.cores.import_uiSet2()

        self.setupConn2()
        self.set_styleSheet('darkstyle')
        self.setQuitOnLastWindowClosed(False)
        sys.exit(self.exec_())

    def setupConn1(self):
        self.login.showLayout.connect(self.showLayout)
        self.forgotPW.showLayout.connect(self.showLayout)
        self.signup.showLayout.connect(self.showLayout)

        self.mainUI.showLayout.connect(self.showLayout)
        self.mainUI.executing.connect(self.executing)
        self.mainUI.addLayout.connect(self.addLayout)
        self.mainUI.sysNotify.connect(self.sysTray.sysNotify)
        self.mainUI.setSetting.connect(self.setSetting)
        self.mainUI.openBrowser.connect(self.openBrowser)

        self.returnValue.connect(self.mainUI.returnValue)

        self.webBrowser.showLayout.connect(self.showLayout)
        self.settingUI.showLayout.connect(self.showLayout)

        print("setup connected 1")

        self.returnValue.connect(self.mainUI.returnValue)

    def setupConn2(self):
        for layout in self.uiSet2:
            layout.showLayout.connect(self.showLayout)

        print("setup connected 2")

    @property
    def registerUI(self):
        return self.layouts

    @pyqtSlot(str, str)
    def showLayout(self, name, mode):
        self.logger.trace('signal comes: {0}, {1}'.format(name, mode))
        if name == 'app':
            layout = self
        else:
            try:
                layout = self.layouts[name]
            except KeyError:
                self.logger.debug('Key is not registered')
                return
            else:
                self.logger.trace("define layout: {0}".format(layout))

        if mode == "hide":
            layout.hide()
        elif mode == "show":
            layout.show()
        elif mode == 'showNor':
            layout.showNormal()
        elif mode == 'showMin':
            layout.showMinimized()
        elif mode == 'showMax':
            layout.showMaximized()
        elif mode == 'quit' or mode == 'exit':
            layout.quit()

        self.setSetting(layout.key, mode)
        self.logger.trace("{0} layout: {1}".format(mode, layout))

    @pyqtSlot(str)
    def openBrowser(self, url):
        self.webBrowser.setUrl(url)
        self.webBrowser.update()
        self.webBrowser.show()

    @pyqtSlot(str, str, str)
    def setSetting(self, key=None, value=None, grp=None):
        self.logger.trace('signal comes: {0}, {1}, {2}'.format(key, value, grp))
        self.settings.initSetValue(key, value, grp)

    @pyqtSlot(str, str)
    def loadSetting(self, key=None, grp=None):
        self.logger.trace('signal comes: {0}, {1}'.format(key, grp))
        value = self.settings.initValue(key, grp)
        if key is not None:
            self.returnValue.emit(key, value)

    @pyqtSlot(str)
    def executing(self, cmd):
        self.logger.trace('signal comes: {0}'.format(cmd))
        if cmd in self.layouts.keys():
            self.logger.trace('run showlayout: {0}'.format(cmd))
            self.showLayout(cmd, 'show')
        elif os.path.isdir(cmd):
            os.startfile(cmd)
        elif cmd == 'open_cmd':
            self.logger.trace('open command prompt')
            os.system('start /wait cmd')
        elif cmd == 'Remove pyc':
            self.logger.trace("clean .pyc files")
            clean_file_ext('.pyc')
        elif cmd == 'Re-config local':
            from appData.LocalCfg import LocalCfg
            self.logger.trace('re config data')
            LocalCfg()
        else:
            self.logger.trace('execute: {0}'.format(cmd))
            subprocess.Popen(cmd)

    @pyqtSlot(object)
    def addLayout(self, layout):
        key = layout.key
        if not key in self.layouts.keys():
            self.layouts[key] = layout
            self.logger.debug("Registered layout '{0}': {1}".format(key, layout))
        else:
            self.logger.debug("Already registered: {0}".format(key))

    def set_styleSheet(self, style):
        from core.StyleSheets import StyleSheets
        stylesheet = dict(darkstyle=StyleSheets('darkstyle').changeStylesheet, stylesheet=StyleSheets('stylesheet').changeStylesheet, )
        self.setStyleSheet(stylesheet[style])

    def multiThread(self, fn):
        worker = Worker.Worker(fn)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)
        return worker

    def progress_fn(self, n):
        print("%d%% done" % n)

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE")

if __name__ == '__main__':
    PLM()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved