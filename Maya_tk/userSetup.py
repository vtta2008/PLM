"""
Script Name: userSetup.py
Author: Do Trinh/Jimmy - TD artist
"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds
import maya.utils as mu
import os, sys, json, logging
from Maya_tk.modules import MayaVariables as var

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
# We can configure the current level to make it disable certain logs when we don't want it.
NAMES = var.MAINVAR
SCRPTH = os.path.join(os.getenv('PROGRAMDATA'), 'Pipeline Tool/scrInfo')
MESSAGE = var.MESSAGE
ID = 'UserSetup'
KEY = 'PYTHONPATH'

logging.basicConfig()
logger = logging.getLogger(NAMES['id'][6])
logger.setLevel(logging.DEBUG)

# ----------------------------------------------------------------------------------------------------------- #
"""                                      USER SETUP - UPDATE ALL PATHS                                      """
# ----------------------------------------------------------------------------------------------------------- #

class InitUserSetup(object):

    def __init__(self):
        super(InitUserSetup, self).__init__()

        hello = 'Hello %s, just wait for a quick setup' % NAMES['user']

        cmds.confirmDialog(t='Welcome', m=hello, b='OK')

        var.createLog('maya')

        SCR = os.path.join( SCRPTH, NAMES['os'][0] )

        PTH = os.path.join( SCRPTH, NAMES['maya'][1] )

        if os.path.exists( SCR ):
            logger.info( 'Start updateing sys path' )
            self.updatePathFromUser(SCR)
            self.updatePathFromUser(PTH)
        else:
            if not os.path.exists(PTH):
                self.loadPathAndUI()
            else:
                self.updatePathFromUser(PTH)
            self.adviceToInstallAnanconda()

        from Maya_tk import InitTool
        reload(InitTool)
        InitTool.initilize()

    def loadPathAndUI(self):
        pass

    def adviceToInstallAnanconda(self):
        title = 'No Ananconda installed'
        message = MESSAGE[ 'NoPythonInstall' ]
        logger.info( message )
        cmds.warning( message )
        cmds.confirmDialog( t=title, m=message, b='OK' )

    def updatePathFromUser(self, scr):

        with open(scr, 'r') as f:
            env = json.load(f)

        for k in env:
            lnks = str(env[k]).split(';')
            for lnk in lnks:
                if os.path.exists(lnk):
                    if not lnk in sys.path:
                        sys.path.append(lnk)
                        logger.info('Updated system path: %s' % lnk)

mu.executeDeferred(InitUserSetup())

# ----------------------------------------------------------------------------------------------------------- #
"""                                                 END OF CODE                                             """
# ----------------------------------------------------------------------------------------------------------- #