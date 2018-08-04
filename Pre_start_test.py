# -*- coding: utf-8 -*-
"""

Script Name: Pre_start_test.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
import os, sys, subprocess, pkg_resources

# Variables
key = "PIPELINE_MANAGER"
ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)))
requirements = ['deprecate', 'msgpack', 'winshell', 'pandas', 'wheel', 'argparse', 'green']

envKeys = [k for k in os.environ.keys()]
program86 = os.getenv('PROGRAMFILES(X86)')
program64 = os.getenv('PROGRAMW6432')
sysPths = os.getenv('PATH').split(';')

checkList = dict()
cfgPyVer = False
cfgPyPth = False
cfgReqs = False

if key in envKeys:
    if os.getenv(key) == ROOT:
        pass
    else:
        os.environ[key] = ROOT
else:
    os.environ[key] = ROOT

def handle_path_error(directory=None):
    if not os.path.exists(directory) or directory is None:
        try:
            raise IsADirectoryError("Path is not exists: {directory}".format(directory=directory))
        except IsADirectoryError as error:
            raise('Caught error: ' + repr(error))

def get_all_path_from_dir(directory):
    filePths = []                                                           # List which will store all file paths.
    dirPths = []                                                            # List which will store all folder paths.
    for root, directories, files in os.walk(directory, topdown=False):      # Walk the tree.
        for filename in files:
            filePths.append(os.path.join(root, filename))                   # Add to file list.
        for folder in directories:
            dirPths.append(os.path.join(root, folder))                      # Add to folder list.
    return [filePths, dirPths]

def get_folder_path(directory):
    handle_path_error(directory)
    return get_all_path_from_dir(directory)[1]

def check_python_package_require(package):
    try:
        import package
    except ImportError:
        print('{0} not installed'.format(package))
    else:
        print('package {0} installed'.format(package))
    finally:
        pass

pyVersion = float(sys.version[:3])
cfgPyVer = True

if 'Anaconda' in sys.version:
    print('Python anaconda found')
    pyRoot = os.getenv('PROGRAMDATA')
    if pyVersion >= 3:
        pyFolder = 'Anaconda3'
    else:
        pyFolder = 'Anaconda2'
else:
    pyOrgDefault = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'Python')
    if not os.path.exists(pyOrgDefault):
        folder86 = get_folder_path(program86)
        folder64 = get_folder_path(program64)
        paths = folder86 + folder64
        for pth in paths:
            if 'python' in pth:
                pyFolder = os.path.basename(pth)
                pyRoot = pth.split(pyFolder)[0]
                break
            else:
                continue
    else:
        pyRoot = pyOrgDefault
        pyFolder = get_folder_path(pyRoot)[0]

pyPth = os.path.join(pyRoot, pyFolder)

if pyPth in sysPths:
    cfgPyPth = True
else:
    os.environ['PATH'] = os.getenv('PATH') + pyPth
    cfgPyPth = True

install_packages = [(d.project_name, d.version) for d in pkg_resources.working_set]
packages = [p[0] for p in install_packages]
versions = [v[1] for v in install_packages]

if 'pip' in packages:
    pipVer = float(versions[packages.index('pip')][:4])
    if pipVer < 18.0:
        subprocess.Popen('python -m pip install --user --upgrade pip', shell=True).wait()
else:
    subprocess.Popen('python -m pip install --user --upgrade pip', shell=True).wait()

for pkg in requirements:
    if not pkg in packages:
        subprocess.Popen('python -m pip install --user --upgrade {0}'.format(pkg), shell=True).wait()

try:
    import cx_Freeze
except ImportError:
    subprocess.Popen('python -m pip install --user --upgrade cx_Freeze', shell=True).wait()
else:
    pass
finally:
    cfgReqs = True

checkList['python version'] = cfgPyVer
checkList['python path'] = cfgPyPth
checkList['python requirement'] = cfgReqs

check = True
for value in checkList.keys():
    if value is not True:
        continue
    else:
        check = False

if check:
    print('configurations is not completed!')
else:
    print('configuration completed!')
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/08/2018 - 12:57 AM
# © 2017 - 2018 DAMGteam. All rights reserved