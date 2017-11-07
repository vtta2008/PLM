# -*-coding:utf-8 -*

"""



"""

from maya import cmds
import logging

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

textures = cmds.ls(type='file')

winID = 'TexturePathEditor'
winTitle = 'Texture Path Editor'

if cmds.window(winID, q=True, exists=True):
    cmds.deleteUI(winID)

cmds.window(winID, title=winTitle, h=500, w=600)

mainLayout = cmds.scrollLayout()
cmds.rowColumnLayout(nc=2, cw=[(1, 200), (2, 390)])

for i in range(len(textures)):
    pthId = 'texPth' + str(i + 1)
    tex = textures[i]
    cmds.text(l=tex)
    cmds.textField(pthId, tx=cmds.getAttr("%s.fileTextureName" % tex))
    i += 1

cmds.showWindow(winID)