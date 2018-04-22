# coding=utf-8
"""
Script Name: variables.py
Author: Do Trinh/Jimmy - 3D artist, pipelineTD artist.

Description:
    This script is the place that all the variables will be referenced from here
"""
# -------------------------------------------------------------------------------------------------------------
""" Import modules """
# -------------------------------------------------------------------------------------------------------------
import logging
import os
import platform
import winshell
import message

# PyQt5 modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ------------------------------------------------------
# DEFAULT VARIABLES
# ------------------------------------------------------

# ui elements
__center__ = Qt.AlignCenter
__right__ = Qt.AlignRight
__left__ = Qt.AlignLeft
frameStyle = QFrame.Sunken | QFrame.Panel

# main.py
__appname__ = "Pipeline Tool"
__module__ = "main"
__version__ = "13.0.1"
__organization__ = "DAMG team"
__website__ = "www.damgteam.com"
__email__ = "dot@damgteam.com"
__author__ = "Trinh Do, a.k.a: Jimmy"

TITLEBLANK = 'Blank title will be considered as "Tester"'

# encode.py
STRINPUT = 'password'
HEXINPUT = '70617373776F7264'
ENCODE = ['hexadecimal', 'ascii', 'unicode']
OPERATION = dict(encode=['hex', 'string'], pathInfo=['create', 'read', 'modify'])

# getData.py
MAIN_NAMES = dict(info='apps.config',
                  prod='prod.content',
                  log='user.timelog',
                  login='user.info',
                  web='webs.pipeline',
                  maya='maya.pipeline',
                  mayaEnv='env.maya',
                  appdata=['appData', 'scrInfo'],
                  sysEnv='env.os',
                  key='PIPELINE_TOOL',
                  )

USER_CLASS = ['', 'Admin', 'Supervisor', 'Artist', 'Tester']

ERROR_LOG = dict(

    first_name = "Firstname cannot be blank",
    last_name = "Lastname cannot be blank"

)

def createInfo():
    appDir = os.getcwd()
    infoDir = os.path.join(appDir, 'appData/db')
    return infoDir

inforDir = createInfo()

USERNAME = platform.node()

MAIN_ID = dict(Main='Tools Manager',
               LogIn='Log in',
               About='About Pipeline Tool',
               Credit='From Author')

APPDATA = [inforDir, os.path.join(os.getcwd().split('ui')[0], MAIN_NAMES['appdata'][0]), ]

MAIN_MESSAGE = dict(About=message.MAIN_ABOUT,
                    Credit=message.MAIN_CREDIT,
                    status='Pipeline Application', )

MAIN_TABID = ['', 'User', 'Functions', 'Project', 'Admin', ]

MAIN_PLUGIN = dict(winshell='winshell')

MAIN_URL = dict(Help='https://www.dot.damgteam.com/', )

MAIN_PACKPAGE = dict(job=['TD', 'Comp', 'Design', 'Office', 'UV', 'Sound'],
                     TD=['Maya', '3ds Max', 'Mudbox', 'Houdini FX', 'ZBrush', 'Mari', 'Substance Painter',],
                     Comp=['NukeX', 'Hiero', 'After Effects', 'Premiere Pro'],
                     Design=['Photoshop', 'Illustrator'],
                     Office=['Word', 'Excel'],
                     UV=['UVLayout'],
                     Sound=['Audition'],
                     instruction=['documentation'],
                     website=['doc'],
                     image=['icons', 'imgs'],
                     py=['utilities', 'ui', ],
                     ext=['.exe', 'PipelineTool.py', '.lnk'],
                     sysOpts=["Host Name", "Product ID", "System Manufacturer",
                              "System Model",
                              "System type", "BIOS Version", "Domain", "Windows Directory", "Total Physical Memory",
                              "Available Physical Memory", "Logon Server"],
                     temp=os.path.join(os.getcwd(), 'temp'),
                     info=os.path.join(os.getcwd().split('ui')[0], 'appData'),
                     desktop=winshell.desktop(),
                     current=os.getcwd(),
                     root=os.getcwd().split('ui')[0],
                     appData=APPDATA[0],
                     filter=['Non-commercial', 'Uninstall', 'Verbose', 'License', 'Skype'],
                     adobe=['CS5', 'CS6', 'CC'],
                     geo=[300, 300, 300, 400, 350], )

MAIN_ROOT = dict(main=MAIN_PACKPAGE['root'])