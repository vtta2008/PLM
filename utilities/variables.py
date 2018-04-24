# coding=utf-8
"""

Script Name: variables.py
Author: Do Trinh/Jimmy - 3D artist, pipelineTD artist.

Description:
    This place is a storage of variables

"""

__appname__ = "Pipeline Tool"
__module__ = "variables"
__version__ = "13.0.1"
__organization__ = "DAMG team"
__website__ = "www.dot.damgteam.com"
__email__ = "dot@damgteam.com"
__author__ = "Trinh Do, a.k.a: Jimmy"

# -------------------------------------------------------------------------------------------------------------
""" Import modules """
# -------------------------------------------------------------------------------------------------------------
# Python
import logging
import os
import platform
import winshell

# Plt tools
from utilities import message as mess

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain logs """
# -------------------------------------------------------------------------------------------------------------
logPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'logs', 'variables.log')
logger = logging.getLogger('variables')
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# ------------------------------------------------------
# DEFAULT VARIABLES
# ------------------------------------------------------
# main.py
appname = "Pipeline Tool"
module = "main"
version = "13.0.1"
organization = "DAMG team"
website = "www.dot.damgteam.com"
email = "dot@damgteam.com"
author = "Trinh Do, a.k.a: Jimmy"

# encode.py
STRINPUT = 'password'
HEXINPUT = '70617373776F7264'
ENCODE = ['hexadecimal', 'ascii', 'unicode']
OPERATION = dict(encode=['hex', 'string'], pathInfo=['create', 'read', 'modify'])

# getData.py
USER_CLASS = ['', 'Admin', 'Supervisor', 'Artist', 'Tester']

USERNAME = platform.node()

PLT_ID = dict(

    Main=__appname__,
    LogIn='Log in',
    About='About Pipeline Tool',
    Credit='From Author'

)

PLT_TABID = ['', 'User', 'Functions', 'Project', 'Admin', ]

PLT_URL = dict(

    Home = 'https://www.dot.damgteam.com/',
    Help = 'https://www.dot.damgteam.com/',

)

PLT_MESS = dict(About=mess.PLT_ABOUT,
                    Credit=mess.PLT_CREDIT,
                    status='Pipeline Application', )

PLT_PATH = dict(

    info = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData'),
    temp = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'temp'),
    desktop = winshell.desktop(),
    db = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'database.db')

)

PLT_PACKAGE = dict(

    job=['TD', 'Comp', 'Design', 'Office', 'UV', 'Sound'],
    TD=['Maya', '3ds Max', 'Mudbox', 'Houdini FX', 'ZBrush', 'Mari', 'Substance Painter',],
    Comp=['NukeX', 'Hiero', 'After Effects', 'Premiere Pro'],
    Design=['Photoshop', 'Illustrator'],
    Office=['Word', 'Excel'],
    UV=['UVLayout'],
    Sound=['Audition'],
    sysOpts=["Host Name", "Product ID", "System Manufacturer", "System Model", "System type", "BIOS Version", "Domain",
             "Windows Directory", "Total Physical Memory", "Available Physical Memory", "Logon Server"],
    filter=['Non-commercial', 'Uninstall', 'Verbose', 'License', 'Skype'],
    root = os.getenv('PIPELINE_TOOL'),
    py = ['utilities','ui'],
    image=['icons', 'imgs'],
    ext=['.exe', 'PipelineTool.py', '.lnk'],

)

# Setting Path
LAYOUT_SETTING_PTH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'settings', 'Plt.ini')

USER_SETTING_PTH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'settings', 'User.ini')

DB_PATH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'database.db')