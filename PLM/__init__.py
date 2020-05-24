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
import os, sys, traceback, subprocess
from termcolor                      import cprint

# PLM
from .version                       import Version
from .GLobalSetting                 import GlobalSetting
from .decoration                    import DamgProp

# -------------------------------------------------------------------------------------------------------------
""" Metadatas """

__envKey__                          = "PLM"
__appName__                         = "Pipeline Manager (PLM)"
__version__                         = Version()

__apiName__                         = "DAMG API"
__apiVersion__                      = Version(0, 0, 1)

# -------------------------------------------------------------------------------------------------------------
""" utilities function """

def __copyright__():
    return 'Copyright (C) DAMGTEAM. All right reserved.'

def exception_handler(exc_type, exc_value, exc_traceback):
    if hasattr(sys, 'ps1') or not sys.stderr.isatty():
        return sys.__excepthook__(exc_type, exc_value, exc_traceback)
    else:
        return traceback.format_exception(exc_type, exc_value, exc_traceback)

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

def parent_directory(path):
    path                            = os.path.abspath(os.path.join(path, os.pardir)).replace('\\', '/')
    path_exists(path)
    return path

def directory_name(path):
    return os.path.basename(path)

# -------------------------------------------------------------------------------------------------------------
""" setting up hook and output """

# Exception hook
sys.excepthook                      = exception_handler
PIPE                                = subprocess.PIPE

# get current directory path
cwd                                 = current_directory()

if directory_name(cwd) == directory_name(parent_directory(cwd)) == __envKey__:
    ROOT_APP                        = parent_directory(cwd)
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
            ROOT_APP                = parent_directory(ROOT)

cprint("{0} v{1}".format(__appName__, __version__), 'cyan')

glbSetting                          = GlobalSetting()

try:
    os.getenv(__envKey__)
except KeyError:
    process = subprocess.Popen('SetX {0} {1}'.format(__envKey__, ROOT), stdout=PIPE, stderr=PIPE, shell=True).wait()
else:
    if os.getenv(__envKey__)   != ROOT:
        subprocess.Popen('SetX {0} {1}'.format(__envKey__, ROOT), stdout=PIPE, stderr=PIPE, shell=True).wait()
finally:
    glbSetting.cfgable = True


if glbSetting.qtBinding == 'PyQt5':
    try:
        import PyQt5
    except ImportError:
        subprocess.Popen('python -m pip install {0}={1} --user'.format(GLobalSetting.qtBinding, GLobalSetting.qtVersion), shell=True).wait()
    finally:
        from PyQt5.QtCore import pyqtSlot as Slot, pyqtSignal as Signal, pyqtProperty as Property
elif glbSetting.qtBinding == 'PySide2':
    try:
        import PySide2
    except ImportError:
        subprocess.Popen('python -m pip install {0}={1} --user'.format(GLobalSetting.qtBinding, GLobalSetting.qtVersion), shell=True).wait()
    finally:
        from PySide2.QtCore import Slot, Signal, Property


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/16/2020 - 2:15 AM
# © 2017 - 2019 DAMGteam. All rights reserved