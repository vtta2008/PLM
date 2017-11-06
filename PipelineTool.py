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
import os, sys, logging, subprocess, json, shutil
from tk import appFuncs as func
from tk import autoUpdate as update

# We can configure the current level to make it disable certain logs when we don't want it.
logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ------------------------------------------------------
# DEFAULT VARIABLES
# ------------------------------------------------------
key = 'PIPELINE_TOOL'
toolName = 'Pipeline Tool'
scrInstall = os.getcwd()


# Check environment key to get the path to source code
func.checkEnvKey(key, scrInstall, toolName)

# Name of required packages which should be installed along with Anaconda
packages = ['pywinauto', 'winshell', 'pandas']

# Check if packages are not installed, install it
for pkg in packages:
    func.checkPackageInstall(pkg)

# Create temporary database, this data will be replaced in the future when I have an online server.
update.createTempData()

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