# -*- coding: utf-8 -*-
"""

Script Name: Configurations.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, subprocess, pkg_resources, json
from platform import system

# PyQt5
from PyQt5 import __file__ as pyqt_path
from PyQt5.QtCore import pyqtSignal

# PLM
from core.Storage import PObj

key = "PIPELINE_MANAGER"
ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)))
requirements = ['deprecate', 'msgpack', 'winshell', 'pandas', 'wheel', 'argparse', 'green']
program86 = os.getenv('PROGRAMFILES(X86)')
program64 = os.getenv('PROGRAMW6432')
__groupname__ = "DAMGteam"
__appname__ = "PLM"

class Configurations(PObj):

    key  = 'configurations'
    checkList = dict()
    checkInfo = dict()
    cfgReport = pyqtSignal(str)

    def __init__(self, appKey, rootDir, mode='alpha', parent=None):
        super(Configurations, self).__init__(parent)

        self.appKey                     = appKey
        self.rootDir                    = rootDir
        self.mode                       = mode
        self.install_packages           = list()
        self.packages                   = list()
        self.versions                   = list()
        self._pthInfo                   = False
        self.cfgs                       = True

        self.cfgOs                      = self.cfg_platform()
        self.cfgRoot                    = self.cfg_envVariable(self.appKey, self.rootDir)
        self.cfgCfgPth                  = self.cfg_cfgDir()
        self.cfgLocalDB                 = self.cfg_localDB()
        self.cfgPyQt                    = self.cfg_pyqt_env()
        self.cfgPyVer                   = self.cfg_pyVersion()
        self.cfgPyPth                   = self.cfg_pyPath(self.get_pyPth())
        self.cfgPip                     = self.cfg_pip()
        self.cfgFree                    = self.cfg_deepFreeze()
        self.cfgReqs                    = self.cfg_requirements()

        self.checkList['platform']      = self.cfgOs
        self.checkList['root']          = self.cfgRoot
        self.checkList['paths']         = self.cfgCfgPth
        self.checkList['localDB']       = self.cfgLocalDB
        self.checkList['pyqt']          = self.cfgPyQt
        self.checkList['version']       = self.cfgPyVer
        self.checkList['path']          = self.cfgPyPth
        self.checkList['pip']           = self.cfgPip
        self.checkList['deepFreeze']    = self.cfgFree
        self.checkList['requirement']   = self.cfgReqs

        for key in self.checkList.keys():
            if self.checkList[key]:
                continue
            else:
                self.cfgs = False

        if not self.cfgs:
            self.send_report('configurations is not completed!')
        else:
            self.send_report('configuration completed!')

    def cfg_platform(self):
        self.checkInfo['platform'] = system()
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

        self.checkInfo[key] = value
        return True

    def cfg_cfgDir(self, fileName='PLM.cfg', **pthInfo):

        pthInfo['root']         = self.rootDir
        pthInfo['config']       = self.set_dir('cfg')
        pthInfo['mtd']          = self.set_dir('mtd', 'cfg')
        pthInfo['setting']      = self.set_dir('settings', 'cfg')
        pthInfo['log']          = self.set_dir('logs', 'cfg')
        pthInfo['cache']        = self.set_dir('cache', 'cfg')
        pthInfo['preferences']  = self.set_dir('preferences', 'cfg')

        pthInfo['appData']      = self.set_dir('appData')
        pthInfo['documents']    = self.set_dir('docs', 'appData')
        pthInfo['source']       = self.set_dir('scr', 'appData')

        pthInfo['core']         = self.set_dir('core')

        pthInfo['img']          = self.set_dir('imgs')
        pthInfo['icon']         = self.set_dir('icons', 'imgs')
        pthInfo['avatar']       = self.set_dir('avatar', 'imgs')
        pthInfo['logo']         = self.set_dir('logo', 'imgs')
        pthInfo['picture']      = self.set_dir('pics', 'imgs')
        pthInfo['tag']          = self.set_dir('tags', 'imgs')
        pthInfo['webIcon']      = self.set_dir('web', 'imgs')

        pthInfo['plugin']       = self.set_dir('plg_ins')

        pthInfo['qss']          = self.set_dir('qss')

        pthInfo['tanker']       = self.set_dir('tankers')
        pthInfo['houdini']      = self.set_dir('pHoudini', 'tankers')
        pthInfo['mari']         = self.set_dir('pMari', 'tankers')
        pthInfo['maya']         = self.set_dir('pMaya', 'tankers')
        pthInfo['nuke']         = self.set_dir('pNuke', 'tankers')
        pthInfo['zbrush']       = self.set_dir('pZBrush', 'tankers')

        pthInfo['tool'] = self.set_dir('tools')

        pthInfo['ui'] = self.set_dir('ui')

        pthInfo['utilities'] = self.set_dir('utilities')

        self.pthInfo = pthInfo
        self._pthInfo = True
        pth = os.path.join(pthInfo['config'], fileName)
        return self.compare_data(pth, pthInfo)

    def cfg_localDB(self):
        if self._pthInfo:
            self.pthInfo['localDB'] = os.path.join(self.pthInfo['appData'], 'local.db')
            if not os.path.exists(self.pthInfo['localDB']):
                from core.SQLS import SQLS
                SQLS()

        return self._pthInfo

    def cfg_pyqt_env(self):
        if self.cfgOs:
            pyqt = os.path.dirname(pyqt_path)
            key = 'QT_QPA_PLATFORM_PLUGIN_PATH'
            value = os.path.join(pyqt, "plugins")
            check = self.cfg_envVariable(key, value)
        else:
            check = False
        return check

    def cfg_pyVersion(self):
        self.pyVersion = float(sys.version[:3])
        self.checkInfo['version'] = sys.version
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

    def cfg_deepFreeze(self):
        try:
            import cx_Freeze
        except ImportError:
            subprocess.Popen('python -m pip install --user --upgrade cx_Freeze', shell=True).wait()
        finally:
            return True

    def cfg_requirements(self):
        for pkg in requirements:
            check = self.check_pyPkg(pkg)
            if not check:
                subprocess.Popen('python -m pip install --user --upgrade {0}'.format(pkg), shell=True).wait()
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
            pyRoot = os.getenv('PROGRAMDATA')
            if self.pyVersion > 2:
                pyFolder = 'Anaconda3'
            else:
                pyFolder = 'Anaconda2'
        else:
            pyOrgDefault = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'Python')
            if not os.path.exists(pyOrgDefault):
                folder86 = self.get_dir_path(program86)
                folder64 = self.get_dir_path(program64)
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
                pyFolder = self.get_dir_path(pyRoot)[0]

        return os.path.join(pyRoot, pyFolder)

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
        self.path_error(directory)
        return self.get_all_paths(directory)[1]

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
        if not os.path.exists(pth):
            os.mkdir(pth)
        return pth

    def check_pyPkg(self, pkg):
        self.install_packages = self.get_pkgs()
        self.packages = [p[0] for p in self.install_packages]
        self.versions = [v[1] for v in self.install_packages]
        if pkg in self.packages:
            return True
        else:
            return False

    def path_error(self, directory=None):
        if not os.path.exists(directory) or directory is None:
            try:
                raise IsADirectoryError("Path is not exists: {directory}".format(directory=directory))
            except IsADirectoryError as error:
                raise ('Caught error: ' + repr(error))

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
        with open(filePth, 'w') as f:
            json.dump(data, f, indent=4)
        return True

    def send_report(self, mess):
        self.cfgReport.emit(mess)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/08/2018 - 6:20 PM
# © 2017 - 2018 DAMGteam. All rights reserved