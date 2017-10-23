from maya import cmds
import pymel.core as pm
import maya, os, json, pprint, logging, time
from functools import partial
from maya.app.renderSetup.views.renderSetupButton import *
from maya import OpenMayaUI as omui
import maya.app.renderSetup.views.lightEditor.lightTypeManager as typeMgr
import maya.app.renderSetup.views.utils as viewsUtils
import  mtoa.utils as mutils

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
from Maya_tk.modules import MayaVariables as var
from Maya_tk.modules import toolBoxIIfuncs

NAMES = var.MAINVAR
SCRPTH = var.SCRPTH
VERSION = var.MAYAVERSION
DIRECTORY = os.path.join(cmds.internalVar(usd=True), 'userLibrary')
logging.basicConfig()
logger = logging.getLogger('toolBoxIII')
logger.setLevel(logging.DEBUG)

from Maya_tk.plugins import Qt
from Maya_tk.plugins.Qt import QtWidgets, QtCore, QtGui

if Qt.__binding__.startswith('PyQt'):
    logger.debug('Using sip')
    from sip import wrapinstance as wrapInstance
    from Maya_tk.plugins.Qt.QtCore import pyqtSignal as Signal
elif Qt.__binding__ == 'PySide':
    from shiboken import wrapInstance
    from Maya_tk.plugins.Qt.QtCore import Signal
else:
    logger.debug('Using shiboken2')
    from shiboken2 import wrapInstance
    from Maya_tk.plugins.Qt.QtCore import Signal

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

def getDock(name='DAMGtoolBoxIIIDock'):
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
    ctrl = cmds.workspaceControl(name, label='DAMG Tool Box III - All About Lighting')

    # Use the OpenMayaUI API to get the actual Qt widget associated with the name
    qtCtrl = omui.MQtUtil_findControl(ctrl)

    # Use wrapInstance to convert it to something Python can understand (QWidget)
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
    return ptr

def deleteDock(name='DAMGtoolBoxIIIdock'):
    """
    A simple function to delete the given dock
    Args:
        name: the name of the dock
    """
    if cmds.workspaceControl(name, query=True, exists=True):
        cmds.deleteUI(name)


from Maya_tk.plugins.Qt.QtWidgets import *
from Maya_tk.plugins.Qt.QtGui import *
from Maya_tk.plugins.Qt.QtCore import *

class LightManager( QtWidgets.QWidget ):

    onSolo = QtCore.Signal(bool)

    def __init__(self, light):
        super( LightManager, self ).__init__()
        if isinstance(light, basestring):
            light = pm.PyNode(light)

        self.light = light
        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)

        self.name = QtWidgets.QCheckBox()
        self.name.setChecked(self.light.visibility.get())
        self.name.toggled.connect(lambda val: self.light.getTransform().visibility.set(val))

        def setLightVisibility(val):
            self.light.visibility.set(val)

        layout.addWidget(self.name, 0, 0)
        self.setName = QtWidgets.QLabel(str(self.light.getTransform()))
        self.setName.setMinimumWidth(120)
        layout.addWidget(self.setName, 0, 1)

        soloBtn = QtWidgets.QPushButton('Solo')
        soloBtn.setCheckable(True)
        soloBtn.toggled.connect(lambda val: self.onSolo.emit(val))
        soloBtn.setMinimumWidth(80)
        layout.addWidget(soloBtn, 0, 2)

        deleteBtn = QtWidgets.QPushButton('Delete')
        deleteBtn.clicked.connect(self.deleteLight)
        deleteBtn.setMinimumWidth(80)
        layout.addWidget(deleteBtn, 0, 3)

        intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        intensity.setMinimum(0)
        intensity.setMaximum(1000)
        intensity.setMinimumWidth(160)
        intensity.setValue(self.light.intensity.get())
        intensity.valueChanged.connect(lambda val: self.light.intensity.set(val))
        layout.addWidget(intensity, 0, 4, 1, 1)

        self.colorBtn = QtWidgets.QPushButton()
        self.colorBtn.setMinimumWidth(80)
        self.colorBtn.clicked.connect(self.setColor)
        layout.addWidget(self.colorBtn, 0, 5)

    def setButtonColor(self, color=None):
        if not color:
            color = self.light.color.get()

        assert len(color) == 3, "You must provide a list of 3 colors"

        r,g,b = [c*255 for c in color]

        self.colorBtn.setStyleSheet('background-color: rgba(%s, %s, %s, 1.0)' % (r,g,b))

    def setColor(self):
        lightColor = self.light.color.get()
        color = pm.colorEditor(rgbValue=lightColor)

        r,g,b,a = [float(c) for c in color.split()]
        color = (r,g,b)

        self.light.color.set(color)
        self.setButtonColor(color)

    def disableLight(self, value):
        self.name.setChecked(not value)

    def deleteLight(self):
        self.setParent(None)
        self.setVisible(False)
        self.deleteLater()

        pm.delete(self.light.getTransform())

class LightLibrary(dict):

    def createDirectory(selfself, directory=DIRECTORY):
        if not os.path.exists( directory ):
            os.mkdir( directory )

    def save(self, name, screenshot=True, directory=DIRECTORY, **info):

        self.createDirectory( directory )

        path = os.path.join( directory, '%s.ma' % name )
        infoFile = os.path.join( directory, '%s.json' % name )

        info[ 'name' ] = name
        info[ 'path' ] = path

        cmds.file( rename=path )

        if cmds.ls( sl=True ):
            cmds.file( force=True, type='mayaAscii', exportSelected=True )
        else:
            cmds.file( save=True, type='mayaAscii', force=True )

        if screenshot:
            info[ 'screenshot' ] = self.saveScreenshot( name, directory=directory )

        with open( infoFile, 'w' ) as f:
            json.dump( info, f, indent=4 )

        self[ name ] = info

    def remove(self, name, directory=DIRECTORY):
        mayapath = os.path.join(directory, '%s.ma' % name)
        jsonpath = os.path.join(directory, '%s.json' % name)
        imagepath = os.path.join(directory, '%s.jpg' % name)

        items = [mayapath, jsonpath, imagepath]

        for item in items:
            cmds.sysFile(item, delete=True)

    def reference(self, name, directory=DIRECTORY):
        mayapath = os.path.join(directory, '%s.ma' % name)
        cmds.file(mayapath, reference=True, usingNamespaces=False)

    def find(self, directory=DIRECTORY):
        self.clear()

        if not os.path.exists( directory ):
            return

        files = os.listdir( directory )
        mayafiles = [ f for f in files if f.endswith( '.ma' ) ]

        for ma in mayafiles:
            name, ext = os.path.splitext( ma )
            path = os.path.join( directory, ma )

            infoFile = '%s.json' % name
            if infoFile in files:
                infoFile = os.path.join( directory, infoFile )

                with open( infoFile, 'r' ) as f:
                    info = json.load( f )
            else:
                info = {}

            screenshot = '%s.jpg' % name
            if screenshot in files:
                info[ 'screenshot' ] = os.path.join( directory, name )

            info[ 'name' ] = name
            info[ 'path' ] = path

            self[ name ] = info

    def load(self, name):
        path = self[ name ][ 'path' ]
        cmds.file( path, i=True, usingNamespaces=False )

    def saveScreenshot(self, name, directory=DIRECTORY):
        cmds.viewFit()
        path = os.path.join( directory, '%s.jpg' % name )
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)
        cf = cmds.currentTime(q=True)
        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200,
                       showOrnaments=False, startTime=cf, endTime=cf, viewer=False)
        return path

class toolBoxIII( QtWidgets.QWidget ):

    mayaLightTypes = {

        "pointLight": cmds.pointLight,
        "ambientLight": cmds.ambientLight,
        "spotLight": cmds.spotLight,
        "directionalLight": cmds.directionalLight,
        "areaLight": partial( cmds.shadingNode, 'areaLight', al=True ),
        "volumeLight": partial( cmds.shadingNode, 'volumeLight', al=True )
    }

    vrayLightTypes = {

        "VRayLightRectShape": partial( cmds.shadingNode, 'VRayLightRectShape', al=True ),
        "VRayLightDomeShape": partial( cmds.shadingNode, 'VRayLightDomeShape', al=True ),
        "VRayLightSphereShape": partial( cmds.shadingNode, 'VRayLightSphereShape', al=True ),
        "VRayLightIESShape": partial( cmds.shadingNode, 'VRayLightIESShape', al=True ),
        "VRayLightMesh": partial(cmds.shadingNode, 'VRayLightMeshShape', al=True),
        "VRayLightMeshLightLinking": partial(cmds.shadingNode, 'VRayLightMeshLightLinkingShape', al=True),
        "VRayPluginNodeLightShapeShape": partial(cmds.shadingNode, 'VRayPluginNodeLightShapeShape', al=True),
        "VRaySunShape": partial(cmds.shadingNode, 'VRayGeoSun', al=True)

    }

    renderManLightTypes = {

        "PxrAovLight": partial(cmds.shadingNode, 'PxrAovLight', al=True),
        "PxrDiskLight": partial(cmds.shadingNode, 'PxrDiskLight', al=True),
        "PxrDistantLight": partial(cmds.shadingNode, 'PxrDistantLight', al=True),
        "PxrDomeLight": partial(cmds.shadingNode, 'PxrDomeLight', al=True),
        "PxrEnvDayLight": partial(cmds.shadingNode, 'PxrEnvDayLight', al=True),
        "PxrMeshLight": partial(cmds.shadingNode, 'PxrMeshLight', al=True),
        "PxrPortalLight": partial(cmds.shadingNode, 'PxrPortalLight', al=True),
        "PxrRectLight": partial(cmds.shadingNode, 'PxrRectLight', al=True),
        "PxrSphereLight": partial(cmds.shadingNode, 'PxrSphereLight', al=True)

    }

    arnoldLightTypes = {

        "aiAreaLight": partial(cmds.shadingNode, 'aiAreaLight', al=True),
        "aiMeshLight": mutils.createMeshLight,
        "aiPhotometricLight": partial(cmds.shadingNode, 'aiPhotometricLight', al=True),
        "aiSkyDomeLight": partial(cmds.shadingNode, 'aiSkyDomeLight', al=True)

    }

    BUTTON_SIZE = viewsUtils.dpiScale( 20 )

    def __init__(self, dock=True):
        if dock:
            parent = getDock()
        else:
            deleteDock()

            try:
                cmds.deleteUI('LightingManager')
            except:
                logger.debug('No previous UI exists')

            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName('LightingManager')
            parent.setWindowTitle('Lighting Manager')

            dlgLayout = QtWidgets.QVBoxLayout(parent)

        super( toolBoxIII, self ).__init__( parent=parent )

        self.setWindowTitle('Lighting Manager')

        self.buildUI()

        self.populate()

        self.parent().layout().addWidget(self)

        if not dock:
            parent.show()

        self.userAppDir = cmds.internalVar( userAppDir=True )
        self.userLibaryDir = self.userAppDir + 'userLibrary'
        if not os.path.exists( self.userLibaryDir ):
            os.mkdir( self.userLibaryDir )

    def buildUI(self):
        self.layout = QtWidgets.QGridLayout(self)
        pluginLights = typeMgr.pluginLights()
        self.mayaLights = sorted(typeMgr.mayaLights())
        self.vrayLights = sorted([f for f in pluginLights if f.startswith("VRay")])
        self.renderManLights = sorted([f for f in pluginLights if f.startswith("Pxr")])
        self.arnoldLights = sorted([f for f in pluginLights if f.startswith("ai")])

        iconBtnWidget = QtWidgets.QWidget()
        self.iconBtnLayout = QtWidgets.QHBoxLayout(iconBtnWidget)
        self.layout.addWidget(iconBtnWidget, 0,0)
        self.iconBtnLayout.addWidget( QtWidgets.QLabel( "Maya_tk: " ) )

        # self.mayaLightTB = QtWidgets.QToolBar('Maya_tk Light')
        self.getMayaLight()

        self.getVrayLight()

        self.getRenderManLight()

        #self.getArnoldLight()

        self.lightLibraryUI()

        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        self.layout.addWidget(scrollArea, 1,0,1,5)

    def lightLibraryUI(self):
        libraryLabel = QtWidgets.QLabel( '')
        libraryLabel.setAlignment( QtCore.Qt.AlignCenter )
        self.layout.addWidget( libraryLabel, 0,0,1,4)

        libHeaderWidget = QtWidgets.QWidget()
        libHeaderLayout = QtWidgets.QHBoxLayout(libHeaderWidget)

        libHeaderScrollArea = QtWidgets.QScrollArea()
        libHeaderScrollArea.setWidget( libHeaderWidget )
        libHeaderScrollArea.setWidgetResizable( True )
        libHeaderScrollArea.setMaximumHeight(45)

        self.layout.addWidget( libHeaderScrollArea, 2,0,1,5)
        self.saveNameField = QtWidgets.QLineEdit()
        self.saveNameField.setMinimumWidth( 60)
        libHeaderLayout.addWidget( self.saveNameField )

        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.setMinimumWidth(120)
        saveBtn.clicked.connect( self.saveItem )
        libHeaderLayout.addWidget( saveBtn )

        buf = 12
        self.listLibWidget = QtWidgets.QListWidget()
        self.listLibWidget.setViewMode( QtWidgets.QListWidget.IconMode )
        self.listLibWidget.setIconSize( QtCore.QSize(60,60) )
        self.listLibWidget.setResizeMode( QtWidgets.QListWidget.Adjust )
        self.listLibWidget.setGridSize( QtCore.QSize( 60+ buf,60 + buf ) )
        self.layout.addWidget( self.listLibWidget, 3, 0, 1, 5)

        libFooterWidget = QtWidgets.QWidget()
        # libFooterWidget.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum )
        self.libFooterLayout = QtWidgets.QGridLayout( libFooterWidget )
        self.libFooterLayout.setContentsMargins( QtCore.QMargins( 2, 2, 2, 2 ) )

        # Create QScrollArea
        scrollLibArea = QtWidgets.QScrollArea()
        scrollLibArea.setWidget( libFooterWidget )
        scrollLibArea.setWidgetResizable( True )
        scrollLibArea.setMaximumHeight( 45 )
        self.layout.addWidget( scrollLibArea, 4,0,1,5 )

        # Create QPlushButton
        importLibBtn = QtWidgets.QPushButton( 'Import')
        importLibBtn.setMinimumWidth(120 )
        importLibBtn.clicked.connect( self.loadItem )
        self.libFooterLayout.addWidget( importLibBtn, 0, 0 )

        # # Create QPlushButton
        referenceBtn = QtWidgets.QPushButton('Reference' )
        referenceBtn.setMinimumWidth( 120 )
        referenceBtn.clicked.connect( self.referenceItem )
        self.libFooterLayout.addWidget( referenceBtn, 0, 1 )
        #
        # Create QPlushButton
        removeBtn = QtWidgets.QPushButton( 'Remove' )
        removeBtn.setMinimumWidth( 120 )
        removeBtn.clicked.connect( self.removeItem )
        self.libFooterLayout.addWidget( removeBtn, 0, 2 )

    def populateAll(self):
        self.populateLibrarySection()
        self.populateManagerSection()

    def saveItem(self):
        name = self.saveNameField.text()
        if not name.strip():
            cmds.warning("You must give a name")
            cmds.confirmDialog(t='Warning', m='You must give a name', b='OK')
            return

        files = [f for f in os.listdir(DIRECTORY)]

        for file in files:
            if name in file:
                cmds.confirmDialog( t='Confirm', m='File %s already exists, override?' % name,
                                    b=[ 'Yes', 'No' ], db='Yes', cb='No', dismissString='No' )

        self.library.save(name)
        self.saveNameField.setText('')
        self.populateAll()

    def removeItem(self):
        currentItem = self.listLibWidget.currentItem()
        if not currentItem:
            self.warningFunction( 'You must select something' )
            return
        self.library.remove(currentItem)
        self.populateAll()

    def loadItem(self):
        currentItem = self.listLibWidget.currentItem()
        if not currentItem:
            self.warningFunction( 'You must select an item' )

        name = currentItem.text()
        self.library.load(name)
        self.populateAll()

    def referenceItem(self):
        name = self.listLibWidget.currentItem().text() or ""
        if name=="":
            self.warningFunction( 'You must select something' )
            return

        self.library.reference(name)
        self.populateAll()

    def populateLibrarySection(self):
        self.listLibWidget.clear()
        self.library.find()

        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listLibWidget.addItem(item)

            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

    def getMayaLight(self):
        for lightType in self.mayaLights:
            icon = QIcon( typeMgr.getIcon( lightType ) )
            cmd = partial( self.createNewLight, lightType )
            toolTip = 'Create a new ' + lightType
            # mayaLightAction = self.createAction( lightType, icon, cmd, toolTip)
            # self.mayaLightTB.addAction(mayaLightAction)
            button = self.iconButton( cmd, icon, toolTip )
            self.iconBtnLayout.addWidget( button )
        # self.iconBtnLayout.addWidget(self.mayaLights)

    def getVrayLight(self):
        self.vrayLightTB = QtWidgets.QToolBar( 'Vray Light' )
        if len( self.vrayLights ) > 0:
            self.iconBtnLayout.addWidget( QtWidgets.QLabel( "|" ) )
            self.iconBtnLayout.addWidget( QtWidgets.QLabel( "Vray: " ) )
            for lightType in self.vrayLights:
                icon = QIcon( typeMgr.getIcon( lightType ) )
                cmd = partial( self.createNewLight, lightType )
                toolTip = 'Create a new ' + lightType
                # vrayLightAction = self.createAction( lightType,  icon, cmd, toolTip )
                # self.vrayLightTB.addAction( vrayLightAction )
                button = self.iconButton( cmd, icon, toolTip )
                self.iconBtnLayout.addWidget( button )
        else:
            pass

    def getRenderManLight(self):
        if len( self.renderManLights ) > 0:
            self.iconBtnLayout.addWidget( QtWidgets.QLabel( "|" ) )
            self.iconBtnLayout.addWidget( QtWidgets.QLabel( "RenderMan: " ) )
            for lightType in self.renderManLights:
                icon = QIcon( typeMgr.getIcon( lightType ) )
                cmd = partial( self.createNewLight, lightType )
                toolTip = 'Create a new ' + lightType
                # renderManLightAction = self.createAction( lightType,  icon, cmd, toolTip )
                # mayaLightTB.addAction( renderManLightAction )
                button = self.iconButton( cmd, icon, toolTip )
                self.iconBtnLayout.addWidget( button )
        else:
            pass

    def getArnoldLight(self):
        if len( self.arnoldLights ) > 0:
            self.iconBtnLayout.addWidget( QtWidgets.QLabel( "|" ) )
            self.iconBtnLayout.addWidget( QtWidgets.QLabel( "Arnold: " ) )
            for lightType in self.arnoldLights:
                icon = QIcon( typeMgr.getIcon( lightType ) )
                cmd = partial( self.createNewLight, lightType )
                toolTip = 'Create a new ' + lightType
                # arnoldLightAction = self.createAction( lightType, icon, cmd, toolTip )
                # mayaLightTB.addAction( arnoldLightAction )
                button = self.iconButton( cmd, icon, toolTip )
                self.iconBtnLayout.addWidget( button )
        # self.iconBtnLayout.addStretch(1)
        else:
            pass

    def iconButton(self, cmd, icon, toolTip):
        button = RenderSetupButton( self, icon, self.BUTTON_SIZE )
        button.setToolTip( toolTip )
        button.clicked.connect( partial( cmd ) )
        return button

    def createAction(self, lightType, icon, cmd, toolTip):
        action = QtWidgets.QAction(icon, lightType, self)
        action.setStatusTip(toolTip)
        action.triggered.connect(partial(cmd))
        return action

    def createNewLight(self, lightType=None, *args):
        if lightType in self.mayaLights:
            func = self.mayaLightTypes[lightType]
        else:
            pass

        if lightType in self.vrayLights:
            func = self.vrayLightTypes[lightType]
        else:
            pass

        if lightType in self.renderManLights:
            func = self.renderManLightTypes[lightType]
        else:
            pass

        if lightType in self.arnoldLights:
            func = self.arnoldLightTypes[lightType]
        else:
            pass

        light = func()

        self.addLight( light )

    def addLight(self, light):
        widget = LightManager( light )
        self.scrollLayout.addWidget( widget )
        widget.onSolo.connect(self.onSolo)

    def onSolo(self, value):
        lightWidgets = self.findChildren( LightManager )
        for widget in lightWidgets:
            if widget != self.sender():
                widget.disableLight(value)

    def populate(self):
        while self.scrollLayout.count():
            widget = self.scrollLayout.takeAt(0).widget()
            if widget:
                widget.setVisible(False)
                widget.deleteLater()

        type = [str(f) for f in self.mayaLights + typeMgr.pluginLights()]
        for light in pm.ls(type=type):
            self.addLight(light)
