# -*-coding:utf-8 -*

"""

"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds
import pymel.core as pm
import maya, os, json, pprint, logging, time
from functools import partial
from maya import OpenMayaUI as omui
import  mtoa.utils as mutils

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

WINTITLE = 'Lighting Manager'

class LightWidget(QtWidgets.QWidget):

    onSolo = QtCore.Signal(bool)

    def __init__(self, light):
        super(LightWidget, self).__init__()

        if isinstance(light, basestring):
            light = pm.PyNode(light)

        self.light = light

        self.buildUI()

    def buildUI(self):

        # Create a layout
        layout = QtWidgets.QGridLayout(self)
        layout.setContentsMargins(2,2,2,2)

        # Create a check box of light for visibility
        self.name = QtWidgets.QCheckBox(str(self.light.getTransform()))
        self.name.setChecked(self.light.visibility.get())
        self.name.toggled.connect(lambda val: self.light.getTransform().visibility.set(val))
        layout.addWidget(self.name, 0,0)

        # Create a solo button, it will turn on only the light selected, and disable all others
        soloBtn = QtWidgets.QPushButton('Solo')
        soloBtn.setMaximumWidth(40)
        soloBtn.setCheckable(True)
        soloBtn.toggled.connect(lambda val: self.onSolo.emit(val))
        layout.addWidget(soloBtn, 0,1)

        # Create delete button, delete the light selected
        deleteBtn = QtWidgets.QPushButton('Delete')
        deleteBtn.setMaximumWidth(40)
        deleteBtn.clicked.connect(self.deleteLight)
        layout.addWidget(deleteBtn, 0, 2)

        # intensity of light
        intensityLight = QtWidgets.QLineEdit(str(self.light.intensity.get()))
        intensityLight.setMaximumWidth(80)
        intensityLight.textChanged.connect(lambda val: self.light.intensity.set(float(val)))
        layout.addWidget(intensityLight, 0,3)

        # Change mode of light
        self.colorBtn = QtWidgets.QPushButton()
        self.colorBtn.setMaximumSize(20,20)
        self.setButtonColor()
        self.colorBtn.clicked.connect(self.setColorLight)
        layout.addWidget(self.colorBtn, 0,4)

    def setButtonColor(self, color=None):
        if not color:
            color = self.light.color.get()

        assert len(color) == 3, "You must provide a list of 3 colors"

        r,g,b = [c*255 for c in color]

        self.colorBtn.setStyleSheet('background-color: rgba(%s,,%s,%s,1.0)' % (r,g,b))

    def setColorLight(self):

        lightColor = self.light.color.get()

        # load color editor UI from Maya
        color = pm.colorEditor(rgbValue=lightColor)

        # Convert color value above to rgba
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

class ToolBoxV(QtWidgets.QDialog):

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

    def __init__(self):
        super(ToolBoxV, self).__init__()
        # Set title of window
        self.setWindowTitle(WINTITLE)
        # Load UI
        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)
        layout.setContentsMargins(5,5,5,5)

        # Create a label to note for Maya light
        mayaLightLabel = QtWidgets.QLabel('Maya Lights')
        mayaLightLabel.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(mayaLightLabel, 0,0,1,6)

        # Create a label to note for Vray light
        vrayLightLabel = QtWidgets.QLabel('Vray Lights')
        vrayLightLabel.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(vrayLightLabel, 0,6,1,8)

        # Create a combo box that has the list of Maya light type
        self.mayaLightTypeCB = QtWidgets.QComboBox()
        # Put lightType into combo Box (Maya lights)
        for lightType in sorted(self.mayaLightTypes):
            self.mayaLightTypeCB.addItem(lightType)

        layout.addWidget(self.mayaLightTypeCB, 1,0,1,4)

        # Create a button to create the light base on the selection of the combo box
        createMayaLightBtn = QtWidgets.QPushButton('Create')
        createMayaLightBtn.clicked.connect(partial(self.createLight, 'Maya Light'))
        layout.addWidget(createMayaLightBtn, 1,4,1,2)

        # Create a combo box that has the list of Vray light type
        self.vrayLightTypeCB = QtWidgets.QComboBox()
        # Put lightType into combo Box (Maya lights)
        for lightType in sorted(self.vrayLightTypes):
            self.vrayLightTypeCB.addItem(lightType)

        layout.addWidget(self.vrayLightTypeCB, 1,6,1,6)

        # Create a button to create the light base on the selection of the combo box
        createVrayLightBtn = QtWidgets.QPushButton('Create')
        createVrayLightBtn.clicked.connect(partial(self.createLight, 'Vray Light'))
        layout.addWidget(createVrayLightBtn, 1,12,1,2)

        # Create Scroll layout to add the light created from buttons above into main layout via LightWidget class
        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea, 2,0,1,14)

    def createLight(self, lightTypePlugin):

        # base on create button to get the combo box light type
        if lightTypePlugin == 'Maya Light':
            lightType = self.mayaLightTypeCB.currentText()
            func = self.mayaLightTypes[lightType]
        elif lightTypePlugin == 'Vray Light':
            lightType = self.vrayLightTypeCB.currentText()
            func = self.vrayLightTypes[lightType]

        # Create the light
        light = func()
        self.addLight(light)

    def addLight(self, light):

        widget = LightWidget(light)
        self.scrollLayout.addWidget(widget)
        widget.onSolo.connect(self.onSolo)

    def onSolo(self, value):

        lightWidgets = self.findChildren(LightWidget)

        for widget in lightWidgets:
            if widget != self.sender():
                widget.disableLight(value)



def showUI():
    ui = ToolBoxV()
    ui.show()
    return ui

# --------------------------------------------------------------------------------------------------------
# END OF CODE
# --------------------------------------------------------------------------------------------------------