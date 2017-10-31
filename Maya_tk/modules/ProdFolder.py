# -*-coding:utf-8 -*
"""

Script Name: ProdFolder.py

Author: Do Trinh/Jimmy - 3D artist, leader DAMG team.

Description:
    This script is main file to create folder structure in pipeline

for any question or feedback, feel free to email me: dot@damgteam.com or damgteam@gmail.com

"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds
from functools import partial
import os, sys, json, logging

# -------------------------------------------------------------------------------------------------------------
# VARIABLES
# -------------------------------------------------------------------------------------------------------------
DESKTOPPTH = os.path.join( os.environ['HOMEPATH'], 'desktop' )

PRODPROFILE = dict( name=[ 'mwm', 'Midea Wasing Machine' ] )
WINPROFILE = dict( prodpthUI=[ 'ProdPthUI', 'Create New Project', 'SET UP NEW PROJECT' ] )

APPS = [ 'maya', 'zbrush', 'mari', 'nuke', 'photoshop', 'houdini', 'after effects' ]

MASTER = [ 'assets', 'sequences', 'deliverables', 'documents', 'editorial', 'sound', 'resources', 'RnD' ]
TASKS = [ 'art', 'modeling', 'rigging', 'surfacing' ]
SEQTASKS = [ 'anim', 'comp', 'fx', 'layout', 'lighting' ]
ASSETS = {'heroObj': [ 'washer', 'dryer' ], 'environment': [], 'props': [ ]}
STEPS = ['publish', 'review', 'work']

MODELING = [ 'scenes', 'fromZ', 'toZ', 'objImport', 'objExport', 'movie' ]
RIGGING = [ 'scenes', 'reference' ]
SURFACING = ['scenes', 'sourceimages', 'images', 'movie']
LAYOUT = [ 'scenes', 'sourceimages', 'images', 'movie', 'alembic']
LIGHTING = [ 'scenes', 'sourceimages', 'images', 'cache', 'reference' ]
FX = [ 'scenes', 'sourceimages', 'images', 'cache', 'reference', 'alembic' ]
ANIM = LAYOUT

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

# get button functions data
def importBTS():
    from Maya_tk.modules import MayaFuncs
    reload(MayaFuncs)
    return MayaFuncs

# ----------------------------------------------------------------------------------------------------------- #
"""                                MAIN CLASS: CREATE PRODUCTION FOLDER HIERARCHY                           """
# ----------------------------------------------------------------------------------------------------------- #

class ProdFolder( object ):

    info = {}
    winid = WINPROFILE['prodpthUI'][0]
    title = WINPROFILE['prodpthUI'][1]
    label = WINPROFILE['prodpthUI'][2]
    bts = importBTS()

    h1 = 200

    def __init__(self):

        self.infoDir = self.createInfo()
        infoFile = PRODPROFILE['name'][0] + '.production'
        self.infoPth = os.path.join(self.infoDir, infoFile)

        print self.infoPth

        self.newInfo()

    def newInfo(self, *args):
        self.buildUI()

    def buildUI(self):
        """
        Main UI just to confirm very basic info of production
        :return:
        """

        w=500
        h = 30

        # Production name by default
        prodName = "VoxelPicture"
        # Check if UI exists
        if cmds.window( self.winid, q=True, exists=True ):
            cmds.deleteUI( self.winid )
        # Create UI
        cmds.window( self.winid, t=self.title, rtf=True, wh=(w, 25*h))
        # Main layout
        mainLayout = cmds.scrollLayout('main', hst=15, vst=15)

        # Title
        self.bts.makeSeparator(h=h/6, w=w)
        cmds.text(l=self.label, h=h, w=w, align='center')
        self.bts.makeSeparator(h=h/6, w=w)

        # Content
        nc = 7
        w1 = (nc-2)*(w/30)
        adj1 = nc - 2

        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc, [w1, w1, adj1, w1, adj1, w-(3*w1)-(3*adj1), adj1]))

        cmds.text(l='Project Name', align='center')

        self.prodName = cmds.textField(tx=prodName)
        cmds.text(l="")
        cmds.button(l='Set Path', c=self.setPth)
        cmds.text(l="")
        self.setPath = cmds.textField(tx = "E:/")

        cmds.setParent(mainLayout)

        cmds.text(l="")
        cmds.text(l="DUE TO THE POSSIBILITY TO USE RENDER FARM SERVICE \n SETTING PATH TO E DRIVE IS ALWAYS PREFERABLE",
                  align='center', w=w, h=h, bgc=(0,.5,1), fn="boldLabelFont")
        cmds.text(l="")

        nc = 9
        w2 = (w-(5*adj1))/(nc-5)

        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc, [adj1, w2, adj1, w2, adj1, w2, adj1, w2, adj1]))

        cmds.text(l="")
        cmds.text(l="Project Mode")
        cmds.text(l="")
        self.setMode = cmds.optionMenu()
        cmds.menuItem(l="Group Mode", p=self.setMode)
        cmds.menuItem(l="Production Mode", p=self.setMode)
        cmds.text(l="")
        cmds.text(l="Sequences")
        cmds.text(l="")
        self.numShot = cmds.intField(v=1)
        cmds.text(l="")
        cmds.setParent(mainLayout)
        cmds.text(l="")

        nc = 13
        w3 = (w-(7*adj1))/(nc-7)

        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc, [adj1, w3, adj1, w3, adj1, w3, adj1, w3, adj1, w3, adj1, w3, adj1]))

        cmds.text(l="")
        cmds.text(l="Character:")
        cmds.text(l="")
        self.numChar = cmds.intField(v=1, cc=partial(self.charNameColumn, (w-(4*adj1))/3))
        cmds.text(l="")
        cmds.text(l="Environment")
        cmds.text(l="")
        self.numEnv = cmds.intField(v=1, cc=partial(self.envNameColumn, (w-(4*adj1))/3))
        cmds.text(l="")
        cmds.text(l="Props")
        cmds.text(l="")
        self.numProps = cmds.intField(v=1, cc=partial(self.propsNameColumn, (w-(4*adj1))/3))
        cmds.text(l="")

        cmds.setParent(mainLayout)
        cmds.text(l="")

        nc = 7
        w4 = (w-(4*adj1))/(nc-4)

        cmds.rowColumnLayout(nc=3, cw=[(1,w/3),(2,w/3),(3,w/3)])
        cmds.text(l="Characters Name")
        cmds.text(l="Envs Name")
        cmds.text(l="Props Name")


        cmds.setParent(mainLayout)
        cmds.text(l="")

        self.editableColumnsLayout = cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc, [adj1, w4, adj1, w4, adj1, w4, adj1]))

        cmds.text(l="")
        self.charColumn = cmds.columnLayout(w=w4)
        self.firstCharColumn = cmds.columnLayout(w=w4)
        cmds.textField(p=self.firstCharColumn, w=w4-10)
        cmds.setParent(self.editableColumnsLayout)

        cmds.text(l="")
        self.envColumn = cmds.columnLayout(w=w4)
        self.firstEnvColumn = cmds.columnLayout(w=w4)
        cmds.textField(p = self.firstEnvColumn, w=w4-10)
        cmds.setParent(self.editableColumnsLayout)

        cmds.text(l="")
        self.propsColumn = cmds.columnLayout(w=w4)
        self.firstPropsColumn = cmds.columnLayout(w=w)
        cmds.textField(p=self.firstPropsColumn, w=w4-10)
        cmds.setParent(self.editableColumnsLayout)
        cmds.text(l="")

        cmds.setParent(mainLayout)

        self.bts.makeSeparator(h=10, w=w)

        cmds.rowColumnLayout(nc=3, cw=[(1,w/3),(2,w/3),(3,w/3)])
        cmds.text(l="")
        cmds.button(l="CREATE PROJECT", c=self.createProject)
        cmds.text(l="")

        cmds.setParent(mainLayout)
        cmds.text(l="")


        cmds.showWindow(self.winid)

    def charNameColumn(self, w, *args):
        if cmds.columnLayout(self.firstCharColumn, q=True, exists=True):
            cmds.deleteUI(self.firstCharColumn)

        if cmds.scrollLayout('charNameColumn', q=True, exists=True):
            cmds.deleteUI('charNameColumn')

        charNameColumn = cmds.scrollLayout('charNameColumn', p = self.charColumn, w=w, h=self.h1, hst=15, vst=15)
        chars = cmds.intField(self.numChar, q=True, v=True)

        for i in range(chars):
            id = "char" + str(i + 1)
            cmds.textField(id, w=w-10)
            i += 1

        return charNameColumn

    def envNameColumn(self, w, *args):

        if cmds.columnLayout(self.firstEnvColumn, q=True, exists=True):
            cmds.deleteUI(self.firstEnvColumn)

        if cmds.scrollLayout('envNameColumn', q=True, exists=True):
            cmds.deleteUI('envNameColumn')

        envNameColumn = cmds.scrollLayout('envNameColumn', p=self.envColumn, w=w, h=self.h1, hst=15, vst=15)
        envs = cmds.intField(self.numEnv, q=True, v=True)

        for i in range(envs):
            id = 'env' + str(i+1)
            cmds.textField(id, w=w-10)
            i+=1

        return envNameColumn

    def propsNameColumn(self, w, *args):

        if cmds.columnLayout(self.firstPropsColumn, q=True, exists=True):
            cmds.deleteUI(self.firstPropsColumn)

        if cmds.scrollLayout('propsNameColumn', q=True, exists=True):
            cmds.deleteUI('propsNameColumn')

        propsNameColumn = cmds.scrollLayout('propsNameColumn', p=self.propsColumn, w=w, h=self.h1, hst=15, vst=15)
        props = cmds.intField(self.numProps, q=True, v=True)

        for i in range(props):
            id = 'props' + str(i+1)
            cmds.textField(id, w=w-10)
            i+=1

        return propsNameColumn

    def setPth(self, *args):
        pth = cmds.fileDialog2(cap='set production path', fm=3, okc='Set')
        dir = self.getDirFromUnicode(pth[0])
        cmds.textField(self.setPath, edit=True, tx=dir)

    def createProject(self):
        pass

    def Txt(self, txt, *args):
        self.blank()
        cmds.text(l=txt, align='center')
        self.blank()

    def TxtField(self, id, txt, *args):
        cmds.textField(id, tx=txt)

    def blankParent(self, *args):
        self.blank(10)
        cmds.setParent('..')

    def prodFolders(self, apps = APPS, master = MASTER, assets = ASSETS, steps = STEPS, tasks = TASKS, seqTasks = SEQTASKS, *args):
        """
        Create all folders in productions
        """
        dir = str( cmds.textField('ProdPth', q=True, tx=True ) )
        name = str( cmds.textField('ProdName', q=True, tx=True ) )
        prodPth = os.path.join( dir, name )

        self.info['name'] = name
        self.info['dir'] = prodPth

        if not os.path.exists( prodPth ):
            cmds.sysFile( prodPth, md=True )

        for f in master:
            cmds.sysFile( os.path.join( prodPth, f ), md=True )

        assetsPth = os.path.join( prodPth, master[ 0 ] )
        self.info['assetsPth'] = assetsPth

        for asset in assets:
            assetDir = os.path.join( assetsPth, asset )
            cmds.sysFile( assetDir, md=True )
            for a in assets[ asset ]:
                assetPth = os.path.join( assetDir, a)
                self.info['a'] = assetPth
                cmds.sysFile( assetPth, md=True )
                self.taskTreeFolder( apps=apps, pth=assetPth, steps=steps, tasks=tasks )

        if len( assets[ 'environment' ] ) == 0:
            envPth = os.path.join( assetsPth, 'environment' )
            self.info['environment'] = envPth
            self.taskTreeFolder( apps=apps, pth=envPth, steps=steps, tasks=tasks )

        if len( assets[ 'props' ] ) == 0:
            propsPth = os.path.join( assetsPth, 'props' )
            self.info['props'] = propsPth
            self.taskTreeFolder( apps=apps, pth=propsPth, steps=steps, tasks=tasks )

        seqPth = os.path.join( prodPth, master[ 1 ] )
        self.info['sequences'] = seqPth
        numOfShots = cmds.intField( self.numShots, q=True, v=True )
        prodName = cmds.textField( self.prodName, q=True, tx=True )

        for i in range( numOfShots ):
            shotName = '%s_shot_%s' % (prodName, (i + 1))
            shotsPth = os.path.join( seqPth, shotName )
            cmds.sysFile( shotsPth, md=True )
            self.taskTreeFolder( apps=apps, pth=shotsPth, steps=steps, tasks=seqTasks )

        if cmds.window( self.winid, q=True, exists=True ):
            cmds.deleteUI( self.winid )

        with open(self.infoPth, 'w') as f:
            json.dump(self.infoPth, f,indent=4)

    def taskTreeFolder(self, apps, pth, steps, tasks):
        for task in tasks:
            taskPth = os.path.join( pth, task )
            cmds.sysFile( taskPth, md=True )
            for step in steps:
                path = os.path.join(taskPth, step)
                cmds.sysFile( path, md=True )
                if step == 'work':
                    if task == 'modeling':
                        for app in ['maya', 'zbrush']:
                            cmds.sysFile(os.path.join(path, app), md=True )
                            if app == 'maya':
                                self.mayaFolderTask( path, MODELING )
                    elif task == 'rigging' or task == 'anim':
                        cmds.sysFile( os.path.join( path, 'maya' ), md=True )
                        for folder in RIGGING:
                            cmds.sysFile( os.path.join( os.path.join( path, 'maya' ), folder ), md=True )
                    elif task == 'comp':
                        cmds.sysFile( os.path.join( path, 'nuke' ), md=True )
                    elif task == 'layout':
                        for app in ['maya', 'after effects']:
                            cmds.sysFile( os.path.join( path, app ), md=True )
                            if app == 'maya':
                                self.mayaFolderTask( path, LAYOUT )
                    elif task == 'fx':
                        for app in ['maya', 'houdini']:
                            cmds.sysFile( os.path.join( path, app ), md=True )
                            if app == 'maya':
                                self.mayaFolderTask( path, FX )
                    elif task == 'surfacing':
                        for app in ['maya', 'zbrush', 'mari', 'nuke', 'photoshop']:
                            appPth = os.path.join( path, app )
                            cmds.sysFile(appPth, md=True )
                            if app == 'maya':
                                self.mayaFolderTask( path, SURFACING )
                    elif task == 'lighting':
                        mayaPth = os.path.join( path, 'maya' )
                        cmds.sysFile(mayaPth, md=True )
                        for folder in LIGHTING:
                            folderPth = os.path.join(mayaPth, folder )
                            cmds.sysFile(folderPth, md=True )

    def mayaFolderTask(self, path, task):
        mayaPth = os.path.join( path, 'maya' )
        for folder in task:
            cmds.sysFile( os.path.join( mayaPth, folder ), md=True )



    def blank(self, h=5, t=1, *args):
        for i in range( t ):
            cmds.text( l='', h=h )
            i += 1

    def getDirFromUnicode(self, path, *args):
        for dirpath, dirnames, filenames in os.walk( path ):
            return dirpath

    def createInfo(self, *args):
        appDir = os.getenv( 'PROGRAMDATA' )
        infoDir = os.path.join( appDir, 'Pipeline Tool/prodInfo' )
        if not os.path.exists( infoDir ):
            os.makedirs( infoDir )
        return infoDir

# ----------------------------------------------------------------------------------------------------------- #
"""                                               END OF CODE                                               """
# ----------------------------------------------------------------------------------------------------------- #


