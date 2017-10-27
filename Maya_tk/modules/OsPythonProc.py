# -*-coding:utf-8 -*

"""
Script Name: OsPythonProc.py
Author: Do Trinh/Jimmy - TD artist

Description:
    This is the procedure will run before start building UI, another inspection
    to make sure everything is updated.

"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds, mel
import os, sys, json, shutil, logging, webbrowser

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
from Maya_tk.modules import MayaVariables as var
NAMES = var.MAINVAR
MESSAGE = var.MESSAGE
SCRPTH = os.path.join(os.getenv('PROGRAMDATA'), 'Pipeline Tool/scrInfo')

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
"""                                   MAIN CLASS: INSPECT DATA                                              """
# ----------------------------------------------------------------------------------------------------------- #

class OsPythonProc( object ):

    def __init__(self):

        super(OsPythonProc, self).__init__()

        self.getExternalPython()

        logger.info("thank you for using DAMG team product.")

    def getExternalPython(self):
        mayaPth = os.path.join(SCRPTH, NAMES['maya'][ 1 ] )
        with open( mayaPth, 'r' ) as f:
            self.toolPth = json.load( f )

        if not os.path.exists(NAMES['mayaEnvPth']):
            self.writeToMayaEnv(self.toolPth)

        osPth = os.path.join( SCRPTH, 'evn.os' )
        if not os.path.exists(osPth):
            try:
                import winshell
            except ImportError:
                ws = os.system('pip install winshell')
                if ws == 0:
                    logger.info( 'you have installed winshell')
                else:
                    self.noPythonInstall()
                    pass
            else:
                logger.info('Successfully Intergrade Python!!!')
        else:
            with open(osPth, 'r') as f:
                self.osTool = json.dump(f)
            self.writeToMayaEnv(self.osTool)

    def writeToMayaEnv(self, dictionary):
        with open( NAMES['mayaEnvPth'], 'a+' ) as f:
            for key in dictionary:
                f.write( key.upper() + ' = ' + dictionary[key] + '\n')

    def noPythonInstall(self):
        title = 'No Python external installed'
        message = MESSAGE['NoPythonInstall']
        logger.info( message )
        cmds.warning( message )
        cmds.confirmDialog(t= title,m = message, b='OK' )
        webbrowser.open(NAMES['url'][0])

if __name__=='__main__':
    OsPythonProc()