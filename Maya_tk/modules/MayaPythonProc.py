# -*-coding:utf-8 -*

"""
Script Name: DAMGsetup.py
Author: Do Trinh/Jimmy - TD artist

Description:
    It basically checkes all the files in folder to makes ure everthing is there. Then copy some files to folders
    as required like userSetup.py or saving the path of DAMG tool folder to sys.path for next use.
"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds # Maya_tk Python command
import os, sys, json, shutil, getpass, platform, re, logging

from Maya_tk.modules import MayaVariables as var
# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
NAMES = var.MAINVAR
SCRPTH = os.path.join(os.getenv('PROGRAMDATA'), 'PipelineTool/scrInfo')

# -------------------------------------------------------------------------------------------------------------
# MAKE MAYA UNDERSTAND QT UI AS MAYA WINDOW,  FIX VERSION CONVENTION
# -------------------------------------------------------------------------------------------------------------
# We can configure the current level to make it disable certain logs when we don't want it.
logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
# CHECK THE CORRECT BINDING THAT BE USING UNDER QT.PY
# -------------------------------------------------------------------------------------------------------------
# While Qt.py lets us abstract the actual Qt library, there are a few things it cannot do yet
# and a few support libraries we need that we have to import manually.
# if Qt.__binding__=='PySide':
#     logger.debug('Using PySide with shiboken')
#     from shiboken import wrapInstance
#     from Maya_tk.plugins.Qt.QtCore import Signal
# elif Qt.__binding__.startswith('PyQt'):
#     logger.debug('Using PyQt with sip')
#     from sip import wrapinstance as wrapInstance
#     from Maya_tk.plugins.Qt.QtCore import pyqtSignal as Signal
# else:
#     logger.debug('Using PySide2 with shiboken2')
#     from shiboken2 import wrapInstance
#     from Maya_tk.plugins.Qt.QtCore import Signal
# ----------------------------------------------------------------------------------------------------------- #
"""                   AIN CLASS: MAYA EXECUTE PYTHON - DAMG PIPELINE TOOL INSTALLATION                      """
# ----------------------------------------------------------------------------------------------------------- #
class MayaPythonProc( object ):

    #file list in Installation folder
    icons_lst = [f for f in os.listdir(os.path.join(os.getcwd(), 'Maya_tk/icons')) if f.endswith('.png') or f.endswith('.jpg')]
    modules_lst = [f for f in os.listdir(os.path.join(os.getcwd(), 'Maya_tk/modules')) if f.endswith('.py')]
    scrRoot_lst = [f for f in os.listdir(os.path.join(os.getcwd(), 'Maya_tk')) if f.endswith( '.py' )]
    #---------------------------------------------------------
    # List file names for CHECK LIST
    checkList = dict(icons=NAMES['mayaIcon'], modules=NAMES['mayaModule'], master=NAMES['mayaRoot'])
    fileList = dict(icons=icons_lst, modules=modules_lst, master=scrRoot_lst)
    # ---------------------------------------------------------
    # Make variables just in case you miss something.
    message_missing = []

    def __init__(self):
        super( MayaPythonProc, self ).__init__()

        self.checkAllFiles()

    def checkAllFiles(self):
        for part in self.checkList:
            logger.info('start inspecting %s folder' % part)
            for file in self.checkList[part]:
                if file in self.fileList[part]:
                    logger.info("%s exists, keep seeking..." % file)
                else:
                    logger.info("could not find: %s in: %s" % (file, (os.path.join(NAMES['mayaRootDir'], part))))
                    self.message_missing.append("%s in %s" % (file, (os.path.join(NAMES['mayaRootDir'], part))))

        if self.message_missing==[]:
            logger.info("Finish checking, all files are there")
        else:
            self.showMissing()

        self.setupFolderAndPath()

    def setupFolderAndPath(self, **info):
        infoUser = {}
        userPath = os.path.join(SCRPTH, NAMES['maya'][0])

        infoUser['source folder'] = NAMES['mayaRootDir']
        infoUser['user name'] = getpass.getuser()
        infoUser['artist name'] = platform.node()
        infoUser['operating system'] = platform.system() + "/" + platform.platform()
        infoUser['python version'] = platform.python_version()

        with open(userPath, 'w') as f:
            json.dump(infoUser, f, indent=4)

        logger.info('Saving file to %s' % userPath)

        infoPath = {}
        toolPath = os.path.join( SCRPTH, '%s' % NAMES[ 'maya' ][1] )
        for part in ['icons', 'modules', 'packages']:
            infoPath[part] = os.path.join(NAMES['mayaRootDir'], part)

        with open(toolPath, 'w') as f:
            json.dump(infoPath, f, indent=4)

        logger.info('Saving file to %s' % toolPath)

        self.applyToolPathIntoSystem()

    def applyToolPathIntoSystem(self, *args):
        srcInfo = os.path.join(SCRPTH, NAMES['maya'][1])
        if os.path.exists(srcInfo):
            with open(srcInfo, 'r') as f:
                paths = json.load(f)
            for path in paths:
                if os.path.exists( paths[ path ] ):
                    if not paths[ path ] in sys.path:
                        sys.path.append( paths[ path ] )
                    else:
                        pass
                else:
                    continue
        else:
            message = ('Could not find %s in %s,\n'  % (NAMES['maya'][1], srcInfo))
            self.warningMessage(message=message)

    def updateLayout(self):
        folName = ['workspaces', 'shelves',]
        for i in range(0, 2):
            scr = os.path.join(NAMES['mayaRootDir'], 'layout') + '/' + NAMES['mayaLayout'][i]
            if not os.path.exists(scr):
                message = "missing %s, it should be in: %s, ignore." % (NAMES['mayaLayout'][i], scr)
                logger.info(message)
                cmds.warning(message)
            else:
                des = os.path.join(NAMES['mayaRootDir'], folName[i]) + '/' + NAMES['mayaLayout'][i]
                if os.path.exists(des):
                    logger.info('Already updated %s layout, ignore.' % folName[i])
                else:
                    logger.info('updating %s...' % folName[i])
                    shutil.copy2(scr, des)
                i+=1

    def showMissing(self, *args):
        message = " "
        for m in self.message_missing:
            message = 'missing file: ' + message + m + ";"
        self.warningMessage( message=message )
        logger.info(message)
        sys.exit()

    def warningMessage(self, message="None"):
        cmds.confirmDialog(
            t = 'Warning',
            m = ( message + "\n"
                "please re-install the tool, or contact Jimmy for help" + "\n"
                ),
            b = 'OK'
        )
        logger.info(message)
        cmds.warning(message)

if __name__=='main':
    MayaPythonProc()