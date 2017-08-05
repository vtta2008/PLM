import maya.cmds as cmds
import pymel.core as pm
import maya, os, json, pprint, Qt, logging, time
from Qt import QtWidgets, QtCore, QtGui
from functools import partial
from maya.app.renderSetup.views.renderSetupButton import *
from maya import OpenMayaUI as omui
import maya.app.renderSetup.views.lightEditor.lightTypeManager as typeMgr
import maya.app.renderSetup.views.utils as viewsUtils
import mtoa.utils as mutils

logging.basicConfig()

logger = logging.getLogger('LightingManager')

logger.setLevel(logging.DEBUG)

if Qt.__binding__.startswith('PyQt'):
    logger.debug('Using sip')
    from sip import wrapinstance as wrapInstance
    from Qt.QtCore import pyqtSignal as Signal
elif Qt.__binding__ == 'PySide':
    from shiboken import wrapInstance
    from Qt.QtCore import Signal
else:
    logger.debug('Using shiboken2')
    from shiboken2 import wrapInstance
    from Qt.QtCore import Signal

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

def getDock(name='DAMGtoolBoxIIIDock'):
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

class DAMGtoolBoxIII( QtWidgets.QWidget ):

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

        super( DAMGtoolBoxIII, self ).__init__( parent=parent )
        self.setWindowTitle('Lighting Manager')
        self.buildUI()
        self.populate()

        #self.parent().layout().addWidget(self)

        #if not dock:
            #parent.show()

        self.userAppDir = cmds.internalVar( userAppDir=True )
        self.userLibaryDir = self.userAppDir + 'userLibrary'
        if not os.path.exists( self.userLibaryDir ):
            os.mkdir( self.userLibaryDir )

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)
        pluginLights = typeMgr.pluginLights()
        self.mayaLights = sorted(typeMgr.mayaLights())
        self.vrayLights = sorted([f for f in pluginLights if f.startswith("VRay")])
        self.renderManLights = sorted([f for f in pluginLights if f.startswith("Pxr")])
        self.arnoldLights = sorted([f for f in pluginLights if f.startswith("ai")])

        iconBtnWidget = QtWidgets.QWidget()
        iconBtnLayout = QtWidgets.QHBoxLayout(iconBtnWidget)
        layout.addWidget(iconBtnWidget, 0, 1)
        iconBtnLayout.addWidget( QtWidgets.QLabel( "Maya: " ) )

        for lightType in self.mayaLights:
            icon = QIcon(typeMgr.getIcon(lightType))
            button = RenderSetupButton(self, icon, self.BUTTON_SIZE)
            toolTip = 'Create a new ' + lightType
            button.setToolTip(toolTip)
            button.clicked.connect(partial(self.createNewLight, lightType))
            iconBtnLayout.addWidget(button)

        if len(self.vrayLights) > 0:
            iconBtnLayout.addWidget( QtWidgets.QLabel( "|" ) )
            iconBtnLayout.addWidget( QtWidgets.QLabel( "Vray: " ) )
            for lightType in self.vrayLights:
                icon = QIcon(typeMgr.getIcon(lightType))
                button = RenderSetupButton(self, icon, self.BUTTON_SIZE)
                toolTip = 'Create a new ' + lightType
                button.setToolTip( toolTip )
                button.clicked.connect( partial( self.createNewLight, lightType ) )
                iconBtnLayout.addWidget(button)
        else:
            pass

        if len(self.renderManLights) > 0:
            iconBtnLayout.addWidget(QtWidgets.QLabel("|"))
            iconBtnLayout.addWidget( QtWidgets.QLabel( "RenderMan: " ) )
            for lightType in self.renderManLights:
                icon = QIcon(typeMgr.getIcon(lightType))
                button = RenderSetupButton(self, icon, self.BUTTON_SIZE)
                toolTip = 'Create a new ' + lightType
                button.setToolTip( toolTip )
                button.clicked.connect( partial( self.createNewLight, lightType ) )
                iconBtnLayout.addWidget(button)
        else:
            pass

        if len(self.arnoldLights) > 0:
            iconBtnLayout.addWidget(QtWidgets.QLabel("|"))
            iconBtnLayout.addWidget( QtWidgets.QLabel( "Arnold: " ) )
            for lightType in self.arnoldLights:
                icon = QIcon(typeMgr.getIcon(lightType))
                button = RenderSetupButton(self, icon, self.BUTTON_SIZE)
                toolTip = 'Create a new ' + lightType
                button.setToolTip( toolTip )
                button.clicked.connect( partial( self.createNewLight, lightType ) )
                iconBtnLayout.addWidget(button)

        iconBtnLayout.addStretch(1)

        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea, 1, 0, 1, 2)

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
        widget = LightWidget( light )
        self.scrollLayout.addWidget( widget )
        widget.onSolo.connect(self.onSolo)

    def onSolo(self, value):
        lightWidgets = self.findChildren(LightWidget)
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

class LightWidget(QtWidgets.QWidget):

    onSolo = QtCore.Signal(bool)

    def __init__(self, light):
        super(LightWidget, self).__init__()
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

def showUI():
    ui = DAMGtoolBoxIII()
    ui.show()
    return ui

"""

def getMayaMainWindow():
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr

def getDock(name='LightingManagerDock'):
    deleteDock(name)
    ctrl = cmds.workspaceControl(name, label='Lighting Manager')
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
    return ptr

def deleteDock(name='LightingManagerDock'):
    if cmds.workspaceControl(name, q=True, exists=True):
        cmds.deleteUI(name)
"""