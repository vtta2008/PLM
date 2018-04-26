# -*-coding:utf-8 -*
"""

Script Name: CustomViewer.py
Author: Do Trinh/Jimmy - TD artist

Description:
    It will make an individual viewer from chossen camera.

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

import logging
import os
from functools import partial  # partial module can store variables to method

# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA MODULES
# -------------------------------------------------------------------------------------------------------------
import maya.cmds as cmds

from plt_plugins.maya.modules import MayaVariables as var

# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA MODULES
# -------------------------------------------------------------------------------------------------------------

NAMES = var.MAINVAR
ICONS = var.ICONS
VERSION = NAMES['mayaVersion']
RESX = 1280
RESY = 720
DIRECTORY = os.path.join(cmds.internalVar(usd=True), 'capture')
CAMSHAPE = 'template_renderCamShape'
CAMNAME = 'template_renderCam'

# # -------------------------------------------------------------------------------------------------------------
# # IMPORT QT MODULES
# # -------------------------------------------------------------------------------------------------------------
# import Qt # plugin module go with DAMGtool to make UI
# from Qt import QtWidgets, QtCore, QtGui

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
#
# def getMayaMainWindow():
#     win = omui.MQtUtil_mainWindow()
#     ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
#     return ptr
#
# def getDock(name='Custom Viewer', label='Custom Viewer', version=VERSION):
#     deleteDock( name )
#     if version>=2017:
#         ctrl = cmds.workspaceControl(name,label=label)
#     else:
#         ctrl = cmds.dockControl(name, label=label)
#     qtCtrl = omui.MQtUtil_findControl(ctrl)
#     ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
#     return ptr
#
# def deleteDock(name='Custom Viewer', version=VERSION):
#     """
#     A simple function to delete the given dock
#     Args:
#         name: the name of the dock
#     """
#     if version >= 2017:
#         if cmds.workspaceControl(name, query=True, exists=True):
#             cmds.deleteUI(name)
#     else:
#         if cmds.dockControl(name, query=True, exists=True):
#             cmds.deleteUI(name)

def importBTS():
    from plt_maya.modules import MayaFuncs
    reload(MayaFuncs)
    return MayaFuncs


def getCameraList():
    camLst = []
    camShapes = cmds.ls(type='camera')
    for shape in camShapes:
        name = cmds.listRelatives(shape, p=True)[0]
        camLst.append(name)
    return camLst


def populateCamViewerUI(*args):
    cam = cmds.textScrollList('camLst', query=True, si=True)

    cmds.deleteUI('chooseCam')

    CustomViewer(cam=cam[0])


def chooseCamera():
    chooseCamID = 'chooseCam'
    if not cmds.window(chooseCamID, query=True, exists=True):
        chooseCam = cmds.window(chooseCamID, t='Available Camera')
        cmds.columnLayout()
        cmds.text(l='Please, choose camera to view', align='center')
        cmds.text(l='')
        cmds.textScrollList('camLst', append=cmds.ls(type='camera'))
        cmds.text(l='')
        cmds.button(l='OK', c=populateCamViewerUI, w=100)
        cmds.text(l='')
        cmds.showWindow(chooseCam)
    else:
        pass


class CustomViewer(object):
    camLst = getCameraList()

    bts = importBTS()
    screenViewer = 'Screen Viewer'

    def __init__(self, cam, w=RESX, h=RESY, dock=True):

        self.W = w
        self.H = h

        super(CustomViewer, self).__init__()

        self.camName = cam

        self.buildUI()

    def buildUI(self):
        fileName = 'capture'
        adj = 10
        if cmds.objExists(self.camName):
            cmds.setAttr((self.camName + ".farClipPlane"), k=True)
            cmds.setAttr((self.camName + ".nearClipPlane"), k=True)
            cmds.select(clear=True)

        if cmds.window('User Viewer', query=True, exists=True):
            cmds.deleteUI('User Viewer')

        renderViewID = cmds.window('User Viewer', s=True, t='User Viewer' + ': ' + self.camName.split('Shape')[0])
        masterLayout = cmds.columnLayout(adj=True)
        viewer = cmds.paneLayout(w=self.W, h=self.H)
        self.panel = cmds.modelPanel(mbv=0, label="Custom Viewer", cam=self.camName)

        tempLayout = cmds.modelPanel(self.panel, q=1, bl=True)

        cmds.modelEditor(self.panel, e=True, grid=0, da="smoothShaded")
        cmds.modelEditor(self.panel, e=True, allObjects=1, nurbsSurfaces=1, polymeshes=1, subdivSurfaces=1,
                         nurbsCurves=1, cv=1, hulls=1, planes=1, cameras=1, imagePlane=1, joints=0, ikHandles=0,
                         deformers=1, dynamics=0, fluids=1, hairSystems=1, follicles=1, nCloths=1, nParticles=1,
                         nRigids=1, dynamicConstraints=1, locators=1, dimensions=1, pivots=1, handles=1, textures=1,
                         strokes=1, motionTrails=1, pluginShapes=1, clipGhosts=1, greasePencils=1, manipulators=1,
                         hud=1)

        cmds.setParent(masterLayout)
        self.bts.makeSeparator(h=5, w=self.W)
        nc = 15
        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwE(nc=nc, w=self.W, adj=adj), h=25)

        cmds.checkBox(label="Grid", v=False,
                      onc=(partial(self.changeSetting, 'grid', 1)),
                      ofc=(partial(self.changeSetting, 'grid', 0)))
        cmds.checkBox(label="Nurbs", align="left", v=True,
                      onc=(partial(self.changeSetting, 'nurbsSurfaces', 1)),
                      ofc=(partial(self.changeSetting, 'nurbsSurfaces', 0)))
        cmds.checkBox(label="Polys", align="left", v=True,
                      onc=(partial(self.changeSetting, 'polymeshes', 1)),
                      ofc=(partial(self.changeSetting, 'polymeshes', 0)))
        cmds.checkBox(label="Curves", align="left", v=True,
                      onc=(partial(self.changeSetting, 'nurbsCurves', 1)),
                      ofc=(partial(self.changeSetting, 'nurbsCurves', 0)))
        cmds.checkBox(label="Joints", align="left", v=False,
                      onc=(partial(self.changeSetting, 'joints', 1)),
                      ofc=(partial(self.changeSetting, 'joints', 0)))
        cmds.checkBox(label="HUD", align="left", v=True,
                      onc=(partial(self.changeSetting, 'hud', 1)),
                      ofc=(partial(self.changeSetting, 'hud', 0)))
        cmds.checkBox(label="Viewport2", align="left", v=True,
                      onc=(partial(self.changeSetting, 'rnm', 'vp2Renderer')),
                      ofc=(partial(self.changeSetting, 'rnm', 'base_OpenGL_Renderer')))

        focalLst = [12, 20, 27, 35, 45, 50, 80, 100, 125]

        cmds.optionMenu("RS_lensOpt", label="Lens", w=80)
        for i in focalLst:
            cmds.menuItem(l=str(i))
        cmds.optionMenu("RS_lensOpt", edit=True, v="35")
        cmds.setAttr((self.camName + ".focalLength"), 35)
        cmds.optionMenu("RS_lensOpt", edit=True, cc=self.setFocallength)
        cmds.setParent(masterLayout)

        self.bts.makeSeparator(h=5, w=self.W)
        nc = 4
        mainSetting = cmds.rowColumnLayout(nc=nc, cw=self.bts.cwE(nc=nc, w=self.W, adj=adj))

        cmds.columnLayout(adj=True)
        cmds.frameLayout(bv=True, lv=False)
        self.seqNumber = cmds.intFieldGrp(l='Sequence Number')
        self.shotNumber = cmds.intFieldGrp(l='Shot Number')
        self.stageCheck = cmds.textFieldGrp(l='Shot Stage', tx='')
        nc = 2
        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwE(nc=nc, w=(self.W - adj) / 4, adj=adj / 2))
        self.bts.makeAcoolButton('Create Shot Display', 'Create Shot Display', self.shotHUD)
        self.bts.makeAcoolButton('Delete Shot Display', 'Delete', self.delHUD)
        cmds.setParent(mainSetting)

        cmds.columnLayout(adj=True)
        cmds.frameLayout(bv=True, lv=False)
        cmds.optionMenu('ActiveCam', l='Camera', w=80)
        for cam in self.camLst:
            if cmds.objExists(cam):
                print cam

        for i in self.camLst:
            cmds.menuItem(l=str(i))
        cmds.optionMenu('ActiveCam', edit=True, cc=self.changeActiveCamera)
        cmds.setParent(mainSetting)

        cmds.setParent(masterLayout)
        self.bts.makeSeparator(h=5, w=self.W)
        self.bts.makeAcoolButton('Capture this frame', "Capture", partial(self.captureImage, fileName))
        cmds.control(tempLayout, e=1, visible=False)
        cmds.showWindow(renderViewID)

        logger.info(renderViewID)

    def getShotNumber(self, *args):
        shotNumber = cmds.intFieldGrp(self.shotNumber, query=True, value1=True)
        selectedNodes = cmds.selectedNodes() or []
        if not len(selectedNodes) == 0:
            mainObj = selectedNodes[-1]
            positionList = cmds.getAttr('%s.translate' % mainObj)
        else:
            positionList = [0.0, 0.0, 0.0]

        positionList[0] = shotNumber

        return positionList

    def shotStage(self, *args):
        stageCheck = cmds.textFieldGrp(self.stageCheck, query=True, tx=True)
        sSelectedNodes = cmds.selectedNodes()
        print stageCheck

    def shotHUD(self, *args):
        shot = cmds.intFieldGrp(self.shotNumber, query=True, value1=True)
        seq = cmds.intFieldGrp(self.seqNumber, query=True, value1=True)
        blk = 0
        seCT = 1
        self.shotStage()
        cmds.headsUpDisplay('HUDShotNumber', section=seCT, block=blk, blockSize='medium',
                            label='Scene %s - Shot %s' % (str(seq), str(shot)), command=self.shotNumber)

    def delHUD(self, *args):
        cmds.headsUpDisplay('stageHUD', rem=True)
        cmds.headsUpDisplay('HUDShotNumber', rem=True)

    def changeSetting(self, flag, mode, *args):
        if flag == 'grid':
            cmds.modelEditor(self.panel, e=True, grid=mode)
        elif flag == 'nurbsSurfaces':
            cmds.modelEditor(self.panel, e=True, nurbsSurfaces=mode)
        elif flag == 'polymeshes':
            cmds.modelEditor(self.panel, e=True, polymeshes=mode)
        elif flag == 'nurbsCurves':
            cmds.modelEditor(self.panel, e=True, nurbsCurves=mode)
        elif flag == 'joints':
            cmds.modelEditor(self.panel, e=True, joints=mode)
        elif flag == 'HUD':
            cmds.modelEditor(self.panel, e=True, hud=mode)
        elif flag == 'rnm':
            cmds.modelEditor(self.panel, e=True, rnm=mode)

    def setFocallength(self, *args):
        focal = cmds.optionMenu('RS_lensOpt', query=True, v=True)
        cmds.setAttr(self.camName + '.focalLength', float(focal))

    def changeActiveCamera(self, *args):
        camera = cmds.optionMenu('ActiveCam', query=True, v=True) + 'Shape'
        cmds.modelEditor(self.panel, e=True, cam=camera)

    def captureImage(self, name, directory=DIRECTORY, *args):
        if not os.path.exists(directory):
            os.mkdir(directory)

        path = os.path.join(directory, '%s' % name)
        w = RESX
        h = RESY
        currentTime = cmds.currentTime(query=True)
        cmds.playblast(v=False, frame=currentTime, wh=(w, h), p=100, orn=False, fmt="image", filename=path)
        cmds.layoutDialog(dismiss="1")

# -------------------------------------------------------------------------------------------------------------
# END OF CODE
# -------------------------------------------------------------------------------------------------------------
