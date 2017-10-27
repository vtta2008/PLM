# -*-coding:utf-8 -*

"""


"""

from maya import cmds, mel
import maya.OpenMaya as om
from functools import partial

import os, sys, logging, shutil

from Maya_tk.modules import MayaVariables as var
NAMES = var.MAINVAR
SCRPTH = os.path.join(os.getenv('PROGRAMDATA'), 'Pipeline Tool/scrInfo')
ICONS = var.ICONS
TITLE = var.TITLE
MESSAGE = var.MESSAGE

WIDTH = 450
ICONWIDTH = 30

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
if Qt.__binding__=='PySide':
    logger.debug('Using PySide with shiboken')
    from shiboken import wrapInstance
    from Maya_tk.plugins.Qt.QtCore import Signal
elif Qt.__binding__.startswith('PyQt'):
    logger.debug('Using PyQt with sip')
    from sip import wrapinstance as wrapInstance
    from Maya_tk.plugins.Qt.QtCore import pyqtSignal as Signal
else:
    logger.debug('Using PySide2 with shiboken2')
    from shiboken2 import wrapInstance
    from Maya_tk.plugins.Qt.QtCore import Signal

def geticon(icon):
    iconPth = os.path.join(os.getcwd(), 'Maya_tk/icons')
    path = os.path.join(iconPth, icon)
    return path

def clearOptionMenu(name, *args):
    #Option menus are tiresome because you have to use its full name as parent name
    optionMenuFullName = None
    try:
        menuItems = cmds.optionMenu(name, q = True, ill = True)

        if menuItems != None and menuItems != []:
            cmds.deleteUI(menuItems)

        firstItem = menuItems[0]
        optionMenuFullName = firstItem[:-len(firstItem.split('|')[-1])-1]  #strip out the child menu item name along with its preceeding "|" symbol.
    except:
        pass

    return optionMenuFullName

def refreshCamList(name, *args):
    menuOption = clearOptionMenu(name)

    camLst = cmds.ls(type='camera')
    for cam in camLst:
        cmds.menuItem(l=cam, parent=menuOption)

def resizeImage(sourceImage, outputImage, width, height):

    image = om.MImage()
    image.readFromFile(sourceImage)

    image.resize( width, height )
    image.writeToFile( outputImage, 'png')

def importCamTemp(*args):
    tempPth = os.path.join(cmds.internalVar(usd=True), 'templateData')
    if not os.path.exists(tempPth):
        cmds.sysFile(tempPth, md=True)

def showAllHideLayers(visible, *args):

    allLayers = cmds.ls( type='displayLayer' )

    if not visible:
        visible = True
    else:
        visible = False

    for i in range( len( allLayers ) ):
        cmds.setAttr( allLayers[ i ] + '.visibility', visible )

def trackingCommand(*args):
    if cmds.window('Command detect', query=True, exists=True):
        cmds.deleteUI('Command detect')

    cmds.window('Command detect')
    cmds.columnLayout()
    cmds.cmdScrollFieldReporter( width=400, height=100 )
    cmds.showWindow('Command detect')

def openScriptEditor(*args):
    try:
        mel.eval( 'charcoalEditor' )
    except RuntimeError:
        pass
    else:
        mel.eval('ScriptEditor;')

def customViewer(*args):
    from Maya_tk.modules import CustomViewer
    reload( CustomViewer )

    resolution = {'HD 720': [1280, 720], 'HD 1080': [1920, 1080], 'HD 540': [960, 540]}
    res = cmds.optionMenu('resViewPanel', q=True, v=True)

    w = resolution[res][0]
    h = resolution[res][1]
    cam = cmds.optionMenu('camListPanel', q=True, v=True)
    CustomViewer.CustomViewer(cam, w, h)

def layerManagerUI(*args):
    from Maya_tk.modules import LayerManager
    reload(LayerManager)
    LayerManager.LayerManager()

def demoButton(*args):
    l='Demo Button'
    c=waitforupdate
    button = cmds.button(l=l, c=c)
    return button

def setSymbolCheckable(ids, anns, ccs, types, icons, w=ICONWIDTH, *args):
    """
    Make a checkable symbol button
    :param ids: set id for button (list)
    :param anns: annotation of button (list)
    :param ccs: command for button when click (list)
    :param w: width of button, also is the high
    :return: a symbol check box button
    """
    for i in range(len(ids)):
        # get icon path from default path
        icon = geticon(icons[i])
        cmd = ccs[i]
        var = types[i]
        cc = partial(cmd, var)
        cmds.symbolCheckBox(ids[i],ann=anns[i],i=icon,cc=cc,v=True,w=w,h=w)
        i+=1

def makeSeparator(h, w, hr=True, style='in', *args):
    """
    make a separator to divide sections in layout
    :param h: height
    :param w: width
    :param hr:
    :return:
    """
    if not hr:
        cmds.separator(style=style, h=h, hr=hr)
    else:
        cmds.text( l="", h=h )
        cmds.separator( style=style, w=w)
        cmds.text( l="", h=h )

def iconButton(ann, icon, command, wh=ICONWIDTH, *args):
    """
    Make a single icon button
    :param ann: annotation
    :param icon: icon name
    :param wh: width and high
    :return: an icon button
    """
    image = geticon(icon)
    cmds.symbolButton(ann=ann, i=image, c=command, h=wh, w=wh)

def setIconButton(anns, commands, icons, width=ICONWIDTH, *args):
    """
    Make multiple icon buttons
    :param cmd: list of command
    :param ic: list of icon name file
    :param tt: list of tool tip (annotation)
    :param w: width
    :return: multi icon buttons
    """
    num = len(anns)
    for i in range(num):
        command = commands[i]
        iconButton(anns[i], geticon(icons[i]), command, width)
        i+=1

def makeAcoolButton(ann, label, cmd, *args):
    """
    Make a styled button
    :param label: button name
    :param cmd: command for button
    :return:
        button with a border
    """
    cmds.frameLayout( bv=True, lv=False )
    cmds.button(ann=ann, l=label, c=cmd )
    cmds.setParent( '..' )

def setCoolButton(anns, commands, labels, *args):
    for i in range(len(anns)):
        makeAcoolButton(ann=anns[i], label=labels[i], cmd=commands[i])
        i+=1

def refreshBtn(command, wh=25, *args):
    iconButton("Refresh", geticon('refresh.icon.png'), command, wh=wh)

def cwE(nc, w, adj, *args):
    """
    Create column width profile for cmds.rowColumnlayout command
    :param nc: number of columns
    :param w: total width of whole layout
    :param adj: adjustment number to fit all columns to layout
    :return:
    column width
    """
    width = (w-adj)/nc
    cw = []
    for i in range(nc):
        columnID = i+1
        cw.append((columnID, width))
    return cw

def cwCustomize(nc, widthList, *args):
    cw = []
    for i in range(nc):
        id = i+1
        width = widthList[i]
        column = (id, width)
        cw.append(column)
        i+=1
    return cw

def waitforupdate(*args):
    key = 'waitForUpdate'
    cmds.confirmDialog( t=TITLE[key], m=MESSAGE[key], b="OK")

def warningFunc(key, *args):
    message = MESSAGE[key]
    title = TITLE[key]
    cmds.confirmDialog(t=title, m=message, b='OK')
    cmds.warning(message)
    logger.info(message)

def reloadDataMainUI(*args):
    from Maya_tk import InitTool
    reload(InitTool)
    InitTool.initilize()

def refreshMainUI(*args):
    from Maya_tk.modules import MayaMainUI
    reload(MayaMainUI)
    MayaMainUI.MayaMainUI()

def newProd(*args):
    from Maya_tk.modules import ProdFolder
    reload( ProdFolder )
    ProdFolder.ProdFolder()

def lightManager(*args):
    from Maya_tk.modules import toolBoxIII
    reload( toolBoxIII )
    toolBoxIII.showUI()

def channelBoxUI(*args):
    from Maya_tk.modules import ChannelBox
    reload(ChannelBox)
    ChannelBox.ChannelBox()

def toolBoxI(*args):
    from Maya_tk.modules import toolBoxI
    reload( toolBoxI )
    toolBoxI.DAMGtoolBoxI()

def createGear(*args):
    from Maya_tk.modules.modeling import gearCreator
    reload(gearCreator)
    gearCreator.gear()

def toolBoxII(*args):
    from Maya_tk.modules import toolBoxII
    reload( toolBoxII )
    toolBoxII.DAMGtoolBoxII()

def toolBoxIII(*args):
    from Maya_tk.modules import toolBoxIII
    reload( toolBoxIII )
    toolBoxIII.toolBoxIII()

def toolBoxIV(*args):
    from Maya_tk.modules import toolBoxIV
    reload( toolBoxIV )
    toolBoxIV.toolBoxIV()

def publishUI(*args):
    from Maya_tk.modules import DataHandle_studio
    reload(DataHandle_studio)
    DataHandle_studio.DataHandle().publishUI()

def loaderUI(*args):
    from Maya_tk.modules import DataHandle_studio
    reload(DataHandle_studio)
    DataHandle_studio.DataHandle().loaderUI()

def snapshotUI(*args):
    from Maya_tk.modules import DataHandle_studio
    reload(DataHandle_studio)
    DataHandle_studio.DataHandle().snapshotUI()

def projManagerUI(*args):
    from Maya_tk.modules import ProjectManager
    reload( ProjectManager )
    ProjectManager.projectManager()

def groupCenter(*args):
    a = cmds.ls( sl=True )
    cmds.group( n=a[ 0 ] + "_group" )

def deleteHis(*args):
    a = cmds.ls( sl=True )
    if (len( a ) > 0):
        cmds.DeleteHistory()

def freezeTransformation(*args):
    a = cmds.ls( sl=True )
    if (len( a ) > 0):
        cmds.makeIdentity( apply=True )

def format_bytes(bytes_num=0, *args):
    sizes = [ "B", "KB", "MB", "GB", "TB" ]
    i = 0
    dblbyte = bytes_num
    while (i < len( sizes ) and bytes_num >= 1024):
        dblbyte = bytes_num / 1024.0
        i = i + 1
        bytes_num = bytes_num / 1024
    size = str( round( dblbyte, 2 ) ) + " " + sizes[ i ]
    return size

def openVrayVFB(*args):
    cmds.loadPlugin( "vrayformaya", quiet=True )
    cmds.pluginInfo( 'vrayformaya', edit=True, autoload=True )
    cmds.setAttr("defaultRenderGlobals.currentRenderer", "vray", type="string")
    cmds.vray("showVFB")

def openProjFolder(*args):
    projPth = cmds.workspace(q=True, rd=True)
    cmds.launch(dir=projPth)

def openSceneFolder(*args):
    projPth = cmds.workspace(q=True, rd=True)
    scenePth = os.path.join(projPth, "scenes")
    cmds.launch(dir=scenePth)

def openSourceimagesFolder(*args):
    projPth = cmds.workspace(q=True, rd=True)
    sourceImagesPth = os.path.join(projPth, "sourceimages")
    cmds.launch(dir=sourceImagesPth)

def openSnapShotFolder(*args):
    projPth = cmds.workspace(q=True, rd=True)
    snapShotPth = os.path.join(projPth, "scenes/snapShot")
    os.startfile(snapShotPth)

def openPublishFolder(*args):
    projPth = cmds.workspace(q=True, rd=True)
    publishPth = os.path.join(projPth.split('work')[0], "publish/maya")
    os.startfile(publishPth)

def centerPivot(*args):
    curSel = cmds.ls(sl=True)
    if ( len(curSel) > 0 ):
        cmds.xform(cp=True)

def gotoObjectmod(*args):
    curSel = cmds.ls(sl=True)
    if ( len(curSel) > 0 ):
        pick1st = curSel[0]
        ioF = pick1st.index('f')-1
        objName = pick1st[0:ioF]
        cmds.select(objName, r=1)

def Chop(*args):
    curSel = cmds.ls(sl=True)
    if ( len(curSel) > 0 ):
        cmds.polyChipOff(ch=1, kft=1, dup=0, off=0)
        gotoObjectmod()
        cmds.polySeparate()
    else:
        print "nothing selected, please select faces"

def normalOnOff(*args):
    a = cmds.ls(sl=True)
    if ( len(a) > 0 ):
        cmds.ToggleFaceNormalDisplay()

def reverseNormal(*args):
    a = cmds.ls(sl=True)
    if ( len(a) > 0 ):
        cmds.polyNormal(nm=0)

def ChildSel(*args):
    a = cmds.ls(sl=True)
    if ( len(a) > 0 ):
        cmds.select(hi=True)

def JointOff(*args):
    JointsSel = cmds.ls(sl=True)
    Joints = []
    for item in JointsSel:
        Joints.append(item)
    NumOfJoints = int(len(JointsSel))
    for i in range(NumOfJoints):
        JointsName = Joints[i]
        cmds.setAttr(JointsName + '.displayLocalAxis',0)
        i+=1
    
def JointOn(*args):
    JointsSel = cmds.ls(sl=True)
    Joints = []
    for item in JointsSel:
        Joints.append(item)
    NumOfJoints = int(len(JointsSel))
    for i in range(NumOfJoints):
        JointsName = Joints[i]
        cmds.setAttr(JointsName + '.displayLocalAxis', 1)
        i+=1

def createSingleDispNode(*args):
    curSel = cmds.ls(sl=True)
    if curSel == []:
        print "No object selected, can not create single Displacement node"
        print "Please select an object"
    else:
        cmds.vray("objectProperties", "add_single", "VRayDisplacement")
        for i in curSel:
            objName = (str(curSel[i]) + '_Displacement')
            cmds.rename('vrayDisplacement', objName)

def createMultiDispNode(*args):
    a = cmds.ls(sl=True)
    numOfSel = len(a)
    if (numOfSel == 0):
        print "No object selected, can not create any Displacement node"
        print "Please select objects that you want"
    else:
        cmds.vray("objectProperties", "add_multiple", "VRayDisplacement")    

def createJointFromSelections(*args):
    vtx = cmds.ls(sl=True, fl=True)
    for v in vtx:
        cmds.select(cl=True)
        jnt = cmds.joint()
        pos = cmds.xform(v, q=True, ws=True, t=True)
        cmds.xform(jnt, ws=True, t=pos)

def createLocatorFromSelection(*args):
    vtx = cmds.ls(sl=True, fl=True)
    for v in vtx:
        cmds.select(cl=True)
        loc = cmds.spaceLocator()
        pos = cmds.xform(v, q=True, ws=True, t=True)
        cmds.xform(loc, ws=True, t=pos)

def createClusterFromSelection(*args):
    vtx = cmds.ls(sl=True, fl=True)
    for v in vtx:
        cmds.select(cl=True)
        clu = cmds.cluster()
        pos = cmds.xform(v, q=True, ws=True, t=True)
        cmds.xform(clu, ws=True, t=pos)

def spreadSheetUI(*args):
    if cmds.window("sheetID", exists=True):
        cmds.deleteUI('sheetID')

    sheetID = cmds.window("sheetID", t="Spread Sheet Editor", widthHeight=(400, 300))
    cmds.paneLayout()
    activeList = cmds.selectionConnection(activeList=True)
    cmds.spreadSheetEditor(mainListConnection=activeList)
    cmds.showWindow(sheetID)

def setDisplay(type=None, *args):
    global checkIcon, attrType, num, selection
    if type=='surfaceShape':
        checkIcon = cmds.symbolCheckBox('gcb', q=True, v=True)
        selection = cmds.ls( type=type )
        attrType = ".overrideVisibility"
        num = [0, 1]
    elif type=='camera':
        checkIcon = cmds.symbolCheckBox('ccb', q=True, v=True)
        selection = cmds.ls( type=type )
        attrType = ".overrideVisibility"
        num = [0, 1]
    elif type=='nurbsCurve':
        checkIcon = cmds.symbolCheckBox('ncb', q=True, v=True)
        selection = cmds.ls( type=type )
        attrType = ".overrideVisibility"
        num = [0, 1]
    elif type=='light':
        checkIcon = cmds.symbolCheckBox('lcb', q=True, v=True)
        selection = cmds.ls(type=('light','locator'))
        attrType = ".overrideVisibility"
        num = [0, 1]
    elif type=='joint':
        checkIcon = cmds.symbolCheckBox('jcb', q=True, v=True)
        selection = cmds.ls( type=type )
        attrType = ".drawStyle"
        num = [2, 0]

    for i in range(len(selection)):
        cmds.setAttr(selection[i] + ".overrideEnabled", num[1])
        if checkIcon:
            cmds.setAttr(selection[i] + attrType, num[1])
        else:
            cmds.setAttr(selection[i] + attrType, num[0])
        i += 1

def pipelineLayout(*args):
    cmds.confirmDialog(t="doing it now", m="I am old Code with it", b="OK")

def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    if not os.access( path, os.W_OK ):
        # Is the error an access error ?
        os.chmod( path, stat.S_IWRITE )
        os.unlink( path )
    else:
        raise

def aboutThisTool(*args):
    if cmds.window('mainUIAbout', exists=True):
        cmds.deleteUI('mainUIAbout')
    cmds.window('mainUIAbout', t="About DAMG pipeline tool")
    cmds.columnLayout()
    cmds.text(l=MESSAGE['mainUIabout'])
    cmds.showWindow('mainUIAbout')

def NameTheFileForLater(*args):
    ## opens a window to name where the file is going and upon saving playblasts to there
    #make the text field query-able
    cmds.textField("FileNameGoesHere",q=True,text=True)
    #Open file directory window thing
    NameOfFile = cmds.fileDialog2(fileMode=0, caption="Save Playblast To")
    #returns file directory
    TheMagicalDirectory=cmds.file( NameOfFile[0],q=True,exn=True);
    #make file directory useable as a string, removes the .* at the end
    fileNamer=TheMagicalDirectory.replace(' ', '')[:-2]
    #place the directory/file name into the text field to edit if desired
    cmds.textField("FileNameGoesHere",e=True,text=fileNamer)

def TimeToPlayBlast(*args):
    resolution = {'HD 720': [1280, 720], 'HD 1080': [1920, 1080], 'HD 540': [960, 540]}
    #Playblasts The Scene
    res = cmds.optionMenu('resViewPanel', q=True, v=True)
    filePath=cmds.textField("FilePathGoesHere",q=True,text=True)
    fileName=cmds.textField("FileNameGoesHere",q=True,text=True)
    NameOfFile=os.path.join(filePath, fileName)

    WidthField=resolution[res][0]
    HeightField=resolution[res][1]
    #make the integer field for quality 0-100
    QualityField=cmds.intField("QualityField",q=True,value=True)
    #Make the checkbox for the show ornaments
    OrnamentsCheck=cmds.checkBox("OrnamentsCheck",q=True,value=True)
    #get ready to print the width of the play blast in the script editor
    editor=cmds.playblast(activeEditor=True)
    #hide all objects in view
    cmds.modelEditor(editor,edit=True,allObjects=False)
    #make polygons visible only
    cmds.modelEditor(editor,edit=True,polymeshes=True)
    #make cv's hidden
    cmds.modelEditor(editor,edit=True,cv=False)
    #make hulls hidden
    cmds.modelEditor(editor,edit=True,hulls=False)
    #make grid hidden
    cmds.modelEditor(editor,edit=True,grid=False)
    #make selected items hidden
    cmds.modelEditor(editor,edit=True,sel=False)
    #make heads up display hidden
    cmds.modelEditor(editor,edit=True,hud=False)
    #playblast from selected settings
    cmds.playblast(filename=NameOfFile, format="qt", sequenceTime=0, clearCache=1, viewer=True,
                   showOrnaments=OrnamentsCheck, framePadding=4, percent=100, compression="H.264",
                   quality=QualityField, widthHeight=(WidthField,HeightField), forceOverwrite=True)

def styleColumn121(ann, label, cmd, adj, w, *args):
    nc=2
    style121Layout = cmds.columnLayout(w=w, adj=True)
    cmds.columnLayout(adj=True)
    makeAcoolButton(ann[0], label[0], cmd[0])
    cmds.setParent('..')
    cmds.rowColumnLayout(nc=nc, cw=cwE(nc, w, adj))
    makeAcoolButton(ann[1], label[1], cmd[1])
    makeAcoolButton(ann[2], label[2], cmd[2])
    cmds.setParent('..')
    cmds.columnLayout(adj=True)
    makeAcoolButton(ann[3], label[3], cmd[3])
    cmds.setParent(style121Layout)
    cmds.setParent('..')
    return style121Layout

def styleColumn212(ann, label, cmd, adj, w, *args):
    nc=2
    style212Layout = cmds.columnLayout(adj=True)
    cmds.rowColumnLayout(nc=nc, cw=cwE(nc, w, adj))
    makeAcoolButton(ann[0], label[0], cmd[0])
    makeAcoolButton(ann[1], label[1], cmd[1])
    cmds.setParent('..')
    cmds.columnLayout(w=w, adj=True)
    makeAcoolButton(ann[2], label[2], cmd[2])
    cmds.setParent('..')
    cmds.rowColumnLayout(nc=nc, cw=cwE(nc, w, adj))
    makeAcoolButton(ann[3], label[3], cmd[3])
    makeAcoolButton(ann[4], label[4], cmd[4])
    cmds.setParent(style212Layout)
    cmds.setParent('..')
    return style212Layout