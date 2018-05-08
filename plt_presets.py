# -*- coding: utf-8 -*-
"""

Script Name: plt_preset.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    collection of preset before run main app

"""

# -------------------------------------------------------------------------------------------------------------
""" About Plt """

__appname__ = "Pipeline Tool"
__module__ = "Plt"
__version__ = "13.0.1"
__organization__ = "DAMG team"
__website__ = "www.dot.damgteam.com"
__email__ = "dot@damgteam.com"
__author__ = "Trinh Do, a.k.a: Jimmy"
__root__ = "PLT_RT"
__db__ = "PLT_DB"
__st__ = "PLT_ST"

# -------------------------------------------------------------------------------------------------------------
""" Import modules """

# Python
import os
import shutil
import yaml
import logging

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain logs """

logPth = os.path.join(os.getenv(__root__), 'appData', 'logs', 'plt_preset.log')
logger = logging.getLogger('plt_preset')
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)

# -------------------------------------------------------------------------------------------------------------
""" Plt tools """

from utilities import utils as func
from utilities import sql_local as usql

# -------------------------------------------------------------------------------------------------------------
""" Preset """

def preset3_maya_intergrate():
    # Pipeline tool module paths for Maya.
    maya_tk = os.path.join(os.getenv(__root__), 'maya')

    # Name of folders
    mayaTrack = ['util', 'maya', 'plt.maya.icons', 'modules', 'plugins', 'Animation', 'MayaLib', 'Modeling', 'Rigging',
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
    userSetup_plt_path = os.path.join(os.getenv(__root__), 'plt_plugins', 'maya', 'userSetup.py')
    userSetup_maya_path = os.path.join(os.path.expanduser('~/Documents/maya/2017/prefs/scripts'), 'userSetup.py')

    if not os.path.exists(userSetup_plt_path) or not os.path.exists(userSetup_plt_path):
        pass
    else:
        shutil.copy2(userSetup_plt_path, userSetup_maya_path)

def preset4_gather_configure_info():
    """
    Get config info
    :return:
    """
    # Configure root path
    MAIN_CONFIG_PATH = os.path.join(os.getenv(__root__), 'appData', 'config', 'main.yml')

    # Seeking config file
    func.Collect_info()

    # Get info from file
    with open(MAIN_CONFIG_PATH, 'r') as f:
        APPINFO = yaml.load(f)

    return APPINFO