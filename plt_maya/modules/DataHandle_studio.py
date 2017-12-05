# -*-coding:utf-8 -*
"""

Script Name: DataHandle_studio.py
Author: Do Trinh/Jimmy - TD artist

Description:
    This is the most important tools I have been making ever, it is the set of snapshot, publish and loader.

    Snapshot will capture out your current viewer, also save out your work incrementally with note made by user
    so that you can comeback to exactly moment you do snapshot via loader tool.

    Publish will publish your current version and automatically save out the next version so you can keep continuing
    working in your progress. Another artist may use your publish.

    Loader is to load your snapshot.

"""

import json
import logging
import os
import shutil

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds

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

def importBTS():
    from plt_maya.modules import MayaFuncs
    reload(MayaFuncs)
    return MayaFuncs


IMAGESIZE = (900, 540)
W1 = IMAGESIZE[0] / 3
W2 = IMAGESIZE[0]
W = W1 + W2
ADJ = 10


class DataHandle(object):
    bts = importBTS()

    def __init__(self):
        self.curPth = cmds.workspace(q=True, rd=True)
        self.workPth = os.path.join(self.curPth, "scenes")
        self.filePth = cmds.file(q=True, loc=True)

        self.snapShotPth = os.path.join(self.curPth, "scenes/snapShot")
        if not os.path.exists(self.snapShotPth):
            cmds.sysFile(self.snapShotPth, md=True)

        self.publishPth = os.path.join(self.curPth.split('work')[0], "publish/maya/")
        if not os.path.exists(self.publishPth):
            cmds.sysFile(self.publishPth, md=True)

        numOfSectInPth = len((self.curPth.split("work")[0]).split("/"))
        self.assetName = (self.curPth.split("work")[0]).split("/")[(numOfSectInPth - 3)]
        self.taskName = (self.curPth.split("work")[0]).split("/")[(numOfSectInPth - 2)]
        self.baseFileName = self.assetName + "_" + self.taskName
        # get file save
        saveFilesList = [f.split('.ma')[0] for f in os.listdir(self.workPth) if self.baseFileName in f]
        if (len(saveFilesList) == 0):
            cmds.file(rename=self.baseFileName + "_v001")
            cmds.file(save=True, type='mayaAscii')
        else:
            for file in saveFilesList:
                num = file.split("_v")[-1]
                if "." in num or "-" in num or "_" in num:
                    saveFilesList.remove(file)

        fileVersion = [f.split(self.baseFileName + '_v')[-1] for f in saveFilesList]

        if fileVersion == []:
            self.maxVer = '001'
        else:
            self.maxVer = (str(max([int(f) for f in fileVersion]))).zfill(3)

        self.verFileName = self.baseFileName + '_v' + self.maxVer + '.ma'

        ssFilesList = [f for f in os.listdir(self.snapShotPth) if
                       f.endswith('.ma') and self.verFileName.split('.ma')[0] in f]

        if (len(ssFilesList) == 0):
            reversion = ["001"]
        elif (len(ssFilesList) == 1):
            reversion = ["002"]
        else:
            reversion = [((f.split('_v')[-1]).split('_r')[-1]).split('.ma')[0] for f in ssFilesList]

        self.maxRever = (str(max([int(f) for f in reversion]) + 1)).zfill(3)

        self.reverFileName = self.verFileName.split('.ma')[0] + "_r" + self.maxRever + '.ma'

        self.publishNameFile = self.verFileName.split("_v")[0] + "_v" + str(
            int((self.verFileName.split(".")[0]).split("_v")[-1]) + 1).zfill(3) + ".ma"

        self.filePublishPth = os.path.join(self.publishPth, self.verFileName)

        self.publishRevName = self.publishNameFile.split('.ma')[0] + "_r001.ma"

        publishImageName = self.publishRevName.split('.ma')[0] + ".jpg"

        self.snapShotImageName = self.reverFileName.split(".ma")[0] + ".jpg"

        self.fileSavePth = os.path.join(self.workPth, self.verFileName)

        self.fileSnapShotPth = os.path.join(self.snapShotPth, self.reverFileName)

        self.imageSnapShotPth = os.path.join(self.snapShotPth, self.snapShotImageName)

        self.imagepublishPth = os.path.join(self.snapShotPth, publishImageName)

    def snapshotUI(self):
        title = 'Snapshot'
        # START MAKING SNAPSHOT WINDOW UI
        self.screenShotImage(self.imageSnapShotPth)
        # header
        if cmds.window('ssWinID', q=True, exists=True):
            cmds.deleteUI('ssWinID')

        ssWinID = cmds.window('ssWinID', t=title)
        snapshotLayout = cmds.columnLayout(w=W)
        self.headerLayout('Snapshot Menu', W1, W2)
        cmds.setParent(snapshotLayout)
        # body
        nc = 2
        mlo_ro2 = cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc=nc, widthList=[W1, W2]))
        # left row - snap shot menu)
        leftColumn = cmds.columnLayout(adj=True)
        self.bts.makeSeparator(h=5, w=W1)
        cmds.text(l="SnapShot File Details: ", h=30)
        # -----------------------------------
        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc=nc, widthList=[80, 220]))
        cmds.text(l="File Version", align='center')
        cmds.optionMenu('snapshotFileName', w=215)
        cmds.menuItem('fileName_item1', l=self.verFileName)

        cmds.text(l='Reversion', align='center')
        self.reversionName = cmds.optionMenu('reversionName', w=215)
        cmds.menuItem(l=self.reverFileName)
        cmds.setParent(leftColumn)
        # -----------------------------------
        self.bts.makeSeparator(h=5, w=W1)
        cmds.textField('ssComment', h=50, w=W1)
        self.bts.makeSeparator(h=5, w=W1)
        # -----------------------------------
        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwE(nc=nc, w=W1, adj=(ADJ / 2)))
        self.bts.makeAcoolButton('Screenshot and Increment Save', "Save File", self.snapShotSaveFile)
        self.bts.makeAcoolButton('Close Snapshot Window', "Close", self.snapshotClose)
        cmds.setParent('..')
        self.bts.makeSeparator(h=5, w=W1)
        # -----------------------------------
        cmds.setParent(mlo_ro2)
        cmds.columnLayout()
        self.bts.makeSeparator(h=5, w=W2)
        cmds.image(image=self.imageSnapShotPth, w=IMAGESIZE[0], h=IMAGESIZE[1])
        cmds.text(l=self.snapShotImageName, w=W2, align='center')
        # -----------------------------------
        # show snap shot UI
        cmds.setParent(snapshotLayout)
        self.bts.makeSeparator(h=5, w=W)
        cmds.showWindow(ssWinID)

    def publishUI(self):
        title = 'Publish'
        # START MAKING PUBLISH WINDOW UI
        self.screenShotImage(self.imagepublishPth)
        # Header
        if cmds.window('plWinID', q=True, exists=True):
            cmds.deleteUI('plWinID')
        # -----------------------------------
        plWinID = cmds.window('plWinID', t=title)
        publishLayout = cmds.columnLayout(w=W)
        self.headerLayout('Publish Menu', W1, W2)
        cmds.setParent(publishLayout)
        # body
        nc = 2
        mlo_ro2 = cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc=nc, widthList=[W1, W2]))
        # -----------------------------------
        cmds.columnLayout(adj=True)
        cmds.text(l="Publish File Details: ", h=30)
        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc=nc, widthList=[80, 220]))
        cmds.text(l="File Version")
        cmds.optionMenu('publishFileName', w=215)
        cmds.menuItem('fileName_item1', l=self.verFileName)
        # -----------------------------------
        cmds.text(l="Reversion: ")
        self.reversionName = cmds.optionMenu('reversionName', w=210)
        self.reversionName_item1 = cmds.menuItem('reversionName_item1', l=self.publishRevName)
        cmds.setParent('..')
        self.bts.makeSeparator(h=5, w=W1)
        cmds.text(l="Comment:")
        self.bts.makeSeparator(h=5, w=W1)
        cmds.textField('plComment', h=30, w=W1)
        self.bts.makeSeparator(h=5, w=W1)
        # -----------------------------------
        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwE(nc=nc, w=W1, adj=(ADJ / 2)))
        self.bts.makeAcoolButton('Publish a version', "Publish File", self.publishFile)
        self.bts.makeAcoolButton('Close Publish Window', "Close", self.publishClose)
        cmds.setParent('..')
        self.bts.makeSeparator(h=5, w=W1)
        # -----------------------------------
        cmds.setParent(mlo_ro2)
        cmds.columnLayout()
        cmds.image(image=self.imagepublishPth, w=IMAGESIZE[0], h=IMAGESIZE[1])
        cmds.text(l=self.snapShotImageName, w=W2, align='center')
        # -----------------------------------
        # show publish UI
        cmds.setParent(publishLayout)
        self.bts.makeSeparator(h=5, w=W)
        cmds.showWindow(plWinID)

    def loaderUI(self):
        title = "Loader"

        self.save_ssExt = [f for f in os.listdir(self.snapShotPth) if f.endswith('.ma')]
        self.save_ssImg = [f for f in os.listdir(self.snapShotPth) if f.endswith('.jpg')]

        if cmds.window('loaderUI', q=True, exists=True):
            cmds.deleteUI('loaderUI')

        loaderUI = cmds.window('loaderUI', t=title, rtf=True)
        self.loaderMainLayout = cmds.columnLayout()
        self.headerLayout('Loader', W1, W2)
        cmds.setParent(self.loaderMainLayout)
        # body
        nc = 2
        self.mlo_ro2 = cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc=nc, widthList=[W1, W2]))
        # left row
        cmds.columnLayout(adj=True)
        cmds.text(l="File Details: ", h=30)
        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc=nc, widthList=[80, 220]))
        cmds.text(l="File: ")
        self.ssFile_Menu = cmds.optionMenu('ssFileMenu', cc=self.refreshImage)
        for i in range(len(self.save_ssExt)):
            cmds.menuItem(l=self.save_ssExt[i])
            i += 1
        cmds.setParent('..')
        self.bts.makeSeparator(h=5, w=W1)
        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwE(nc=nc, w=W1, adj=(ADJ / 2)))
        self.bts.makeAcoolButton('Load File', 'Load File', self.openFile)
        self.bts.makeAcoolButton('Close Loader Window', "Close", self.closeFile)
        cmds.setParent('..')
        self.bts.makeSeparator(h=5, w=W1)

        cmds.text(l="Comment:")
        self.bts.makeSeparator(h=5, w=W1)
        cmds.text('comment', l='', w=W1)

        cmds.setParent(self.mlo_ro2)
        # right row
        cmds.columnLayout(adj=True)
        imgPth = self.getImagePth()
        if not os.path.exists(imgPth):
            imageVisible = False
            textVisible = True
        else:
            imageVisible = True
            textVisible = False

        self.imageDisplay = cmds.image(i=imgPth, vis=imageVisible)
        self.viewText = cmds.text(l="No data to show", align='center', w=IMAGESIZE[0], h=IMAGESIZE[1], vis=textVisible)

        cmds.setParent(self.loaderMainLayout)
        self.bts.makeSeparator(h=5, w=W)
        cmds.showWindow(loaderUI)

    def getImagePth(self):
        value = str(cmds.optionMenu('ssFileMenu', query=True, value=True))
        pth = os.path.join(self.snapShotPth, value).split('.ma')[0] + '.jpg'
        if not os.path.exists(pth):
            logger.info('can not find image')
            pth = ""
        else:
            pass

        return pth

    def headerLayout(self, name, w1, w2):
        self.bts.makeSeparator(h=5, w=W)
        nc = 2
        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc=2, widthList=[W1, W2]))
        cmds.text(l=name, align='center')
        cmds.text(l='Snap Shot viewer')
        cmds.setParent('..')
        self.bts.makeSeparator(h=5, w=W)

    def screenShotImage(self, path):
        view = omui.M3dView.active3dView()
        image = om.MImage()
        view.readColorBuffer(image, True)
        image.resize(IMAGESIZE[0], IMAGESIZE[1])
        image.writeToFile(path, 'jpg')

    def publishFile(self, *args, **info):
        cmds.file(save=True, type='mayaAscii')
        shutil.copy2(self.fileSavePth, self.filePublishPth)
        cmds.file(rename=str(self.publishNameFile + ".ma"))
        cmds.file(save=True, type='mayaAscii')

        name = self.publishNameFile.split('.ma')[0] + "_r001"
        infoFile = os.path.join(self.snapShotPth, '%s.comment' % name)

        info['Name'] = name + ".ma"
        info['Comment'] = cmds.textField('plComment', q=True, tx=True)
        info['SnapShot'] = self.fileSnapShotPth
        info['Image'] = self.imageSnapShotPth

        with open(infoFile, 'w') as f:
            json.dump(info, f, indent=4)

        shutil.copy2(self.fileSavePth, self.snapShotPth + "/" + name + ".ma")
        if cmds.window('plWinID', exists=True):
            cmds.deleteUI('plWinID')

    def publishClose(self, *args):
        if os.path.exists(self.imageSnapShotPth) is True:
            cmds.sysFile(self.imageSnapShotPth, delete=True)
        if os.path.exists(self.imagepublishPth) is True:
            cmds.sysFile(self.imagepublishPth, delete=True)
        if cmds.window('plWinID', exists=True):
            cmds.deleteUI('plWinID')

    def snapShotSaveFile(self, *args, **info):
        name = self.reverFileName.split('.ma')[0]
        infoFile = os.path.join(self.snapShotPth, '%s.comment' % name)

        info['Name'] = self.reverFileName
        info['Comment'] = cmds.textField('ssComment', q=True, tx=True)
        info['SnapShot'] = self.fileSnapShotPth
        info['Image'] = self.imageSnapShotPth

        cmds.file(rename=self.verFileName)
        cmds.file(save=True, type='mayaAscii')
        shutil.copy2(self.fileSavePth, self.fileSnapShotPth)

        with open(infoFile, 'w') as f:
            json.dump(info, f, indent=4)

        if cmds.window('ssWinID', exists=True):
            cmds.deleteUI('ssWinID')

    def snapshotClose(self, *args):
        if os.path.exists(self.imageSnapShotPth) is True:
            cmds.sysFile(self.imageSnapShotPth, delete=True)
        if os.path.exists(self.imagepublishPth) is True:
            cmds.sysFile(self.imagepublishPth, delete=True)
        if cmds.window('ssWinID', exists=True):
            cmds.deleteUI('ssWinID')

    def refreshImage(self, *args, **info):
        imgPth = str(self.getImagePth())
        if not os.path.exists(imgPth):
            cmds.image(self.imageDisplay, e=True, vis=False)
            cmds.text(self.viewText, e=True, vis=False)
        else:
            cmds.image(self.imageDisplay, e=True, image=imgPth, vis=True)
            cmds.text(self.viewText, e=True, vis=False)

        infoPth = (imgPth.split('.jpg')[0]) + '.comment'
        if not os.path.exists(infoPth):
            comment = "No comment"
        else:
            with open(infoPth, 'r') as f:
                rawInfo = json.load(f)
            comment = rawInfo['Comment']

        cmds.text('comment', e=True, l=comment)

    def openFile(self, *args):
        cmds.file(new=True, f=True)
        value = cmds.optionMenu('ssFileMenu', query=True, value=True)
        cmds.file(self.snapShotPth + "/" + value, open=True)
        cmds.file(rename=self.verFileName)
        cmds.file(save=True, type='mayaAscii')
        if cmds.window('loaderUI', exists=True):
            cmds.deleteUI('loaderUI')

    def closeFile(self, *args):
        if cmds.window('loaderUI', exists=True):
            cmds.deleteUI('loaderUI')

            # -------------------------------------------------------------------------------------------------------------
            # END OF CODE
            # -------------------------------------------------------------------------------------------------------------
