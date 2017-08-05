import maya.cmds as cmds
import maya.mel as mel
import os


def openVrayVFB():
    cmds.loadPlugin( "vrayformaya" )
    cmds.pluginInfo( 'vrayformaya', edit=True, autoload=True )
    cmds.setAttr( "defaultRenderGlobals.currentRenderer", "vray", type="string" )
    cmds.vray( "showVFB" )

def quitButtonMenu():
    import DAMGmasterToolControlMaya
    reload ( DAMGmasterToolControlMaya )
    damgteam = DAMGmasterToolControlMaya.damgPipelineMayaUI()
    try:
        damgteam.workspaceName
    except NameError:
        print "DAMG's tool UI is not existed"
        print "Creating new DAMG's tool UI..."
    else:
        if cmds.workspaceControl(damgteam.workspaceName, exists=True):
            cmds.deleteUI(damgteam.workspaceName)

def openProjFolder():
    projPth = cmds.workspace(q=True, rd=True)
    os.startfile(projPth)

def openSceneFolder():
    projPth = cmds.workspace(q=True, rd=True)
    scenePth = projPth + "/scenes"
    os.startfile(scenePth)

def openSourceimagesFolder():
    projPth = cmds.workspace(q=True, rd=True)
    sourceImagesPth = projPth + "/sourceimages"
    os.startfile(sourceImagesPth)

def openSnapShotFolder():
    projPth = cmds.workspace(q=True, rd=True)
    snapShotPth = projPth + "/scenes/snapshot"
    os.startfile(snapShotPth)

def openPublishFolder():
    projPth = cmds.workspace(q=True, rd=True)
    publishPth = projPth.split('work')[0] + "publish/maya"
    os.startfile(publishPth)

def centerPivot():
    a = cmds.ls(sl=True)
    if ( len(a) > 0 ):
        cmds.xform(cp=True)

def Chop():
    def gotoObjectmod():
        a = cmds.ls(sl=True)

        if ( len(a) > 0 ):
            pick1st = a[0]
            ioF = pick1st.index('f')-1
            objName = pick1st[0:ioF]
            cmds.select(objName, r=1)

    a = cmds.ls(sl=True)

    if ( len(a) > 0 ):
        cmds.polyChipOff(ch=1, kft=1, dup=0, off=0)
        gotoObjectmod()
        cmds.polySeparate()
    else:
        print "nothing selected, please select faces"

def normalOnOff():
    a = cmds.ls(sl=True)
    if ( len(a) > 0 ):
        cmds.ToggleFaceNormalDisplay()

def reverseNormal():
    a = cmds.ls(sl=True)
    if ( len(a) > 0 ):
        cmds.polyNormal(nm=0)

def ChildSel():
    a = cmds.ls(sl=True)
    if ( len(a) > 0 ):
        cmds.select(hi=True)

def JointOff():
    JointsSel = cmds.ls(sl=True)
    Joints = []
    
    for item in JointsSel:
        Joints.append(item)
    
    NumOfJoints = int(len(JointsSel))
    i = 0
    
    for item in range(NumOfJoints):
        JointsName = Joints[i]
        cmds.setAttr(JointsName + '.displayLocalAxis',0)
        i = i + 1
    
def JointOn():
    JointsSel = cmds.ls(sl=True)
    Joints = []
    
    for item in JointsSel:
        Joints.append(item)
    
    NumOfJoints = int(len(JointsSel))
    i = 0
    
    for item in range(NumOfJoints):
        JointsName = Joints[i]
        cmds.setAttr(JointsName + '.displayLocalAxis',1)
        i = i + 1

def Yeallow():
    a = cmds.ls(sl=True, fl=True)
    childs = cmds.listRelatives(a, c=True)
    
    if (len(childs) == 1):
        CtrlsSel = cmds.ls(sl=True)
        Ctrls = []
            
        for item in CtrlsSel:
            Ctrls.append(item)
        
        NumOfCtrls = int(len(CtrlsSel))
        i = 0
        
        for item in range(NumOfCtrls):
            CtlrName = Ctrls[i]
            CtlrNameNode = CtlrName + "Shape"
            cmds.setAttr(CtlrNameNode + '.overrideEnabled', 1)
            cmds.setAttr(CtlrNameNode + '.overrideColor', 17)
            i = i + 1
    if (len(childs) > 1):
        i = 0
        for i in range(len(childs)):
            cmds.setAttr(childs[i] + '.overrideEnabled', 1)
            cmds.setAttr(childs[i] + '.overrideColor', 17)

def Cyan():
    a = cmds.ls(sl=True, fl=True)
    childs = cmds.listRelatives(a, c=True)
    
    if (len(childs) == 1):
        CtrlsSel = cmds.ls(sl=True)
        Ctrls = []
            
        for item in CtrlsSel:
            Ctrls.append(item)
        
        NumOfCtrls = int(len(CtrlsSel))
        i = 0
        
        for item in range(NumOfCtrls):
            CtlrName = Ctrls[i]
            CtlrNameNode = CtlrName + "Shape"
            cmds.setAttr(CtlrNameNode + '.overrideEnabled', 1)
            cmds.setAttr(CtlrNameNode + '.overrideColor', 18)
            i = i + 1
    if (len(childs) > 1):
        i = 0
        for i in range(len(childs)):
            cmds.setAttr(childs[i] + '.overrideEnabled', 1)
            cmds.setAttr(childs[i] + '.overrideColor', 18)

        i = i + 1

def createSingleDispNode():
    a = cmds.ls(sl=True)
    numOfSel = len(a)
    if (numOfSel == 0):
        print "No object selected, can not create single Displacement node"
        print "Please select an object"
    else:
        cmds.vray("objectProperties", "add_single", "VRayDisplacement")
        for i in numOfSel:
            objName = (str(a[i]) + '_Displacement')
        cmds.rename('vrayDisplacement',objName)

def createMultiDispNode():
    a = cmds.ls(sl=True)
    numOfSel = len(a)
    if (numOfSel == 0):
        print "No object selected, can not create any Displacement node"
        print "Please select objects that you want"
    else:
        cmds.vray("objectProperties", "add_multiple", "VRayDisplacement")    

def createJointFromSelections():
    vtx = cmds.ls(sl=True, fl=True)
    for v in vtx:
        cmds.select(cl=True)
        jnt = cmds.joint()
        pos = cmds.xform(v, q=True, ws=True, t=True)
        cmds.xform(jnt, ws=True, t=pos)

def createLocatorFromSelection():
    vtx = cmds.ls(sl=True, fl=True)
    for v in vtx:
        cmds.select(cl=True)
        loc = cmds.spaceLocator()
        pos = cmds.xform(v, q=True, ws=True, t=True)
        cmds.xform(loc, ws=True, t=pos)

def createClusterFromSelection():
    vtx = cmds.ls(sl=True, fl=True)
    for v in vtx:
        cmds.select(cl=True)
        clu = cmds.cluster()
        pos = cmds.xform(v, q=True, ws=True, t=True)
        cmds.xform(clu, ws=True, t=pos)

def spreadSheetUI():
    if cmds.window("sheetID", exists=True):
        cmds.deleteUI('sheetID')

    sheetID = cmds.window("sheetID", t="Spread Sheet Editor", widthHeight=(400, 300))
    cmds.paneLayout()
    activeList = cmds.selectionConnection(activeList=True)
    cmds.spreadSheetEditor(mainListConnection=activeList)
    cmds.showWindow(sheetID)

def setDisplay(type=None):
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

def pipelineLayout():
    cmds.confirmDialog(t="doing it now", m="I am oldCode on it", b="OK")

def aboutThisTool():
    if cmds.window('About', exists=True):
        cmds.deleteUI('About')
    aboutID = cmds.window('About', t="About DAMG pipeline tool")
    cmds.rowColumnLayout(nc=3, cw=[(1,10),(2,350),(3,10)])
    cmds.columnLayout()
    cmds.text(l="")
    cmds.setParent('..')

    cmds.columnLayout()
    cmds.text(l="")
    cmds.text(l="Thank you for using DAMG products", align='left')
    cmds.text(l="")
    cmds.text(l="This is the tool to study Python for Maya", align='left')
    cmds.text(l="Built and developed by JimJim - DoTrinh", align='left')

    cmds.text(l="")
    cmds.text(l="Special thank to lectures and friends in Media Design School:", align='left')
    cmds.text(l="")
    cmds.text(l="   Oliver Hilbert", align='left')
    cmds.text(l="   Brian Samuel", align='left')
    cmds.text(l="   Kelly Bechtle-Woods", align='left')
    cmds.text(l="")
    cmds.text(l="   Brandon Hayman", align='left')

    cmds.text(l="")
    cmds.text(l="A big thank to DAMG team's members:", align='left')
    cmds.text(l="   Duong Minh Duc & Tran Huyen Trang", align='left')

    cmds.text(l="")
    cmds.text(l="for any question or feedback, email me at: dot@damgteam.com", align='left')
    cmds.text(l="")
    cmds.setParent('..')

    cmds.columnLayout()
    cmds.text(l="")
    cmds.setParent( '..' )

    cmds.showWindow('About')
