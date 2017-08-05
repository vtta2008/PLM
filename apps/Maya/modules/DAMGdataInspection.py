"""
Script Name: DAMGdataInspection.py
Author: Do Trinh/Jimmy - TD artist

Description:
    This is the procedure will run before start building UI, another inspection
    to make sure everything is updated.

"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import maya.cmds as cmds
import maya.mel as mel
import os, sys, json

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
VERSION = int(cmds.about(v=True))

# *********************************************************************************************************** #
# ----------------------------------------------------------------------------------------------------------- #
"""                        MAIN CLASS: DAMG DATA INSPECTION                                                 """
# ----------------------------------------------------------------------------------------------------------- #
# *********************************************************************************************************** #

class DAMGinspectionData( object ):

    user_prefs = cmds.internalVar(upd=True)

    user_scripts = user_prefs + 'scripts/'

    modules_checkList = ['DAMGchannelBox.py',
                         'DAMGdataInspection.py',
                         'DAMGfileManagerForMaya.py',
                         'DAMGfunctionsAppsTransfer.py',
                         'DAMGfunctionsToolForMaya.py',
                         'DAMGmasterToolControlMaya.py',
                         'DAMGprojectManager.py',
                         'DAMGtoolBoxI.py',
                         'DAMGtoolBoxII.py',
                         'DAMGtoolBoxIII.py', ]

    icons_apps_checkLst = ['DAMGaftereffecticon.png', 'DAMGhieroicon.png', 'DAMGhoudiniicon.png', 'DAMGillustratoricon.png',
                           'DAMGmariicon.png', 'DAMGmudboxicon.png', 'DAMGnukexicon.png', 'DAMGphotoshopicon.png',
                           'DAMGpremiereicon.png', 'DAMGzbrushicon.png']

    icons_mainUI_checkLst = ['camera.icon.png', 'clock.icon.png', 'createMayaFolder.icon.png', 'gotoapp.icon.png',
                             'graphEditor.icon.png', 'hypershader.icon.png', 'nodeEditor.icon.png', 'object.icon.png',
                             'openLoad.icon.png', 'openProjectFolder.icon.png', 'openPublishFolder.icon.png',
                             'openSceneFolder.icon.png', 'openSnapShotFolder.icon.png', 'openSourceimagesFolder.icon.png',
                             'outliner.icon.png', 'pluinManager.icon.png', 'projectManager.icon.png', 'publish.icon.png',
                             'refresh.icon.png', 'renderSetting.icon.png', 'scriptEditor.icon.png', 'setProject.icon.png',
                             'snapshot.icon.png', 'toolboxI.icon.png', 'toolboxII.icon.png', 'toolboxIII.icon.png',
                             'uvEditor.icon.png', 'vrayVFB.icon.png']

    icons_shelf_checkLst = ['gotoapp.shelf.icon.png', 'openload.shelf.icon.png', 'publish.shelf.icon.png',
                             'setup.shelf.icon.png', 'snapshot.shelf.icon.png', 'toolboxI.shelf.icon.png',
                             'toolboxII.shelf.icon.png', 'toolboxIII.shelf.icon.png', 'tool.shelf.icon.png']

    icons_toolBox2_checkLst = ['axisRotation.icon.png', 'twoAxisRotation.icon.png', 'twoDboldCircle.icon.png',
                               'twoDcircleArrowicon.png', 'twoDirections.icon.png', 'twoDstyleArrow.icon.png',
                               'threeDcircleArrow.icon.png', 'threeDstyleArrow.icon.png', 'fourSidesArrow.icon.png',
                               'fiveWingsFan.icon.png', 'arrowBothSide.icon.png', 'arrowCurve.icon.png',
                               'bearFootControl.icon.png', 'boldPlusNurbs.icon.png', 'circlePlus.icon.png',
                               'clockArrowDown.icon.png', 'clockArrowUp.icon.png', 'crossControl.icon.png',
                               'crownCurve.icon.png', 'cubeCurve.icon.png', 'cubeOnBase.icon.png',
                               'cylinderCurve.icon.png', 'diamond.icon.png', 'earControl.icon.png',
                               'eyeControl.icon.png', 'femaleSymbol.icon.png', 'fishNail.icon.png',
                               'fistCurve.icon.png', 'footControl1.icon.png', 'footControl2.icon.png',
                               'halfSphere.icon.png', 'handNurbs.icon.png', 'headJawControl.icon.png',
                               'lipControl.icon.png', 'locatorControl.icon.png', 'maleSymbol.icon.png',
                               'masterControl.icon.png', 'moveControl1.icon.png', 'moveControl2.icon.png',
                               'nailArrowDown.icon.png', 'nailArrowUp.icon.png', 'orginControl.icon.png',
                               'plusNurbs.icon.png', 'pointNote.icon.png', 'pyramid.icon.png',
                               'rotationControl.icon.png', 'singleRotateControl.icon.png', 'sliderControl.icon.png',
                               'sphereControl.icon.png', 'sphereSquare.icon.png', 'spikeCrossControl.icon.png',
                               'tongueControl.icon.png', 'twoWayArrow.icon.png', 'upperLipControl.icon.png',
                               'zigZagCircle.icon.png']

    keys = ['master', 'icons_apps', 'icons_mainUI', 'icons_shelf', 'icons_toolBox2', 'layout', 'plugins',
                 'modules', 'userLibrary', 'oldCode']


    DAMGtoolPth = {}

    def __init__(self):
        self.checkAndReUpdateInfoPath()

        self.checkFiles( path=self.DAMGtoolPth[ 'modules' ], ext="InitTool.py", checkList=self.modules_checkList )
        self.checkFiles( path=self.DAMGtoolPth[ 'icons_apps' ], ext=".png", checkList=self.icons_apps_checkLst )
        self.checkFiles( path=self.DAMGtoolPth[ 'icons_mainUI' ], ext=".png", checkList=self.icons_mainUI_checkLst )
        self.checkFiles( path=self.DAMGtoolPth[ 'icons_shelf' ], ext=".png", checkList=self.icons_shelf_checkLst )
        self.checkFiles( path=self.DAMGtoolPth[ 'icons_toolBox2' ], ext=".png", checkList=self.icons_toolBox2_checkLst )

        print "finish Checking, thank you for using DAMG team product."

        self.loadDAMGmainUI()

    def loadDAMGmainUI(self, version=VERSION):
        from DAMGmodules import DAMGmasterToolControlMaya
        reload( DAMGmasterToolControlMaya )
        DAMGmasterToolControlMaya.DAMGmasterToolControlMaya()
        if version>=2017:
            self.changeCurrentLayout()
        else:
            pass

    def changeCurrentLayout(self, layoutName = 'DAMGlayout'):
        layoutExt = '.json'
        layoutPth = cmds.internalVar( upd=True ) + 'workspaces/'
        DAMGlayout = layoutPth + layoutName + layoutExt

        if not os.path.exists( DAMGlayout ):
            DAMGlayout = self.DAMGtoolPth[ 'layout' ] + layoutName + layoutExt

        layouts = cmds.workspaceLayoutManager( listLayouts=True )

        for layout in layouts:
            if layoutName in layout:
                cmds.workspaceLayoutManager( i=DAMGlayout, sc=layoutName )

        mel.eval( 'onSetCurrentLayout "DAMGpipelineTool";' )

    def checkAndReUpdateInfoPath(self, version=VERSION):
        names = [ 'infoPath.json', 'userSetup.py', '__init__.py', 'Qt.py' ]

        for name in names:
            self.getToolPath( name=name )

        jsonPth = self.user_scripts + names[ 0 ]

        with open( jsonPth, 'r' ) as f:
            self.DAMGtoolPth = json.load( f )

        for key in self.DAMGtoolPth:
            if not key in self.keys:
                message = "info in file: '%s' in: '%s' isn't right, please restart Maya" % (names[0], self.user_scripts)
                self.warningMessage(message)
                sys.exit()
            else:
                continue

        for path in self.DAMGtoolPth:
            if not self.DAMGtoolPth[ path ] in sys.path:
                sys.path.append( self.DAMGtoolPth[ path ] )
            else:
                continue

    def checkFiles(self, path=None, ext=None, checkList=None):
        fileList = [ f for f in os.listdir( path ) if f.endswith( ext ) or f.endswith(ext.upper())]
        file_missing = [ ]
        print ""
        print "start checking files in '%s'" % path
        print ""
        for file in checkList:
            if file in fileList:
                print "%s%s exists" % (path, file)
                continue
            else:
                file_missing.append( file )
        if len( file_missing ) > 0:
            message = "Missing files: \n"
            for m in file_missing:
                message = message + m + "\n"
            message = message + 'It should be in %s \n' % self.DAMGtoolPth[ 'modules' ]
            self.warningMessage( message=message )
            sys.exit()
        else:
            print ""
            print "finish checking in '%s', all files there" % path
            print ""
            pass

    def getToolPath(self, name=""):
        path = self.user_scripts + name
        if not os.path.exists( path ):
            message = ("Opps, it is like the file '%s' in '%s' has been moved or deleted.\n"
                       + "Please reinstall DAMG pipeline tool") % (name, path)
            self.warningMessage( message=message )
            sys.exit()
        else:
            pass

    def warningMessage(self, message=""):
        cmds.confirmDialog(
            t = 'Warning',
            m = message,
            b = 'OK'
        )
        cmds.warning(message)