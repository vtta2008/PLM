"""
Script Name: DAMGsetup.py
Author: Do Trinh/Jimmy - TD artist

Description:
    It basically checkes all the files in folder to makes ure everthing is there. Then copy some files to folders
    as required like userSetup.py or saving the path of DAMG tool folder to sys.path for next use.
"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds # Maya Python command
import os
import sys
import json
import shutil
import getpass
import platform
import re
import logging # debug module to solve the version convention problem

# We can configure the current level to make it disable certain logs when we don't want it.
logging.basicConfig()
logger = logging.getLogger('DAMGsetup')
logger.setLevel(logging.DEBUG)

# *********************************************************************************************************** #
# ----------------------------------------------------------------------------------------------------------- #
"""                        MAIN CLASS: DAMGsetup - DAMG PIPELINE TOOL INSTALLATION                          """
# ----------------------------------------------------------------------------------------------------------- #
# *********************************************************************************************************** #

class DAMGsetup(object):
    # Get name of User
    user = getpass.getuser()

    # ---------------------------------------------------------
    # Get the path of current version of Maya in user computer
    user_prefs = cmds.internalVar(upd=True)
    user_workspaces = user_prefs + 'workspaces/'
    user_shelves = cmds.internalVar(ush=True)

    # ---------------------------------------------------------
    # From paths above store some variables of DAMG tool folder
    scrInstall = cmds.internalVar( usd=True ) + 'DAMGpipelineTool/'
    scrIcons_apps = scrInstall + 'icons/apps_icon/'
    scrIcons_mainUI = scrInstall + 'icons/mainUI_icon/'
    scrIcons_shelf = scrInstall + 'icons/Maya.Shelf.icon/'
    scrIcons_toolBox2 = scrInstall + 'icons/Maya.ToolBox2.icon/'
    scrLayout = scrInstall + 'layout/'
    scrPlugins = scrInstall + 'plugins/'
    scrModules = scrInstall + 'modules/'
    scrUserLibrary = scrInstall + 'userLibrary/'
    scrWorking = scrInstall + 'oldCode/'

    # ---------------------------------------------------------
    # Then put them all together in a dictionary
    pluginPth = {
        'master': scrInstall,
        'icons_apps': scrIcons_apps,
        'icons_mainUI': scrIcons_mainUI,
        'icons_shelf': scrIcons_shelf,
        'icons_toolBox2': scrIcons_toolBox2,
        'layout': scrLayout,
        'plugins': scrPlugins,
        'modules': scrModules,
        'userLibrary': scrUserLibrary,
        'oldCode': scrWorking
    }

    #file list in Installation folder
    icons_apps_lst = [ f for f in os.listdir( scrIcons_apps ) if f.endswith( '.png' ) or f.endswith( '.PNG' ) ]
    icons_mainUI_lst = [ f for f in os.listdir( scrIcons_mainUI ) if f.endswith('.png') or f.endswith( '.PNG' ) ]
    icons_shelf_lst = [ f for f in os.listdir( scrIcons_shelf ) if f.endswith('.png') or f.endswith( '.PNG' ) ]
    icons_toolBox2_lst = [ f for f in os.listdir( scrIcons_toolBox2 ) if f.endswith('.png') or f.endswith( '.PNG' ) ]
    layout_lst = [f for f in os.listdir( scrLayout ) if f.endswith( '.json' ) or f.endswith('.mel')]
    plugins_lst = [ f for f in os.listdir( scrPlugins ) if f.endswith( 'InitTool.py' ) or f.endswith( '.mel' ) ]
    modules_lst = [ f for f in os.listdir( scrModules ) if f.endswith( 'InitTool.py' ) ]
    userLibrary_lst = [f for f in os.listdir( scrUserLibrary) if f.endswith('.ma')]
    scrMaster_lst = [ f for f in os.listdir( scrInstall ) if f.endswith( 'InitTool.py' ) ]

    #---------------------------------------------------------
    # List file names for CHECK LIST
    # Icons check list
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

    # Plugin which always needs to go with DAMG tool
    plugins_checkLst = [ 'Qt.py' ]

    # ALl the modules of DAMG tool
    modules_checkLst = [  'DAMGchannelBox.py',
                          'DAMGdataInspection.py',
                          'DAMGfileManagerForMaya.py',
                          'DAMGfunctionsAppsTransfer.py',
                          'DAMGfunctionsToolForMaya.py',
                          'DAMGmasterToolControlMaya.py',
                          'DAMGprojectManager.py',
                          'DAMGtoolBoxI.py',
                          'DAMGtoolBoxII.py',
                          'DAMGtoolBoxIII.py' ]

    # Specific Library path for user in local pc, idealy you can save anything you are working for next use
    userLibrary_checkLst = []

    # Files in master folder
    scrMaster_checkLst = [ 'DAMGsetup.py', 'userSetup.py' ]

    # Layout file, only for maya 2017 and later
    layout_checkLst = [ 'DAMGlayout.json', 'shelf_DAMG.mel' ]

    # ---------------------------------------------------------
    # Store all the variables above to a dictionary
    checkList = { 'icons_apps': icons_apps_checkLst,
                  'icons_mainUI': icons_mainUI_checkLst,
                  'icons_shelf': icons_shelf_checkLst,
                  'icons_toolBox2': icons_toolBox2_checkLst,
                  'layout': layout_checkLst,
                  'plugins': plugins_checkLst,
                  'modules': modules_checkLst,
                  'userLibrary': userLibrary_checkLst,
                  'master': scrMaster_checkLst }

    fileList = { 'icons_apps': icons_apps_lst,
                 'icons_mainUI': icons_mainUI_lst,
                 'icons_shelf': icons_shelf_lst,
                 'icons_toolBox2': icons_toolBox2_lst,
                 'layout': layout_lst,
                 'plugins': plugins_lst,
                 'modules': modules_lst,
                 'userLibrary': userLibrary_lst,
                 'master': scrMaster_lst }

    # ---------------------------------------------------------
    # Make variables just in case you miss something.
    # Missing parts variable
    icons_apps_missing = []
    icons_mainUI_missing = [ ]
    icons_shelf_missing = [ ]
    icons_toolBox2_missing = [ ]
    layout_missing = []
    plugins_missing = []
    modules_missing = []
    userLibrary_missing = []
    scrmaster_missing = []

    file_missing = { 'icons_apps': icons_apps_missing,
                     'icons_mainUI': icons_mainUI_missing,
                     'icons_shelf': icons_shelf_missing,
                     'icons_toolBox2': icons_toolBox2_missing,
                     'layout': layout_missing,
                     'plugins': plugins_missing,
                     'modules': modules_missing,
                     'userLibrary': userLibrary_missing,
                     'master': scrmaster_missing}

    message_missing = [ ]

    #UI variables
    winSetupID = 'DAMGsetup'
    winTitle = 'DAMG pipeline tool v13 setup'
    text = 'Do you want to install DAMG Pipeline Tool v13 ?'
    width3 = 400
    blank = 10
    winWidth = width3 + (3 * blank)
    winHeight = winWidth / 3
    width7 = (winWidth - (4 * blank)) / 3
    cw3 = [ (1, blank), (2, width3), (3, blank) ]
    cw7 = [ (1, blank), (2, width7), (3, blank), (4, width7), (5, blank), (6, width7), (7, blank) ]

    def __init__(self):
        super(DAMGsetup, self).__init__()

        #self.buildUI()

        self.installTool()

    # -------------------------------------------
    # BUILD UI
    # -------------------------------------------
    def buildUI(self):
        """
        This will define a very simple Layout, just to get confirmation from user to start installing
        It also report if there is something wrong during the process.
        :return: 
                A window UI
        """
        text = "Do you want to intall DAMG pipeline tool v13 in your computer?"

        if cmds.window( self.winSetupID, q=True, exists=True ):
            cmds.deleteUI( self.winSetupID )
        cmds.window( self.winSetupID, t=self.winTitle, w=self.winWidth, h=self.winHeight )
        mlo = cmds.columnLayout( w=self.winWidth )

        cmds.rowColumnLayout( nc=3, cw=self.cw3 )
        cmds.text( l="" )
        cmds.text( 'showStatus', l=text, align='center', h=2 * self.winHeight / 3, w=self.winWidth )
        cmds.text( l="" )
        cmds.setParent( '..' )

        cmds.rowColumnLayout( nc=7, cw=self.cw7 )
        cmds.text( l="" )
        cmds.button( l='Install', w=self.width7, c=self.installTool)
        cmds.text( l="" )
        cmds.button( l='Repair', w=self.width7, c=self.repairTool)
        cmds.text( l="" )
        cmds.button( l='Close', w=self.width7, c=self.stopInstallation)
        cmds.text( l="" )
        cmds.setParent( mlo )
        cmds.text(l="", h=10)

        cmds.showWindow( self.winSetupID )

    # installation precess
    def stopInstallation(self, *args):
        cmds.deleteUI( self.winSetupID )
        return

    def repairTool(self, *args):
        pass

    def installTool(self, *args):
        self.checkAllFiles()
        self.setupFolderAndPath()
        self.applyToolPathIntoSystem()
        self.dataInstpection()
        # print " "
        # print "Installation finishes, thank you for using DAMGteam's product\nHave fun!"
        # print " "

    def showMissing(self):
        message = ""
        for m in self.message_missing:
            message = 'missing file: ' + message + m + "; \n"
        self.warningMessage( message=message )
        sys.exit()

    def copyFiles(self, userSetup, folderPackpage, qtModule):
        # destination path
        userSetup_pth = self.user_prefs + 'scripts/' + userSetup
        folderPackpage_pth = self.user_prefs + 'scripts/' + folderPackpage
        qtModule_pth = self.user_prefs + 'scripts/' + qtModule

        #source path
        scrUserSetup_pth = self.scrInstall + userSetup
        scrfolderPackpage_pth = self.scrInstall + folderPackpage
        scrQtModule_pth = self.scrPlugins + qtModule

        source = [ scrUserSetup_pth, scrfolderPackpage_pth, scrQtModule_pth ]
        destination = [ userSetup_pth, folderPackpage_pth, qtModule_pth ]

        for i in range(len(destination)):
            if os.path.exists(destination[i]):
                #message = "file '%s' is already in '%s'" % (name[i], destination[i])
                #print message
                pass
            else:
                shutil.copy2(source[i], destination[i])
            i += 1

    def warningMessage(self, message="None"):
        cmds.confirmDialog(
            t = 'Warning',
            m = (
                "Could not install because those files/folders are missing: \n"
                + message +
                "please re-download the tool and start it over. \n"
                ),
            b = 'OK'
        )
        cmds.warning(message)

    def checkAllFiles(self):
        self.message_missing = []
        for path in self.checkList:
            for file in self.checkList[path]:
                if file in self.fileList[path]:
                    #text = "%s checkd, exist." % (self.pluginPth[path] + file)
                    #print text
                    continue
                else:
                    text = "missing %s in %s" % (file, self.pluginPth[path ])
                    #print text
                    self.message_missing.append("%s in %s" % (file, self.pluginPth[path ]) )

        if self.message_missing==[]:
            text = "Finish checking, all files are there"
            logger.info(text)
        else:
            self.showMissing()

    def setupFolderAndPath(self, **info):
        infoFileName = 'infoPath'
        infoUserName = 'infoUser'
        toolPath = os.path.join(self.user_prefs, 'scripts/%s.json' % infoFileName)
        userPath = os.path.join(self.scrUserLibrary, '%s.json' % infoUserName)
        infoPath = {}
        infoUser = {}

        values = {}
        cache = os.popen2( "SYSTEMINFO" )
        source = cache[ 1 ].read()
        sysOpts = [ "Host Name", "OS Name", "OS Version", "Product ID", "System Manufacturer", "System Model",
                    "System type", "BIOS Version", "Domain", "Windows Directory", "Total Physical Memory",
                    "Available Physical Memory", "Logon Server" ]

        infoUser[ 'source folder' ] = self.scrInstall
        infoUser[ 'user name' ] = self.user
        infoUser[ 'artist name' ] = platform.node()
        infoUser[ 'operating system' ] = platform.system() + "/" + platform.platform()
        infoUser[ 'python version' ] = platform.python_version()

        for opt in sysOpts:
            values[ opt ] = [ item.strip() for item in re.findall( "%s:\w*(.*?)\n" % (opt), source, re.IGNORECASE ) ][
                0 ]

        for item in values:
            infoUser[item] = values[item]

        with open(userPath, 'w') as f:
            json.dump(infoUser, f, indent=4)

        for name in self.pluginPth:
            path = self.pluginPth[ name ]
            infoPath[ name ] = path
            if not path in sys.path:
                sys.path.append( path )

        with open(toolPath, 'w') as f:
            json.dump(infoPath, f, indent=4)

        logger.info( 'Saving file to %s' % toolPath )

        userSetup = 'userSetup.py'
        folderPackpage = '__init__.py'
        qtModule = 'Qt.py'

        self.copyFiles(userSetup, folderPackpage, qtModule)

    def applyToolPathIntoSystem(self):
        scrData = cmds.internalVar( upd=True ) + 'scripts/infoPath.json'
        if os.path.exists( scrData ):
            with open( scrData, 'r' ) as f:
                paths = json.load( f )
            for path in paths:
                if os.path.exists( paths[ path ] ):
                    if not paths[ path ] in sys.path:
                        sys.path.append( paths[ path ] )
                        #print "%s: (%s) has been appended to system path" % (path, paths[ path ])
                    else:
                        #print "section %s: (%s) already in system path, ignore" % (path, paths[ path ])
                        pass
                else:
                    continue

    def dataInstpection(self):
        from DAMGmodules import DAMGdataInspection
        reload( DAMGdataInspection )
        DAMGdataInspection.DAMGinspectionData()