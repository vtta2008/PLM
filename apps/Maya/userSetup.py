"""
Script Name: userSetup.py
Author: Do Trinh/Jimmy - TD artist
"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import maya.cmds as cmds
import json
import sys
import os

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
VERSION = int(cmds.about(v=True))

# *********************************************************************************************************** #
# ----------------------------------------------------------------------------------------------------------- #
"""                        MAIN CLASS: DAMG USER SETUP - UPDATE ALL PATHS                                   """
# ----------------------------------------------------------------------------------------------------------- #
# *********************************************************************************************************** #
class DAMGuserSetup(object):

    scrData = cmds.internalVar( upd=True ) + 'scripts/infoPath.json'

    paths = {}

    def __init__(self):
        if os.path.exists(self.scrData):
            with open( self.scrData, 'r' ) as f:
                self.paths = json.load( f )

            self.findModulePath()

        self.openCommandPort()

    def findModulePath(self):
        for path in self.paths:
            if os.path.exists( self.paths[path] ):
                if not self.paths[path ] in sys.path:
                    sys.path.append( self.paths[path ] )
                else:
                    pass
            else:
                continue

    def openCommandPort(self, port=':4344'):
        if not cmds.commandPort(port, q=True):
            cmds.commandPort(n=port)

user = DAMGuserSetup()