#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: MayaVariables.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
print("Import from modules: {file}".format(file=__name__))
print("Directory: {path}".format(path=__file__.split(__name__)[0]))
__root__ = "PLT_RT"
# -------------------------------------------------------------------------------------------------------------
""" Import """

import datetime
import platform

from maya import cmds

MAYAENVPTH = os.path.join(cmds.internalVar(usd=True).split('scripts')[0], 'Maya.env')

MAYAVERSION = int(cmds.about(v=True))

MAINVAR = dict(

    dir = 'PipelineTool/scrInfo',

    user = platform.node(),

    url = ['https://www.continuum.io/downloads', ],

    TD=[ 'Maya', '3Ds max', 'Mudbox', 'Houdini FX', 'ZBrush', 'Mari' ],

    UV=[ 'UVLayout' ],

    Sound=[ 'Audition' ],

    Comp=[ 'NukeX', 'Hiero', 'After Effects', 'Premiere Pro' ],

    Design=[ 'Photoshop', 'Illustrator', 'InDesign' ],

    Office=[ 'Word', 'Excel', 'PowerPoint' ],

    envKey = ['LOCALAPPDATA', 'SYSTEMINFO', 'PYTHONHOME', 'PROGRAMDATA'],

    subKey = 'Local',

    os = ['sys.config', 'os.config', 'path.config', 'timelog.sch', 'webs.pipeline'],

    job=[ 'TD', 'Comp', 'Design', 'Office', 'UV', 'Sound'],

    filter=[ 'Non-commercial', 'Uninstall', 'Verbose', 'License', 'Skype' ],

    sysOpt = ["Host Name", "OS Name", "OS Version", "Product ID", "System Manufacturer", "System Model",
              "System type", "BIOS Version", "Domain", "Windows Directory", "Total Physical Memory",
              "Available Physical Memory", "Logon Server"],

    id = ['ChannelBox', 'MayaFuncs', 'MayaMainUI', 'MayaPythonProc', 'MayaVariables', 'OsPythonProc',
          'ProdFolder', 'ProjectManager', 'toolBoxI', 'toolBoxII', 'toolBoxIII', 'toolBoxIV', 'DataHandle', 'InitTool'],

    ext=[ '.exe', '.py', '.lnk' ],

    py=[ 'utilities', 'ui', 'plugins', '' ],

    maya = ['maya.user', 'maya.os', 'maya.os'],

    mayaLayout = ['plt.json', 'shelf_plt.mel'],

    mayaRoot = ['userSetup.py', 'InitTool.py'],

    mayaModule = ['ChannelBox.py', 'MayaFuncs.py', 'MayaMainUI.py', 'MayaPythonProc.py', 'MayaVariables.py',
                  'OsPythonProc.py', 'ProdFolder.py', 'ProjectManager.py', 'ToolBoxI.py', 'ToolBoxII.py',
                  'ToolBoxIII.py', 'ToolBoxIV.py','DataHandle_studio.py', ],

    mayaPlugin = ['Qt.py',],

    mayaIcon = ['After Effects CC.icon.png', 'Hiero.icon.png', 'Houdini FX.icon.png', 'Illustrator CC.icon.png',
                      'Mari.icon.png', 'Mudbox 2017.icon.png', 'NukeX.icon.png', 'Photoshop CC.icon.png',
                      'Premiere Pro CC.icon.png', 'ZBrush 4R7.icon.png', 'cam.icon.png', 'clock.icon.png',
                      'createMayaFolder.icon.png', 'toolboxIV.icon.png', 'graphEditor.icon.png', 'hypershader.icon.png',
                      'nodeEditor.icon.png', 'obj.icon.png','openLoad.icon.png', 'openProjectFolder.icon.png',
                      'openPublishFolder.icon.png', 'openSceneFolder.icon.png', 'openSnapShotFolder.icon.png',
                      'openSourceimagesFolder.icon.png','outliner.icon.png', 'pluinManager.icon.png',
                      'projectManager.icon.png', 'publish.icon.png','Refresh.icon.png', 'renderSetting.icon.png',
                      'scriptEditor.icon.png', 'setProject.icon.png', 'snapshot.icon.png', 'toolboxI.icon.png',
                      'toolboxII.icon.png', 'toolboxIII.icon.png', 'uvEditor.icon.png', 'vrayVFB.icon.png',
                      'toolboxIV.shelf.icon.png', 'openload.shelf.icon.png', 'publish.shelf.icon.png',
                      'setup.shelf.icon.png', 'snapshot.shelf.icon.png', 'toolboxI.shelf.icon.png',
                      'toolboxII.shelf.icon.png', 'toolboxIII.shelf.icon.png', 'tool.shelf.icon.png',
                      'axisRotation.icon.png', 'twoAxisRotation.icon.png', 'twoDboldCircle.icon.png',
                      'twoDcircleArrow.icon.png', 'twoDirections.icon.png', 'twoDstyleArrow.icon.png',
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
                      'zigZagCircle.icon.png', 'spreadsheet.icon.png','channelBox.icon.png',],

    mayaExt = ['.png', '.jpg', '.py', '.mel', '.ma', '.psd', '.exr'],

    mayaLabel = ['Channel Box', "Pipeline Tool",'','','','','','', '','All About Controller'],

    mayaVersion = MAYAVERSION,

    mayaRootDir = cmds.internalVar(usd=True),

    mayaIconDir = cmds.internalVar(ubd=True),

    mayaEnvPth = MAYAENVPTH,
)

TITLE = dict(
    NoPythonInstall = 'No Python installation found',

    waitForUpdate = 'Wait for update',

)

MESSAGE = dict(

    NoPythonInstall =
"""
                         
You do not have external Python installed in your computer.
Some functions may not work, I recommend you install Ananconda 
Python 2.7. You can download it for free at:
    
    'https://www.continuum.io/downloads'
                      
""",

    missingModule =
"""
Missing module: 
    
""",

    canNotFindIt = "Could not find the ",

    notInstalledTool = """ You have not installed Pipeline Manager yet, please install it, thank you """,

    waitForUpdate =
"""
this function is currenly under construction, please wait for next update.             
JimJim  
""",
    mainUIabout =
"""
Thank you for using DAMG products.
Built and developed by JimJim - DoTrinh

Special thank to lectures and friends in Media Design School:

Oliver Hilbert
Brian Samuel
Kelly Bechtle-Woods

Brandon Hayman
    
A big thank to DAMG team's members:

Duong Minh Duc & Tran Huyen Trang
    
for any question or feedback, email me at: dot@damgteam.com
"""
)



ICONS = os.path.join(os.getenv(__root__), 'imgs', 'maya.icon')

# Get common data directory for every apps
def getScrPth(mainVar):
    localAppDir = os.getenv( mainVar[ 'envKey' ][3])

    pipelineDataPth = os.path.join( localAppDir, mainVar['dir'] )
    if not os.path.exists( pipelineDataPth ):
        os.mkdir( pipelineDataPth )
    return pipelineDataPth

def getDate():
    t = datetime.datetime.timetuple(datetime.datetime.now())
    date = '%s/%s/%s' % (str(t.tm_mday), str(t.tm_mon), str(t.tm_year))
    return date

def getTime():
    t = datetime.datetime.timetuple( datetime.datetime.now() )
    time = '%s:%s' % (str(t.tm_hour), str(t.tm_min))
    return time

def createLog(apps, event='log in', data=MAINVAR):
    SCRPTH = getScrPth(MAINVAR)

    d = getDate()
    t = getTime()

    content = d + ': ' + data['user'] + ': ' + event + ' ' + apps.upper() + ' at ' + t + '\n'

    log = os.path.join(SCRPTH, data['os'][3])

    with open(log, 'a+' ) as f:
        f.write(content)

# -------------------------------------------------------------------------------------------------------------
# END OF CODE
# -------------------------------------------------------------------------------------------------------------