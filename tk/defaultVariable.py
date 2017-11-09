# coding=utf-8
"""
Script Name: defaultVariable.py
Author: Do Trinh/Jimmy - 3D artist, pipelineTD artist.

Description:
    This script is the place that all the variables will be referenced from here
"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import os, sys, winshell, platform, logging
from tk import message

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ------------------------------------------------------
# DEFAULT VARIABLES
# ------------------------------------------------------
# encode.py
STRINPUT = 'password'
HEXINPUT = '70617373776F7264'
ENCODE = ['hexadecimal', 'ascii', 'unicode']
OPERATION = dict( encode=[ 'hex', 'string' ], pathInfo=[ 'create', 'read', 'modify' ] )

# getData.py
MAIN_NAMES = dict( info='apps.pipeline',
                   prod='prod.content',
                   log='user.timelog',
                   login='user.info',
                   web='webs.pipeline',
                   maya='maya.pipeline',
                   mayaEnv = 'env.maya',
                   appdata=['appData', 'scrInfo'],
                   sysEnv = 'env.os',
                   key = 'PIPELINE_TOOL',
                   )

USER_CLASS = ['', 'Admin','Supervisor','Artist', 'tester']

# Create environment variable by custom key
def createKey(key, path, *args):
    """
    Create custom enviroment Key in sys.
    all of those keys are temporary,
    it will be none once pipeline tool shut down.
    """
    logger.info('install new environment variable')

    os.environ[key] = path

def checkEnvKey(key, path, *args):
    try:
        pth = os.getenv(key)
        if pth == None or pth == '':
            createKey(key, path)
    except KeyError:
        createKey(key, path)
    else:
        pass

def createInfo():
    key = 'PROGRAMDATA'
    path = os.getcwd()

    checkEnvKey(key, path)

    appDir = os.getenv('PROGRAMDATA')

    infoDir = os.path.join(appDir, 'PipelineTool/scrInfo')

    if not os.path.exists(infoDir):
        os.makedirs(infoDir)
    return infoDir

inforDir = createInfo()

USERNAME = platform.node()

MAIN_ID = dict( Main='Tools Manager',
                LogIn = 'Log in',
                About='About Pipeline Tool',
                Credit='From Author')

APPDATA = [inforDir, os.path.join(os.getcwd().split('ui')[0], MAIN_NAMES['appdata'][0]),]

MAIN_MESSAGE = dict( About=message.MAIN_ABOUT,
                     Credit=message.MAIN_CREDIT,
                     status='Pipeline Application', )

MAIN_TABID = ['', 'Profile', 'Tools', 'Developer']

MAIN_PLUGIN = dict(winshell='winshell')

MAIN_URL = dict( Help='https://dot.damgteam.com/', )

MAIN_PACKPAGE = dict( job=[ 'TD', 'Comp', 'Design', 'Office', 'UV', 'Sound' ],
                      TD=[ 'Maya', '3Ds max', 'Mudbox', 'Houdini FX', 'ZBrush', 'Mari' ],
                      Comp=[ 'NukeX', 'Hiero', 'After Effects', 'Premiere Pro' ],
                      Design=[ 'Photoshop', 'Illustrator', 'InDesign' ],
                      Office=[ 'Word', 'Excel', 'PowerPoint' ],
                      UV=[ 'UVLayout' ],
                      Sound=[ 'Audition' ],
                      instruction=[ 'documentation' ],
                      website=[ 'doc' ],
                      image=[ 'icons', 'imgs' ],
                      py=[ 'tk', 'ui',],
                      ext=[ '.exe', 'PipelineTool.py', '.lnk' ],
                      sysOpts=[ "Host Name", "OS Name", "OS Version", "Product ID", "System Manufacturer",
                                "System Model",
                                "System type", "BIOS Version", "Domain", "Windows Directory", "Total Physical Memory",
                                "Available Physical Memory", "Logon Server" ],
                      temp=os.path.join(os.getcwd(), 'temp'),
                      info=os.path.join(os.getcwd().split( 'ui' )[ 0 ], 'appData'),
                      desktop=winshell.desktop(),
                      current=os.getcwd(),
                      root=os.getcwd().split( 'ui' )[ 0 ],
                      appData=APPDATA[0],
                      filter=[ 'Non-commercial', 'Uninstall', 'Verbose', 'License', 'Skype' ],
                      adobe=[ 'CS5', 'CS6', 'CC' ],
                      geo=[ 300, 300, 300, 400, 350], )

MAIN_ROOT = dict(main=MAIN_PACKPAGE['root'])