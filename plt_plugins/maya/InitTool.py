# coding=utf-8

"""
Script Name: InitTool.py
Author: Do Trinh/Jimmy - TD artist

Description:
    It basically checkes all the files in folder to makes ure everthing is there. Then copy some files to folders
    as required like userSetup.py or saving the path of DAMG tool folder to sys.path for next use.
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

from plt_plugins.maya.modules import MayaVariables as var

NAMES = var.MAINVAR

# ----------------------------------------------------------------------------------------------------------- #
"""                          MAIN CLASS: INITTOOL - DAMG PIPELINE DATA INSTALLATION                         """
# ----------------------------------------------------------------------------------------------------------- #
class InitTool(object):

    def __init__(self):
        super(InitTool, self).__init__()

        self.MayaPythonProc()

    def MayaPythonProc(self):
        from plt_plugins.maya.modules import MayaPythonProc
        reload(MayaPythonProc)
        MayaPythonProc.MayaPythonProc()
        self.MayaMainUI()

    def OsPythonProc(self):
        from plt_plugins.maya.modules import OsPythonProc
        reload(OsPythonProc)
        OsPythonProc.OsPythonProc()
        self.MayaMainUI()

    def MayaMainUI(self):
        from plt_plugins.maya.modules import MayaMainUI
        reload(MayaMainUI)
        MayaMainUI.MayaMainUI()

def main():
    InitTool()

if __name__=='__main__':
    main()