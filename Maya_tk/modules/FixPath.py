# -*-coding:utf-8 -*

"""



"""

from maya import cmds
from functools import partial
import os, shutil, logging
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


TEXTURE_NODES = cmds.ls(type='file')
REFERENCE_NODES = cmds.ls(references=True)

winID = 'TexturePathEditor'
winTitle = 'Texture Path Editor'
CW=[(1, 200), (2, 20), (3, 370), (4, 80)]
W = 680
BLUE = (0, 0, .5)
RED = (1, 0, 0)

class FixPath(object):

    def __init__(self):
        super(FixPath, self).__init__()

        self.buildUI()

    def buildUI(self):

        if cmds.window(winID, q=True, exists=True):
            cmds.deleteUI(winID)

        cmds.window(winID, title=winTitle, w=W)

        mainLayout = cmds.scrollLayout()
        texturePart = cmds.frameLayout(l='TEXTURE', lv=True, cll=True)

        for i in range(len(TEXTURE_NODES)):
            cmds.rowColumnLayout(nc=4, cw=CW)
            texPthID = 'texPth' + str(i+1)
            tex = TEXTURE_NODES[i]
            cmds.text(l=tex)
            cmds.text(texPthID, l='', bgc=self.getbgc(cmds.getAttr("%s.fileTextureName" % tex)))
            cmds.textField(texPthID, tx=cmds.getAttr("%s.fileTextureName" % tex))
            cmds.button(l='Fix Path', c=partial(self.fixTexturePth, texPthID, tex))
            cmds.setParent('..')
            i += 1

        cmds.setParent(mainLayout)

        referencePart = cmds.frameLayout(l='REFERENCE', lv=True, cll=True)

        for i in range(len(REFERENCE_NODES)):
            cmds.rowColumnLayout(nc=4, cw=CW)
            refPthID = 'refPth' + str(i+1)
            ref = (REFERENCE_NODES[i].split(':')[-1]).split('RN')[0]
            cmds.text(l=ref)
            cmds.text(refPthID, l='')
            i+=1

        cmds.showWindow(winID)

    def getbgc(self, pth, *args):
        fixPth = os.path.join(cmds.workspace(q=True, rd=True), 'sourceimage')

        if pth[0:len(fixPth)] == fixPth:
            bgc = BLUE
        else:
            bgc = RED

        return bgc


    def fixTexturePth(self, id, tex, *args):
        curPrjPth = cmds.workspace(q=True, rd=True)
        sourceimagesPth = os.path.join(curPrjPth, 'sourceimages')

        scrPth = cmds.textField(id, q=True, tx=True)

        fileName = os.path.basename(scrPth)

        desPth = os.path.join(sourceimagesPth, fileName)

        if not os.path.exists(scrPth) and os.path.exists(desPth):
            cmds.setAttr("%s.fileTextureName" % tex, desPth, type='string')
            cmds.textField(id, edit=True, tx=desPth)
            cmds.text(id, edit=True, bgc=BLUE)
        elif not os.path.exists(scrPth) and not os.path.exists(desPth):
            cmds.confirmDialog(t='Could not find the file', m='texture file: %s is not exists' % scrPth, b='OK')
        elif os.path.exists(desPth):
            cmds.setAttr("%s.fileTextureName" % tex, desPth, type='string')
            cmds.textField(id, edit=True, tx=desPth)
            cmds.text(id, edit=True, bgc=BLUE)
        else:
            shutil.copy2(scrPth, desPth)
            cmds.setAttr("%s.fileTextureName" % tex, desPth, type='string')
            cmds.textField(id, edit=True, tx=desPth)
            cmds.text(id, edit=True, bgc=BLUE)

def initialize():
    FixPath()

if __name__=='__main__':
    initialize()