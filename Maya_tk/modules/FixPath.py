# -*-coding:utf-8 -*
"""

Script Name: FixPath.py
Author: Do Trinh/Jimmy - TD artist

Description:
    It will load all the texture path that you used in your scene and check, if it is not relative path, it will copy
    it to your sourceimages folder.

"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds
from functools import partial
import os, shutil, logging

# We can configure the current level to make it disable certain logs when we don't want it.
logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
# List all texture node in the scene
TEXTURE_NODES = cmds.ls(type='file')
# List all reference node in the scene
REFERENCE_NODES = cmds.ls(references=True)
# Win id will be assigned to UI
winID = 'TexturePathEditor'
# Window title of the UI
winTitle = 'Texture Path Editor'
# Details of column width
CW = [(1, 5), (2, 20), (3, 5), (4, 300), (5, 5), (6, 80), (7, 5)]
# Width of window UI
W = 420
# Color code
GREEN = (0, 1, 0)
RED = (1, 0, 0)

# ----------------------------------------------------------------------------------------------------------- #
"""                        MAIN CLASS: FIXPATH - LIST AND CHECK ALL THE TEXTURE PATH                        """


# ----------------------------------------------------------------------------------------------------------- #
class FixPath(object):
    def __init__(self):
        # ALways super class
        super(FixPath, self).__init__()
        # Build UI
        self.buildUI()

    def buildUI(self):
        # Check if UI exists, delete it
        if cmds.window(winID, q=True, exists=True):
            cmds.deleteUI(winID)

        # Start declares UI
        cmds.window(winID, title=winTitle, w=W)
        # Create main layout of UI, scroll layout will be awesome
        mainLayout = cmds.scrollLayout()

        cmds.separator(w=W, style='in')
        cmds.text(l='NOTE:', align='left', w=W)
        cmds.text(l="")
        cmds.text(l="GREEN means your path is relative path", bgc=GREEN)
        cmds.text(l="")
        cmds.text(l="RED means your path is wrong, maybe your path link to\n"
                    " a file being outside of project path or not exist", bgc=RED)
        cmds.text(l="")
        cmds.separator(w=W, style='in')

        texturePart = cmds.frameLayout(l='TEXTURE', lv=True, cll=True)

        # A loop of details layout for every texture nodes using column width variable
        for i in range(len(TEXTURE_NODES)):
            texPthID = 'texPth' + str(i + 1)
            tex = TEXTURE_NODES[i]
            cmds.columnLayout()
            cmds.text(l=tex, align='center')
            cmds.setParent('..')
            cmds.rowColumnLayout(nc=7, cw=CW)
            cmds.text(l='')
            cmds.text(texPthID, l='', bgc=self.getbgc(cmds.getAttr("%s.fileTextureName" % tex)))
            cmds.text(l='')
            cmds.textField(texPthID, tx=cmds.getAttr("%s.fileTextureName" % tex))
            cmds.text(l='')
            cmds.button(l='Auto Fix', c=partial(self.fixTexturePth, texPthID, tex))
            cmds.text(l='')
            cmds.setParent('..')
            cmds.columnLayout()
            cmds.separator(w=W)
            cmds.text(l='')
            cmds.setParent('..')
            i += 1

        cmds.setParent(mainLayout)

        # referencePart = cmds.frameLayout(l='REFERENCE', lv=True, cll=True)
        #
        # for i in range(len(REFERENCE_NODES)):
        #     cmds.rowColumnLayout(nc=4, cw=CW)
        #     refPthID = 'refPth' + str(i+1)
        #     ref = (REFERENCE_NODES[i].split(':')[-1]).split('RN')[0]
        #     cmds.text(l=ref)
        #     cmds.text(refPthID, l='')
        #     i+=1

        cmds.showWindow(winID)

    def getbgc(self, pth, *args):

        # Check the path of the texture base on the file name, if it is not relative path, return red color, otherwise return green.
        fixPth = os.path.join(cmds.workspace(q=True, rd=True), 'sourceimage')

        if pth[0:len(fixPth)] == fixPth:
            bgc = GREEN
        else:
            bgc = RED

        return bgc

    def fixTexturePth(self, id, tex, *args):
        # Get the current project path
        curPrjPth = cmds.workspace(q=True, rd=True)
        # Get sourceimages folder of project
        sourceimagesPth = os.path.join(curPrjPth, 'sourceimages')
        # Get texture path from texture node
        scrPth = cmds.textField(id, q=True, tx=True)
        # Get texture file name
        fileName = os.path.basename(scrPth)
        # Create a relative path by default
        desPth = os.path.join(sourceimagesPth, fileName)

        # Check the path of texture node
        if not os.path.exists(scrPth) and os.path.exists(desPth):
            cmds.setAttr("%s.fileTextureName" % tex, desPth, type='string')
            cmds.textField(id, edit=True, tx=desPth)
            cmds.text(id, edit=True, bgc=GREEN)
        elif not os.path.exists(scrPth) and not os.path.exists(desPth):
            cmds.confirmDialog(t='Could not find the file', m='texture file: %s is not exists' % scrPth, b='OK')
            logger.info('texture file: %s is not exists' % scrPth)
        elif os.path.exists(desPth):
            cmds.setAttr("%s.fileTextureName" % tex, desPth, type='string')
            cmds.textField(id, edit=True, tx=desPth)
            cmds.text(id, edit=True, bgc=GREEN)
        else:
            shutil.copy2(scrPth, desPth)
            cmds.setAttr("%s.fileTextureName" % tex, desPth, type='string')
            cmds.textField(id, edit=True, tx=desPth)
            cmds.text(id, edit=True, bgc=GREEN)


def initialize():
    # Run class FixPath
    FixPath()


if __name__ == '__main__':
    initialize()

    # --------------------------------------------------------------------------------------------------------
    # END OF CODE
    # --------------------------------------------------------------------------------------------------------
