# -*- coding: utf-8 -*-
"""

Script Name: _data.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, platform, subprocess, json, shutil, pkg_resources, requests
from platform import system

PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT

try:
    from importlib import reload
except ImportError:
    pass

PLATFORM = 'Windows'
API_MINIMUM = 0.64

# PyQt5
from PyQt5                          import __file__ as pyqt_path
from PyQt5.QtCore                   import QProcess

from appData                        import metadatas as m
from .dirs                          import *
from .pths                          import *
from .text                          import *
from .keys                          import *
from .settingFormats                import *
from .settingOptions                import *
from bin.data.localSQL              import SQLS
from bin                            import DAMG, DAMGDICT, DAMGLIST

try:
    import winshell
except ImportError:
    subprocess.Popen('python -m pip install winshell --user', shell=True).wait()
    import winshell

from cores.EnvVariableManager       import EnvVariableManager

# -------------------------------------------------------------------------------------------------------------
""" Environment configKey """

__envKey__              = m.__envKey__
PLMAPPID                = m.PLMAPPID
VERSION                 = m.VERSION
COPYRIGHT               = m.COPYRIGHT

# -------------------------------------------------------------------------------------------------------------
""" DAMG team """

__copyright__           = m.COPYRIGHT
__organization__        = m.__organization__
__groupname__           = m.__groupname__
__damgSlogan__          = m.__damgSlogan__
__website__             = m.__website__
__author1__             = m.__author1__
__author2__             = m.__author2__
__Founder__             = m.__author1__
__CoFonder1__           = m.__author2__
__email1__              = m.__email1__
__email2__              = m.__email2__

# -------------------------------------------------------------------------------------------------------------
""" PipelineTool """

__project__             = m.__project__
__appname__             = m.__appname__
__appShortcut__         = m.__appShortcut__
__version__             = m.__version__
__versionFull__         = m.VERSION
__cfgVersion__          = m.__cfgVersion__
__verType__             = m.__verType__
__reverType__           = m.__reverType__
__about__               = m.__about__
__homepage__            = m.__homepage__
__plmSlogan__           = m.__plmSlogan__
__plmWiki__             = m.__plmWiki__

# -------------------------------------------------------------------------------------------------------------
""" Server """

__globalServer__        = m.__globalServer__
__globalServerCheck__   = m.__globalServerCheck__
__globalServerAutho__   = m.__globalServerAutho__

__localPort__           = m.__localPort__
__localHost__           = m.__localHost__
__localServer           = m.__localServer__
__localServerCheck__    = m.__localServerCheck__
__localServerAutho__    = m.__localServerAutho__

__google__              = m.__google__
__googleVN__            = m.__googleVN__
__googleNZ__            = m.__googleNZ__

__email__               = m.__email__

__packages_dir__        = m.__packages_dir__
__classifiers__         = m.__classifiers__
__download__            = m.__download__
__description__         = m.__description__
__readme__              = m.__readme__
__modules__             = m.__modules__
__pkgsReq__             = m.__pkgsReq__



# -------------------------------------------------------------------------------------------------------------
""" Config directories """

class ConfigManager(DAMG):

    key                                 = 'Configurations'

    checkList                           = DAMGDICT()
    install_packages                    = DAMGDICT()
    mainInfo                            = DAMGDICT()

    appInfo                             = DAMGDICT()
    deviceInfo                          = DAMGDICT()
    dirInfo                             = DAMGDICT()
    pthInfo                             = DAMGDICT()
    pyInfo                              = DAMGDICT()
    envInfo                             = DAMGDICT()
    iconInfo                            = DAMGDICT()
    avatarInfo                          = DAMGDICT()
    logoInfo                            = DAMGDICT()
    mayaIconInfo                        = DAMGDICT()
    nodeIconInfo                        = DAMGDICT()
    tagIconInfo                         = DAMGDICT()
    webInfo                             = DAMGDICT()
    picInfo                             = DAMGDICT()

    packages                            = DAMGLIST()
    versions                            = DAMGLIST()

    printOutput                         = False
    subprocess                          = False
    cfgs                                = True
    _pthInfo                            = False
    _iconInfo                           = False
    _mainPkgs                           = False
    _appInfo                            = False

    allInfo                             = DAMGDICT()
    allInfo.add('system', deviceInfo)
    allInfo.add('dirs', dirInfo)
    allInfo.add('paths', pthInfo)
    allInfo.add('pyPths', pyInfo)
    allInfo.add('env', envInfo)
    allInfo.add('icon', iconInfo)
    allInfo.add('avatar', avatarInfo)
    allInfo.add('logo', logoInfo)
    allInfo.add('mayaIcon', mainInfo)
    allInfo.add('nodeIcon', nodeIconInfo)
    allInfo.add('tagIcon', tagIconInfo)
    allInfo.add('webIcon', webInfo)
    allInfo.add('pics', picInfo)

    def __init__(self):
        super(ConfigManager, self).__init__(self)

        self.appKey                     = 'DAMGTEAM'
        self.rootDir                    = ROOT_DIR

        if self.subprocess:
            self.process = subprocess.Popen
        else:
            self.process = QProcess

        self.checkList['platform']      = self.cfg_platform()
        self.checkList['dirs']          = self.cfg_cfgDir()
        self.checkList['paths']         = self.cfg_cfgPth()
        self.checkList['localDB']       = self.cfg_localDB()
        self.checkList['python path']   = self.cfg_pyPath(self.get_pyPth())
        self.checkList['requirement']   = self.cfg_requirements()
        self.checkList['maya']          = self.cfg_maya()
        self.checkList['envKeys']       = self.cfg_envVars()
        self.checkList['icon']          = self.cfg_iconPth()
        self.checkList['avatar']        = self.cfg_avatarPth()
        self.checkList['logo']          = self.cfg_logoPth()
        self.checkList['mayaIcon']      = self.cfg_mayaIconPth()
        self.checkList['nodeIcon']      = self.cfg_nodeIconPth()
        self.checkList['apps']          = self.cfg_app_installed()
        self.checkList['mainPkg']       = self.cfg_mainPkgs()

        for key in self.checkList.keys():

            if self.checkList[key]:
                continue
            else:
                self.cfgs = False
                break
        self.folder_settings(CFG_DIR, 'h')
        pths, fns = self.get_all_paths(CFG_DIR)
        listObj = pths + fns
        self.batch_folder_settings(listObj, 'h')

        self.allInfo.update()
        # with open(os.path.join(CFG_DIR, 'masters.cfg'), 'w+') as f:
        #     json.dump(self.allInfo, f, indent=4)
        #     f.close()

    def cfg_platform(self):

        sysOpts                             = SYS_OPTS
        cache                               = subprocess.Popen("SYSTEMINFO", stdin=PIPE, stdout=PIPE)
        source                              = cache.communicate()[0].decode('utf-8')

        self.deviceInfo['os']               = system()
        self.deviceInfo['os version']       = platform.version()
        self.deviceInfo['os system']        = platform.machine()
        self.deviceInfo['device name']      = platform.node()

        self.deviceInfo['python']           = platform.python_build()
        self.deviceInfo['python version']   = platform.python_version()

        values = {}

        for opt in sysOpts:
            values[opt] = [item.strip() for item in re.findall("%s:\w*(.*?)\n" % (opt), source, re.IGNORECASE)][0]

        r = requests.get('https://api.ipdata.co').json()
        print(r)

        for key in r:
            k = (str(key))
            for c in ['ip', 'city', 'country_name']:
                if k == c:
                    self.deviceInfo[k] = str(r[key])
                else:
                    self.deviceInfo[k] = 'unknown'

        self.deviceInfo.add('values', values)

        self.save_data(deviceCfg, self.deviceInfo)
        return True

    def cfg_cfgDir(self):
        from . import dirs
        notKeys = ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__file__', '__cached__',
                   '__builtins__', 'os', '__envKey__', 'cfgdir']
        keys = [k for k in vars(dirs).keys() if not k in notKeys]
        for k in keys:
            self.dirInfo[k] = vars(dirs)[k].replace('\\', '/')

        self.save_data(dirCfg, self.dirInfo)

        return True

    def cfg_cfgPth(self):
        from . import pths
        notKeys = ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__file__', '__cached__',
                   '__builtins__', 'os', '__envKey__', 'cfgdir', 'CFG_DIR', 'SETTING_DIR', 'DB_DIR', 'LOG_DIR',
                   'QSS_DIR', 'RCS_DIR', 'SCSS_DIR']

        keys = [k for k in vars(pths).keys() if not k in notKeys]
        for k in keys:
            self.pthInfo[k] = vars(pths)[k]

        self.save_data(pthCfg, self.pthInfo)
        return True

    def cfg_localDB(self):
        if not os.path.exists(LOCAL_DB):
            SQLS(LOCAL_DB)
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

    def cfg_requirements(self):
        for pkg in __pkgsReq__:
            check = self.check_pyPkg(pkg)
            if not check:
                cmd = 'python -m pip install --user --upgrade {0}'.format(pkg)
                self.run_command(cmd, self.printOutput)

        return True

    def cfg_maya(self):

        tanker = dict(modules=['anim', 'lib', 'modeling', 'rendering', 'simulating', 'surfacing', ], )

        pVal = ""
        pyList = [os.path.join(MAYA_DIR, k) for k in tanker] + [os.path.join(MAYA_DIR, "modules", p) for p in tanker["modules"]]

        for p in pyList:
            pVal += p + ';'

        EnvVariableManager('PYTHONPATH', pVal, 'add')

        usScr = os.path.join(MAYA_DIR, 'userSetup.py')
        if os.path.exists(usScr):
            mayaVers = [os.path.join(MAYA_DIR, v) for v in autodeskVer if os.path.exists(os.path.join(MAYA_DIR, v))] or []
            if not len(mayaVers) == 0 or not mayaVers == []:
                for usDes in mayaVers:
                    shutil.copy(usScr, usDes)

        return True

    def cfg_envVars(self):
        for key in os.environ.keys():
            self.envInfo[key] = os.getenv(key)

        self.save_data(pyEnvCfg, self.envInfo)
        return True

    def cfg_iconPth(self):

        icon12 = DAMGDICT()
        icon16 = DAMGDICT()
        icon24 = DAMGDICT()
        icon32 = DAMGDICT()
        icon48 = DAMGDICT()
        icon64 = DAMGDICT()

        for i in  [i.replace('\\', '/') for i in self.get_file_path(ICON_DIR_12) if '.icon' in i]:
            icon12.add(os.path.basename(i).split('.icon')[0], i)

        for i in  [i.replace('\\', '/') for i in self.get_file_path(ICON_DIR_16) if '.icon' in i]:
            icon16.add(os.path.basename(i).split('.icon')[0], i)

        for i in  [i.replace('\\', '/') for i in self.get_file_path(ICON_DIR_24) if '.icon' in i]:
            icon24.add(os.path.basename(i).split('.icon')[0], i)

        icon32['Logo'] = os.path.join(os.getenv(self.appKey), 'imgs/logo/PLM', '32x32.png')
        icon32['DAMG'] = os.path.join(os.getenv(self.appKey), 'imgs/logo/DAMGTEAM', '32x32.png')
        icon32['Sep'] = 'separato.png'                                           # Custom some info to debug
        icon32['File'] = 'file.png'

        for i in  [i.replace('\\', '/') for i in self.get_file_path(ICON_DIR_32) if '.icon' in i]:
            icon32.add(os.path.basename(i).split('.icon')[0], i)

        for i in  [i.replace('\\', '/') for i in self.get_file_path(ICON_DIR_48) if '.icon' in i]:
            icon48.add(os.path.basename(i).split('.icon')[0], i)

        for i in  [i.replace('\\', '/') for i in self.get_file_path(ICON_DIR_64) if '.icon' in i]:
            icon64.add(os.path.basename(i).split('.icon')[0], i)

        self.iconInfo.add('icon12', icon12)
        self.iconInfo.add('icon16', icon16)
        self.iconInfo.add('icon32', icon32)
        self.iconInfo.add('icon48', icon48)
        self.iconInfo.add('icon64', icon64)

        self._iconInfo = True

        self.save_data(appIconCfg, self.iconInfo)
        return True

    def cfg_avatarPth(self):
        for i in [i.replace('\\', '/') for i in self.get_file_path(AVATAR_DIR) if '.avatar' in i]:
            self.avatarInfo.add(os.path.basename(i).split('.avatar')[0], i)

        self.save_data(avatarCfg, self.avatarInfo)
        return True

    def cfg_logoPth(self):

        plmInfo = DAMGDICT()
        damgInfo = DAMGDICT()

        for i in [i.replace('\\', '/') for i in self.get_file_path(DAMG_LOGO_DIR)]:
            damgInfo.add(os.path.basename(i), i)

        for i in [i.replace('\\', '/') for i in self.get_file_path(PLM_LOGO_DIR)]:
            plmInfo.add(os.path.basename(i), i)

        self.logoInfo.add('PLM', plmInfo)
        self.logoInfo.add('DAMGTEAM', damgInfo)

        self.save_data(logoCfg, self.logoInfo)
        return True

    def cfg_mayaIconPth(self):
        for i in [i.replace('\\', '/') for i in self.get_file_path(MAYA_ICON_DIR) if '.icon' in i]:
            self.mayaIconInfo.add(os.path.basename(i).split('.icon')[0], i)

        self.save_data(mayaIconCfg, self.mayaIconInfo)
        return True

    def cfg_nodeIconPth(self):
        for i in [i.replace('\\', '/') for i in self.get_file_path(NODE_ICON_DIR)]:
            self.nodeIconInfo.add(os.path.basename(i), i)

        self.save_data(nodeIconCfg, self.nodeIconInfo)
        return True

    def cfg_picInfo(self):

        for i in [i.replace('\\', '/') for i in self.get_file_path(PIC_DIR)]:
            self.picInfo.add(os.path.basename(i), i)

        self.save_data(picCfg, self.picInfo)
        return True

    def cfg_app_installed(self):
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
            self.appInfo[str(name)] = str(appPth[appName.index(name)])

        self._appInfo = True

        self.save_data(appsCfg, self.appInfo)
        return True

    def cfg_mainPkgs(self):

        delKeys = []
        for key in self.appInfo:
            for k in KEYDETECT:
                if k in key:
                    delKeys.append(key)
                    # print("KEY DETECTED: {0}. Append to list to be deleted later".format(configKey))

        for key in delKeys:
            self.del_key(key, self.appInfo)

        keepKeys = [k for k in KEYPACKAGE if k in self.appInfo and k in self.iconInfo['icon32']]
        # Custom functions

        # show layout
        self.mainInfo['About']                  = ['About PLM', self.iconInfo['icon32']['About'], 'About']
        self.mainInfo['CodeOfConduct']          = ['Code of Conduct', self.iconInfo['icon32']['CodeOfConduct'], 'CodeOfConduct']
        self.mainInfo['Contributing']           = ['Contributing', self.iconInfo['icon32']['Contributing'], 'Contributing']
        self.mainInfo['ReConfig']               = ['Re configuring qssPths', self.iconInfo['icon32']['ReConfig'], 'ReConfig']
        self.mainInfo['Reference']              = ['Reference', self.iconInfo['icon32']['Reference'], 'Reference']
        self.mainInfo['PLM wiki']               = ['PLM wiki', self.iconInfo['icon32']['PLM wiki'], "{key}".format(key=__plmWiki__)]
        self.mainInfo['Browser']                = ['Browser', self.iconInfo['icon32']['Browser'], "Browser"]
        self.mainInfo['OpenConfig']             = ['Open config folder', self.iconInfo['icon32']['OpenConfig'], '']
        self.mainInfo['Version']                = ['Version Info', 'Version', 'Version']
        self.mainInfo['Licence']                = ['Licence Info', 'Licence', 'Licence Info']

        self.mainInfo['Organisation']           = ['Organisation', 'OrganisationManager', 'Organisation']
        self.mainInfo['Team']                   = ['Team', 'TeamManager', 'Team']
        self.mainInfo['Project']                = ['Project', 'ProjectManager', 'Project']
        self.mainInfo['Task']                   = ['Task', 'TaskManager', 'Task']

        self.mainInfo['SettingUI']              = ['PLM Settings', 'Settings', 'SettingUI']
        self.mainInfo['Configuration']          = ['PLM Configuration', 'Configuration', 'Configuration']
        self.mainInfo['Showall']                = ['showall', 'ShowAll', 'showall']

        self.mainInfo['Alpha']                  = ['Open Alpha Map Library', 'AlphaLibrary', 'AlphaLibrary']
        self.mainInfo['HDRI']                   = ['Open HDRI Map Library', 'HDRILibrary', 'HDRILibrary']
        self.mainInfo['Texture']                = ['Open Texture Map Library', 'TextureLibrary', 'TextureLibrary']

        self.mainInfo['Feedback']               = ['Feedback', 'Feedback', 'Feedback']
        self.mainInfo['ContactUs']              = ['Contact Us', 'ContactUs', 'ContactUs']

        self.mainInfo['Restore']                = ['Restore', 'Restore', 'PipelineManager']
        self.mainInfo['Maximize']               = ['Maximize', 'Maximize', 'PipelineManager']
        self.mainInfo['Minimize']               = ['Minimize', 'Minimize', 'PipelineManager']

        self.mainInfo['Apperance']              = ['Appearance', 'Appearance', 'Appearance']

        # Executing
        self.mainInfo['CleanPyc']               = ['Clean ".pyc" files', self.iconInfo['icon32']['CleanPyc'], 'CleanPyc']
        self.mainInfo['Debug']                  = ['Run PLM Debugger', self.iconInfo['icon32']['Debug'], 'Debug']
        self.mainInfo['Exit']                   = ['Exit PLM', self.iconInfo['icon32']['Exit'], 'Exit']
        self.mainInfo['ConfigFolder']           = ['Go To Config Folder', 'ConfigFolder', CFG_DIR]
        self.mainInfo['IconFolder']             = ['Go To Icon Folder', 'IconFolder', APP_ICON_DIR]
        self.mainInfo['SettingFolder']          = ['Go To Setting Folder', 'SettingFolder', SETTING_DIR]
        self.mainInfo['AppFolder']              = ['Go To PLM Folder', 'AppFolder', ROOT_DIR]
        self.mainInfo['Command Prompt']         = ['Open command prompt', self.iconInfo['icon32']['Command Prompt'], 'open_cmd']

        self.mainInfo['Cut']                    = ['Cut', 'Cut', 'Cut']
        self.mainInfo['Copy']                   = ['Copy', 'Copy', 'Copy']
        self.mainInfo['Paste']                  = ['Paste', 'Paste', 'Paste']

        self.mainInfo['bright']                 = ['bright', 'bright', 'bright']
        self.mainInfo['dark']                   = ['dark', 'dark', 'dark']
        self.mainInfo['chacoal']                = ['chacoal', 'chacoal', 'chacoal']
        self.mainInfo['nuker']                  = ['nuker', 'nuker', 'nuker']

        # Update link
        self.mainInfo['pythonTag']              = ['pythonLink', 'pythonTagIcon', 'https://docs.anaconda.com/anaconda/reference/release-notes/']
        self.mainInfo['licenceTag']             = ['licenceLink', 'licenceTagIcon', 'https://github.com/vtta2008/damgteam/blob/master/LICENCE']
        self.mainInfo['versionTag']             = ['versionLink', 'versionTagIcon', 'https://github.com/vtta2008/damgteam/blob/master/appData/documentations/version.rst']

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
            if key == 'UserSetting':
                self.mainInfo[key] = ['Profile', self.getAppIcon(32, key), 'User Profile']
            elif key == 'SignIn':
                self.mainInfo[key] = ['Sign In', self.getAppIcon(32, key), 'SignIn']
            elif key == 'SignUp':
                self.mainInfo[key] = ['New Account', self.getAppIcon(32, key), 'Create new account']
            elif key == 'SwtichAccount':
                self.mainInfo[key] = ['Change Account', self.getAppIcon(32, key), 'Change other account']
            elif key == 'SignOut':
                self.mainInfo[key] = ['Sign Out', self.getAppIcon(32, key), 'Log Out']
            else:
                self.mainInfo[key] = [key, self.getAppIcon(32, key), "{0}".format(key)]

        for key in CONFIG_SYSTRAY:
            if key in self.appInfo:
                self.mainInfo[key] = [key, self.getAppIcon(32, key), self.appInfo[key]]
            elif key in FIX_KEY.keys():
                self.mainInfo[key] = [key, self.getAppIcon(32, key), FIX_KEY[key]]
            else:
                self.mainInfo[key] = [key, self.getAppIcon(32, key), key]

        self.save_data(mainCfg, self.mainInfo)

        return True

    def getAppIcon(self, size=32, iconName="AboutPlm"):
        return os.path.join(ICON_DIR_32, iconName + ".icon.png")

    def get_pkg_version(self, pkg):
        check = self.check_pyPkg(pkg)
        if check:
            return float(self.versions[self.packages.index(pkg)][:4])
        else:
            return None

    def get_system_path(self):
        return os.getenv('PATH').split(';')[0:-1]

    def get_pkgs(self):
        for py in pkg_resources.working_set:
            self.pyInfo.add(py.project_name, py.version)

        self.save_data(pyPackageCfg, self.pyInfo)

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
            EnvVariableManager('PATH', pth, 'add')

        return True

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
        if self.mode.config in ['Alpha', 'alpha', 'dev', 'test']:
            if subRoot is not None:
                root = self.check_dir(self.rootDir, subRoot)
            else:
                root = self.rootDir
        else:
            localAppData = self.check_dir(os.path.join(self.rootDir, 'appData/.config'))
            cfgCompany = self.check_dir(localAppData, __groupname__)
            root = self.check_dir(cfgCompany, __appname__)

        pth = self.check_dir(root, folName)
        # print("Set directory: {}".format(pth))
        return pth

    def check_dir(self, root, folName=None):
        if folName is None:
            pth = root
        else:
            pth = os.path.join(root, folName).replace('\\', '/')
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

        with open(filePth, 'w+') as f:
            json.dump(data, f, indent=4)
            f.close()
        return True

    def del_key(self, key, data):
        try:
            del data[key]
        except KeyError:
            dict.pop(key, None)

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
                    "CommandIncorrectError: Expected command 'HIDE' and 'UNHIDE' (both are not case sensitive)")
        else:
            raise ("PlatformCompatibleError: (Unknown Operating System) Only Windows and Darwin(Mac) are Supported")

    def batch_folder_settings(self, listObj, mode):
        for obj in listObj:
            if os.path.exists(obj):
                self.folder_settings(obj, mode)
            else:
                print('{0}: PathError: Could not find the specific path: {1}'.format(self.__class__.__name__, obj))

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

    def run_command(self, cmd, printOutput=False):
        args = [arg for arg in cmd.split(' ')]
        # print( '%s %s' % (cmd, ' '.join( args )) )
        t = " ".join(args)
        if self.subprocess:
            try:
                if sys.platform == 'win32':
                    proc = self.process(args=args, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=False)
                else:
                    proc = self.process(args=args, close_fds=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
                output = proc.stdout.read()
                proc.wait()
            except EnvironmentError as e:
                output = 'ErrorRunning {0} {1}: {2}'.format(cmd, t, str(e))
        else:
            proc = self.process()
            proc.setStandardInputFile(proc.nullDevice())
            proc.setStandardOutputFile(proc.nullDevice())
            proc.setStandardErrorFile(proc.nullDevice())

            if proc.state() != 2:
                proc.waitForStarted()
                proc.waitForFinished()
                if "|" in t or ">" in t or "<" in t:
                    proc.start('sh -c "' + cmd + ' ' + t + '"')
                else:
                    proc.start(cmd + " " + t)

            try:
                output = str(proc.readAll(), encoding='utf8').rstrip()
            except TypeError:
                output = str(proc.readAll()).rstrip()

        if printOutput:
            print(output.decode().replace('\\', '/'))

        return output

configManager = ConfigManager()

# -------------------------------------------------------------------------------------------------------------
""" Config qssPths from text file """

def read_file(fileName):

    filePth = os.path.join(RAWS_DATA_DIR, fileName)

    if not os.path.exists(filePth):
        filePth = os.path.join(DOCUMENTATION_DIR, "{}.rst".format(fileName))

    if os.path.exists(filePth):
        with open(filePth, 'r') as f:
            data = f.read()
        return data

QUESTIONS = read_file('QUESTION')
ABOUT = read_file('ABOUT')
CREDIT = read_file('CREDIT')
CODECONDUCT = read_file('CODECONDUCT')
CONTRIBUTING = read_file('CONTRIBUTING')
REFERENCE = read_file('REFERENCE')
LICENCE_MIT = read_file('LICENCE_MIT')

actionTypes = ['DAMGACTION', 'DAMGShowLayoutAction', 'DAMGStartFileAction', 'DAMGExecutingAction', 'DAMGOpenBrowserAction', ]

layoutTypes = ['DAMGUI', 'DAMGWIDGET', ] + actionTypes

with open(mainCfg, 'r') as f:
    mainData = json.load(f)
    f.close()

CONFIG_OFFICE = [k for k in mainData.keys() if k in CONFIG_OFFICE]

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:56 PM
# Pipeline manager - DAMGteam
