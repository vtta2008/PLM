# -*-coding:utf-8 -*
"""

Script Name: ProdFolder.py

Author: Do Trinh/Jimmy - 3D artist, leader DAMG team.

Description:
    This script is main file to create folder structure in pipeline

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
import sys
from functools import partial

# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds

# -------------------------------------------------------------------------------------------------------------
# VARIABLES
# -------------------------------------------------------------------------------------------------------------
DESKTOPPTH = os.path.join(os.environ['HOMEPATH'], 'desktop')

PRODPROFILE = dict(name=['mwm', 'Midea Wasing Machine'])
WINPROFILE = dict(prodpthUI=['ProdPthUI', 'Create New Project', 'SET UP NEW PROJECT'])

APPS = ['maya', 'zbrush', 'mari', 'nuke', 'photoshop', 'houdini', 'after effects']

MASTER = ['assets', 'sequences', 'deliverables', 'documents', 'editorial', 'sound', 'resources', 'RnD']
TASKS = ['art', 'Modeling', 'rigging', 'surfacing']
SEQTASKS = ['anim', 'comp', 'fx', 'layout', 'lighting']
ASSETS = {'heroObj': ['washer', 'dryer'], 'environment': [], 'props': []}
STEPS = ['publish', 'review', 'work']

MODELING = ['scenes', 'fromZ', 'toZ', 'objImport', 'objExport', 'movie']
RIGGING = ['scenes', 'reference']
SURFACING = ['scenes', 'sourceimages', 'images', 'movie']
LAYOUT = ['scenes', 'sourceimages', 'images', 'movie', 'alembic']
LIGHTING = ['scenes', 'sourceimages', 'images', 'cache', 'reference']
FX = ['scenes', 'sourceimages', 'images', 'cache', 'reference', 'alembic']
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
    from plt_plugins.maya.modules import MayaFuncs
    reload(MayaFuncs)
    return MayaFuncs


# ----------------------------------------------------------------------------------------------------------- #
"""                                MAIN CLASS: CREATE PRODUCTION FOLDER HIERARCHY                           """


# ----------------------------------------------------------------------------------------------------------- #

class ProdFolder(object):
    info = {}
    winid = WINPROFILE['prodpthUI'][0]
    title = WINPROFILE['prodpthUI'][1]
    label = WINPROFILE['prodpthUI'][2]
    bts = importBTS()

    h1 = 200

    def __init__(self):

        self.buildUI()

    def buildUI(self):
        """
        Main UI just to confirm very basic info of production
        :return:
        """

        w = 500
        h = 30

        # Production name by default
        prodName = "VoxelPicture"
        # Check if UI exists
        if cmds.window(self.winid, q=True, exists=True):
            cmds.deleteUI(self.winid)
        # Create UI
        cmds.window(self.winid, t=self.title, rtf=True, wh=(w, 25 * h))
        # Main layout
        mainLayout = cmds.scrollLayout('main', hst=15, vst=15)

        # Title
        self.bts.makeSeparator(h=h / 6, w=w)
        cmds.text(l=self.label, h=h, w=w, align='center')
        self.bts.makeSeparator(h=h / 6, w=w)

        # Content
        nc = 9
        adj1 = 5
        w2 = (w - (5 * adj1)) / (nc - 5)

        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc, [adj1, w2, adj1, w2, adj1, w2, adj1, w2, adj1]))
        cmds.text(l="")
        cmds.text(l='Project Name', align='center')
        cmds.text(l="")
        self.prodName = cmds.textField(tx=prodName)
        cmds.text(l="")
        cmds.text(l="Abbreviated as", align='center')
        cmds.text(l="")
        self.prodShort = cmds.textField(tx='vxp')
        cmds.text(l="")

        cmds.setParent(mainLayout)
        cmds.text(l="")

        nc = 5
        w1 = 100

        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc, [adj1, w1, adj1, w - (3 * adj1 + w1), adj1]))

        cmds.text(l="")
        cmds.button(l='Set Path', c=self.setPth)
        cmds.text(l="")
        self.setPath = cmds.textField(tx="E:/")
        cmds.text(l="")

        cmds.setParent(mainLayout)
        cmds.text(l="")
        cmds.text(l="DUE TO THE POSSIBILITY TO USE ONLINE RENDER SERVICE\n"
                    "SETTING PATH TO E DRIVE IS ALWAYS PREFERABLE\n"
                    "IF YOU DO NOT USE THAT KIND OF SERVICE, NEVER MIND",
                  align='center', w=w, h=2 * h, bgc=(0, .5, 1), fn="boldLabelFont")
        cmds.text(l="")

        nc = 9

        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc, [adj1, w2, adj1, w2, adj1, w2, adj1, w2, adj1]))

        cmds.text(l="")
        cmds.text(l="Project Mode")
        cmds.text(l="")
        self.setMode = cmds.optionMenu()
        cmds.menuItem(l="Group Mode", p=self.setMode)
        cmds.menuItem(l="Studio Mode", p=self.setMode)
        cmds.text(l="")
        cmds.text(l="Sequences")
        cmds.text(l="")
        self.numShot = cmds.intField(v=1, min=1)
        cmds.text(l="")
        cmds.setParent(mainLayout)
        cmds.text(l="")

        nc = 13
        w3 = (w - (7 * adj1)) / (nc - 7)

        cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc,
                                                            [adj1, w3, adj1, w3, adj1, w3, adj1, w3, adj1, w3, adj1, w3,
                                                             adj1]))

        cmds.text(l="")
        cmds.text(l="Character:")
        cmds.text(l="")
        self.numChar = cmds.intField(v=1, min=1, cc=partial(self.charNameColumn, (w - (4 * adj1)) / 3))
        cmds.text(l="")
        cmds.text(l="Environment:")
        cmds.text(l="")
        self.numEnv = cmds.intField(v=1, min=1, cc=partial(self.envNameColumn, (w - (4 * adj1)) / 3))
        cmds.text(l="")
        cmds.text(l="Props:")
        cmds.text(l="")
        self.numProps = cmds.intField(v=1, min=1, cc=partial(self.propsNameColumn, (w - (4 * adj1)) / 3))
        cmds.text(l="")

        cmds.setParent(mainLayout)
        cmds.text(l="")

        nc = 7
        w4 = (w - (4 * adj1)) / (nc - 4)

        cmds.rowColumnLayout(nc=3, cw=[(1, w / 3), (2, w / 3), (3, w / 3)])
        cmds.text(l="Characters Name")
        cmds.text(l="Envs Name")
        cmds.text(l="Props Name")

        cmds.setParent(mainLayout)
        cmds.text(l="")

        self.editableColumnsLayout = cmds.rowColumnLayout(nc=nc, cw=self.bts.cwCustomize(nc,
                                                                                         [adj1, w4, adj1, w4, adj1, w4,
                                                                                          adj1]))

        cmds.text(l="")
        self.charColumn = cmds.columnLayout(w=w4)
        self.firstCharColumn = cmds.columnLayout(w=w4)
        cmds.textField('char1', p=self.firstCharColumn, w=w4 - 10)
        cmds.setParent(self.editableColumnsLayout)

        cmds.text(l="")
        self.envColumn = cmds.columnLayout(w=w4)
        self.firstEnvColumn = cmds.columnLayout(w=w4)
        cmds.textField('env1', p=self.firstEnvColumn, w=w4 - 10)
        cmds.setParent(self.editableColumnsLayout)

        cmds.text(l="")
        self.propsColumn = cmds.columnLayout(w=w4)
        self.firstPropsColumn = cmds.columnLayout(w=w)
        cmds.textField('props1', p=self.firstPropsColumn, w=w4 - 10)
        cmds.setParent(self.editableColumnsLayout)
        cmds.text(l="")

        cmds.setParent(mainLayout)

        self.bts.makeSeparator(h=10, w=w)

        cmds.rowColumnLayout(nc=3, cw=[(1, w / 3), (2, w / 3), (3, w / 3)])
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

        charNameColumn = cmds.scrollLayout('charNameColumn', p=self.charColumn, w=w, h=self.h1, hst=15, vst=15)
        chars = cmds.intField(self.numChar, q=True, v=True)

        for i in range(chars):
            id = "char" + str(i + 1)
            cmds.textField(id, w=w - 10)
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
            id = 'env' + str(i + 1)
            cmds.textField(id, w=w - 10)
            i += 1

        return envNameColumn

    def propsNameColumn(self, w, *args):

        if cmds.columnLayout(self.firstPropsColumn, q=True, exists=True):
            cmds.deleteUI(self.firstPropsColumn)

        if cmds.scrollLayout('propsNameColumn', q=True, exists=True):
            cmds.deleteUI('propsNameColumn')

        propsNameColumn = cmds.scrollLayout('propsNameColumn', p=self.propsColumn, w=w, h=self.h1, hst=15, vst=15)
        props = cmds.intField(self.numProps, q=True, v=True)

        for i in range(props):
            id = 'props' + str(i + 1)
            cmds.textField(id, w=w - 10)
            i += 1

        return propsNameColumn

    def setPth(self, *args):
        pth = cmds.fileDialog2(cap='set production path', fm=3, okc='Set')
        dir = self.getDirFromUnicode(pth[0])
        cmds.textField(self.setPath, edit=True, tx=dir)

    def createProject(self, *args):
        prjName = cmds.textField(self.prodName, q=True, tx=True)
        setPth = cmds.textField(self.setPath, q=True, tx=True)
        self.rootPth = os.path.join(setPth, prjName)

        if os.path.exists(self.rootPth):
            cmds.confirmDialog(t='Opps',
                               m='The path: %s\nis NOT EMPTY or:\nthis NAME has been USED for another project\n'
                                 'please choose another name' % self.rootPth, b='Ok')
            sys.exit()

        self.shortName = cmds.textField(self.prodShort, q=True, tx=True)

        self.modeSetting = cmds.optionMenu(self.setMode, q=True, v=True)

        self.numSeq = cmds.intField(self.numShot, q=True, v=True)
        self.numOfChar = cmds.intField(self.numChar, q=True, v=True)
        self.numOfEnv = cmds.intField(self.numEnv, q=True, v=True)
        self.numOfProps = cmds.intField(self.numProps, q=True, v=True)

        # Create content by set mode
        if self.modeSetting == 'Studio Mode':
            self.prjStudioMode()
        elif self.modeSetting == 'Group Mode':
            self.prjGroupMode()

    def prjStudioMode(self, *args):
        # Create master folder
        os.mkdir(self.rootPth)
        # Create content of master Folder
        master = ['assets', 'sequences', 'deliverables', 'documents', 'editorial', 'sound', 'resources', 'RnD']
        steps = ['publish', 'review', 'work']
        mayaFolders = ['scenes', 'sourceimages', 'images', 'movie', 'alembic', 'reference']

        for f in master:
            contentMasterPth = os.path.join(self.rootPth, f)
            os.mkdir(contentMasterPth)

        # Assets content
        assetsTasks = ['art', 'Modeling', 'surfacing', 'rigging']
        assetsSections = ['characters', 'environment', 'props']

        assetsPth = os.path.join(self.rootPth, 'assets')
        for section in assetsSections:
            assetsSectionsPth = os.path.join(assetsPth, section)
            os.mkdir(assetsSectionsPth)
            if section == 'characters':
                for i in range(self.numOfChar):
                    charName = 'char' + str(i + 1)
                    folCharName = cmds.textField(charName, q=True, tx=True)
                    if folCharName == "" or folCharName == None:
                        folCharName = 'character_' + str(i + 1)
                    folCharPth = os.path.join(assetsSectionsPth, folCharName)
                    os.mkdir(folCharPth)
                    for task in assetsTasks:
                        assetsTaskPth = os.path.join(folCharPth, task)
                        os.mkdir(assetsTaskPth)
                        for step in steps:
                            assetsTaskStepPth = os.path.join(assetsTaskPth, step)
                            os.mkdir(assetsTaskStepPth)
                        assetsWorkTaskPth = os.path.join(assetsTaskPth, 'work')
                        if task == 'art':
                            apps = ['photoshop', 'maya']
                        elif task == 'Modeling':
                            apps = ['zbrush', 'maya', 'mudbox', 'houdini']
                        elif task == 'surfacing':
                            apps = ['mari', 'maya', 'substance', 'photoshop']
                        elif task == 'rigging':
                            apps = ['maya']

                        for app in apps:
                            appPth = os.path.join(assetsWorkTaskPth, app)
                            os.mkdir(appPth)
                            if app == 'maya':
                                for f in mayaFolders:
                                    mayaPth = os.path.join(appPth, f)
                                    os.mkdir(mayaPth)
                    i += 1
            elif section == 'environment':
                for i in range(self.numOfEnv):
                    envName = 'env' + str(i + 1)
                    folEnvName = cmds.textField(envName, q=True, tx=True)
                    if folEnvName == "" or folEnvName == None:
                        folEnvName = 'env_' + str(i + 1)
                    folEnvPth = os.path.join(assetsSectionsPth, folEnvName)
                    os.mkdir(folEnvPth)
                    for task in assetsTasks:
                        assetsTaskPth = os.path.join(folEnvPth, task)
                        os.mkdir(assetsTaskPth)
                        for step in steps:
                            assetsTaskStepPth = os.path.join(assetsTaskPth, step)
                            os.mkdir(assetsTaskStepPth)
                        assetsWorkTaskPth = os.path.join(assetsTaskPth, 'work')
                        if task == 'art':
                            apps = ['photoshop', 'maya']
                        elif task == 'Modeling':
                            apps = ['zbrush', 'maya', 'mudbox', 'houdini']
                        elif task == 'surfacing':
                            apps = ['mari', 'maya', 'substance', 'photoshop']
                        elif task == 'rigging':
                            apps = ['maya']

                        for app in apps:
                            appPth = os.path.join(assetsWorkTaskPth, app)
                            os.mkdir(appPth)
                            if app == 'maya':
                                for f in mayaFolders:
                                    mayaPth = os.path.join(appPth, f)
                                    os.mkdir(mayaPth)
                    i += 1
            elif section == 'props':
                for i in range(self.numOfProps):
                    propsName = 'props' + str(i + 1)
                    folPropsName = cmds.textField(propsName, q=True, tx=True)

                    if folPropsName == "" or folPropsName == None:
                        folPropsName = 'props_' + str(i + 1)

                    folPropsPth = os.path.join(assetsSectionsPth, folPropsName)

                    os.mkdir(folPropsPth)
                    for task in assetsTasks:
                        assetsTaskPth = os.path.join(folPropsPth, task)
                        os.mkdir(assetsTaskPth)
                        for step in steps:
                            assetsTaskStepPth = os.path.join(assetsTaskPth, step)
                            os.mkdir(assetsTaskStepPth)
                        assetsWorkTaskPth = os.path.join(assetsTaskPth, 'work')
                        if task == 'art':
                            apps = ['photoshop', 'maya']
                        elif task == 'Modeling':
                            apps = ['zbrush', 'maya', 'mudbox', 'houdini']
                        elif task == 'surfacing':
                            apps = ['mari', 'maya', 'substance', 'photoshop']
                        elif task == 'rigging':
                            apps = ['maya']

                        for app in apps:
                            appPth = os.path.join(assetsWorkTaskPth, app)
                            os.mkdir(appPth)
                            if app == 'maya':
                                for f in mayaFolders:
                                    mayaPth = os.path.join(appPth, f)
                                    os.mkdir(mayaPth)
                    i += 1

        # Sequences content

        seqTask = ['anim', 'comp', 'fx', 'layout', 'lighting']

        sequencesPth = os.path.join(self.rootPth, 'sequences')
        for i in range(self.numSeq):
            folName = self.shortName + "_" + "shot_" + str(i + 1)
            seqPth = os.path.join(sequencesPth, folName)
            os.mkdir(seqPth)
            for task in seqTask:
                seqTaskPth = os.path.join(seqPth, task)
                os.mkdir(seqTaskPth)
                for step in steps:
                    seqTaskStepPth = os.path.join(seqTaskPth, step)
                    os.mkdir(seqTaskStepPth)
                seqTaskWorkPth = os.path.join(seqTaskPth, 'work')
                if task == 'anim':
                    apps = ['maya', 'after effect', 'houdini']
                elif task == 'comp':
                    apps = ['nuke', 'after effect', 'photoshop']
                elif task == 'fx':
                    apps = ['maya', 'houdini']
                elif task == 'layout':
                    apps = ['maya']
                elif task == 'lighting':
                    apps = ['maya']

                for app in apps:
                    appPth = os.path.join(seqTaskWorkPth, app)
                    os.mkdir(appPth)
                    if app == 'maya':
                        for f in mayaFolders:
                            mayaPth = os.path.join(appPth, f)
                            os.mkdir(mayaPth)
            i += 1

    def prjGroupMode(self, *args):
        pass

    def getDirFromUnicode(self, path, *args):
        for dirpath, dirnames, filenames in os.walk(path):
            return dirpath



# ----------------------------------------------------------------------------------------------------------- #
"""                                               END OF CODE                                               """
# ----------------------------------------------------------------------------------------------------------- #
