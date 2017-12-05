# coding=utf-8
"""

Script Name: ToolBoxIV.py
Author: Do Trinh/Jimmy - TD artist

Description:
    It is simply load UI for you in order to open other software inside Maya

"""

from maya import cmds
import os, sys, logging, subprocess, json, shutil
from functools import partial
from plt_maya.modules import MayaVariables as var

from plt_maya.plugins import Qt

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
NAMES = var.MAINVAR
MESSAGE = var.MESSAGE
SCRPTH = os.path.join(os.getenv('PROGRAMDATA'), 'PipelineTool/scrInfo')

WINID = 'AppsManager'
SUBID = 'Chosing version'
TITLE = 'Apps Manager'

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
if Qt.__binding__ == 'PySide':
    logger.debug('Using PySide with shiboken')
    from shiboken import wrapInstance
    from plt_maya.plugins.Qt.QtCore import Signal
elif Qt.__binding__.startswith('PyQt'):
    logger.debug('Using PyQt with sip')
    from sip import wrapinstance as wrapInstance
else:
    logger.debug('Using PySide2 with shiboken2')
    from shiboken2 import wrapInstance
    from plt_maya.plugins.Qt.QtCore import Signal


def geticon(icon):
    iconPth = os.path.join(os.getcwd(), 'icons')
    return os.path.join(iconPth, icon)


# ----------------------------------------------------------------------------------------------------------- #
"""                        MAIN CLASS: APPSMANAGER - GET ALL APPS INSTALLED IN MAYA                         """


# ----------------------------------------------------------------------------------------------------------- #

class toolBoxIV(object):
    def __init__(self):
        super(toolBoxIV, self).__init__()

        self.getAppData()

    def getAppData(self):

        self.scrApps = os.path.join(SCRPTH, 'apps.config')
        if not os.path.exists(self.scrApps):
            self.warningMessage(MESSAGE['canNotFindIt'])
        else:
            self.buildUI()

    def warningMessage(self, message):
        cmds.confirmDialog(t='Warning', m=message, b='OK')
        logger.info(message)
        sys.exit()

    def buildUI(self):
        apps = ['ZBrush 4R8', 'Mudbox 2017', 'Mari', 'Houdini FX', 'NukeX', 'Hiero',
                'Photoshop CC', 'Illustrator CC', 'Premiere Pro CC', 'After Effects CC']

        with open(self.scrApps, 'r') as f:
            info = json.load(f)

        appInfo = info['pipeline']

        if cmds.window(WINID, exists=True):
            cmds.deleteUI(WINID)

        cmds.window(WINID, t=TITLE, rtf=True)
        cmds.rowColumnLayout(nc=5, cw=self.cw(5, 45))

        keys = [k for k in appInfo]

        for app in apps:
            if app in keys:
                icon = app + '.icon.png'
                iconPth = geticon(icon)
                if not os.path.exists(iconPth):
                    shutil.copy2(appInfo[app][1], iconPth)

                toolTip = 'Open ' + app
                path = appInfo[app][2]
                self.makeACoolButton(toolTip, icon, partial(self.openApps, path))

        cmds.showWindow(WINID)

    def cw(self, nc, w, *args):
        cw = []
        for i in range(nc):
            column = (i + 1, w)
            cw.append(column)
            i += 1
        return cw

    def openApps(self, path, *args):
        subprocess.Popen(path)

    def makeACoolButton(self, ann, image, command, *args):
        icon = geticon(image)
        cmds.frameLayout(borderVisible=True, labelVisible=False)
        cmds.symbolButton(ann=ann, i=icon, c=command, h=40, w=40)
        cmds.setParent('..')

        # -------------------------------------------------------------------------------------------------------------
        # END OF CODE
        # -------------------------------------------------------------------------------------------------------------
