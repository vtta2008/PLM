from maya import cmds
import os, sys, json, unicodedata

class projectManager( object ):
    def __init__(self):
        if cmds.window('projectManagerUI', exists=True):
            cmds.deleteUI('projectManagerUI')

        self.buildUI()

    def buildUI(self):
        self.projectManagerUI = cmds.window( 'projectManagerUI', t='Project Manager', rtf=True )
        mlo = cmds.columnLayout()
        cmds.separator( style='in', w=400 )
        cmds.text( l="", h=2 )
        cmds.optionMenu('setMode', l='Set Mode')
        cmds.menuItem( l="Production" )
        cmds.menuItem( l="Group")
        cmds.menuItem( l="Personal" )
        cmds.text( l="", h=2 )
        cmds.setParent(mlo)
        cmds.text( l="", h=2 )
        cmds.separator( style='in', w=400 )
        cmds.rowColumnLayout( nc=4, cw=[ (1, 100), (2, 100), (3, 100), (4, 100) ] )
        cmds.button( l="New", ann="Create a new project", command=self.newProject )
        cmds.button( l="Load", ann="Load Project", command=self.loadProjectContent )
        cmds.button( l="Remove" )
        cmds.button( l="Close", command=self.closeUI )
        cmds.setParent( mlo )
        cmds.separator( style='in', w=400 )
        cmds.rowColumnLayout( nc=3, cw=[ (1, 150), (2, 50), (3, 200) ] )
        cmds.text( l="ProjectName", align='center' )
        cmds.text( l="Mode", align='center' )
        cmds.text( l="Path", align='center' )
        cmds.setParent( mlo )
        cmds.text( l="", h=2 )
        cmds.separator( style='in', w=400 )
        cmds.rowColumnLayout( nc=3, cw=[ (1, 150), (2, 50), (3, 200) ] )
        self.loadProjectContent( self )
        cmds.setParent( mlo )
        cmds.text( l="", h=2 )
        cmds.separator( style='in', w=400 )
        cmds.showWindow( 'projectManagerUI' )

    def loadProjectContent(self, *args):
        cmds.textField(text="", vis=False, w=400, h=300)
            
    def newProject(self, *args):
        modeSelect = cmds.optionMenu('modeSelect', query=True, v=True)
        if modeSelect == "Group":
            self.newprojectUI_groupMode(self)
        if modeSelect == "Personal":
            self.newprojectUI_personalMode(self)

    def closeUI(self, *args):
        if cmds.window('projectManagerUI', exists=True):
            cmds.deleteUI('projectManagerUI') 

    def newprojectUI_personalMode(self, *args):
        if cmds.window('pmWinUI', exists=True):
            cmds.deleteUI('pmWinUI')
            
        JTpmWinID = cmds.window("pmWinUI", t="New project - Personal Mode", w=600)
        tab1 = cmds.paneLayout(configuration="horizontal2")
        lo1 = cmds.columnLayout()
        cmds.button()
        cmds.showWindow(JTpmWinID)
        
    def newprojectUI_groupMode(self, *args):
        def makeAcoolButton(btn, comm, widt):
            cmds.frameLayout(borderVisible=True, labelVisible=False)
            cmds.button(l=btn, command=comm, w=widt)
            cmds.setParent('..')
        
        if cmds.window('pmWinUI', exists=True):
            cmds.deleteUI('pmWinUI')
        
        JTpmWinID = cmds.window("pmWinUI", t="New project - Group Mode", w=600)
        tab1 = cmds.paneLayout(configuration="horizontal2")
        # make pane layout /1st layer
        cmds.columnLayout()
        #make project setting section
        lo1_rll = cmds.columnLayout(w=600)
        #3rd layer
        cmds.rowColumnLayout(nc=2, cat=[1, "both", 1], cw=([1,150],[2,450]))
        makeAcoolButton('Set project Path', self.browseDir, 75)
        global saveprojectPath
        saveprojectPath = ""
        cmds.textField('projectPth', text=saveprojectPath)
        #come back to 2nd layer
        cmds.setParent(lo1_rll)
        #4 rows for 4 sections /3rd layer
        lo1_rll_rl1 = cmds.rowColumnLayout(nc=4, cat=[1, "both", 1], cw=[(1,120),(2,120),(3,120),(4,240)])
        #character name row /4th layer
        cmds.columnLayout()
        #list of folders in pre project folders /5th layer
        cmds.columnLayout(h=260)
        #come back to 3rd layer
        cmds.setParent(lo1_rll_rl1)
        #environment objects row
        cmds.columnLayout()
        #come back to 3rd layer
        cmds.setParent(lo1_rll_rl1)
        #props objects row
        cmds.columnLayout()
        #come back to 3rd layer
        cmds.setParent(lo1_rll_rl1)
        #project details row /4th layer
        lo1_rll_rl1_lo4 = cmds.columnLayout()
        cmds.text(l="Details", w=240, h=20, align='center')   
        #details column /5th layer
        cmds.setParent(tab1)
        cmds.showWindow(JTpmWinID)
    
    def browseDir(self, *args):
        #get the path from MEL
        path = cmds.fileDialog2(fm=3, ff='directory')
        saveprojectPath = path[0].encode('utf-8')
        #set the textField text to the directory that was returned from MEL
        cmds.textField('projectPth', edit=True, text=saveprojectPath)
    
    def createFolderStructure(self, *args):
        #get name project:
        curProjName = cmds.textField("prjFullName", text = True, query = True)
        #get current project path:
        curProjPath = cmds.textField('projectPth', query=True, text=True)
        stage_Ls = ['assets', 'deliverables', 'documents', 'editorial', 'reference', 'RnD', 'sequences', 'resources']
        assets_Ls = ['character', 'enviroment', 'props']
        task_Ls = ['art', 'modeling', 'rigging', 'surfacing', 'lighting', 'FX', 'anim', 'comp', 'layout']
        documents_Ls = ['template', 'moodboard', 'schedule', 'script', 'sound', 'storyboard', 'title', 'tools']
        editorial_Ls = ['animatic', 'edit', 'poster']
        resources_Ls = ['lighting', 'camera rig']
        art_task = ['pts & illus', 'maya', 'zbrush', 'reference']
        modeling_task = ['zbrush', 'maya', 'mudbox', 'houdini']
        rigging_task = ['maya']
        surfacing_task = ['maya', 'mari', 'substance', 'photoshop']
        shotTask_apps = ['maya', 'houdini', 'nuke', 'AE']
        work_Ls = ['publish', 'review', 'work']
        
        shots = cmds.intField('numOfShots', v=True, query=True)
        chars = cmds.intField('numOfChars', v=True, query=True)
        shortName = cmds.textField('prjShortName', text=True, query=True)
        
        charName_Ls = []
        numChars = cmds.intField('numOfChars', v=True, query=True)
        i = 0
        for i in range(int(numChars)):
            number = i + 1
            getCharName = cmds.textField(str('charName' + str(number)), text=True, query=True)
            charName_Ls.append(getCharName)
            i = i + 1
        
        envObj_Ls = []
        numEnvObj = cmds.intField('numOfenvObj', v=True, query=True)
        i = 0
        for i in range(int(numEnvObj)):
            number = i + 1
            getEnvObjName = cmds.textField(str('envObj' + str(number)), text=True, query=True)
            envObj_Ls.append(getEnvObjName)
            i = i + 1

        props_Ls = []
        numProps = cmds.intField('numOfProps', v=True, query=True)
        i = 0
        for i in range(int(numProps)):
            number = i + 1
            getPropName = cmds.textField(str('prop' + str(number)), text=True, query=True)
            props_Ls.append(getPropName)

        p = curProjPath + "/" +curProjName
        
        #master folder (name of project)
        cmds.sysFile(curProjPath + "/" + curProjName, md=True)
        
        #folder for stages of product
        i = 0
        for i in range(len(stage_Ls)):
            cmds.sysFile(p + "/" + stage_Ls[i], md=True)
            i = i + 1
        
        #folder structure inside stages folder:
        path = p + "/" + stage_Ls[0]
        i = 0
        for i in range(len(assets_Ls)):
            cmds.sysFile(path + "/" + assets_Ls[i], md=True)
            i = i + 1
        
        #character folder
        path = path + "/" + assets_Ls[0]
        i = 0
        for i in range(len(charName_Ls)):
            cmds.sysFile(path + "/" + charName_Ls[i], md=True)
            path1 = path + "/" + charName_Ls[i]
            item = 0
            for item in range(len(task_Ls[:4])):
                cmds.sysFile(path1 + "/" + task_Ls[item], md=True)
                path2 = path1 + "/" + task_Ls[item]
                obj = 0
                for obj in range(len(work_Ls)):
                    cmds.sysFile(path2 + "/" + work_Ls[obj], md=True)
                    obj = obj + 1
                item = item + 1
            path3 = path1 + "/" + task_Ls[0] + "/" + work_Ls[2]
            a = 0
            for a in range(len(art_task)):
                cmds.sysFile(path3 + "/" + art_task[a], md=True)
                a = a + 1
            path3 = path1 + "/" + task_Ls[1] + "/" + work_Ls[2]
            a = 0
            for a in range(len(modeling_task)):
                cmds.sysFile(path3 + "/" + modeling_task[a], md=True)
                a = a + 1
            path3 = path1 + "/" + task_Ls[2] + "/" + work_Ls[2]
            a = 0
            for a in range(len(rigging_task)):
                cmds.sysFile(path3 + "/" + rigging_task[a], md=True)
                a = a + 1
            path3 = path1 + "/" + task_Ls[3] + "/" + work_Ls[2]
            a = 0
            for a in range(len(surfacing_task)):
                cmds.sysFile(path3 + "/" + surfacing_task[a], md=True)
                a = a + 1
            i = i + 1
        
        #environment folder
        path = path = p + "/" + stage_Ls[0] + "/" + assets_Ls[1]
        i = 0
        for i in range(len(envObj_Ls)):
            cmds.sysFile(path + "/" + envObj_Ls[i], md=True)
            path1 = path + "/" + envObj_Ls[i]
            item = 0
            for item in range(len(task_Ls[:4])):
                cmds.sysFile(path1 + "/" + task_Ls[item], md=True)
                path2 = path1 + "/" + task_Ls[item]
                obj = 0
                for obj in range(len(work_Ls)):
                    cmds.sysFile(path2 + "/" + work_Ls[obj], md=True)
                    obj = obj + 1
                item = item + 1
            path3 = path1 + "/" + task_Ls[0] + "/" + work_Ls[2]
            a = 0
            for a in range(len(art_task)):
                cmds.sysFile(path3 + "/" + art_task[a], md=True)
                a = a + 1
            path3 = path1 + "/" + task_Ls[1] + "/" + work_Ls[2]
            a = 0
            for a in range(len(modeling_task)):
                cmds.sysFile(path3 + "/" + modeling_task[a], md=True)
                a = a + 1
            path3 = path1 + "/" + task_Ls[2] + "/" + work_Ls[2]
            a = 0
            for a in range(len(rigging_task)):
                cmds.sysFile(path3 + "/" + rigging_task[a], md=True)
                a = a + 1
            path3 = path1 + "/" + task_Ls[3] + "/" + work_Ls[2]
            a = 0
            for a in range(len(surfacing_task)):
                cmds.sysFile(path3 + "/" + surfacing_task[a], md=True)
                a = a + 1        
            i = i + 1

        #props folder
        path = p + "/" + stage_Ls[0] + "/" + assets_Ls[2]
        i = 0
        for i in range(len(props_Ls)):
            cmds.sysFile(path + "/" + props_Ls[i], md=True)
            path1 = path + "/" + props_Ls[i]
            item = 0
            for item in range(len(task_Ls[:4])):
                cmds.sysFile(path1 + "/" + task_Ls[item], md=True)
                path2 = path1 + "/" + task_Ls[item]
                obj = 0
                for obj in range(len(work_Ls)):
                    cmds.sysFile(path2 + "/" + work_Ls[obj], md=True)
                    obj = obj + 1
                item = item + 1
            path3 = path1 + "/" + task_Ls[0] + "/" + work_Ls[2]
            a = 0
            for a in range(len(art_task)):
                cmds.sysFile(path3 + "/" + art_task[a], md=True)
                a = a + 1
            path3 = path1 + "/" + task_Ls[1] + "/" + work_Ls[2]
            a = 0
            for a in range(len(modeling_task)):
                cmds.sysFile(path3 + "/" + modeling_task[a], md=True)
                a = a + 1
            path3 = path1 + "/" + task_Ls[2] + "/" + work_Ls[2]
            a = 0
            for a in range(len(rigging_task)):
                cmds.sysFile(path3 + "/" + rigging_task[a], md=True)
                a = a + 1
            path3 = path1 + "/" + task_Ls[3] + "/" + work_Ls[2]
            a = 0
            for a in range(len(surfacing_task)):
                cmds.sysFile(path3 + "/" + surfacing_task[a], md=True)
                a = a + 1        
            i = i + 1

        #document folder:
        path = p + "/" + stage_Ls[2]
        i = 0
        for i in range(len(documents_Ls)):
            cmds.sysFile(path + "/" + documents_Ls[i], md=True)
            i = i + 1
            
        #editorial folder:
        path = p + "/" + stage_Ls[3]
        i = 0
        for i in range(len(editorial_Ls)):
            cmds.sysFile(path + "/" + editorial_Ls[i], md=True)
            i = i + 1
        
        #sequences folder:
        sequence_Ls = []
        i = 0
        
        for i in range(int(shots)):
            shotNum = i + 1
            if shotNum <= 9:
                shotName = shortName + "_" + "0" + str(shotNum)
                sequence_Ls.append(shotName)
            if shotNum > 9:
                shotName = shortName + "_" + str(shotNum)
                sequence_Ls.append(shotName)
            i = i + 1
        sequence_task = task_Ls[4:]
        path = p + "/" + stage_Ls[6]
        i = 0
        for i in range(len(sequence_Ls)):
            cmds.sysFile(path + "/" + sequence_Ls[i], md=True)
            nextPth = path + "/" + sequence_Ls[i]
            item = 0
            for item in range(len(sequence_task)):
                cmds.sysFile(nextPth + "/" + sequence_task[item], md=True)
                next_Pth = nextPth + "/" + sequence_task[item]
                a = 0
                for obj in range(len(work_Ls)):
                    cmds.sysFile(next_Pth + "/" + work_Ls[a], md=True)
                    a = a + 1
                Pth = next_Pth + "/" + work_Ls[2]
                a = 0
                for a in range(len(shotTask_apps)):
                    cmds.sysFile(Pth + "/" + shotTask_apps[a], md=True)
                    a = a + 1
                item = item + 1
            i = i + 1

        #resources folder
        path = p + "/" + stage_Ls[7]
        i = 0
        for i in range(len(resources_Ls)):
            cmds.sysFile(path + "/" + resources_Ls[i], md=True)
            i = i + 1

    def setProj(self, *args):
        import maya.mel as mel
        mel.eval('setProjectFromFileDialog;')

    def mayaFolder(self, *args):
        curPth = cmds.workspace(q=True, rd=True)
        maya_Ls = ['scenes', 'images', 'sourceimages', 'clips', 'renderData', 'scripts', 'data', 'apps', 'cache']
        i = 0
        for i in range(len(maya_Ls)):
            cmds.sysFile(curPth + "/" + maya_Ls[i], md=True)
            i = i + 1
