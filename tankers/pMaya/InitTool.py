# coding=utf-8

"""
Script Name: InitTool.py
Author: Do Trinh/Jimmy - TD artist

Description:
    It basically checkes all the files in folder to makes ure everthing is there. Then copy some files to folders
    as required like userSetup.py or saving the path of DAMG tool folder to sys.path for next use.
"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from tankers.pMaya.modules import MayaVariables as var

NAMES = var.MAINVAR

# ----------------------------------------------------------------------------------------------------------- #
"""                          MAIN CLASS: INITTOOL - DAMG PIPELINE DATA INSTALLATION                         """
# ----------------------------------------------------------------------------------------------------------- #
class InitTool(object):

    def __init__(self):
        super(InitTool, self).__init__()

        self.MayaPythonProc()

    def MayaPythonProc(self):
        from apps.maya.modules import MayaPythonProc
        reload(MayaPythonProc)
        MayaPythonProc.MayaPythonProc()
        self.MayaMainUI()

    def OsPythonProc(self):
        from appPackages.maya.modules import OsPythonProc
        reload(OsPythonProc)
        OsPythonProc.OsPythonProc()
        self.MayaMainUI()

    def MayaMainUI(self):
        from appPackages.maya.modules import MayaMainUI
        reload(MayaMainUI)
        MayaMainUI.MayaMainUI()

def main():
    InitTool()

if __name__=='__main__':
    main()