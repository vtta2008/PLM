# -*- coding: utf-8 -*-
"""

Script Name: plt_preset.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    collection of preset before run main app

"""

__appname__ = "Pipeline Tool"
__module__ = "presets"
__version__ = "13.0.1"
__organization__ = "DAMG team"
__website__ = "www.dot.damgteam.com"
__email__ = "dot@damgteam.com"
__author__ = "Trinh Do, a.k.a: Jimmy"

# -------------------------------------------------------------------------------------------------------------
""" Import modules """
# -------------------------------------------------------------------------------------------------------------
# Python modules
import os
import shutil
import pip
import subprocess
import time
import yaml
import logging

# Pipeline Tool modules
from utilities import utils as func
from utilities import utils_sql as usql

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain logs """
# -------------------------------------------------------------------------------------------------------------
logPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'logs', 'plt_preset.log')
logger = logging.getLogger('plt_preset')
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)

# Path value.
SCR_PATH = os.getcwd()

def preset1_plt_root_path():
    """
    Create and locate root path by a environment key.
    :return: environment variable.
    """
    global SCR_PATH
    # Key name.
    KEY = 'PIPELINE_TOOL'
    TOOL_NAME = 'PipelineTool'
    # Path value.
    SCR_PATH = os.getcwd()
    # Set key, path into environment variable.
    os.environ[KEY] = SCR_PATH
    return KEY, TOOL_NAME

def preset2_plt_database_path():
    """
    Define database path and check.
    :return: database path.
    """
    appDataPath = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData')
    DATA_PATH = os.path.join(appDataPath, 'database.db')

    # Backup database.
    DATA_BACKUP = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'backup', 'database.db')
    MAIN_CONFIG_PATH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'config', 'main_config.yml')

    # If database file is missing, copy the backup one.
    if not os.path.exists(DATA_PATH):
        shutil.copy2(DATA_BACKUP, DATA_PATH)
    return MAIN_CONFIG_PATH

def preset3_install_extra_python_package():
    """
    There are multiple pyton packages needs to be installed
    :return: Extra python packages installed
    """
    # Packages checklist.
    packages = ['pywinauto', 'winshell', 'pandas', 'opencv-python', 'pyunpack']

    # Query current packages
    checkList = []

    pyPkgs = {}

    pyPkgs['__mynote__'] = 'import pip; pip.get_installed_distributions()'
    for package in pip.get_installed_distributions():
        name = package.project_name
        if name in packages:
            checkList.append(name)

    resault = [p for p in packages if p not in checkList]

    # Run a quick check, install if need.
    if len(resault) > 0:
        for package in resault:
            subprocess.Popen("pip install %s" % package)
            time.sleep(5)

    return True

def preset4_maya_intergrate():
    # Pipeline tool module paths for Maya.
    maya_tk = os.path.join(SCR_PATH, 'plt_maya')

    # Name of folders
    mayaTrack = ['util', 'plt_maya', 'icons', 'modules', 'plugins', 'Animation', 'MayaLib', 'Modeling', 'Rigging',
                 'Sufacing']
    pythonValue = ""
    pythonList = []
    for root, dirs, files in os.walk(maya_tk):
        for dir in dirs:
            if dir in mayaTrack:
                dirPth = os.path.join(root, dir)
                pythonList.append(dirPth)
    pythonList = list(set(pythonList))
    for pth in pythonList:
        pythonValue += pth + ';'
    os.environ['PYTHONPATH'] = pythonValue

    # Copy userSetup.py from source code to properly maya folder
    userSetup_plt_path = os.path.join(os.getcwd(), 'plt_maya', 'userSetup.py')
    userSetup_maya_path = os.path.join(os.path.expanduser('~/Documents/maya/2017/prefs/scripts'), 'userSetup.py')

    if not os.path.exists(userSetup_plt_path):
        pass
    elif not os.path.exists(userSetup_plt_path):
        pass
    else:
        shutil.copy2(userSetup_plt_path, userSetup_maya_path)

def preset5_gather_configure_info():
    """
    Get config info
    :return:
    """
    # Configure root path
    MAIN_CONFIG_PATH = preset2_plt_database_path()

    # Seeking config file
    func.Generate_info()

    # Get info from file
    with open(MAIN_CONFIG_PATH, 'r') as f:
        APPINFO = yaml.load(f)

    return APPINFO

def preset6_query_user_info():
    """
    Query user info
    :return: user info
    """
    currentUserData = usql.query_current_user()
    curUser = currentUserData[2]
    unix = currentUserData[0]
    token = currentUserData[1]
    rememberLogin = currentUserData[3]
    status = currentUserData[-1]
    usql.check_sys_configuration(curUser)
    return unix, token, curUser, rememberLogin, status