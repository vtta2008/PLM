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
import os, sys, json

# -------------------------------------------------------------------------------------------------------------
# VARIABLES
# -------------------------------------------------------------------------------------------------------------
DESKTOPPTH = os.path.join( os.environ['HOMEPATH'], 'desktop' )

PRODPROFILE = dict( name=[ 'mwm', 'Midea Wasing Machine' ] )
WINPROFILE = dict( prodpthUI=[ 'ProdPthUI', 'Production directory', 'Quick Folder Setup' ] )

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

# ----------------------------------------------------------------------------------------------------------- #
"""                                MAIN CLASS: CREATE PRODUCTION FOLDER HIERARCHY                           """
# ----------------------------------------------------------------------------------------------------------- #

class ProdFolder( object ):

    info = {}
    winid = WINPROFILE['prodpthUI'][0]
    title = WINPROFILE['prodpthUI'][1]
    label = WINPROFILE['prodpthUI'][2]

    def __init__(self):

        self.infoDir = self.createInfo()
        infoFile = PRODPROFILE['name'][0] + '.production'
        self.infoPth = os.path.join(self.infoDir, infoFile)

        if not os.path.exists( self.infoPth ):
            self.newInfo()
        else:
            cmds.confirmDialog(t='Warning', m='This produciton is already created', b='OK')

    def newInfo(self, *args):
        self.buildUI()

    def buildUI(self):
        """
        Main UI just to confirm very basic info of production
        :return:
        """
        # Production name by default
        prodName = PRODPROFILE['name'][0]
        # Check if UI exists
        if cmds.window( self.winid, q=True, exists=True ):
            cmds.deleteUI( self.winid )
        # Create UI
        cmds.window( self.winid, t=self.title )
        # Main layout
        cmds.columnLayout('main')
        cmds.text( l=self.label, h=30, w=315, align='center')
        # Line 1
        cmds.rowColumnLayout( nc=9, cw=self.cw( nc=5, wi=75, w=75 ) )
        self.Txt("Prod Name" )
        self.prodName = cmds.textField( tx=prodName )
        self.Txt('Sequenes')
        self.numShots = cmds.intField( v=9 )
        self.blankParent()
        # Line 2
        cmds.rowColumnLayout( nc=5, cw=self.cw( nc=5, wi=210, w=105 ) )
        self.TxtField('ProdPth', DESKTOPPTH)
        cmds.button( l='Set Path', c=self.setPth )
        self.blankParent()
        # Line 3
        cmds.rowColumnLayout( nc=5, cw=self.cw( nc=5, wi=210, w=105 ) )
        self.TxtField('ProdName', prodName)
        cmds.button(l='Create folders', c=self.prodFolders)
        self.blankParent()
        # Show window
        cmds.showWindow( self.winid )

    def Txt(self, txt, *args):
        self.blank()
        cmds.text(l=txt)
        self.blank()

    def TxtField(self, id, txt, *args):
        cmds.textField(id, tx=txt)

    def blankParent(self, *args):
        self.blank(10)
        cmds.setParent('..')

    def cw(self, nc=7, bl=5, ids=[2], wi=200, w=100, *args):
        """
        calculating column width and return them as flag in rowColumnLayout command
        :return: cw
        """
        cw = [ ]
        i = 0
        for i in range( nc ):
            if (i + 3) % 2 == 0:
                for id in ids:
                    if (i + 1) == id:
                        tump = (i + 1, wi)
                    else:
                        tump = (i + 1, w)
                    cw.append( tump )
            elif (i + 3) % 2 == 1:
                tump = (i + 1, bl)
                cw.append( tump )
            i += 1
        return cw

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

    def setPth(self, *args):
        pth = cmds.fileDialog2( cap='set production path', fm=3, okc='Set' )
        dir = self.getDirFromUnicode( pth[ 0 ] )
        cmds.textField('ProdPth', edit=True, tx=dir )

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


