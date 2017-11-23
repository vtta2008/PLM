# -*-coding:utf-8 -*
"""


"""

from maya import cmds, mel
from functools import partial

import logging, sys

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

WINID = 'Layer Manager'
TITLE = 'Layer Manager'
LABELW = 30
INPUTW = 189
ADJ = 20
RP = 6
UIW = LABELW + INPUTW + ADJ


def importBTS():
    from modules import MayaFuncs
    reload( MayaFuncs )
    return MayaFuncs


class LayerManager( object ):
    bts = importBTS()

    def __init__(self):
        super( LayerManager, self ).__init__()

        self.buildUI()

    def buildUI(self):

        if cmds.window( WINID, query=True, exists=True ):
            cmds.deleteUI( WINID )

        winid = cmds.window( WINID, t=TITLE, maximizeButton=False, minimizeButton=True, sizeable=True,
                             resizeToFitChildren=False, menuBar=True, menuBarVisible=True )

        cmds.menu( l='File', tearOff=False )
        cmds.menuItem( l='Refresh', c=self.bts.layerManagerUI )
        cmds.menuItem( l='Show All', c=partial( self.showAllHideLayers, True ))

        lmLayout = cmds.formLayout( numberOfDivisions=100 )
        lmScroll = cmds.scrollLayout( hst=16, vst=16, cr=True, minChildWidth=UIW )
        cmds.columnLayout( adjustableColumn=True, rowSpacing=RP )
        cmds.columnLayout( adjustableColumn=True )
        curAllLayer = cmds.ls( type='displayLayer' )
        for i in range( len( curAllLayer ) ):
            cmds.rowColumnLayout( nc=2, cw=[ (1, LABELW), (2, INPUTW) ] )
            # onButton = 'onButton' + str( i )
            # offButton = 'offButton' + str( i )
            isoButton = 'isoButton' + str( i )

            cmds.button( isoButton, l='Iso', c='mel.eval("layerVisInv(" + "\"" + allLayer[i] + "\"" + ")")' )
            transparent = False
            colorIndex = cmds.getAttr( curAllLayer[ i ] + ".color" )
            if colorIndex == 0: transparent = True
            cmds.layerButton( l=curAllLayer[ i ], name=curAllLayer[ i ], transparent=transparent, w=UIW,
                              command=('mel.eval("layerEditorLayerButtonSelect #m #1")'),
                              doubleClickCommand=('mel.eval("createLayerEditorQuickEditWindow { \"#1\" }"'),
                              renameCommand=('mel.eval(("layerEditorLayerButtonRename #1 #2"))'),
                              typeCommand=('mel.eval("layerEditorLayerButtonTypeChange #1")'),
                              visibleCommand=('mel.eval("layerEditorLayerButtonVisibilityChange #1")'),
                              dropCallback=('mel.eval("layerEditorLayerButtonDrop")'),
                              dragCallback=('mel.eval("layerEditorLayerButtonDrag")')
                              )
            i += 1
        cmds.setParent( lmLayout )

        refreshBtn = cmds.button( 'refreshBtn', l='Refresh', c='func.layerManagerUI()' )
        closeBtn = cmds.button( 'closeBtn', l='Close', c='cmds.deleteUI(winID)' )

        attachForm = [ (lmScroll, "top", 2), (lmScroll, "left", 2), (lmScroll, "right", 2), (refreshBtn, 'left', 2),
                       (refreshBtn, 'bottom', 2), (refreshBtn, 'bottom', 2), (closeBtn, 'bottom', 2),
                       (closeBtn, 'right', 2) ]
        attachControl = [ (lmScroll, 'bottom', 2, refreshBtn), ]
        attachNone = ([ str( refreshBtn ), 'top' ], [ str( closeBtn ), 'top' ])
        attachPosition = ([ str( refreshBtn ), 'right', 2, 50 ], [ closeBtn, 'left', 2, 50 ])

        cmds.formLayout( lmLayout, e=True, af=attachForm, ac=attachControl, an=attachNone, ap=attachPosition )

        cmds.showWindow( winid )

    def layerVisInv(self, activeLayer, *args):
        allLayers = cmds.ls( type='displayLayer' )

        if len( allLayers ) == 0:
            logger.info( 'No layers exists' )
            sys.exit()

        for i in range( len( allLayers ) ):

            if allLayers[ i ] != activeLayer:
                cmds.setAttr( allLayers[ i ] + '.visibility', False )
            i += 1

        cmds.setAttr( activeLayer + '.visibility', True )

    def layerVisToggle(self, activeLayer, *args):
        allLayers = cmds.ls( type='displayLayer' )
        visible = cmds.getAttr( activeLayer + '.visibility' )

        if not visible:
            visible = True
        else:
            visible = False

        cmds.setAttr( activeLayer + '.visibility', visible )

    def showAllHideLayers(self, visible, *args):

        allLayers = cmds.ls( type='displayLayer' )

        if not visible:
            visible = True
        else:
            visible = False

        for i in range( len( allLayers ) ):
            cmds.setAttr( allLayers[ i ] + '.visibility', visible )


if __name__=='m__main__':
    LayerManager()