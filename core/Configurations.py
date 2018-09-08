# -*- coding: utf-8 -*-
"""

Script Name: Configurations.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
from __future__ import absolute_import, print_function, unicode_literals

# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, platform, json, subprocess, pkg_resources, shutil

# PLM
from bin.data.pydamg.element import DCfg

# PtQt5
from PyQt5.QtCore import (pyqtSignal, QByteArray, QDataStream, QIODevice, QThread)
from PyQt5.QtNetwork import (QTcpServer, QTcpSocket)

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

from core.Loggers import Loggers



class ConfigSystem(DCfg):

    def __init__(self, root=None, mode=None):

        if root is None:
            raise EnvironmentError("Need a specific path to be able to config evironment key")
        else:
            if not os.path.exists(root):
                raise EnvironmentError("Need a valid path to be able to config evironment key")
            else:
                self._root = root
                try:
                    os.getenv('ROOT')
                except KeyError:
                    subprocess.Popen('SetX {0} {1}'.format('ROOT', self._root), shell=True).wait()
                else:
                    if os.getenv('ROOT') != self._root:
                        subprocess.Popen('SetX {0} {1}'.format('ROOT', self._root), shell=True).wait()

        self._device_name               = platform.node()

        self._os_name                   = platform.system()
        self._os_type                   = platform.machine()
        self._os_version                = platform.version()

        self._osInfo                    = "{0} - {1} - ver:{2}".format(self._os_name, self._os_type, self._os_version)

        self._pyPath                    = sys.prefix

    def __str__(self):
        return json.dumps(self.data, default=lambda obj: obj.data, indent=4)

    def __repr__(self):
        return json.dumps(self.data, default=lambda obj: obj.data, indent=4)

    def data(self):
        self['operating system'] = self._osInfo
        self['os name'] = self._os_name
        self['os version'] = self._os_version
        self['python path'] = self._pyPath

        return self

    @property
    def root(self):
        return self._root

    @property
    def osInfo(self):
        return self._osInfo

    @property
    def device_name(self):
        return self._device_name

    @property
    def python(self):
        key = '%PATH%'
        value = '{0};{1}'.format(key, self._pyPath)
        if not self._pyPath in os.getenv('PATH'):
            subprocess.Popen('SetX {0} {1}'.format(key, value), shell=True).wait()
        return self._pyPath

# -------------------------------------------------------------------------------------------------------------
""" Thread connecting """

class SocketThread(QThread):

    error = pyqtSignal(QTcpSocket.SocketError)

    def __init__(self, socketDescriptor, text, parent):
        super(SocketThread, self).__init__(parent)

        self.logger = Loggers(self)
        self.socketDescriptor = socketDescriptor
        self.text = text

    def run(self):

        tcpSocket = QTcpSocket()

        if not tcpSocket.setSocketDescriptor(self.socketDescriptor):
            self.error.emit(tcpSocket.error())
            self.logger.error(tcpSocket.error())
            return

        block = QByteArray()
        outstr = QDataStream(block, QIODevice.WriteOnly)
        outstr.setVersion(QDataStream.Qt_4_0)
        outstr.writeUInt16(0)
        outstr.writeQString(self.text)
        outstr.device().seek(0)
        outstr.writeUInt16(block.size() - 2)

        tcpSocket.write(block)
        tcpSocket.disconnectFromHost()
        tcpSocket.waitForDisconnected()


class ServerCfg(QTcpServer):

    def incomingConnection(self, socketDescriptor):
        thread = SocketThread(socketDescriptor, "You have notification", self)
        thread.finished.connect(thread.deleteLater)
        thread.start()

class ConfigPython(DCfg):
    pass

import winshell
from platform import system

# PyQt5
from PyQt5 import __file__ as pyqt_path
from PyQt5.QtCore import pyqtSignal

from app import __groupname__, __appname__, __plmWiki__, __pkgsReq__
# PLM

from core.keys import autodeskVer, KEYDETECT, KEYPACKAGE, CONFIG_APPUI, CONFIG_SYSTRAY, FIX_KEY
from core.paths import PLM_LOGO_32, DAMG_LOGO_32, ICON_DIR_32, PROGRAM64, PROGRAM86, LOCALAPPDATA, PROGRAMDATA

# -------------------------------------------------------------------------------------------------------------
""" Configurations """

class Configurations(DCfg):

    key  = 'configurations'
    checkList = dict()
    cfgInfo = dict()
    cfgError = dict()
    cfgReport = pyqtSignal(str)

    def __init__(self, appKey, rootDir, mode='alpha', parent=None):
        super(Configurations, self).__init__(parent)

        self.appKey                     = appKey
        self.rootDir                    = rootDir
        self.mode                       = mode

        self.install_packages           = list()
        self.packages                   = list()
        self.versions                   = list()

        self.cfgs                       = True

        self._pthInfo                   = False
        self._iconInfo                  = False
        self._mainPkgs                  = False
        self._appInfo                   = False

        self.checkList['platform']      = self.cfg_platform()
        self.checkList['root']          = self.cfg_envVariable(self.appKey, self.rootDir)
        self.checkList['paths']         = self.cfg_cfgDir()
        self.checkList['localDB']       = self.cfg_localDB()
        self.checkList['pyqt']          = self.cfg_pyqt_env()
        self.checkList['version']       = self.cfg_pyVersion()
        self.checkList['path']          = self.cfg_pyPath(self.get_pyPth())
        self.checkList['pip']           = self.cfg_pip()
        self.checkList['deepFreeze']    = self.cfg_cx_Freeze()
        self.checkList['requirement']   = self.cfg_requirements()
        self.checkList['maya']          = self.cfg_maya()
        self.checkList['envKeys']       = self.cfg_envVars()
        self.checkList['iconPths']      = self.cfg_iconPth()
        self.checkList['apps']          = self.get_app_installed()
        self.checkList['mainPkg']       = self.cfg_mainPkgs()

        for key in self.checkList.keys():

            if self.checkList[key]:
                continue
            else:
                self.cfgs = False

        self.folder_settings(self.pthInfo['config'], 'h')
        pths, fns = self.get_all_paths(self.pthInfo['config'])
        listObj = pths + fns
        self.batch_folder_settings(listObj, 'h')

    def cfg_platform(self):
        self.cfgInfo['platform'] = system()
        if system() == 'Windows':
            return True
        else:
            return False

    def cfg_envVariable(self, key, value):

        envKeys = [k for k in os.environ.keys()]

        if not key in envKeys:
            os.environ[key] = value
        else:
            if os.getenv(key) != value:
                os.environ[key] = value

        return True

    def cfg_cfgDir(self, fileName='PLM.cfg', **pthInfo):

        pthInfo['root']         = self.rootDir

        pthInfo['bin']          = self.set_dir('bin')
        pthInfo['resource']          = self.set_dir('resource', 'bin')

        pthInfo['config']       = self.set_dir('cfg')
        pthInfo['mtd']          = self.set_dir('mtd', 'cfg')
        pthInfo['setting']      = self.set_dir('settings', 'cfg')
        pthInfo['log']          = self.set_dir('logs', 'cfg')
        pthInfo['cache']        = self.set_dir('cache', 'cfg')
        pthInfo['preferences']  = self.set_dir('preferences', 'cfg')
        pthInfo['tmp']          = self.set_dir('.tmp', 'cfg')

        pthInfo['appData']      = self.set_dir('appData')
        pthInfo['documents']    = self.set_dir('docs', 'appData')
        pthInfo['source']       = self.set_dir('documents', 'appData')

        pthInfo['core']         = self.set_dir('core')

        pthInfo['img']          = self.set_dir('imgs')
        pthInfo['icon']         = self.set_dir('icons', 'imgs')
        pthInfo['avatar']       = self.set_dir('avatar', 'imgs')
        pthInfo['logo']         = self.set_dir('logo', 'imgs')
        pthInfo['picture']      = self.set_dir('pics', 'imgs')
        pthInfo['tag']          = self.set_dir('tags', 'imgs')
        pthInfo['webIcon']      = self.set_dir('web', 'imgs')

        pthInfo['plugin']       = self.set_dir('plg_ins')

        pthInfo['tanker']       = self.set_dir('tankers')
        pthInfo['houdini']      = self.set_dir('pHoudini', 'tankers')
        pthInfo['mari']         = self.set_dir('pMari', 'tankers')
        pthInfo['maya']         = self.set_dir('pMaya', 'tankers')
        pthInfo['nuke']         = self.set_dir('pNuke', 'tankers')
        pthInfo['zbrush']       = self.set_dir('pZBrush', 'tankers')

        pthInfo['ui'] = self.set_dir('ui')

        pthInfo['utilities'] = self.set_dir('utilities')

        for pth in pthInfo.values():
            self.create_folder(pth)
            if not os.path.exists(pth):
                print("Could not create folder: {0}".format(pth))
                self.cfgError['paths error'] = pth

        self.pthInfo = pthInfo
        self._pthInfo = True

        pth = os.path.join(pthInfo['config'], fileName)
        self.compare_data(pth, pthInfo)
        return True

    def cfg_localDB(self):
        if self._pthInfo:
            self.pthInfo['localDB'] = os.path.join(self.pthInfo['appData'], 'local.db')
            if not os.path.exists(self.pthInfo['localDB']):
                from assets.data.SQLS import SQLS
                SQLS(self.pthInfo['localDB'])

        return self._pthInfo

    def cfg_pyqt_env(self):
        if self.checkList['platform']:
            pyqt = os.path.dirname(pyqt_path)
            key = 'QT_QPA_PLATFORM_PLUGIN_PATH'
            value = os.path.join(pyqt, "plugins")
            check = self.cfg_envVariable(key, value)
        else:
            check = False
        return check

    def cfg_pyVersion(self):
        self.pyVersion = float(sys.version[:3])
        self.cfgInfo['version'] = sys.version
        return True

    def cfg_pyPath(self, pyPth):
        sysPths = self.get_system_path()
        addPyPath = False
        for pth in sysPths:
            if pth == pyPth:
                continue
            else:
                addPyPath = True
        if not addPyPath:
            os.environ['PATH'] = os.getenv('PATH') + pyPth
            addPyPath = True

        return addPyPath

    def cfg_pip(self):
        pipVer = self.get_pkg_version('pip')
        if pipVer is None:
            subprocess.Popen('python -m pip install --user --upgrade pip', shell=True).wait()
        else:
            if pipVer < 18.0:
                subprocess.Popen('python -m pip install --user --upgrade pip', shell=True).wait()
        return True

    def cfg_cx_Freeze(self):
        try:
            import cx_Freeze
        except ImportError:
            subprocess.Popen('python -m pip install --user --upgrade cx_Freeze', shell=True).wait()
        finally:
            return True

    def cfg_requirements(self):
        for pkg in __pkgsReq__:
            check = self.check_pyPkg(pkg)
            if not check:
                subprocess.Popen('python -m pip install --user --upgrade {0}'.format(pkg), shell=True).wait()
        return True

    def cfg_maya(self):
        tk = os.path.join(os.getenv(self.appKey), 'tankers', 'pMaya')
        tanker = dict(modules=['anim', 'lib', 'modeling', 'rendering', 'simulating', 'surfacing', ], )

        pVal = ""
        pyList = [os.path.join(tk, k) for k in tanker] + [os.path.join(tk, "modules", p) for p in tanker["modules"]]

        for p in pyList:
            pVal += p + ';'
        os.environ['PYTHONPATH'] = pVal

        usScr = os.path.join(os.getenv(self.appKey), 'packages', 'maya', 'userSetup.py')
        if os.path.exists(usScr):
            mayaVers = [os.path.join(tk, v) for v in autodeskVer if os.path.exists(os.path.join(tk, v))] or []
            if not len(mayaVers) == 0 or not mayaVers == []:
                for usDes in mayaVers:
                    shutil.copy(usScr, usDes)

        self.send_report('Maya is implemented')
        return True

    def cfg_envVars(self, fileName='envKey.cfg', **envKeys):
        for key in os.environ.keys():
            envKeys[key] = os.getenv(key)
        pth = os.path.join(self.pthInfo['config'], fileName)
        self.compare_data(pth, envKeys)
        return True

    def cfg_iconPth(self, fileName='appIcon.cfg', **iconInfo):

        iconInfo['Logo'] = PLM_LOGO_32
        iconInfo['DAMG'] = DAMG_LOGO_32
        iconInfo['Sep'] = 'separato.png'                                           # Custom some info to debug
        iconInfo['File'] = 'file.png'

        iconlst = [i for i in self.get_file_path(ICON_DIR_32) if '.icon' in i]    # Get list of icons in imgage folder

        for i in iconlst:
            iconInfo[os.path.basename(i).split('.icon')[0]] = i

        self.iconInfo = iconInfo
        self._iconInfo = True

        pth = os.path.join(self.pthInfo['config'], fileName)
        self.compare_data(pth, self.iconInfo)

        return True

    def cfg_mainPkgs(self, fileName='main.cfg', **mainInfo):

        self.mainInfo = mainInfo

        delKeys = []
        for key in self.appInfo:
            for k in KEYDETECT:
                if k in key:
                    delKeys.append(key)
                    self.send_report("KEY DETECTED: {0}. Append to list to be deleted later".format(key))

        for key in delKeys:
            self.del_key(key, self.appInfo)

        keepKeys = [k for k in KEYPACKAGE if k in self.appInfo and k in self.iconInfo]

        # Custom functions
        self.mainInfo['About'] = ['About PLM', self.iconInfo['About'], 'About']
        self.mainInfo['Exit'] = ['Exit Pipeline Manager', self.iconInfo['Exit'], 'Exit']
        self.mainInfo['CleanPyc'] = ['Clean ".pyc" files', self.iconInfo['CleanPyc'], 'CleanPyc']
        self.mainInfo['CodeConduct'] = ['Code of Conduct', self.iconInfo['CodeConduct'], 'Code of Conduct']
        self.mainInfo['Contributing'] = ['Contributing', self.iconInfo['Contributing'], 'Contributing']
        self.mainInfo['ReConfig'] = ['Re configuring data', self.iconInfo['Reconfig'], 'Re Config']
        self.mainInfo['Reference'] = ['Reference', self.iconInfo['Reference'], 'Reference']
        self.mainInfo['Command Prompt'] = ['Open command prompt', self.iconInfo['Command Prompt'], 'open_cmd']
        self.mainInfo['PLM wiki'] = ['PLM wiki', self.iconInfo['PLM wiki'], "{key}".format(key=__plmWiki__)]
        self.mainInfo['PLMBrowser'] = ['PlmBrowser', self.iconInfo['PLMBrowser'], "PLMBrowser"]
        self.mainInfo['OpenConfig'] = ['Open config folder', self.iconInfo['OpenConfig'], '']
        self.mainInfo['Version'] = ['Version Info', 'VersionInfo.icon.png', 'Version Info']
        self.mainInfo['licence'] = ['Licence Info', 'LicenceInfo.icon.png', 'Licence Info']

        for key in self.appInfo:
            if 'NukeX' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --nukex"
            elif 'Hiero' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --hiero"
            elif 'UVLayout' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " -launch"

        qtDesigner = os.path.join(os.getenv('PROGRAMDATA'), 'Anaconda3', 'Library', 'bin', 'designer.exe')
        davinciPth = os.path.join(os.getenv('PROGRAMFILES'), 'Blackmagic Design', 'DaVinci Resolve', 'resolve.exe')

        eVal = [qtDesigner, davinciPth]
        eKeys = ['QtDesigner', 'Davinci Resolve 14']

        for key in eKeys:
            if os.path.exists(eVal[eKeys.index(key)]):
                self.mainInfo[key] = [key, self.getAppIcon(32, key), "{0}".format(eVal[eKeys.index(key)])]

        for key in keepKeys:
            self.mainInfo[key] = [key, self.getAppIcon(32, key), "{0}".format(self.appInfo[key])]

        for key in CONFIG_APPUI:
            self.mainInfo[key] = [key, self.getAppIcon(32, key), "{0}".format(key)]

        for key in CONFIG_SYSTRAY:
            if key in self.appInfo:
                self.mainInfo[key] = [key, self.getAppIcon(32, key), self.appInfo[key]]
            else:
                self.mainInfo[key] = [key, self.getAppIcon(32, key), FIX_KEY[key]]

        pth = os.path.join(self.pthInfo['config'], fileName)
        self.compare_data(pth, self.mainInfo)
        return True

    def getAppIcon(self, size=32, iconName="AboutPlm"):
        iconPth = os.path.join(os.getenv(self.appKey), 'imgs', 'icons', "x" + str(size))
        return os.path.join(iconPth, iconName + ".icon.png")

    def get_app_installed(self, fileName='appInfo.cfg', **appInfo):
        shortcuts = {}
        appName = []
        appPth = []

        all_programs = winshell.programs(common=1)

        for dirpath, dirnames, filenames in os.walk(all_programs):
            relpath = dirpath[1 + len(all_programs):]
            shortcuts.setdefault(relpath, []).extend([winshell.shortcut(os.path.join(dirpath, f)) for f in filenames])
        for relpath, lnks in sorted(shortcuts.items()):
            for lnk in lnks:
                name, _ = os.path.splitext(os.path.basename(lnk.lnk_filepath))
                appName.append(name)
                appPth.append(lnk.path)

        for name in appName:
            appInfo[str(name)] = str(appPth[appName.index(name)])

        self.appInfo = appInfo
        self._appInfo = True

        pth = os.path.join(self.pthInfo['config'], fileName)
        self.compare_data(pth, self.appInfo)
        return True

    def get_pkg_version(self, pkg):
        check = self.check_pyPkg(pkg)
        if check:
            return float(self.versions[self.packages.index(pkg)][:4])
        else:
            return None

    def get_system_path(self):
        return os.getenv('PATH').split(';')[0:-1]

    def get_pkgs(self):
        return [(d.project_name, d.version) for d in pkg_resources.working_set]

    def get_pyPth(self):

        if 'Anaconda' in sys.version:
            pyDirName = [f for f in os.listdir(PROGRAMDATA) if 'Anaconda' in f]
            pyPth = os.path.join(PROGRAMDATA, pyDirName[0])
        else:
            pyDirName = [f for f in (os.listdir(PROGRAM86) + os.listdir(PROGRAM64) + os.listdir(LOCALAPPDATA)) if 'python' in f]
            if os.path.exists(os.path.join(PROGRAM86, pyDirName[0])):
                pyPth = os.path.join(PROGRAM86, pyDirName[0])
            elif os.path.exists(os.path.join(PROGRAM64, pyDirName[0])):
                pyPth = os.path.join(PROGRAM64, pyDirName[0])
            else:
                pyPth = os.path.join(LOCALAPPDATA, pyDirName[0])

        if not os.path.exists(os.path.join(pyPth, 'python.exe')):
            for root, directories, files in os.walk(pyPth, topdown=False):
                for filename in files:
                    if filename == 'python.exe':
                        pyPth = os.path.dirname(filename)
                        break

        pths = [f for f in os.getenv('PATH').split(';') if not f == '']

        if not pyPth in pths:
            pth = ""
            for p in pths:
                pth = pth + p + "; "
            pth = pth + pyPth + "; "
            os.environ['PATH'] = pth

        return pyPth

    def get_all_paths(self, directory):
        filePths = []                                                       # List which will store all file paths.
        dirPths = []                                                        # List which will store all folder paths.
        for root, directories, files in os.walk(directory, topdown=False):  # Walk the tree.
            for filename in files:
                filePths.append(os.path.join(root, filename))               # Add to file list.
            for folder in directories:
                dirPths.append(os.path.join(root, folder))                  # Add to folder list.
        return [filePths, dirPths]

    def get_dir_path(self, directory):
        return self.get_all_paths(directory)[1]

    def get_file_path(self, directory):
        return self.get_all_paths(directory)[0]

    def set_dir(self, folName, subRoot=None):
        if self.mode in ['alpha', 'dev', 'test']:
            if subRoot is not None:
                root = self.check_dir(self.rootDir, subRoot)
            else:
                root = self.rootDir
        else:
            localAppData = self.check_dir(os.getenv('LOCALAPPDATA'))
            cfgCompany = self.check_dir(localAppData, __groupname__)
            root = self.check_dir(cfgCompany, __appname__)

        pth = self.check_dir(root, folName)
        return pth

    def check_dir(self, root, folName=None):
        if folName is None:
            pth = root
        else:
            pth = os.path.join(root, folName)
        return pth

    def check_pyPkg(self, pkg):
        self.install_packages = self.get_pkgs()
        self.packages = [p[0] for p in self.install_packages]
        self.versions = [v[1] for v in self.install_packages]
        if pkg in self.packages:
            return True
        else:
            return False

    def compare_data(self, pth, newData={}):
        if os.path.exists(pth):
            with open(pth, 'r') as f:
                oldData = json.load(f)
            if type(oldData) != type(newData):
                return self.save_data(pth, newData)
            else:
                for key, value in oldData.items():
                    if key in newData.keys() and newData[key] == value:
                        continue
                    else:
                        return self.save_data(pth, newData)
        else:
            return self.save_data(pth, newData)

    def save_data(self, filePth, data):
        if os.path.exists(filePth):
            os.remove(filePth)

        with open(filePth, 'w') as f:
            json.dump(data, f, indent=4)
        return True

    def del_key(self, key, data):
        try:
            del data[key]
        except KeyError:
            dict.pop(key, None)

    def send_report(self, mess):
        self.cfgReport.emit(mess)

    def folder_settings(self, directory, mode):
        if system() == "Windows" or system() == "Darwin":
            if mode == "h":
                if system() == "Windows":
                    subprocess.call(["attrib", "+H", directory])
                elif system() == "Darwin":
                    subprocess.call(["chflags", "hidden", directory])
            elif mode == "s":
                if system() == "Windows":
                    subprocess.call(["attrib", "-H", directory])
                elif system() == "Darwin":
                    subprocess.call(["chflags", "nohidden", directory])
            else:
                raise (
                    "ERROR: (Incorrect Command) Valid commands are 'HIDE' and 'UNHIDE' (both are not case sensitive)")
        else:
            raise ("ERROR: (Unknown Operating System) Only Windows and Darwin(Mac) are Supported")

    def batch_folder_settings(self, listObj, mode):
        for obj in listObj:
            if os.path.exists(obj):
                self.folder_settings(obj, mode)
            else:
                print('Could not find the specific path: %s' % obj)

    def create_folder(self, pth, mode=0o770):
        if os.path.exists(pth):
            return []

        (head, tail) = os.path.split(pth)
        res = self.create_folder(head, mode)
        try:
            original_umask = os.umask(0)
            os.makedirs(pth, mode)
        finally:
            os.umask(original_umask)

        os.chmod(pth, mode)

        res += [pth]
        return res

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/08/2018 - 6:20 PM
# © 2017 - 2018 DAMGteam. All rights reserved