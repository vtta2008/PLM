# coding=utf-8

"""
Script Name: InitTool.py
Author: Do Trinh/Jimmy - TD artist

Description:
    It basically checkes all the files in folder to makes ure everthing is there. Then copy some files to folders
    as required like userSetup.py or saving the path of DAMG tool folder to sys.path for next use.
"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import logging
import os

from plt_maya.modules import MayaVariables as var

NAMES = var.MAINVAR
SCRPTH = os.path.join(os.getenv('PROGRAMDATA'), 'Pipeline Tool/scrInfo')

# We can configure the current level to make it disable certain logs when we don't want it.
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# ----------------------------------------------------------------------------------------------------------- #
"""                          MAIN CLASS: INITTOOL - DAMG PIPELINE DATA INSTALLATION                         """
# ----------------------------------------------------------------------------------------------------------- #
class InitTool(object):

    def __init__(self):
        super(InitTool, self).__init__()

        self.MayaPythonProc()

    def MayaPythonProc(self):
        from modules import MayaPythonProc
        reload(MayaPythonProc)
        MayaPythonProc.MayaPythonProc()
        # self.OsPythonProc()
        self.MayaMainUI()

    def OsPythonProc(self):
        from modules import OsPythonProc
        reload(OsPythonProc)
        OsPythonProc.OsPythonProc()
        self.MayaMainUI()

    def MayaMainUI(self):
        from modules import MayaMainUI
        reload(MayaMainUI)
        MayaMainUI.MayaMainUI()

def initilize():
    InitTool()

if __name__=='__main__':
    initilize()