# -*- coding: utf-8 -*-
"""

Script Name: appFuncs.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script will start some installation then call the main UI of the apps.

"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import logging
import os
import pip
import shutil
import subprocess
import yaml

# We can configure the current level to make it disable certain logs when we don't want it.
logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ------------------------------------------------------
# DEFAULT VARIABLES
# ------------------------------------------------------
key = 'PIPELINE_TOOL'
toolName = 'PipelineTool'
scr = os.getcwd()
# Check environment key to get the path to source code
os.environ[key] = scr
# Name of required packages which should be installed along with Anaconda
packages = ['pywinauto', 'winshell', 'pandas', 'opencv-python', 'pyunpack']

checkList = []

pyPkgs = {}

pyPkgs['__mynote__'] = 'import pip; pip.get_installed_distributions()'

for package in pip.get_installed_distributions():
    name = package.project_name
    if name in packages:
        checkList.append(name)

resault = [p for p in packages if p not in checkList]

if len(resault) > 0:
    for package in resault:
        subprocess.Popen("pip install %s" % packages)

from tk import appFuncs as func

tempDataPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/db/local.config.yml')

if not os.path.exists(tempDataPth):
    token = func.create_new_unique_id()
    with open (tempDataPth, 'w') as f:
        yaml.dump(token, f, default_flow_style=False)

maya_tk = os.path.join(scr, 'Maya_tk')
pythonValue = ""
pythonList = []

mayaBlock = ['tk', 'Maya_tk', 'icons', 'modules', 'plugins', 'Animation', 'MayaLib', 'Modeling', 'Rigging', 'Sufacing']

for root, dirs, files in os.walk(maya_tk):
    for dir in dirs:
        if dir in mayaBlock:
            dirPth = os.path.join(root, dir)
            pythonList.append(dirPth)

pythonList = list(set(pythonList))

for pth in pythonList:
    pythonValue += pth + ';'

os.environ['PYTHONPATH'] = pythonValue

# Copy userSetup.py from source code to properly maya folder
userSetupScr = os.path.join(os.getcwd(), 'Maya_tk/userSetup.py')
userSetupDes = os.path.join(os.path.expanduser('~/Documents/maya/2017/prefs/scripts'), 'userSetup.py')

shutil.copy2(userSetupScr, userSetupDes)

# Load UI of pipeline application for window OS
from ui import DesktopUI
reload(DesktopUI)
DesktopUI.initialize()

# ----------------------------------------------------------------------------------------------------------- #
"""                                                END OF CODE                                              """
# ----------------------------------------------------------------------------------------------------------- #
