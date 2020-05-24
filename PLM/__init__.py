# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    This is our source code directory, which should be named by your application or package you are working on.
    Inside we have the usual __init__.py file signifying that it's a Python package, next there is __main__.py
    which is used when we want to run our application directly with python -m blueprint. Last source file here
    is the app.py which is here really just for demonstration purposes. In real project instead of this app.py
    you would have few top level source files and more directories (internal packages). We will get to contents
    of these files a little later. Finally, we also have resources directory here, which is used for any static
    content your application might need, e.g. images, keystore, etc.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
# Python
import os, sys, subprocess
from termcolor                      import cprint
from pyjavaproperties               import Properties

# PLM
from .globalSettings                import GlobalSettings
from .types                         import Version


# -------------------------------------------------------------------------------------------------------------
""" Metadatas """

__envKey__                          = "PLM"
__appName__                         = "Pipeline Manager (PLM)"
__version__                         = Version()
__organization__                    = "DAMGTEAM"
__apiName__                         = "DAMG API"
__apiVersion__                      = Version(0, 0, 1)

TRADE_MARK                          = '™'

def __copyright__():
    return 'Copyright (C) DAMGTEAM. All right reserved.'

def path_exists(path):
    if not os.path.exists(path):
        cprint("PathNotExistsed: {0}".format(path), 'red', attrs=['blink'])
    return os.path.exists(path)

def create_path(*args):
    path                            = os.path.abspath(os.path.join(*args)).replace('\\', '/')
    path_exists(path)
    return path

def current_directory():
    path                            = os.path.abspath(os.getcwd()).replace('\\', '/')
    path_exists(path)
    return path

def parent_dir(path):
    path                            = os.path.abspath(os.path.join(path, os.pardir)).replace('\\', '/')
    path_exists(path)
    return path

def directory_name(path):
    return os.path.basename(path)

# get current directory path
cwd                                 = current_directory()

if directory_name(cwd) == directory_name(parent_dir(cwd)) == __envKey__:
    ROOT_APP                        = parent_dir(cwd)
    ROOT                            = cwd
else:
    if directory_name(cwd) == __envKey__:
        ROOT_APP                    = cwd
        ROOT                        = create_path(ROOT_APP, __envKey__)
    else:
        try:
            os.getenv(__envKey__)
        except KeyError:
            cprint("Wrong root path. Current directory: {0}".format(cwd), 'red', attrs=['underline', 'blink'])
            sys.exit(__copyright__())
        else:
            ROOT                    = os.getenv(__envKey__)
            ROOT_APP                = parent_dir(ROOT)


bindir                              = os.path.join(ROOT_APP, 'bin')
propFile                            = os.path.join(bindir, 'text.properties').replace('\\', '/')
p                                   = Properties()
p.load(open(propFile))
p.list()

LOCALAPPDATA                            = os.getenv('LOCALAPPDATA')
USER_DIR                                = parent_dir(os.getenv('HOME'))

APPDATA_DAMG                            = create_path(LOCALAPPDATA, __organization__)
APPDATA_PLM                             = create_path(APPDATA_DAMG, __appName__)

CFG_DIR                                 = create_path(APPDATA_PLM, '.configs')
TMP_DIR                                 = create_path(APPDATA_PLM, '.tmp')
CACHE_DIR                               = create_path(APPDATA_PLM, '.cache')
PREF_DIR                                = create_path(APPDATA_PLM, 'preferences')

SETTING_DIR                             = CFG_DIR
DB_DIR                                  = APPDATA_PLM
LOG_DIR                                 = CFG_DIR

APP_SETTING                             = create_path(SETTING_DIR, 'PLM.ini')
USER_SETTING                            = create_path(SETTING_DIR, 'user.ini')
FORMAT_SETTING                          = create_path(SETTING_DIR, 'format.ini')
UNIX_SETTING                            = create_path(SETTING_DIR, 'unix.ini')


cprint("{0} v{1}".format(__appName__, __version__), 'cyan')

glbSettings                         = GlobalSettings()
PIPE                                = subprocess.PIPE
qtBinding                           = glbSettings.qtBinding

try:
    os.getenv(__envKey__)
except KeyError:
    process = subprocess.Popen('SetX {0} {1}'.format(__envKey__, ROOT), stdout=PIPE, stderr=PIPE, shell=True).wait()
else:
    if os.getenv(__envKey__) != ROOT:
        subprocess.Popen('SetX {0} {1}'.format(__envKey__, ROOT), stdout=PIPE, stderr=PIPE, shell=True).wait()
finally:
    glbSettings.cfgable = True


if glbSettings.qtBinding == 'PyQt5':
    try:
        import PyQt5
    except ImportError:
        subprocess.Popen('python -m pip install {0}={1} --user'.format(glbSettings.qtBinding, glbSettings.qtVersion), shell=True).wait()
    finally:
        from PyQt5.QtCore import pyqtSlot as Slot, pyqtSignal as Signal, pyqtProperty as Property
elif glbSettings.qtBinding == 'PySide2':
    try:
        import PySide2
    except ImportError:
        subprocess.Popen('python -m pip install {0}={1} --user'.format(glbSettings.qtBinding, glbSettings.qtVersion), shell=True).wait()
    finally:
        from PySide2.QtCore import Slot, Signal, Property


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/16/2020 - 2:15 AM
# © 2017 - 2019 DAMGteam. All rights reserved