# -*-coding:utf-8 -*

"""

"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds
import maya.mel as mel
from functools import partial
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import os, sys, time, datetime, json, logging

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
from Maya_tk.modules import MayaVariables as var
NAMES = var.MAINVAR
MESSAGE = var.MESSAGE
TITLE = var.TITLE
VERSION = NAMES['mayaVersion']
SCRPTH = os.path.join(os.getenv('PROGRAMDATA'), 'PipelineTool/scrInfo')

# Icon directory:
ICONS = var.ICONS

# Main width of UI
WIDTH = 450
ICONWIDTH = 30

# FIX VERSION CONVENTION
from Maya_tk.plugins import Qt
from Maya_tk.plugins.Qt import QtWidgets, QtCore, QtGui

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
if Qt.__binding__=='PySide':
    logger.debug('Using PySide with shiboken')
    from shiboken import wrapInstance
    from Maya_tk.plugins.Qt.QtCore import Signal
elif Qt.__binding__.startswith('PyQt'):
    logger.debug('Using PyQt with sip')
    from sip import wrapinstance as wrapInstance
    from Maya_tk.plugins.Qt.QtCore import pyqtSignal as Signal
else:
    logger.debug('Using PySide2 with shiboken2')
    from shiboken2 import wrapInstance
    from Maya_tk.plugins.Qt.QtCore import Signal

# Convert PyQt window to Maya_tk window
def getMayaMainWindow():
    """
    Since Maya_tk is Qt, we can parent our UIs to it.
    This means that we don't have to manage our UI and can leave it to Maya_tk.
    Returns:
        QtWidgets.QMainWindow: The Maya_tk MainWindow
    """
    # Use the OpenMayaUI API to get a reference to Maya_tk's MainWindow
    win = omui.MQtUtil_mainWindow()
    # Use the wrapInstance method to convert it to something python can understand (QMainWindow)
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    # Return this to whoever wants it
    return ptr

def getDock(name='Pipeline Tool', label='Pipeline Tool', version = VERSION):
    """
    This function creates a dock with the given name.
    It's an example of how we can mix Maya_tk's UI elements with Qt elements
    Args:
        name: The name of the dock to create
    Returns:
        QtWidget.QWidget: The dock's widget
    """
    # Delete any conflicting docks
    deleteDock( name )
    # Create a workspaceControl dock using Maya_tk's UI tools
    if version>=2017:
        ctrl = cmds.workspaceControl(name,label=label, cl=False, fl=True)
    else:
        ctrl = cmds.dockControl(name, label=label)
    # Use the OpenMayaUI API to get the actual Qt widget associated with the name
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    # Use wrapInstance to convert it to something Python can understand (QWidget)
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
    return ptr

def deleteDock(name='Pipeline Tool', version=VERSION):
    """
    A simple function to delete the given dock
    Args:
        name: the name of the dock
    """
    if version >= 2017:
        if cmds.workspaceControl(name, query=True, exists=True):
            cmds.deleteUI(name)
    else:
        if cmds.dockControl(name, query=True, exists=True):
            cmds.deleteUI(name)

# get button functions data
def importBTS():
    from Maya_tk.modules import MayaFuncs
    reload(MayaFuncs)
    return MayaFuncs

def geticon(icon):
    iconPth = os.path.join(os.getcwd(), 'icons')
    return os.path.join(iconPth, icon)

# ----------------------------------------------------------------------------------------------------------- #
"""                        MAIN CLASS: MAYA MASTER UI - ALL ABOUT CONTROLLER UI                             """
# ----------------------------------------------------------------------------------------------------------- #
class MayaMainUI( QtWidgets.QWidget ):

    icons = ICONS
    curPth = cmds.workspace(q=True, rd=True)
    curPthParts = curPth.split('/')
    curPthList = [f for f in os.listdir(curPth) if os.path.isdir(curPth + f)]
    bts = importBTS()

    def __init__(self, dock=True):

        if dock:
            parent = getDock()
        else:
            deleteDock()
            try:
                cmds.deleteUI('Pipeline Tool')
            except:
                logger.debug('No previous UI exists')

            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName('Pipeline Tool')
            parent.setWindowTitle('Pipeline Tool')
            dialogLayout = QtWidgets.QVBoxLayout(parent)

        super ( MayaMainUI, self ).__init__( parent=parent )

        self.curMode = self.getMode()

        logger.info('get mode: %s' % self.curMode.upper())

        self.buildUI()

        if not dock:
            parent.show()

    def getMode(self):
        if 'work' in self.curPth or 'sequences' in self.curPth:
            self.curMode = 'Studio Mode'
            self.studioModeVar()
        else:
            self.curMode = 'Group Mode'
            self.groupModeVar()

        return self.curMode

    def groupModeVar(self):
        self.prodName = os.path.basename( os.path.normpath( self.curPth ))
        self.prodPth = self.curPth
        self.projPth = self.curPth
        self.assetsPth = self.curPth + 'scenes/assets/'
        self.projPthParts = self.projPth.split('/')

        if not os.path.exists(self.assetsPth):
            cmds.sysFile(self.assetsPth, md=True)

        self.assetsList = [ f for f in os.listdir( self.assetsPth ) if os.path.isdir( self.assetsPth + f ) ]

        if self.assetsList == []:
            # Create demo assets
            assetsSection = ['character', 'environment','props']
            assetsItem = 'assets001'
            task = ['art', 'modeling', 'rigging', 'surfacing']
            for i in assetsSection:
                assetsSectionPth = os.path.join(self.assetsPth, i)
                cmds.sysFile(assetsSectionPth, md=True)
                assetsItemPth = os.path.join(assetsSectionPth, assetsItem)
                cmds.sysFile(assetsItemPth, md=True)
                for i in task:
                    assetsItemTaskPth = os.path.join(assetsItemPth, i)
                    cmds.sysFile(assetsItemTaskPth, md=True)

            self.assetsList = [f for f in os.listdir(self.assetsPth) if os.path.isdir(self.assetsPth + f)]

        self.assetsTaskPth = os.path.join(self.assetsPth, self.assetsList[0])

        self.assetsTaskList = [ f for f in os.listdir( self.assetsTaskPth ) if os.path.isdir(self.assetsTaskPth + f)]
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
        self.stageText = "NA"
        self.stageName = "MA"
        self.curTask = "NA"
        self.curTaskPth = "NA"
        self.reviewPth = os.path.join(self.curPth, 'movies/review')

        self.curStage = self.projPthParts[1]

    def studioModeVar(self):
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
        self.assetsTaskList = [ f for f in os.listdir( self.assetsTaskPth ) if os.path.isdir( self.assetsTaskPth + f ) ]
        self.sequencesList = [ f for f in os.listdir( self.sequencesPth ) if os.path.isdir( self.sequencesPth + f ) ]
        self.sequencesTaskPth = self.sequencesPth + self.sequencesList[0] + '/'
        self.sequencesTaskList = [ f for f in os.listdir( self.sequencesTaskPth ) if
                                   os.path.isdir( self.sequencesTaskPth + f ) ]
        self.curStage = self.projPthParts[1]
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
        # ann1 = ['Open/Load scene','Take a snapshot','Publish file']
        # ic1 = ['openLoad.icon.png','snapshot.icon.png','publish.icon.png']
        # cm1 = [self.bts.loaderUI,self.bts.snapshotUI,self.bts.publishUI]
        # self.bts.setIconButton( ann1, cm1, ic1 )

        anns = ['Hypershader', 'Plugin Manager', 'Outliner','Script Editor', 'Graph Editor', 'UV Editor',
                'Spread Sheet', 'Channel Box', 'Node Editor', 'Vray VFB', 'Render Setting', ]

        commands = ['cmds.HypershadeWindow()', 'cmds.PluginManager()',
                    'mel.eval("OutlinerWindow;")', self.bts.openScriptEditor, 'mel.eval("GraphEditor;")',
                    'mel.eval("TextureViewWindow;")', self.bts.spreadSheetUI, self.bts.channelBoxUI,
                      'cmds.NodeEditorWindow()', self.bts.openVrayVFB, 'cmds.RenderGlobalsWindow()',]

        icons = ['hypershader.icon.png', 'pluinManager.icon.png', 'outliner.icon.png',
                 'scriptEditor.icon.png', 'graphEditor.icon.png', 'uvEditor.icon.png', 'spreadsheet.icon.png',
                 'channelBox.icon.png', 'nodeEditor.icon.png', 'vrayVFB.icon.png', 'renderSetting.icon.png', ]

        w = WIDTH
        w1 = ICONWIDTH
        w2 = w-w1
        #row colummn width for Main UI
        nc2 = 2
        cw2 = [(1,w1),(2,w2)]

        self.layout = QtWidgets.QGridLayout(self)

        cmds.scrollLayout('masterLayout', w=w+16)
        mlo = cmds.rowColumnLayout(nc=nc2, cw=cw2)

        cmds.columnLayout()
        self.bts.iconButton(ann='reloadUI', icon=geticon('Logo.icon.png'), command=self.bts.refreshMainUI)
        self.bts.makeSeparator( h=5, w=ICONWIDTH )
        self.bts.setIconButton(anns, commands, icons)
        self.bts.makeSeparator(h=5, w=ICONWIDTH)

        cmds.setParent(mlo)
        # Menu
        menuBar = cmds.menuBarLayout()
        self.menuSection(menuBar)
        # UI right side sections
        mlor = cmds.columnLayout(w=w2)
        self.tabControls = cmds.tabLayout('mlorTabControls')
        t1 = cmds.columnLayout(w=w2)
        nc=4
        wl1 = [100, 140, 140, 25]
        wl2 = [100, 280, 25]
        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc, wl1))
        cmds.text( l="Prod Name: ", align='center' )
        cmds.textField( 'Prod Name', tx=self.prodName )

        self.setCurModeMenu = cmds.optionMenu('setCurModeMenu', cc=self.bts.waitforupdate, )

        cmds.menuItem(l="Studio Mode", p=self.setCurModeMenu)
        cmds.menuItem(l="Group Mode", p=self.setCurModeMenu)

        self.refreshCheckMode()

        self.bts.refreshBtn(self.refreshCheckMode)
        cmds.setParent('..')

        nc=3
        cmds.rowColumnLayout( nc=nc, cw=self.bts.cwCustomize(nc,wl2))
        cmds.text( l="Production Path", align='center' )
        cmds.textField( 'prodPthTf', tx=self.prodPth )
        self.bts.refreshBtn(self.refreshProdPth)
        cmds.text( l="Project Path", align='center' )
        cmds.textField( 'projPthTf', tx=self.curPth )
        self.bts.refreshBtn(self.refreshProjPth)
        cmds.setParent('..')

        nc=4
        adj = 10
        cmds.rowColumnLayout( nc=4, cw=self.bts.cwE(nc, w2, adj))
        # anns, commands, labels,
        anns = ['Set Project directory', 'Open Project manager UI', 'Create A new production', 'Refresh info']
        commands = [self.setProject, self.bts.projManagerUI, self.bts.newProd, self.refreshInfo]
        labels = ['Set Project', 'Project Manager', 'New Production', 'Refresh Info']
        self.bts.setCoolButton(anns=anns, commands=commands, labels=labels)
        cmds.setParent(t1)

        self.projectContentUI()

        cmds.setParent( t1 )

        cmds.setParent( mlor )
        cmds.separator( style='in', w=w2 )

        mlor_lo1 = cmds.columnLayout( w=w2 )

        self.commonSectionUI()

        cmds.setParent( mlor_lo1 )

        t2 = cmds.columnLayout( parent=self.tabControls, w=w2 )
        modelingTabLayout = self.modelingTab()
        cmds.setParent( self.tabControls )

        t3 = cmds.columnLayout(parent=self.tabControls )
        self.bts.makeAcoolButton("Demo buttons", 'Rigging', self.bts.waitforupdate )
        cmds.setParent( self.tabControls )

        t4 = cmds.columnLayout( parent=self.tabControls )
        sufacingTabLayout = self.surfacingTab()
        cmds.setParent( self.tabControls )

        t5 = cmds.columnLayout(parent=self.tabControls )
        self.bts.makeAcoolButton("Demo buttons",  'Dynamics', self.bts.waitforupdate )
        cmds.setParent( self.tabControls )

        t6 = cmds.columnLayout(parent=self.tabControls )
        animationTabLayout = self.animationTab()
        cmds.setParent( self.tabControls )

        t7 = cmds.columnLayout(parent=self.tabControls )
        self.bts.makeAcoolButton("Demo buttons",  'Light Manager', self.bts.lightManager )
        cmds.setParent( self.tabControls )
        # Create appropriate labels for the ts
        cmds.tabLayout( self.tabControls, edit=True, tabLabel=(
            (t1, "Project"), (t2, "Model"), (t3, "Rig"), (t4, "Surface"), (t5, "FX"), (t6, "Anim"), (t7, "Light")) )

    def animationTab(self):
        animationTabLayout = cmds.columnLayout()

        self.bts.makeAcoolButton("Animation Tweener", 'Tweener', self.bts.tweenerUI)

        cmds.setParent(animationTabLayout)

        return animationTabLayout

    def modelingTab(self):
        modelingTabLayout = cmds.columnLayout()

        self.bts.makeAcoolButton("Create gear sets", 'Create Gear', self.bts.createGear)
        self.bts.makeAcoolButton("Objects Randomizer", 'Randomizer', self.bts.randomizer)

        cmds.setParent(modelingTabLayout)

        return modelingTabLayout

    def surfacingTab(self):
        sufacingTabLayout = cmds.columnLayout()

        self.bts.makeAcoolButton("Vray Material Presets", "Vray Presets", self.bts.vmmApps)

        cmds.setParent(sufacingTabLayout)

        return sufacingTabLayout

    def menuSection(self, parent, *args):
        # file
        cmds.menu( p=parent, label='File', tearOff=True )
        cmds.menuItem( label='New', c='cmds.file(f=True,new=True)' )
        cmds.menuItem( label='Open/Load', c=partial(self.bts.loaderUI, self.curMode))
        cmds.menuItem( label='SnapShot', c=partial(self.bts.snapshotUI, self.curMode))
        cmds.menuItem( label='Publish', c=partial(self.bts.publishUI, self.curMode))
        cmds.menuItem( divider=True )
        cmds.menuItem(label='Reload tool', c=self.bts.reloadDataMainUI)
        cmds.menuItem( divider=True )
        cmds.menuItem( label='Quit', c="cmds.deleteUI('Pipeline Tool')" )

        # about
        cmds.menu( p=parent, label='About', tearOff=True, parent=parent )
        cmds.menuItem( label='About', c=self.bts.aboutThisTool )
        cmds.menuItem( label='Help', c=self.bts.aboutThisTool )

    def projectContentUI(self, *args):
        w = WIDTH - ICONWIDTH
        adj=10
        list1 = [175, 25]
        list2 = [125, 75]

        scrollListH = 150

        # 'scene setup section'
        self.projt1 = cmds.columnLayout( w=w )
        cmds.separator(style='in', w=w)

        nc=2
        projt1_ro1 = cmds.rowColumnLayout( nc=nc, cw=self.bts.cwE(nc=nc, w=w, adj=adj))
        projTabControl = cmds.tabLayout( 'projTabControl', cc=self.refreshProjTab )

        wid = (w-adj)/nc

        projt1_ro1_t1 = cmds.columnLayout( parent=projTabControl, w=(w-adj)/nc)
        cmds.rowColumnLayout( nc=nc, cw=self.bts.cwCustomize(nc=nc, widthList=list1))
        cmds.optionMenu('assetsMenu', l='Assets Type:', cc=self.updateAssetsSections)

        for i in self.assetsList:
            cmds.menuItem( l=i )
        self.bts.refreshBtn(self.bts.waitforupdate)
        cmds.setParent( '..' )

        cmds.rowColumnLayout( nc=nc, cw=self.bts.cwCustomize(nc=nc, widthList=list2))
        assetsTab = cmds.textScrollList('assetsSelectList', ams=False, a=self.assetsTaskList, sc=self.updateSelectionTask, h=scrollListH)

        cmds.popupMenu( parent=assetsTab, ctl=False, button=3 )
        cmds.menuItem( l="Go to", c=self.goToAssetsFolder )

        taskTab = cmds.textScrollList( 'assetsTaskList', ams=False, sc=self.updateAssetsDetailTask, h=scrollListH )
        cmds.popupMenu( parent=taskTab, ctl=False, button=3 )
        cmds.menuItem( l="Set project to", c=self.setProjectToSelectTask )
        cmds.menuItem( l="Go to", c=self.goToAssetsTaskFolder )
        cmds.setParent('..')

        projt1_ro1_t2 = cmds.columnLayout(parent=projTabControl, w=wid)
        cmds.rowColumnLayout( nc=nc, cw=self.bts.cwCustomize(nc=nc, widthList=list1))

        cmds.optionMenu( 'sequencesMenu', l='Shots:', cc=self.updateSequenceSelectTask )
        for i in self.sequencesList:
            cmds.menuItem( l=i )
        self.bts.refreshBtn(self.bts.waitforupdate)
        cmds.setParent( '..' )

        cmds.columnLayout(w=wid)
        shotsTab = cmds.textScrollList('sequencesTaskList', ams=False, a=self.sequencesTaskList, sc=self.updateSequenceDetailTask, h=scrollListH)

        cmds.popupMenu( parent=shotsTab, ctl=False, button=3 )
        cmds.menuItem( l="Set project to" )
        cmds.menuItem( l="Go to" )
        cmds.setParent(projt1_ro1)

        cmds.tabLayout( projTabControl, edit=True, tabLabel=((projt1_ro1_t1, "Assets"), (projt1_ro1_t2, "Shots")))

        cmds.columnLayout('detailsLayout', w=wid)

        detailTabControl = cmds.tabLayout( 'detailTabControl' )

        projt1_lo2_t1 = cmds.columnLayout( parent=detailTabControl, w=(w - adj) / 2 )
        snapShotTab = cmds.textScrollList( 'snapShotList', sc=self.updateViewer, h=scrollListH )
        cmds.popupMenu( parent=snapShotTab, ctl=False, button=3 )
        cmds.menuItem( l="Import" )
        cmds.menuItem( l="Load" )
        cmds.menuItem( l="Open folder" )
        cmds.setParent( '..' )

        projt1_lo2_t2 = cmds.columnLayout( parent=detailTabControl, w=(w-adj)/2 )
        reviewTab = cmds.textScrollList( 'reviewList', sc=self.updateViewer, h=scrollListH )
        cmds.popupMenu( parent=reviewTab, ctl=False, button=3 )
        cmds.menuItem( l="Open folder" )
        cmds.setParent( '..' )

        projt1_lo2_t3 = cmds.columnLayout( parent=detailTabControl, w=(w-adj)/2 )
        publishTab = cmds.textScrollList( 'publishList', sc=self.updateViewer, h=scrollListH )
        cmds.popupMenu( parent=publishTab, ctl=False, button=3 )
        cmds.menuItem( l="Import" )
        cmds.menuItem( l="Create Reference" )
        cmds.menuItem( l="Open folder" )
        cmds.setParent( 'detailsLayout' )

        cm2 = [ self.bts.openPublishFolder, self.bts.openSnapShotFolder, self.bts.openProjFolder,
                self.bts.openSceneFolder, self.bts.openSourceimagesFolder]
        ann2 = ['Go to Publish', 'Go to SnapShot', "Go to Project", 'Go to Scenes', 'Go to SourceImages']
        ic2 = ['openPublishFolder.icon.png', 'openSnapShotFolder.icon.png', 'openProjectFolder.icon.png',
                'openSceneFolder.icon.png', 'openSourceimagesFolder.icon.png']

        cmds.rowColumnLayout(nc=int((wid+5)/30), cw=self.bts.cwE(int((wid+5)/30), wid, 0))
        self.bts.setIconButton(anns=ann2, commands=cm2, icons=ic2)

        cmds.tabLayout( detailTabControl, edit=True,
                        tabLabel=((projt1_lo2_t1, "SnapShot"), (projt1_lo2_t2, "Review"), (projt1_lo2_t3, "Publish")) )
        cmds.setParent( self.projt1 )

        nc = 5
        cmds.rowColumnLayout( nc=nc, cw=self.bts.cwE(nc=nc, w=w, adj=adj))
        cmds.button( l="Open/Load", c=partial(self.bts.loaderUI, self.curMode))
        cmds.button( l="Snap Shot", c=partial(self.bts.snapshotUI, self.curMode))
        cmds.button( l="Review Daily", c=self.bts.waitforupdate)
        cmds.button( l="Publish File", c=partial(self.bts.publishUI, self.curMode))
        cmds.button( l="Info Detail", c=self.infoDetailUI)
        cmds.setParent( self.projt1 )

    def commonSectionUI(self, *args):

        w = WIDTH
        adj = 3

        ann3 = [ 'Tool Box I', 'Tool Box II', 'Tool Box III', 'Tool Box IV', 'Clock and Reminder' ]
        ic3 = ['toolboxI.icon.png', 'toolboxII.icon.png', 'toolboxIII.icon.png', 'toolboxIV.icon.png', 'clock.icon.png']
        cm3 = [self.bts.toolBoxI,self.bts.toolBoxII,self.bts.toolBoxIII,self.bts.toolBoxIV, self.bts.userLib]

        ids = [ 'gcb', 'ccb', 'jcb', 'ncb', 'lcb' ]
        anns = ['Mesh', 'Camera', 'Joint', 'Curves', 'Light']
        types = ['surfaceShape', 'camera', 'joint', 'nurbsCurve', 'light']
        icons = ['obj.icon.png', 'cam.icon.png', 'joint.icon.png', 'curve.icon.png', 'light.icon.png']
        ccs = [self.bts.setDisplay, self.bts.setDisplay, self.bts.setDisplay, self.bts.setDisplay, self.bts.setDisplay,]

        nc=2
        commonBtns = cmds.rowColumnLayout('commonSection2', nc=nc, cw=self.bts.cwE(nc=nc, w=w, adj=adj))

        ann1 = ["Freeze Transformation", "Delete History", "Center Pivot", 'Create transform node in center pivot of current selected']
        label1 = ["FreeTrans", "Del His", "Cen.Pivot", "Grp.Center"]
        command1 = [self.bts.freezeTransformation, self.bts.deleteHis, self.bts.centerPivot, self.bts.groupCenter ]

        ann2 = ['reverse Normal', 'Display normal surface', "Select all children in hierarchy selection", "Create one vray displacement node", "Create multiple vray displacement node"]
        label2 =['Rev.Normal', 'Dis.Normal', "Sel.Children", "Vray Disp", "Mul.Disp"]
        command2 = [self.bts.reverseNormal, self.bts.normalOnOff, 'cmds.select(hi=True)', self.bts.createSingleDispNode, self.bts.createMultiDispNode]

        ann4 = ["Join selected into one Shape node", "Create joints base on selection", "Create locators base on selection", "Create cluster base on selection"]
        label4 = ["Join Shape", "Joint", "Locator", "Cluster"]
        command4 = ['cmds.parent(r=True, s=True)' , self.bts.createJointFromSelections, self.bts.createLocatorFromSelection , self.bts.createClusterFromSelection]

        cmds.setParent('masterLayout')
        commonSection1 = cmds.columnLayout('commonSection1', w=w)
        nc=3

        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwE(nc,w,adj))

        columnStyle1 = self.bts.styleColumn121(ann1, label1, command1, adj/nc, w/nc)

        columnStyle2 = self.bts.styleColumn212(ann2, label2, command2, adj/nc, w/nc)

        columnStyle3 = self.bts.styleColumn121(ann4, label4, command4, adj/nc, w/nc)

        cmds.setParent(commonSection1)
        self.bts.makeSeparator(2,w)
        nc = (w-2*adj)/30
        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwE(nc=nc, w=w, adj=adj))
        self.bts.setSymbolCheckable( ids=ids, anns=anns, ccs=ccs, types=types, icons=icons )
        cmds.separator(style='in', hr=False, h=30)
        self.bts.setIconButton(ann3,cm3, ic3)
        cmds.setParent( '..' )
        self.bts.makeSeparator(2,w)

        nc=2
        wid = w/2
        commonsection3 = cmds.rowColumnLayout('commonsection3', nc=nc, cw=self.bts.cwE(nc, w, 0))

        commonLeftRC = cmds.columnLayout( 'commonLeftRC' )
        commonLeftTabLayout = cmds.tabLayout( 'commonRightTabLayout', p=commonLeftRC )

        mayaWindowTab = cmds.columnLayout(w=wid )
        self.bts.makeSeparator( h=5, w=wid )

        # Panels tab
        adj = 5
        wid = (WIDTH/2)-adj
        mess ="MAKE SELECTED CAMERA \n ONLY PANEL VISIBLE"
        resolution = ['HD 540', 'HD 720', 'HD 1080']

        cmds.columnLayout(adj=True)

        cmds.optionMenu('camListPanel', l='Camera')
        for cam in cmds.ls(type='camera'):
            cmds.menuItem(l=cam)

        cmds.optionMenu('resViewPanel', l='Resolution')
        for cam in resolution:
            cmds.menuItem(l=cam)

        nc=2
        cmds.rowColumnLayout( nc=nc, cw=self.bts.cwE(nc=nc,w=wid,adj=adj))
        cmds.text(l="Quality" )
        cmds.intField( "QualityField", value=100, minValue=0, maxValue=100 )
        cmds.text(l=" Ornament", align='center')
        cmds.checkBox('OrnamentsCheck', l=' ', align='right')
        cmds.setParent('..')

        cmds.columnLayout(w=wid, adj=True)
        self.bts.makeSeparator(2, wid)
        cmds.text(l=mess, bgc=[0,.5,1], font="boldLabelFont" )
        self.bts.makeSeparator(2, wid)
        cmds.textField('FilePathGoesHere', text=self.reviewPth )
        cmds.textField('FileNameGoesHere', text=self.curStage + '_' + self.curTask + '_playblast')

        nc=2
        cmds.rowColumnLayout( nc=nc, cw=self.bts.cwE(nc=nc,w=wid,adj=adj))
        self.bts.makeAcoolButton('Refresh Camera List', 'Refresh', partial(self.bts.refreshCamList, 'camListPanel'))
        self.bts.makeAcoolButton('Create Viewer', 'Create Viewer', self.bts.customViewer)
        self.bts.makeAcoolButton('Change Name and Location' ,"Edit", self.bts.NameTheFileForLater )  # button find directory and file name
        self.bts.makeAcoolButton('Playblast' ,'Playblast', self.bts.TimeToPlayBlast )  # button to playblast

        cmds.setParent( commonLeftTabLayout )

        commonMidTab  = cmds.columnLayout( w=wid )

        cmds.setParent( commonLeftTabLayout )

        commonRightTab = cmds.columnLayout( w=wid )
        self.bts.makeAcoolButton( 'import camera template', 'Camera', self.bts.importCamTemp)

        cmds.tabLayout( commonLeftTabLayout, edit=True, tabLabel=((mayaWindowTab, 'Panels'), (commonMidTab, 'P.Blast'), (commonRightTab, 'Template')) )

        cmds.setParent(commonsection3)

        w=WIDTH/2
        nc = 2

        cmds.columnLayout()
        self.bts.makeSeparator(h=5, w=w)
        cmds.text(l="FINNALIZING SCENE", w=w, align='center')
        self.bts.makeSeparator(h=5, w=w)

        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwE(nc, w, adj))
        self.bts.makeAcoolButton('Delete unuse nodes', 'Clean Node', self.bts.deleteUnusedNode)
        self.bts.makeAcoolButton('Set texture to relative path', 'Fix Tex paths', self.bts.fixTexturePathUI)


        cmds.setParent( 'masterLayout' )

    def infoDetailUI(self, *args):
        h = 240
        w = 320
        self.winID = 'Info Detail'
        self.title = 'Info File'

        if cmds.window(self.winID, query=True, exists=True):
            cmds.deleteUI(self.winID)

        self.winID = cmds.window('Info Detail', t=self.title, h=h, w=w)
        self.detailUI = cmds.columnLayout('detailUI', adj=True)

        cmds.text(l="")
        cmds.separator(style='in', w=w)
        cmds.separator(style='in', w=w)
        cmds.text(l="")

        self.viewText = cmds.text( 'textViewerMainUI', l="No image", align='center', w=w, h=h)
        self.viewImage = cmds.image('imageViewerMainUI', vis=False, w=w, h=h)

        cmds.text( l="" )
        cmds.separator(style='in', w=w)
        cmds.separator(style='in', w=w)
        cmds.text( l='' )

        cmds.text( 'name', l="", align='left')
        cmds.text( 'time', l="", align='left' )
        cmds.text( 'size', l="", align='left' )
        cmds.text( 'commentMainUI', l="", align='left')

        cmds.separator( style='in', w=w )
        cmds.separator( style='in', w=w )

        cmds.showWindow(self.winID)

    # functions of buttons

    def refreshInfo(self, *args):
        self.refreshCheckMode()
        self.refreshProdPth()
        self.refreshProdPth()

    def goToAssetsFolder(self, *args):
        self.getMode()
        item1 = cmds.optionMenu( 'assetsMenu', q=True, value=True)
        item2 = cmds.textScrollList( 'assetsSelectList', q=True, si=True )
        updatePth = os.path.join(os.path.join(self.assetsPth, item1), item2[0])
        if not os.path.exists(updatePth):
            message = "you dont have any assets..."

        os.startfile(updatePth)

    def goToAssetsTaskFolder(self, *args):
        self.getMode()
        item1 = cmds.optionMenu( 'assetsMenu', q=True, value=True )
        item2 = cmds.textScrollList( 'assetsSelectList', q=True, si=True )
        item3 = cmds.textScrollList('assetsTaskList', q=True, si=True)
        updatePth = self.assetsPth + item1 + "/" + item2[ 0 ] + "/" + item3[0]
        os.startfile(updatePth)

    def setProjectToSelectTask(self, *args):
        self.getMode()
        item1 = cmds.optionMenu('assetsMenu', q=True, value=True )
        item2 = cmds.textScrollList('assetsSelectList', q=True, si=True )
        item3 = cmds.textScrollList('assetsTaskList', q=True, si=True)
        updatePth = self.assetsPth + item1 + "/" + item2[ 0 ] + "/" + item3[0] + "/work/maya"
        mel.eval( 'setProject \"' + updatePth + '\"' )
        self.updateWhenChangeProPth()

    def clearDataList(self, *args):
        cmds.textScrollList('snapShotList', e=True, ra=True )
        cmds.textScrollList('reviewList', e=True, ra=True )
        cmds.textScrollList('publishList', e=True, ra=True )

    def refreshProjTab(self, *args):
        if cmds.tabLayout( 'projTabControl', q=True, sti=True ) == 1:
            menuSelect = cmds.optionMenu( 'assetsMenu', q=True, value=True )
            itemSelect1 = cmds.textScrollList( 'assetsSelectList', q=True, si=True )
            itemSelect2 = cmds.textScrollList( 'assetsTaskList', q=True, si=True )
            if isinstance( itemSelect1, list ) or isinstance( itemSelect2, list ) is False:
                cmds.textScrollList('snapShotList', e=True, ra=True )
                cmds.textScrollList('reviewList', e=True, ra=True )
                cmds.textScrollList('publishList', e=True, ra=True )
            else:
                self.updateAssetsDetailTask()

    def updateAssetsSections(self, *args):
        self.getMode()
        menuSelect = cmds.optionMenu( 'assetsMenu', q=True, value=True )
        updatePth = self.assetsPth + menuSelect + '/'
        updateList = [ f for f in os.listdir( updatePth ) if os.path.isdir( updatePth + f ) ]
        cmds.textScrollList( 'assetsSelectList', e=True, ra=True )
        cmds.textScrollList( 'assetsSelectList', e=True, a=updateList )
        self.clearDataList()

    def updateSelectionTask(self, *args):
        self.getMode()
        itemSelect1 = cmds.textScrollList( 'assetsSelectList', q=True, si=True )
        menuSelect = cmds.optionMenu( 'assetsMenu', q=True, value=True )
        updatePth = os.path.join(os.path.join(self.assetsPth, menuSelect), itemSelect1[0])
        updateList = [ f for f in os.listdir( updatePth ) if os.path.isdir(os.path.join(updatePth, f))]
        cmds.textScrollList( 'assetsTaskList', e=True, ra=True )
        cmds.textScrollList( 'assetsTaskList', e=True, a=updateList )
        self.clearDataList()

    def updateAssetsDetailTask(self, *args):
        self.getMode()
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

        baseFolder = 'work/maya/scenes/snapShot'
        if self.curMode == 'Studio Mode':
            updateSnapShotPth = os.path.join(updatePth, baseFolder)
        elif self.curMode == 'Group Mode':
            updateSnapShotPth = os.path.join(updatePth, baseFolder)
        else:
            updateSnapShotPth = os.path.join(updatePth, baseFolder)

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

        if cmds.window('imageViewerMainUI', q=True, exists=True):
            cmds.image('imageViewerMainUI', e=True, vis=False)
            cmds.text('textViewerMainUI', e=True, vis=True)

    def updateSequenceSelectTask(self, *args):
        self.getMode()
        menuSelect = cmds.optionMenu( 'sequencesMenu', q=True, value=True )
        updatePth = self.sequencesPth + menuSelect + '/'
        updateList = [ f for f in os.listdir( updatePth ) if os.path.isdir( updatePth + f ) ]
        cmds.textScrollList( 'sequencesTaskList', e=True, ra=True )
        cmds.textScrollList( 'sequencesTaskList', e=True, a=updateList )
        self.clearDataList()

    def updateSequenceDetailTask(self, *args):
        self.getMode()
        menuSelect = cmds.optionMenu( 'sequencesMenu', q=True, value=True )
        itemSelect = cmds.textScrollList( 'sequencesTaskList', q=True, si=True )
        updatePth = self.sequencesPth + menuSelect + '/' + itemSelect[ 0 ] + '/'
        updatePublishPth = updatePth + 'publish/maya/'
        if not os.path.exists( updatePublishPth ):
            cmds.sysFile( updatePublishPth, md=True )
        updateReviewPth = updatePth + 'review/'

        if not os.path.exists( updateReviewPth ):
            cmds.sysFile( updateReviewPth, md=True )

        baseFolder = 'work/maya/scenes/snapShot'

        if self.curMode == 'Studio Mode':
            updateSnapShotPth = os.path.join(updatePth, baseFolder)
        elif self.curMode == 'Group Mode':
            updateSnapShotPth = os.path.join(updatePth, baseFolder)
        else:
            updateSnapShotPth = os.path.join(updatePth, baseFolder)

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

        if cmds.image('imageViewerMainUI', query=True, exists=True):
            cmds.image('imageViewerMainUI', e=True, vis=False)
            cmds.text('textViewerMainUI', e=True, vis=True)

    def updateViewer(self, *args):

        if not cmds.image( 'imageViewerMainUI', query=True, exists=True):
            sys.exit()
        else:
            self.getMode()
            if cmds.tabLayout( 'projTabControl', q=True, sti=True ) == 1:
                menuSelect = cmds.optionMenu( 'assetsMenu', q=True, value=True ) or [ ]
                itemSelect1 = cmds.textScrollList( 'assetsSelectList', q=True, si=True ) or [ ]
                itemSelect2 = cmds.textScrollList( 'assetsTaskList', q=True, si=True ) or [ ]
                self.updatePth = self.assetsPth + menuSelect + '/' + itemSelect1[ 0 ] + '/' + itemSelect2[ 0 ] + '/'
            elif cmds.tabLayout( 'projTabControl', q=True, sti=True ) == 2:
                menuSelect = cmds.optionMenu('sequencesMenu', q=True, value=True) or []
                itemSelect = cmds.textScrollList('sequencesTaskList', q=True, si=True) or []
                self.updatePth = self.sequencesPth + menuSelect + '/' + itemSelect[0] + '/'

            if cmds.tabLayout( 'detailTabControl', q=True, sti=True ) == 1:
                snapShotItem = cmds.textScrollList( 'snapShotList', q=True, si=True) or []
                if snapShotItem == [ ]:
                    cmds.image('imageViewerMainUI', e=True, vis=False)
                    cmds.text('textViewerMainUI', e=True, vis=True)
                else:
                    if self.curMode == 'Studio Mode':
                        updateImagePth = self.updatePth + 'work/maya/scenes/snapShot/' + snapShotItem[ 0 ] + '.jpg'
                        self.updateCommentPth = self.updatePth + 'work/maya/scenes/snapShot/' + snapShotItem[ 0 ] + '.comment'
                    elif self.curMode == 'Group Mode':
                        updateImagePth = self.updatePth + 'work/maya/snapShot/' + snapShotItem[ 0 ] + '.jpg'
                        self.updateCommentPth = self.updatePth + 'work/maya/snapShot/' + snapShotItem[ 0 ] + '.comment'
                    else:
                        updateImagePth = self.updatePth + 'work/maya/snapShot/' + snapShotItem[ 0 ] + '.jpg'
                        self.updateCommentPth = self.updatePth + 'work/maya/snapShot/' + snapShotItem[ 0 ] + '.comment'

                    updateSnapShotPth = updateImagePth.split('.jpg')[0] + '.png'
                    image = om.MImage()
                    image.readFromFile(updateImagePth)
                    image.resize(205,115)
                    image.writeToFile(updateSnapShotPth, 'png')
                    self.updateInfoFile(filePth=updateSnapShotPth.split('.png')[0] + '.ma')

                    if not os.path.exists( updateImagePth ):
                        cmds.image('imageViewerMainUI', e=True, vis=False)
                        cmds.text('textViewerMainUI', e=True, vis=True)
                        cmds.text('commentMainUI', e=True, l="No comment")
                    else:
                        cmds.image('imageViewerMainUI', e=True, i=updateSnapShotPth, vis=True)
                        cmds.text('textViewerMainUI', e=True, vis=False)
                        self.updateCommentMainUI()

            elif cmds.tabLayout( 'detailTabControl', q=True, sti=True) == 2:
                reviewItem = cmds.textScrollList( 'reviewList', q=True, si=True) or []
                if reviewItem == []:
                    cmds.image('imageViewerMainUI', e=True, vis=False)
                    cmds.text('textViewerMainUI', e=True, vis=True )
                    cmds.text('commentMainUI', e=True, l="No comment")
                else:
                    updateReviewPth = self.updatePth + 'review/' + reviewItem[0]
                    if not os.path.exists( updateReviewPth ):
                        cmds.image('imageViewerMainUI', e=True, vis=False)
                        cmds.text('textViewerMainUI', e=True, vis=True )
                        cmds.text('commentMainUI', e=True, l="No comment")
                    else:
                        cmds.image('imageViewerMainUI', e=True, i=updateReviewPth, vis=True)
                        cmds.text('textViewerMainUI', e=True, vis=False)
                        self.updateCommentMainUI()
            elif cmds.tabLayout('detailTabControl', q=True, sti=True) == 3:
                publishItem = cmds.textScrollList( 'publishList', q=True, si=True) or []
                if publishItem == [ ]:
                    cmds.image('imageViewerMainUI', e=True, vis=False)
                    cmds.text('textViewerMainUI', e=True, vis=True)
                    cmds.text('commentMainUI', e=True, l="No comment")
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

    def updateInfoFile(self, filePth=None, *args):
        if os.path.exists(filePth):
            name = os.path.basename(filePth)
            size = self.bts.format_bytes(bytes_num = os.path.getsize(filePth))
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
        self.getMode()
        cmds.optionMenu( self.setCurModeMenu, e=True, v=self.curMode )
        print "Production: %s is designed for %s" % (self.prodName.upper(), self.curMode)

    def setProject(self, *args):
        mel.eval( "setProjectFromFileDialog;" )
        self.updateWhenChangeProPth()

    def updateWhenChangeProPth(self, *args):
        self.getMode()
        self.refreshCheckMode()
        cmds.textField( 'prodPthTf', e=True, tx=self.prodPth )
        cmds.textField( 'projPthTf', e=True, tx=self.curPth )

    def refreshProdPth(self, *args):
        self.getMode()
        cmds.textField( 'prodPthTf', e=True, tx=self.prodPth )

    def refreshProjPth(self, *args):
        self.getMode()
        cmds.textField( 'projPthTf', e=True, tx=self.curPth )

if __name__=="__main__":
    MayaMainUI()

#End of Main UI