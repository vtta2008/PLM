"""

"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import os
import json
import logging
import maya.app.renderSetup.views.renderSetupButton as marv
import threading
import time
import datetime
import getpass
from functools import partial

# -------------------------------------------------------------------------------------------------------------
# FIND PATHS OF MODULES THAT NOT INSTALLED WITH MAYA BY DEFAULT
# -------------------------------------------------------------------------------------------------------------
def importModule(name='userSetup', ext='InitTool.py'):
    userSetupPth = cmds.internalVar(usd=True) + 'scripts/' + name + ext
    if os.path.exists(userSetupPth):
        import userSetup
        reload(userSetup)

importModule()

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
# ID of DAMG pipeline tool UI

MASTERID = 'DAMGtool.v13'
VERSION = int(cmds.about(v=True))

# -------------------------------------------------------------------------------------------------------------
# IMPORT QT MODULES
# -------------------------------------------------------------------------------------------------------------
import Qt # plugin module go with DAMGtool to make UI
from Qt import QtWidgets, QtCore, QtGui

# -------------------------------------------------------------------------------------------------------------
# MAKE MAYA UNDERSTAND QT UI AS MAYA WINDOW,  FIX VERSION CONVENTION
# -------------------------------------------------------------------------------------------------------------
# We can configure the current level to make it disable certain logs when we don't want it.
logging.basicConfig()
logger = logging.getLogger('DAMGtoolBoxII')
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
# CHECK THE CORRECT BINDING THAT BE USING UNDER QT.PY
# -------------------------------------------------------------------------------------------------------------
# While Qt.py lets us abstract the actual Qt library, there are a few things it cannot do yet
# and a few support libraries we need that we have to import manually.
if Qt.__binding__=='PySide':
    logger.debug('Using PySide with shiboken')
    from shiboken import wrapInstance
    from Qt.QtCore import Signal
elif Qt.__binding__.startswith('PyQt'):
    logger.debug('Using PyQt with sip')
    from sip import wrapinstance as wrapInstance
    from Qt.QtCore import pyqtSignal as Signal
else:
    logger.debug('Using PySide2 with shiboken2')
    from shiboken2 import wrapInstance
    from Qt.QtCore import Signal

# -------------------------------------------------------------------------------------------------------------
# SHOW UI - MAKE UI IS DOCKABLE INSIDE MAYA
# -------------------------------------------------------------------------------------------------------------
def getMayaMainWindow():
    """
    Since Maya is Qt, we can parent our UIs to it.
    This means that we don't have to manage our UI and can leave it to Maya.
    Returns:
        QtWidgets.QMainWindow: The Maya MainWindow
    """
    # Use the OpenMayaUI API to get a reference to Maya's MainWindow
    win = omui.MQtUtil_mainWindow()

    # Use the wrapInstance method to convert it to something python can understand (QMainWindow)
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)

    # Return this to whoever wants it
    return ptr

def getDock(name='DAMGmasterToolControlMayaDock', version = VERSION):
    """
    This function creates a dock with the given name.
    It's an example of how we can mix Maya's UI elements with Qt elements
    Args:
        name: The name of the dock to create
    Returns:
        QtWidget.QWidget: The dock's widget
    """
    # Delete any conflicting docks
    deleteDock( name )

    # Create a workspaceControl dock using Maya's UI tools
    if version>=2017:
        ctrl = cmds.workspaceControl(name, label='DAMGtool.v13')
    elif version<=2016:
        ctrl = cmds.dockControl( name, label='DAMGtool.v13' )

    # Use the OpenMayaUI API to get the actual Qt widget associated with the name
    qtCtrl = omui.MQtUtil_findControl(ctrl)

    # Use wrapInstance to convert it to something Python can understand (QWidget)
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
    return ptr

def deleteDock(name='DAMGmasterToolControlMayaDock', version = VERSION):
    """
    A simple function to delete the given dock
    Args:
        name: the name of the dock
    """
    if version >= 2017:
        if cmds.workspaceControl(name, query=True, exists=True):
            cmds.deleteUI(name)
    elif version <= 2016:
        if cmds.dockControl(name, query=True, exists=True):
            cmds.deleteUI(name)

# *********************************************************************************************************** #
# ----------------------------------------------------------------------------------------------------------- #
"""                        MAIN CLASS: DAMG TOOL BOX II - ALL ABOUT CONTROLLER UI                           """
# ----------------------------------------------------------------------------------------------------------- #
# *********************************************************************************************************** #

class DAMGmasterToolControlMaya( QtWidgets.QWidget ):

    user_prefs = cmds.internalVar( upd=True )
    user_scripts = user_prefs + 'scripts/'

    scrData = cmds.internalVar( upd=True ) + 'scripts/infoPath.json'
    with open( scrData, 'r' ) as f:
        scrPth = json.load( f )
    scrIcons = scrPth[ 'icons_mainUI' ]

    def __init__(self, dock=True):
        if dock:
            parent = getDock()
        else:
            deleteDock()
            try:
                cmds.deleteUI('DAMGmasterUI')
            except:
                logger.debug('No previous UI exists')

            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName('DAMGmasterToolControlMaya')
            parent.setWindowTitle('DAMGtool v13')
            dialogLayout = QtWidgets.QVBoxLayout(parent)

        super (DAMGmasterToolControlMaya, self).__init__(parent=parent)

        self.curPth = cmds.workspace( q=True, rd=True )
        self.curPthParts = self.curPth.split( '/' )
        self.curPthList = [ f for f in os.listdir( self.curPth ) if os.path.isdir( self.curPth + f ) ]
        self.reInitialize()

        self.masterUIid = MASTERID

        self.buildUI()

        if not dock:
            parent.show()

    def reInitialize(self):
        self.curPth = cmds.workspace( q=True, rd=True )
        if 'work' in self.curPth or 'sequences' in self.curPth:
            self.curMode = 'Studio Mode'
            self.studioModeVar()
        elif 'assets' in os.listdir( self.curPth + "scenes/" ) or 'sequences' in os.listdir( self.curPth + "scenes/" ):
            self.curMode = 'Group Mode'
            self.groupModeVar()
        else:
            self.curMode = 'Pesonal Mode'
            self.personalModeVar()

    def personalModeVar(self):
        self.prodName = os.path.basename( os.path.normpath( self.curPth ) )
        self.prodPth = self.curPth.split( self.prodName )[ 0 ]
        self.projPth, self.assetsPth = self.curPth
        self.assetsList = [ f.split(".ma")[0] for f in os.listdir( self.assetsPth ) if f.endswith(".ma") ]
        self.assetsTaskList = ["None"]
        self.assetsTaskPth = "None"
        self.sequencesPth = "None"
        self.sequencesList = ["None"]
        self.stageText = "None"
        self.stageName = "None"
        self.curTask = "None"
        self.curTaskPth = "None"

    def groupModeVar(self):
        self.prodName = os.path.basename( os.path.normpath( self.curPth ))
        self.prodPth = self.curPth.split( self.prodName )[ 0 ]
        self.projPth = self.curPth
        self.assetsPth = self.curPth + 'scenes/assets/'
        self.assetsList = [ f for f in os.listdir( self.assetsPth ) if os.path.isdir( self.assetsPth + f ) ]
        self.assetsTaskPth = self.assetsPth + self.assetsList[ 0 ] + '/'
        self.assetsTaskList = [ f for f in os.listdir( self.assetsTaskPth ) if
                                os.path.isdir( self.assetsTaskPth + f ) ]
        self.sequencesPth = self.curPth + 'scenes/sequences/'
        if not os.path.exists( self.sequencesPth ):
            cmds.sysFile( self.sequencesPth, md=True )
        self.sequencesList = [ f for f in os.listdir( self.sequencesPth ) if
                               os.path.isdir( self.sequencesPth + f ) ]
        if self.sequencesList == [ ]:
            self.sequencesTaskPth = self.sequencesPth + 'shot_01/'
            cmds.sysFile( self.sequencesTaskPth, md=True )
            self.sequencesTaskList = [ 'lighting', 'FX', 'layout', 'animation', 'comp' ]
            for i in self.sequencesTaskList:
                cmds.sysFile( self.sequencesTaskPth + i, md=True )
        else:
            self.sequencesTaskPth = self.sequencesPth + self.sequencesList[ 0 ] + '/'
            self.sequencesTaskList = [ f for f in os.listdir( self.sequencesTaskPth ) if
                                       os.path.isdir( self.sequencesTaskPth + f ) ]
        self.stageText = "None"
        self.stageName = "None"
        self.curTask = "None"
        self.curTaskPth = "None"

    def studioModeVar(self):
        self.curPthParts = self.curPth.split( '/' )
        self.curPthList = [ f for f in os.listdir( self.curPth ) if os.path.isdir( self.curPth + f ) ]
        if 'assets' in self.curPthParts:
            self.stageIndex = self.curPthParts.index( 'assets' )
        elif 'sequences' in self.curPthParts:
            self.stageIndex = self.curPthParts.index( 'sequences' )
        self.prodPth = self.curPth.split( self.curPthParts[ self.stageIndex ] )[ 0 ]
        self.prodName = self.curPthParts[ self.stageIndex - 1 ]
        self.prodList = os.listdir( self.prodPth )
        self.projPth = self.prodName + '/' + self.curPthParts[ self.stageIndex ] + \
                       self.curPth.split( self.curPthParts[ self.stageIndex ] )[ -1 ]
        self.projPthParts = self.projPth.split( '/' )
        if self.curPthParts[ self.stageIndex ] == 'assets':
            self.assetsPth = self.prodPth + self.curPthParts[ self.stageIndex ] + '/'
            self.sequencesPth = self.prodPth + self.prodList[ self.prodList.index( 'sequences' ) ] + '/'
        elif self.curPthParts[ self.stageIndex ] == 'sequences':
            self.sequencesPth = self.prodPth + self.curPthParts[ self.stageIndex ] + '/'
            self.assetsPth = self.prodPth + self.prodList[ self.prodList.index( 'assets' ) ] + '/'
        self.assetsList = [ f for f in os.listdir( self.assetsPth ) if os.path.isdir( self.assetsPth + f ) ]
        self.assetsTaskPth = self.assetsPth + self.assetsList[ 0 ] + '/'
        self.assetsTaskList = [ f for f in os.listdir( self.assetsTaskPth ) if
                                os.path.isdir( self.assetsTaskPth + f ) ]
        self.sequencesList = [ f for f in os.listdir( self.sequencesPth ) if
                               os.path.isdir( self.sequencesPth + f ) ]
        self.sequencesTaskPth = self.sequencesPth + self.sequencesList[ 0 ] + '/'
        self.sequencesTaskList = [ f for f in os.listdir( self.sequencesTaskPth ) if
                                   os.path.isdir( self.sequencesTaskPth + f ) ]
        self.curStage = self.projPthParts[ 1 ]
        if self.curStage == 'assets':
            self.curStagePth = self.assetsPth
            self.curTask = self.projPthParts[ 4 ]
        elif self.curStage == 'sequences':
            self.curStagePth = self.sequencesPth
            self.curTask = self.projPthParts[ 3 ]
        self.curStageList = [ f for f in os.listdir( self.curStagePth ) if os.path.isdir( self.curStagePth + f ) ]
        self.curStageSection = self.projPthParts[ 2 ]
        self.curStageSectionPth = self.curStagePth + self.curStageSection + '/'
        self.curStageSectionList = [ f for f in os.listdir( self.curStageSectionPth ) if
                                     os.path.isdir( self.curStageSectionPth + f ) ]
        self.curWorkingPart = self.projPthParts[ 3 ]
        self.curWorkingPartPth = self.curStageSectionPth + self.curWorkingPart + '/'
        self.curWorkingPartList = [ f for f in os.listdir( self.curWorkingPartPth ) if
                                    os.path.isdir( self.curWorkingPartPth + f ) ]
        if self.curWorkingPart == self.curTask:
            self.curTaskPth = self.curWorkingPartPth
        else:
            self.curTaskPth = self.curWorkingPartPth + self.curTask + '/'
        self.workPth = self.curTaskPth + 'work/maya/'
        if os.path.exists( self.workPth ) == False:
            cmds.sysFile( self.workPth, md=True )
        self.workList = os.listdir( self.workPth )
        self.publishPth = self.curTaskPth + 'publish/maya/'
        if os.path.exists( self.publishPth ) == False:
            cmds.sysFile( self.publishPth, md=True )
        self.publishList = [ f.split( '.ma' )[ 0 ] for f in os.listdir( self.publishPth ) if f.endswith( '.ma' ) ]
        self.reviewPth = self.curTaskPth + 'review/'
        if os.path.exists( self.reviewPth ) == False:
            cmds.sysFile( self.reviewPth, md=True )
        self.reviewList = os.listdir( self.reviewPth )
        self.snapShotPth = self.workPth + 'scenes/snapShot/'
        if os.path.exists( self.snapShotPth ) == False:
            cmds.sysFile( self.snapShotPth, md=True )
        self.snapShotFiles = [ f.split( '.ma' )[ 0 ] for f in os.listdir( self.snapShotPth ) if
                               f.endswith( '.ma' ) ]
        if 'assets' in self.curPthParts:
            self.stageName = self.curWorkingPart
            self.stageText = 'Assets:'
        elif 'sequences' in self.curPthParts:
            self.stageName = self.curStageSection
            self.stageText = 'Shot:'

    def buildUI(self):

        self.layout = QtWidgets.QGridLayout(self)

        def makeAcoolButton(label=None, cmd=None):
            cmds.frameLayout( bv=True, lv=False )
            cmds.button( l=label, c=cmd )
            cmds.setParent( '..' )

        def iconButton(ann=None, icon=None, wh=0, c=None):
            scrData = cmds.internalVar( upd=True ) + 'scripts/infoPath.json'
            with open( scrData, 'r' ) as f:
                scrPth = json.load( f )
            scrIcons = scrPth[ 'icons_mainUI' ]
            image = scrIcons + "/" + icon
            cmds.symbolButton( ann=ann, i=image, h=wh, w=wh, c=c )

        masterLayout = cmds.columnLayout( w=440 )
        # create 2 rows, left is menu icon buttons, right is JT tools UI
        mlo = cmds.rowColumnLayout( nc=2, cw=[ (1, 30), (2, 420) ] )
        # make left row for the bar of icon buttons
        mlo_lmlo = cmds.columnLayout()
        # 'start left row: bar with icon buttons'
        cmds.separator( style="in", w=30, h=5 )
        iconButton( 'Refresh UI', 'refresh.icon.png', 30, self.refreshUI )
        cmds.separator( style="in", w=30, h=5 )

        iconButton( 'Open/Load scene', 'openLoad.icon.png', 30, self.DAMGopen )
        iconButton( 'Take a snapshot', 'snapshot.icon.png', 30, self.DAMGsnapShot )
        iconButton( 'Publish file', 'publish.icon.png', 30, self.DAMGpublish )
        cmds.separator( style="in", w=30, h=10 )

        iconButton( 'Go to Publish Folder', 'openPublishFolder.icon.png', 30, self.openPublishFolder )
        iconButton( 'Go to SnapShot Folder', 'openSnapShotFolder.icon.png', 30, self.openSnapShotFolder )
        iconButton( "Go to Project Folder", 'openProjectFolder.icon.png', 30, self.openProjFolder )
        iconButton( 'Go to Scenes Folder', 'openSceneFolder.icon.png', 30, self.openSceneFolder )
        cmds.separator( style="in", w=30, h=10 )

        iconButton( 'Tool Box I', 'toolboxI.icon.png', 30, self.DAMGtoolBoxI )
        iconButton( 'Tool Box II', 'DAMGtoolBoxII.png', 30, self.DAMGtoolBoxII )
        iconButton( 'Tool Box III', 'DAMGtoolBoxIII.png', 30, self.DAMGtoolBoxIII )
        iconButton( 'Open Apps', 'gotoapp.icon.png', 30, self.DAMGfunctionsAppsTransfer )
        iconButton( 'Clock and Reminder', 'clock.icon.png', 30, self.waitforupdate )
        cmds.separator( style="in", w=30, h=10 )

        cmds.symbolCheckBox( 'gcb', ann='Mesh Display', i='object.icon.png', v=True, w=30, h=30,
                             cc=partial( self.setDisplay, 'surfaceShape' ) )
        cmds.symbolCheckBox( 'ccb', ann='Camera Display', i='camera.icon.png', v=True, w=30, h=30,
                             cc=partial( self.setDisplay, 'camera' ) )
        cmds.symbolCheckBox( 'jcb', ann='Joint Display', i='kinJoint.png', v=True, w=30, h=30,
                             cc=partial( self.setDisplay, 'joint' ) )
        cmds.symbolCheckBox( 'ncb', ann='Curves Display', i='curveCV.png', v=True, w=30, h=30,
                             cc=partial( self.setDisplay, 'nurbsCurve' ) )
        cmds.symbolCheckBox( 'lcb', ann='Light Display', i='spotlight.png', v=True, w=30, h=30,
                             cc=partial( self.setDisplay, 'light' ) )

        cmds.separator( style="in", w=35, h=10 )

        cmds.setParent( mlo )

        menuBar = cmds.menuBarLayout()
        # file
        cmds.menu( label='File', tearOff=True )
        cmds.menuItem( label='New', c='cmds.file(f=True,new=True)' )
        cmds.menuItem( label='Open/Load', c=self.DAMGopen )
        cmds.menuItem( label='SnapShot', c=self.DAMGsnapShot )
        cmds.menuItem( label='Publish', c=self.DAMGpublish )
        cmds.menuItem( divider=True )
        cmds.menuItem( label='Quit', c=self.quitMainUI )
        # data
        cmds.menu( l='Data', tearOff=True )
        cmds.menuItem( l='Save Production Info', c=self.saveMayaInfo )
        cmds.menuItem( l='Inspection Local', c=self.inspectionInfo )

        # about
        cmds.menu( label='About', tearOff=True, parent=menuBar )
        cmds.menuItem( label='Pipeline ', c=self.pipelineLayout )
        cmds.menuItem( label='About pipeline tool', c=self.aboutThisTool )
        # end of menu
        mlor = cmds.columnLayout()
        mlor_trrlo1 = cmds.columnLayout( w=420 )
        # Make a Collapsable frame style layout /3rd layer
        cmds.text( l="", h=5, w=420 )
        cmds.separator( style="in", w=420, h=5 )
        cmds.setParent( '..' )
        # create layout for right row /4th layer
        mlor = cmds.columnLayout( w=420 )
        self.tabControls = cmds.tabLayout( 'mlorTabControls' )
        t1 = cmds.columnLayout( w=420 )
        t1_ro1 = cmds.rowColumnLayout( nc=7, cw=[ (1, 100), (2, 145), (3, 5), (4, 5), (5, 5), (6, 120), (7, 25) ] )
        cmds.text( l="Production Name: ", align='left' )
        projectName = cmds.textField( 'projectName', tx=self.prodName )
        cmds.text( l="" )
        cmds.separator( style='in', hr=False )
        cmds.text( l="" )
        cmds.text( 'curMode', l=self.curMode )
        self.refreshCheckMode()
        iconButton( "Refresh", 'refresh.icon.png', 25, self.refreshCheckMode )
        cmds.setParent( '..' )

        t1_ro2 = cmds.rowColumnLayout( nc=3, cw=[ (1, 100), (2, 280), (3, 25) ] )
        t1_ro2_t1 = cmds.text( l="Production Path:", align='left' )
        prodPthTf = cmds.textField( 'prodPthTf', tx=self.prodPth )
        iconButton( "Refresh", 'refresh.icon.png', 25, self.refreshProdPth )
        t1_ro2_t2 = cmds.text( l="Project Path:", align='left' )
        projPthTf = cmds.textField( 'projPthTf', tx=self.curPth )
        iconButton( "Refresh", 'refresh.icon.png', 25, self.refreshProjPth )
        cmds.setParent( '..' )

        t1_ro3 = cmds.rowColumnLayout( nc=5, cw=[ (1, 135), (2, 2.5), (3, 135), (4, 2.5), (5, 135) ] )
        cmds.button( l="Set Project", c=self.setProject )
        cmds.text( l="" )
        cmds.button( l="Maya Folder", c=self.createMayaFolder )
        cmds.text( l="" )
        cmds.button( l="Project Manager", c=self.DAMGprojectManagerUI )
        cmds.setParent( t1 )

        self.projectContentUI()

        cmds.setParent( t1 )

        cmds.setParent( mlor )
        cmds.separator( style='in', w=420 )

        mlor_lo1 = cmds.columnLayout( w=420 )

        self.commonSectionUI()

        cmds.setParent( mlor_lo1 )

        t2 = cmds.columnLayout( parent=self.tabControls, w=420 )
        t2_ro1 = cmds.rowColumnLayout( nc=2, cw=[ (1, 210), (2, 210) ] )
        t2_ro1_lo1 = cmds.columnLayout()
        makeAcoolButton( 'Create Gear', self.createGear )
        cmds.setParent( '..' )
        t2_ro1_lo2 = cmds.columnLayout()
        cmds.frameLayout( bv=True, lv=False )
        cmds.setParent( self.tabControls )

        t3 = cmds.columnLayout( parent=self.tabControls )
        makeAcoolButton( 'Rigging', self.waitforupdate )
        cmds.setParent( self.tabControls )

        t4 = cmds.columnLayout( parent=self.tabControls )
        makeAcoolButton( 'Surfacing', self.waitforupdate )
        cmds.setParent( self.tabControls )

        t5 = cmds.columnLayout( parent=self.tabControls )
        makeAcoolButton( 'Dynamics', self.waitforupdate )
        cmds.setParent( self.tabControls )

        t6 = cmds.columnLayout( parent=self.tabControls )
        makeAcoolButton( 'Animation', self.waitforupdate )
        cmds.setParent( self.tabControls )

        t7 = cmds.columnLayout( parent=self.tabControls )
        makeAcoolButton( 'Light Manager', self.lightManager )
        cmds.setParent( self.tabControls )
        # Create appropriate labels for the ts
        cmds.tabLayout( self.tabControls, edit=True, tabLabel=(
            (t1, "Project"), (t2, "Model"), (t3, "Rig"), (t4, "Surface"), (t5, "FX"), (t6, "Anim"), (t7, "Light")) )

        ctrl = omui.MQtUtil.findControl(self.masterUIid)

        masterLayoutWidget = wrapInstance(long(ctrl), QtWidgets.QWidget)

        self.layout.addWidget(masterLayoutWidget, 1, 1, 1, 2)

    def projectContentUI(self):
        def iconButton(ann=None, icon=None, wh=0, c=None):
            scrData = cmds.internalVar( upd=True ) + 'scripts/infoPath.json'
            with open( scrData, 'r' ) as f:
                scrPth = json.load( f )
            scrIcons = scrPth[ 'icons_mainUI' ]
            image = scrIcons + "/" + icon
            cmds.symbolButton( ann=ann, i=image, h=wh, w=wh, c=c )

        # 'scene setup section'
        projt1 = cmds.columnLayout( w=420 )
        cmds.separator( style='in', w=420 )

        projt1_ro1 = cmds.rowColumnLayout( nc=2, cw=[ (1, 205), (2, 205) ] )
        projTabControl = cmds.tabLayout( 'projTabControl', cc=self.refreshProjTab )
        projt1_ro1_t1 = cmds.columnLayout( parent=projTabControl, w=200 )
        projt1_ro1_t1_ro1 = cmds.rowColumnLayout( nc=2, cw=[ (1, 175), (2, 25) ] )
        assetsMenu = cmds.optionMenu( 'assetsMenu', l='Assets:', w=175, cc=self.updateAssetsSections )
        for i in self.assetsList:
            menuItem = cmds.menuItem( l=i )
        iconButton( "Refresh", 'refresh.icon.png', 25, self.waitforupdate )
        cmds.setParent( '..' )

        projt1_ro1_t1_lo1 = cmds.rowColumnLayout( nc=2, cw=[ (1, 120), (2, 75) ] )
        assetsTab = cmds.textScrollList( 'assetsSelectList', h=150, w=120, ams=False, a=self.assetsTaskList,
                                         sc=self.updateSelectionTask )
        cmds.popupMenu( parent=assetsTab, ctl=False, button=3 )
        cmds.menuItem( l="Go to", c=self.goToAssetsFolder )
        taskTab = cmds.textScrollList( 'assetsTaskList', h=150, w=70, ams=False, sc=self.updateAssetsDetailTask )
        cmds.popupMenu( parent=taskTab, ctl=False, button=3 )
        cmds.menuItem( l="Set project to", c=self.setProjectToSelectTask )
        cmds.menuItem( l="Go to", c=self.goToAssetsTaskFolder )
        cmds.setParent( projt1_ro1 )

        projt1_ro1_t2 = cmds.columnLayout( parent=projTabControl, w=200 )
        projt1_ro1_t2_ro1 = cmds.rowColumnLayout( nc=2, cw=[ (1, 175), (2, 25) ] )
        sequencesMenu = cmds.optionMenu( 'sequencesMenu', l='Shots:', w=175, cc=self.updateSequenceSelectTask )
        for i in self.sequencesList:
            menuItem = cmds.menuItem( l=i )
        iconButton( "Refresh", 'refresh.icon.png', 25, self.waitforupdate )
        cmds.setParent( '..' )

        projt1_ro1_t2_lo1 = cmds.columnLayout( w=195 )
        shotsTab = cmds.textScrollList( 'sequencesTaskList',
                                        h=150, w=190, ams=False,
                                        a=self.sequencesTaskList,
                                        sc=self.updateSequenceDetailTask )
        cmds.popupMenu( parent=shotsTab, ctl=False, button=3 )
        cmds.menuItem( l="Set project to" )
        cmds.menuItem( l="Go to" )
        cmds.setParent( projt1_ro1 )

        cmds.tabLayout( projTabControl, edit=True, tabLabel=((projt1_ro1_t1, "Assets"), (projt1_ro1_t2, "Shots")) )

        cmds.columnLayout( 'detailsLayout', w=200 )
        cmds.rowColumnLayout( nc=5, cw=[ (1, 35), (2, 60), (3, 5), (4, 30), (5, 65) ] )
        cmds.text( 'stageText', l=self.stageText, align='left' )
        cmds.text( 'stageMainUI', l=self.stageName.upper(), align='center' )
        cmds.separator( style='in', hr=False )
        cmds.text( l='Task:', align='left' )
        cmds.text( 'taskMainUI', l=self.curTask.upper(), align='center' )
        cmds.setParent( '..' )

        cmds.text( l="", h=3 )
        cmds.separator( style='in', w=200 )
        detailTabControl = cmds.tabLayout( 'detailTabControl' )

        projt1_lo2_t1 = cmds.columnLayout( parent=detailTabControl, w=195 )
        snapShotTab = cmds.textScrollList( 'snapShotList', h=157, w=190, sc=self.updateViewer )
        cmds.popupMenu( parent=snapShotTab, ctl=False, button=3 )
        cmds.menuItem( l="Import" )
        cmds.menuItem( l="Load" )
        cmds.menuItem( l="Go to" )
        cmds.setParent( '..' )

        projt1_lo2_t2 = cmds.columnLayout( parent=detailTabControl, w=195 )
        reviewTab = cmds.textScrollList( 'reviewList', h=157, w=190, sc=self.updateViewer )
        cmds.popupMenu( parent=reviewTab, ctl=False, button=3 )
        cmds.menuItem( l="Go to" )
        cmds.setParent( '..' )

        projt1_lo2_t3 = cmds.columnLayout( parent=detailTabControl, w=195 )
        publishTab = cmds.textScrollList( 'publishList', h=157, w=190, sc=self.updateViewer )
        cmds.popupMenu( parent=publishTab, ctl=False, button=3 )
        cmds.menuItem( l="Import" )
        cmds.menuItem( l="Create Reference" )
        cmds.menuItem( l="Go to" )
        cmds.setParent( '..' )

        cmds.tabLayout( detailTabControl, edit=True,
                        tabLabel=((projt1_lo2_t1, "SnapShot"), (projt1_lo2_t2, "Review"), (projt1_lo2_t3, "Publish")) )
        cmds.setParent( projt1 )

        projt1_lo3 = cmds.rowColumnLayout( nc=4, cw=[ (1, 102), (2, 102), (3, 102), (4, 102) ] )
        cmds.button( l="Open/Load", c=self.DAMGopen )
        cmds.button( l="Snap Shot", c=self.DAMGsnapShot )
        cmds.button( l="Review Daily" )
        cmds.button( l="Publish File", c=self.DAMGpublish )
        cmds.setParent( projt1 )

        projt1_lo4 = cmds.columnLayout( w=420 )
        cmds.separator( style='in', w=420 )
        projt1_lo4_ro1 = cmds.rowColumnLayout( nc=3, cw=[ (1, 210), (2, 5), (3, 205) ] )
        cmds.columnLayout( w=210 )
        cmds.frameLayout( bv=True, lv=False )
        self.viewImage = cmds.image( 'imageViewerMainUI', w=205, h=115, vis=False )
        self.viewText = cmds.text( 'textViewerMainUI', l="No image", w=205, h=115, align='center' )
        cmds.setParent( projt1_lo4_ro1 )
        cmds.columnLayout( w=10 )
        cmds.text( l='' )
        cmds.setParent( '..' )
        cmds.columnLayout( w=130 )
        cmds.text( 'name', l="", align='left', h=20 )
        cmds.text( 'time', l="", align='left' )
        cmds.text( 'size', l="", align='left' )
        cmds.text( 'commentMainUI', l="", align='left', h=20 )
        cmds.setParent( projt1 )

        cmds.setParent( '..' )

    def commonSectionUI(self):
        def makeAcoolButton(label=None, cmd=None):
            cmds.frameLayout( bv=True, lv=False )
            cmds.button( l=label, c=cmd )
            cmds.setParent( '..' )

        def iconButton(ann=None, icon=None, wh=0, c=None):
            scrData = cmds.internalVar( upd=True ) + 'scripts/infoPath.json'
            with open( scrData, 'r' ) as f:
                scrPth = json.load( f )
            scrIcons = scrPth[ 'icons_mainUI' ]
            image = scrIcons + '/' + icon
            cmds.symbolButton( ann=ann, i=image, h=wh, w=wh, c=c )

        w = 420
        bl = 2
        iw = 60
        bw = w - 3 * bl - iw

        w2 = iw / 2
        w3 = (bw - 6) / 3
        w6 = (bw - 1) / 6

        cw2 = [ (1, w2), (2, w2) ]
        cw3 = [ (1, w3), (2, w3), (3, w3) ]
        cw5 = [ (1, bl), (2, iw), (3, bl), (4, bw), (5, bl) ]
        cw6 = [ (1, w6), (2, w6), (3, w6), (4, w6), (5, w6), (6, w6) ]

        mlor_lo1_ro1 = cmds.rowColumnLayout( nc=5, cw=cw5 )
        cmds.text( l="" )

        mlor_lo1_ro1_ro1 = cmds.rowColumnLayout( nc=2, cw=cw2 )
        iconButton( 'Vray VFB', 'vrayVFB.icon.png', w2, self.openVrayVFB )
        iconButton( 'Render Setting', 'renderSetting.icon.png', w2, 'cmds.RenderGlobalsWindow()' )
        iconButton( 'Node Editor', 'nodeEditor.icon.png', w2, 'cmds.NodeEditorWindow()' )
        iconButton( 'Hypershader', 'hypershader.icon.png', w2, 'cmds.HypershadeWindow()' )
        iconButton( 'Plugin Manager', 'pluinManager.icon.png', w2, 'cmds.PluginManager()' )
        iconButton( 'Outliner', 'outliner.icon.png', w2, 'mel.eval("OutlinerWindow;")' )
        iconButton( 'Script Editor', 'scriptEditor.icon.png', w2, self.openScriptEditor )
        iconButton( 'Graph Editor', 'graphEditor.icon.png', w2, 'mel.eval("GraphEditor;")' )
        iconButton( 'UV Editor', 'uvEditor.icon.png', w2, 'mel.eval("TextureViewWindow;")' )
        cmds.setParent( mlor_lo1_ro1 )

        cmds.text( l="" )

        mlo3_lo1_ro1_lo1 = cmds.columnLayout( w=bw )
        mlo3_lo1_ro1_lo1_ro1 = cmds.rowColumnLayout( nc=3, cw=cw3 )
        makeAcoolButton( "Freeze Transform", self.freezeTransformation )
        makeAcoolButton( "Join Shape", 'cmds.parent(r=True, s=True)' )
        makeAcoolButton( "Clean Node", 'mel.eval("MLdeleteUnused;")' )
        cmds.setParent( mlo3_lo1_ro1_lo1 )

        mlo3_lo1_ro1_lo1_ro2 = cmds.rowColumnLayout( nc=6, cw=cw6 )
        makeAcoolButton( "Del His", self.deleteHis )
        makeAcoolButton( "Cen Piv", self.centerPivot )
        makeAcoolButton( "Locator", self.createLocatorFromSelection )
        makeAcoolButton( "Cluster", self.createClusterFromSelection )
        makeAcoolButton( "Disp", self.createSingleDispNode )
        makeAcoolButton( "Mul.Disp", self.createMultiDispNode )
        cmds.setParent( mlo3_lo1_ro1_lo1 )

        mlor_lo1_ro1_ro3 = cmds.rowColumnLayout( nc=3, cw=cw3 )
        makeAcoolButton( "Group Center", self.groupCenter )
        makeAcoolButton( "Joint", self.createJointFromSelection )
        makeAcoolButton( "Select Children", 'cmds.select(hi=True)' )
        cmds.setParent( mlor_lo1_ro1 )

        cmds.text( l="" )

    def waitforupdate(self, *args):
        cmds.confirmDialog( t="Wait for update",
                            m="this function is currenly under construction"
                              "please wait for next update",
                            b="OK"
                            )

    def openScriptEditor(self, *args):
        try:
            mel.eval( 'charcoalEditor' )
        except RuntimeError:
            mel.eval( 'ScriptEditor;' )

    def inspectionInfo(self, *args):
        title = "Inspection Report"
        userName = 'userPath.json'
        infoName = 'infoPath.json'
        infoPth = self.user_scripts + infoName
        userPth = cmds.internalVar( usd=True ) + 'DAMGpipelineTool/userLirary/' + userName

        with open( infoPth, 'r' ) as f:
            self.toolPth = json.load( f )
        with open( userPth, 'r') as f:
            self.userPth = json.load(f)

        infoTitle = "User & System Information"
        pathTitle = "Files & data path"
        self.winID = "reportInfo"

        infoTool = [key for key in self.toolPth]
        infoUser = [key for key in self.userPth]

        indexTool = max([len(self.toolPth[f] + f) for f in self.toolPth])
        indexUser = max([len(self.userPth[f] + f) for f in self.userPth])
        index = (indexTool+indexUser)/2

        bl = 10
        w = index*7.5
        w3 = w-(2*bl)
        blh = bl
        cw = [(1,bl),(2,w3),(3,bl)]
        cw3 = [(1,0.2*w3),(2,bl),(3,w3-((0.2*w3)+(0.5*bl)))]

        self.closeReportWindow()

        cmds.window(self.winID, t=title, w=w)

        mlo = cmds.columnLayout( w=w )
        cmds.rowColumnLayout(nc=3, cw=cw)
        cmds.text(l="")
        cmds.columnLayout(w=w3)
        cmds.separator(style='in', w=w3)
        cmds.text(l=infoTitle.upper(), align='center', w=w3)
        cmds.separator( style='in', w=w3 )
        cmds.rowColumnLayout( nc=3, cw=cw3 )

        for i in range(len(infoUser)):
            cmds.text(l=infoUser[i], align='right')
            cmds.text(l=":", align='center')
            cmds.text(l=self.toolPth[infoUser[i]], align='left')

        cmds.setParent( mlo )

        cmds.separator(style='in', w=w3)
        cmds.text(l=pathTitle.upper(), align='center', w=w3)
        cmds.separator( style='in', w=w3 )

        cmds.rowColumnLayout( nc=3, cw=cw3 )

        for i in range( len( infoTool ) ):
            cmds.text( l=infoTool[ i ], align='right' )
            cmds.text( l=":", align='center' )
            cmds.text( l=self.toolPth[ infoTool[ i ] ], align='left' )

        cmds.setParent( mlo )

        cmds.separator(style='in', w=w, h=blh)
        cmds.button(l="OK", w=w, c=self.closeReportWindow)
        cmds.separator( style='in', w=w, h=blh )

        cmds.showWindow(self.winID)

    def closeReportWindow(self, *args):
        if cmds.window( self.winID, query=True, exists=True ):
            cmds.deleteUI( self.winID )

    def format_bytes(self, bytes_num=0):
        sizes = [ "B", "KB", "MB", "GB", "TB" ]
        i = 0
        dblbyte = bytes_num
        while (i < len( sizes ) and bytes_num >= 1024):
            dblbyte = bytes_num / 1024.0
            i = i + 1
            bytes_num = bytes_num / 1024
        size = str( round( dblbyte, 2 ) ) + " " + sizes[ i ]
        return size

    def saveMayaInfo(self, *args):
        infoFile = {}
        user = getpass.getuser()
        infoFile['Mode'] = self.curMode
        infoFile['User'] = user

        list = cmds.fileInfo(q=True)
        for i in list:
            info = cmds.fileInfo(i, q=True)
            if len(info)==1:
                infoFile[i] = info[0]

        if self.curMode == 'Studio Mode':
            filePth = os.path.join(self.prodPth + 'data/', self.prodName + '_data.info')
        elif self.curMode == 'Group Mode':
            filePth = os.path.join(self.curPth+ 'data/', self.prodName + '_data.info')

        if not os.path.exists(self.curPth+ 'data/'):
            cmds.sysFile(self.curPth+ 'data/', md=True)

        with open(filePth, 'w') as f:
            json.dump(infoFile, f, indent=4)

    def goToAssetsFolder(self, *args):
        self.reInitialize()
        item1 = cmds.optionMenu( 'assetsMenu', q=True, value=True)
        item2 = cmds.textScrollList( 'assetsSelectList', q=True, si=True )
        updatePth = self.assetsPth + item1 + "/" + item2[0]
        os.startfile(updatePth)

    def goToAssetsTaskFolder(self, *args):
        self.reInitialize()
        item1 = cmds.optionMenu( 'assetsMenu', q=True, value=True )
        item2 = cmds.textScrollList( 'assetsSelectList', q=True, si=True )
        item3 = cmds.textScrollList('assetsTaskList', q=True, si=True)
        updatePth = self.assetsPth + item1 + "/" + item2[ 0 ] + "/" + item3[0]
        os.startfile( updatePth )

    def setProjectToSelectTask(self, *args):
        self.reInitialize()
        item1 = cmds.optionMenu( 'assetsMenu', q=True, value=True )
        item2 = cmds.textScrollList( 'assetsSelectList', q=True, si=True )
        item3 = cmds.textScrollList('assetsTaskList', q=True, si=True)
        updatePth = self.assetsPth + item1 + "/" + item2[ 0 ] + "/" + item3[0] + "/work/maya"
        mel.eval( 'setProject \"' + updatePth + '\"' )

        self.updateWhenChangeProPth()

    def clearDataList(self):
        cmds.textScrollList( 'snapShotList', e=True, ra=True )
        cmds.textScrollList( 'reviewList', e=True, ra=True )
        cmds.textScrollList( 'publishList', e=True, ra=True )
        cmds.image( 'imageViewerMainUI', e=True, vis=False )
        cmds.text( 'textViewerMainUI', e=True, vis=True )

    def refreshUI(self, *args):
        pass

    def lightManager(self, *args):
        import DAMGtoolBoxIII
        reload( DAMGtoolBoxIII )
        DAMGtoolBoxIII.showUI()

    def createGear(self, *args):
        pass

    def refreshProjTab(self, *args):
        if cmds.tabLayout( 'projTabControl', q=True, sti=True ) == 1:
            menuSelect = cmds.optionMenu( 'assetsMenu', q=True, value=True )
            itemSelect1 = cmds.textScrollList( 'assetsSelectList', q=True, si=True )
            itemSelect2 = cmds.textScrollList( 'assetsTaskList', q=True, si=True )
            if isinstance( itemSelect1, list ) or isinstance( itemSelect2, list ) is False:
                cmds.textScrollList( 'snapShotList', e=True, ra=True )
                cmds.textScrollList( 'reviewList', e=True, ra=True )
                cmds.textScrollList( 'publishList', e=True, ra=True )
            else:
                self.updateAssetsDetailTask()

    def updateAssetsSections(self, *args):
        self.reInitialize()
        menuSelect = cmds.optionMenu( 'assetsMenu', q=True, value=True )
        updatePth = self.assetsPth + menuSelect + '/'
        updateList = [ f for f in os.listdir( updatePth ) if os.path.isdir( updatePth + f ) ]
        cmds.textScrollList( 'assetsSelectList', e=True, ra=True )
        cmds.textScrollList( 'assetsSelectList', e=True, a=updateList )
        self.clearDataList()

    def updateSelectionTask(self, *args):
        self.reInitialize()
        itemSelect1 = cmds.textScrollList( 'assetsSelectList', q=True, si=True )
        menuSelect = cmds.optionMenu( 'assetsMenu', q=True, value=True )
        updatePth = self.assetsPth + menuSelect + '/' + itemSelect1[ 0 ] + '/'
        updateList = [ f for f in os.listdir( updatePth ) if os.path.isdir( updatePth + f ) ]
        cmds.textScrollList( 'assetsTaskList', e=True, ra=True )
        cmds.textScrollList( 'assetsTaskList', e=True, a=updateList )
        self.clearDataList()

    def updateAssetsDetailTask(self, *args):
        self.reInitialize()
        menuSelect = cmds.optionMenu( 'assetsMenu', q=True, value=True )
        itemSelect1 = cmds.textScrollList( 'assetsSelectList', q=True, si=True )
        itemSelect2 = cmds.textScrollList( 'assetsTaskList', q=True, si=True )
        updatePth = self.assetsPth + menuSelect + '/' + itemSelect1[ 0 ] + '/' + itemSelect2[ 0 ] + '/'
        updatePublishPth = updatePth + 'publish/maya/'
        if os.path.exists( updatePublishPth ) == False:
            cmds.sysFile( updatePublishPth, md=True )
        updateReviewPth = updatePth + 'review/'
        if os.path.exists( updateReviewPth ) == False:
            cmds.sysFile( updateReviewPth, md=True )
        if self.curMode == 'Studio Mode':
            updateSnapShotPth = updatePth + 'work/maya/scenes/snapShot/'
        elif self.curMode == 'Group Mode':
            updateSnapShotPth = updatePth + 'work/maya/snapShot/'
        elif self.curMode == 'Personal Mode':
            updateSnapShotPth = updatePth + 'work/maya/snapShot/'

        if not os.path.exists(updateSnapShotPth):
            cmds.sysFile( updateSnapShotPth, md=True )

        updatePublishList = [ f.split( '.ma' )[ 0 ] for f in os.listdir( updatePublishPth ) if f.endswith( '.ma' ) ]
        updateReviewList = [ f for f in os.listdir( updateReviewPth ) ]
        updateSnapShotList = [ f.split( '.ma' )[ 0 ] for f in os.listdir( updateSnapShotPth ) if f.endswith( '.ma' ) ]

        cmds.textScrollList( 'snapShotList', e=True, ra=True )
        cmds.textScrollList( 'reviewList', e=True, ra=True )
        cmds.textScrollList( 'publishList', e=True, ra=True )
        cmds.textScrollList( 'snapShotList', e=True, a=updateSnapShotList )
        cmds.textScrollList( 'reviewList', e=True, a=updateReviewList )
        cmds.textScrollList( 'publishList', e=True, a=updatePublishList )

        cmds.image( 'imageViewerMainUI', e=True, vis=False )
        cmds.text( 'textViewerMainUI', e=True, vis=True )

    def updateSequenceSelectTask(self, *args):
        self.reInitialize()
        menuSelect = cmds.optionMenu( 'sequencesMenu', q=True, value=True )
        updatePth = self.sequencesPth + menuSelect + '/'
        updateList = [ f for f in os.listdir( updatePth ) if os.path.isdir( updatePth + f ) ]
        cmds.textScrollList( 'sequencesTaskList', e=True, ra=True )
        cmds.textScrollList( 'sequencesTaskList', e=True, a=updateList )
        self.clearDataList()

    def updateSequenceDetailTask(self, *args):
        self.reInitialize()
        menuSelect = cmds.optionMenu( 'sequencesMenu', q=True, value=True )
        itemSelect = cmds.textScrollList( 'sequencesTaskList', q=True, si=True )
        updatePth = self.sequencesPth + menuSelect + '/' + itemSelect[ 0 ] + '/'
        updatePublishPth = updatePth + 'publish/maya/'
        if not os.path.exists( updatePublishPth ):
            cmds.sysFile( updatePublishPth, md=True )
        updateReviewPth = updatePth + 'review/'
        if not os.path.exists( updateReviewPth ):
            cmds.sysFile( updateReviewPth, md=True )
        if self.curMode == 'Studio Mode':
            updateSnapShotPth = updatePth + 'work/maya/scenes/snapShot/'
        elif self.curMode == 'Group Mode':
            updateSnapShotPth = updatePth + 'work/maya/snapShot/'

        if not os.path.exists( updateSnapShotPth ):
            cmds.sysFile( updateSnapShotPth, md=True )
        updatePublishList = [ f.split( '.ma' )[ 0 ] for f in os.listdir( updatePublishPth ) if f.endswith( '.ma' ) ]
        updateReviewList = [ f for f in os.listdir( updateReviewPth ) ]
        updateSnapShotList = [ f.split( '.ma' )[ 0 ] for f in os.listdir( updateSnapShotPth ) if f.endswith( '.ma' ) ]
        cmds.textScrollList( 'snapShotList', e=True, ra=True )
        cmds.textScrollList( 'reviewList', e=True, ra=True )
        cmds.textScrollList( 'publishList', e=True, ra=True )
        cmds.textScrollList( 'snapShotList', e=True, a=updateSnapShotList )
        cmds.textScrollList( 'reviewList', e=True, a=updateReviewList )
        cmds.textScrollList( 'publishList', e=True, a=updatePublishList )
        cmds.image( 'imageViewerMainUI', e=True, vis=False )
        cmds.text( 'textViewerMainUI', e=True, vis=True )

    def updateViewer(self, *args):
        if cmds.tabLayout( 'projTabControl', q=True, sti=True ) == 1:
            menuSelect = cmds.optionMenu( 'assetsMenu', q=True, value=True ) or [ ]
            itemSelect1 = cmds.textScrollList( 'assetsSelectList', q=True, si=True ) or [ ]
            itemSelect2 = cmds.textScrollList( 'assetsTaskList', q=True, si=True ) or [ ]
            self.updatePth = self.assetsPth + menuSelect + '/' + itemSelect1[ 0 ] + '/' + itemSelect2[ 0 ] + '/'
        elif cmds.tabLayout( 'projTabControl', q=True, sti=True ) == 2:
            menuSelect = cmds.optionMenu( 'sequencesMenu', q=True, value=True ) or [ ]
            itemSelect = cmds.textScrollList( 'sequencesTaskList', q=True, si=True ) or [ ]
            self.updatePth = self.sequencesPth + menuSelect + '/' + itemSelect[ 0 ] + '/'

        if cmds.tabLayout( 'detailTabControl', q=True, sti=True ) == 1:
            snapShotItem = cmds.textScrollList( 'snapShotList', q=True, si=True ) or [ ]
            if snapShotItem == [ ]:
                cmds.image( 'imageViewerMainUI', e=True, vis=False )
                cmds.text( 'textViewerMainUI', e=True, vis=True )
            else:
                if self.curMode == 'Studio Mode':
                    updateImagePth = self.updatePth + 'work/maya/scenes/snapShot/' + snapShotItem[ 0 ] + '.jpg'
                    self.updateCommentPth = self.updatePth + 'work/maya/scenes/snapShot/' + snapShotItem[ 0 ] + '.comment'
                elif self.curMode == 'Group Mode':
                    updateImagePth = self.updatePth + 'work/maya/snapShot/' + snapShotItem[ 0 ] + '.jpg'
                    self.updateCommentPth = self.updatePth + 'work/maya/snapShot/' + snapShotItem[ 0 ] + '.comment'
                elif self.curMode == 'Personal Mode':
                    updateImagePth = self.updatePth + 'work/maya/snapShot/' + snapShotItem[ 0 ] + '.jpg'
                    self.updateCommentPth = self.updatePth + 'work/maya/snapShot/' + snapShotItem[ 0 ] + '.comment'

                updateSnapShotPth = updateImagePth.split('.jpg')[0] + '.png'
                image = om.MImage()
                image.readFromFile(updateImagePth)
                image.resize(205,115)
                image.writeToFile(updateSnapShotPth, 'png')
                self.updateInfoFile(filePth=updateSnapShotPth.split('.png')[0] + '.ma')

                if not os.path.exists( updateImagePth ):
                    cmds.image( 'imageViewerMainUI', e=True, vis=False )
                    cmds.text( 'textViewerMainUI', e=True, vis=True )
                    cmds.text('commentMainUI', e=True, l="No comment")
                else:
                    cmds.image( 'imageViewerMainUI', e=True, i=updateSnapShotPth, vis=True )
                    cmds.text( 'textViewerMainUI', e=True, vis=False )
                    self.updateCommentMainUI()

        elif cmds.tabLayout( 'detailTabControl', q=True, sti=True ) == 2:
            reviewItem = cmds.textScrollList( 'reviewList', q=True, si=True ) or [ ]
            if reviewItem == []:
                cmds.image( 'imageViewerMainUI', e=True, vis=False )
                cmds.text( 'textViewerMainUI', e=True, vis=True )
                cmds.text( 'commentMainUI', e=True, l="No comment" )
            else:
                updateReviewPth = self.updatePth + 'review/' + reviewItem[ 0 ]
                if not os.path.exists( updateReviewPth ):
                    cmds.image( 'imageViewerMainUI', e=True, vis=False )
                    cmds.text( 'textViewerMainUI', e=True, vis=True )
                    cmds.text( 'commentMainUI', e=True, l="No comment" )
                else:
                    cmds.image( 'imageViewerMainUI', e=True, i=updateReviewPth, vis=True )
                    cmds.text( 'textViewerMainUI', e=True, vis=False )
                    self.updateCommentMainUI()
        elif cmds.tabLayout( 'detailTabControl', q=True, sti=True ) == 3:
            publishItem = cmds.textScrollList( 'publishList', q=True, si=True ) or [ ]
            if publishItem == [ ]:
                cmds.image( 'imageViewerMainUI', e=True, vis=False )
                cmds.text( 'textViewerMainUI', e=True, vis=True )
                cmds.text( 'commentMainUI', e=True, l="No comment" )
            else:
                updatePublishPth = self.updatePth + 'work/maya/scenes/snapShot/' + publishItem[ 0 ] + '_r001.jpg'
                if not os.path.exists( updatePublishPth ):
                    cmds.image( 'imageViewerMainUI', e=True, vis=False )
                    cmds.text( 'textViewerMainUI', e=True, vis=True )
                    cmds.text( 'commentMainUI', e=True, l="No comment" )
                else:
                    cmds.image( 'imageViewerMainUI', e=True, i=updatePublishPth, vis=True )
                    cmds.text( 'textViewerMainUI', e=True, vis=False )
                    self.updateCommentMainUI()

    def updateInfoFile(self, filePth=None):
        if os.path.exists(filePth):
            name = os.path.basename(filePth)
            size = self.format_bytes(bytes_num = os.path.getsize(filePth))
            lastime = datetime.datetime.strptime(time.ctime(os.path.getctime(os.path.join(filePth))), "%a %b %d %H:%M:%S %Y")
            rightTime = datetime.datetime.strptime(str(lastime), '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S - %d %b %Y')
            cmds.text( 'name', e=True, l=name )
            cmds.text( 'size', e=True, l=size )
            cmds.text( 'time', e=True, l=rightTime )

    def updateCommentMainUI(self, *args):
        if os.path.exists( self.updateCommentPth ):
            with open( self.updateCommentPth, 'r' ) as f:
                rawInfo = json.load( f )
                comment = rawInfo[ 'Comment' ]
            cmds.text( 'commentMainUI', e=True, l=comment )
        else:
            cmds.text( 'commentMainUI', e=True, l="No comment" )

    def refreshCheckMode(self, *args):
        self.reInitialize()
        cmds.text( 'curMode', e=True, l=self.curMode )
        print "Production: %s is designed for %s" % (self.prodName.upper(), self.curMode)

    def tick(self, *args):
        self.curTime = time.strftime( '%H:%M:%S' )
        self.timeUpdate = ''
        if self.curTime != self.timeUpdate:
            self.timeUpdate = self.curTime
            self.config = cmds.textField( self.clock, e=True, text=self.curTime )
        self.timeThread = threading.Timer( 1, self.tick )
        self.timeThread.start()

    def setProject(self, *args):
        mel.eval( "setProjectFromFileDialog;" )
        self.updateWhenChangeProPth()

    def updateWhenChangeProPth(self):
        self.reInitialize()
        cmds.text( 'curMode', e=True, l=self.curMode )
        cmds.textField( 'prodPthTf', e=True, tx=self.prodPth )
        cmds.text( 'stageMainUI', e=True, l=self.stageName.upper())
        cmds.textField( 'projPthTf', e=True, tx=self.curPth )
        cmds.text( 'stageText', e=True, l=self.stageText )
        cmds.text( 'taskMainUI',e=True, l=self.curTask.upper() )

    def refreshProdPth(self, *args):
        self.reInitialize()
        cmds.textField( 'prodPthTf', e=True, tx=self.prodPth )

    def refreshProjPth(self, *args):
        self.reInitialize()
        cmds.textField( 'projPthTf', e=True, tx=self.curPth )

    def pipelineLayout(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.aboutThisTool()

    def aboutThisTool(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.aboutThisTool()

    def DAMGtoolBoxI(self, *args):
        import DAMGtoolBoxI
        reload( DAMGtoolBoxI )
        DAMGtoolBoxI.DAMGtoolBoxI()

    def DAMGtoolBoxII(self, *args):
        import DAMGtoolBoxII
        reload( DAMGtoolBoxII )
        DAMGtoolBoxII.DAMGtoolBoxII()

    def DAMGtoolBoxIII(self, *args):
        import DAMGtoolBoxIII
        reload( DAMGtoolBoxIII )
        DAMGtoolBoxIII.DAMGtoolBoxIII()

    def openProjFolder(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.openProjFolder()

    def openSceneFolder(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.openSceneFolder()

    def openSourceimagesFolder(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.openSourceimagesFolder()

    def openSnapShotFolder(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.openSnapShotFolder()

    def openPublishFolder(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.openPublishFolder()

    def DAMGpublish(self, *args):
        import DAMGfileManagerForMaya
        reload( DAMGfileManagerForMaya )
        DAMGfileManagerForMaya.DAMGfileManagerForMaya().DAMGpulishUI()

    def DAMGopen(self, *args):
        import DAMGfileManagerForMaya
        reload( DAMGfileManagerForMaya )
        DAMGfileManagerForMaya.DAMGfileManagerForMaya().DAMGopenLoadFilesUI()

    def DAMGsnapShot(self, *args):
        import DAMGfileManagerForMaya
        reload( DAMGfileManagerForMaya )
        DAMGfileManagerForMaya.DAMGfileManagerForMaya().DAMGsnapShotUI()

    def quitMainUI(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.quitButtonMenu()

    def DAMGfunctionsAppsTransfer(self, *args):
        import DAMGfunctionsAppsTransfer
        reload( DAMGfunctionsAppsTransfer )
        DAMGfunctionsAppsTransfer.DAMGfunctionsAppsTransfer()

    def DAMGprojectManagerUI(self, *args):
        import DAMGprojectManager
        reload( DAMGprojectManager )
        DAMGprojectManager.DAMGprojectManagerUI()

    def createMayaFolder(self, *args):
        pass

    def spreadSheetUI(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.spreadSheetUI()

    def createSingleDispNode(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.createSingleDispNode()

    def createMultiDispNode(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.createMultiDispNode()

    def importDAMGbtf(self):
        import DAMGfunctionsToolForMaya
        reload( DAMGfunctionsToolForMaya )
        return DAMGfunctionsToolForMaya

    def setDisplay(self, type=None, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.setDisplay(type)

    def createJointFromSelection(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.createJointFromSelections()

    def createLocatorFromSelection(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.createLocatorFromSelection()

    def createClusterFromSelection(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.createClusterFromSelection()

    def groupCenter(self, *args):
        a = cmds.ls( sl=True )
        cmds.group( n=a[ 0 ] + "_group" )

    def deleteHis(self, *args):
        a = cmds.ls( sl=True )
        if (len( a ) > 0):
            cmds.DeleteHistory()

    def centerPivot(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.centerPivot()

    def JointOn(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.JointOn()

    def JointOff(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.JointOff()

    def freezeTransformation(self, *args):
        a = cmds.ls( sl=True )
        if (len( a ) > 0):
            cmds.makeIdentity( apply=True )

    def Chop(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.Chop()

    def reverseNormal(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.reverseNormal()

    def normalOnOff(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.normalOnOff()

    def openVrayVFB(self, *args):
        DAMGbuttonsFunction = self.importDAMGbtf()
        DAMGbuttonsFunction.openVrayVFB()
#End of Main UI