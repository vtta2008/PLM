import maya.cmds as cmds
import os
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import json
import shutil

class DAMGfileManagerForMaya( object ):
    def __init__(self):
        #first base information of paths
        self.curPth = cmds.workspace(q=True, rd=True)
        self.workPth = self.curPth + "scenes"

        if 'work' in self.curPth or 'sequences' in self.curPth:
            self.curMode = 'Studio Mode'
            self.studioModeVar()
        elif 'assets' in os.listdir(self.curPth + "scenes/") or 'sequences' in os.listdir(self.curPth + "scenes/"):
            self.curMode = 'Group Mode'
            self.groupModeVar()
        else:
            self.curMode = 'Pesonal Mode'
            self.personalModeVar()

        self.numOfSectInPth = len( (self.curPth.split( "work" )[ 0 ]).split( "/" ) )
        self.assetName = (self.curPth.split( "work" )[ 0 ]).split( "/" )[ (self.numOfSectInPth - 3) ]
        self.taskName = (self.curPth.split( "work" )[ 0 ]).split( "/" )[ (self.numOfSectInPth - 2) ]
        self.baseFileName = self.assetName + "_" + self.taskName
        # get file save
        self.saveFilesList = [ f.split( '.ma' )[ 0 ] for f in os.listdir( self.workPth ) if f.endswith( '.ma' ) ]
        for file in self.saveFilesList:
            num = file.split( "_v" )[ -1 ]
            if "." in num or "-" in num or "_" in num:
                self.saveFilesList.remove( file )
        if (len( self.saveFilesList ) == 0):
            cmds.file( rename=self.baseFileName + "_v001" )
            cmds.file( save=True, type='mayaAscii' )
            self.saveFilesList = [ f.split( '.ma' )[ 0 ] for f in os.listdir( self.workPth ) if f.endswith( '.ma' ) ]
            self.verFileName = self.saveFilesList[ 0 ]
        else:
            self.maxVer = max( [ f.split( "_v" )[ -1 ] for f in self.saveFilesList ] )
            self.verFileName = self.baseFileName + "_v" + self.maxVer
        self.ssFilesList = [ f for f in os.listdir( self.snapShotPth ) if f.endswith( '.ma' ) ]
        if (len( self.ssFilesList ) == 0):
            self.reverFileName = self.verFileName + "_r001.ma"
        else:
            self.maxRever = (str( int( max( [ (f.split( "_r" )[ -1 ]).split( '.ma' )[ 0 ] for f in self.ssFilesList if
                                              self.verFileName in f ] ) ) + 1 )).zfill( 3 )
            self.reverFileName = self.verFileName + "_r" + self.maxRever + '.ma'
        self.publishNameFile = self.verFileName.split( "_v" )[ 0 ] + "_v" + str(
            int( (self.verFileName.split( "." )[ 0 ]).split( "_v" )[ -1 ] ) + 1 ).zfill( 3 ) + ".ma"
        self.filePublishPth = self.publishPth + self.verFileName + ".ma"
        self.publishRevName = self.publishNameFile.split( '.ma' )[ 0 ] + "_r001.ma"
        self.publishImageName = self.publishRevName.split( '.ma' )[ 0 ] + ".jpg"
        self.snapShotImageName = self.reverFileName.split( ".ma" )[ 0 ] + ".jpg"
        self.fileSavePth = self.workPth + "/" + self.verFileName + ".ma"
        self.fileSnapShotPth = self.snapShotPth + "/" + self.reverFileName
        self.imageSnapShotPth = self.snapShotPth + "/" + self.snapShotImageName
        self.imagepublishPth = self.snapShotPth + "/" + self.publishImageName

    def personalModeVar(self):
        pass

    def groupModeVar(self):
        self.filePth = cmds.file(q=True, loc=True)
        self.fileName = os.path.basename(os.path.normpath(self.filePth))
        self.workingPth = self.filePth.split(self.fileName)[0]

    def studioModeVar(self):
        self.snapShotPth = self.curPth + "scenes/snapShot"
        if not os.path.exists( self.snapShotPth ):
            cmds.sysFile( self.snapShotPth, md=True )

        self.publishPth = self.curPth.split( 'work' )[ 0 ] + "publish/maya/"
        if not os.path.exists( self.publishPth ):
            cmds.sysFile( self.publishPth, md=True )

    def DAMGsnapShotUI(self):
        #START MAKING SNAPSHOT WINDOW UI
        self.screenShotImage(self.imageSnapShotPth)
        #header
        if cmds.window('ssWinID', exists=True):
            cmds.deleteUI('ssWinID')
        ssWinID = cmds.window('ssWinID', t="DAMG Snap Shot")
        mlo = cmds.columnLayout()
        cmds.separator(style='in',w=815)
        cmds.text(l="", h=5)
        mlo_ro1 = cmds.rowColumnLayout(nc=5, cat=[1,'both',1], cw=[(1,5),(2,300),(3,5),(4,500),(5,5)])
        cmds.text(l="")
        cmds.text(l="Snap Shot Menu", align='center')
        cmds.text(l="")
        cmds.text(l="Snap Shot viewer")
        cmds.text(l="")
        cmds.setParent('..')
        cmds.text(l="", h=5)
        cmds.separator(style='in',w=815)        
#body
        mlo_ro2 = cmds.rowColumnLayout(nc=5, cat=[1,'both',1], cw=[(1,5),(2,300),(3,5),(4,500),(5,5)])
        cmds.separator(style='in', hr=False)
    #left row - snap shot menu
        mlo_ro2_lo1 = cmds.columnLayout()
        cmds.separator(style='in',w=300)
        cmds.text(l="", h=5)
        cmds.text(l="SnapShot File Details: ")
        cmds.text(l="", h=5)
        cmds.rowColumnLayout(nc=3, cw=[(1,80),(2,5),(3,215)])
        cmds.text(l="File Version")
        cmds.text(l="")
        cmds.optionMenu('fileName', w=210)
        cmds.menuItem('fileName_item1', l=self.verFileName)
        cmds.text(l="File Reversion")
        cmds.text(l="")
        self.reversionName = cmds.optionMenu('reversionName', w=210)
        self.reversionName_item1 = cmds.menuItem('reversionName_item1', l=self.reverFileName)
        cmds.setParent('..')
        cmds.text(l="", h=5)
        cmds.separator(style='in',w=300)
        cmds.text(l="Comment:")
        cmds.text(l="", h=5)
        cmds.textField('ssComment', h=50, w=300)
        cmds.text(l="", h=110)
        cmds.separator(style='in',w=300)
        cmds.text(l="",h=5)
        mlo_ro2_lo1_ro1 = cmds.rowColumnLayout(nc=3, cat=[1,'both',1], cw=[(1,147.5),(2,5),(3,147.5)])
        buttonSave = cmds.button(l="Save File", c=self.snapShotSaveFile)
        cmds.text(l="")
        buttonClose = cmds.button(l="Close", c=self.snapShotClose)
        cmds.setParent('..')
        cmds.text(l="",h=5)
        cmds.separator(style='in',w=300)
    #end of lef row
        cmds.setParent(mlo_ro2)
        cmds.separator(style='in', hr=False)
        mlo_ro2_lo2 = cmds.columnLayout()
        cmds.image(image=self.imageSnapShotPth, w=500, h=263)
        cmds.separator(style='in', w=500)
        cmds.text(l="", h=5)
        cmds.text(l=self.snapShotImageName,w=500, align='center')
        cmds.text(l="", h=5)
        cmds.separator(style='in', w=500)
    #end of right row
#show snap shot UI
        cmds.showWindow('ssWinID')

    def DAMGpulishUI(self):
        #START MAKING PUBLISH WINDOW UI
        self.screenShotImage(self.imagepublishPth)
        #Header
        if cmds.window('plWinID', exists=True, rtf=True):
            cmds.deleteUI('plWinID')
        plWinID = cmds.window('plWinID', t="DAMG Publish")
        mlo = cmds.columnLayout()
        cmds.separator(style='in',w=815)
        cmds.text(l="", h=5)
        mlo_ro1 = cmds.rowColumnLayout(nc=5, cat=[1,'both',1], cw=[(1,5),(2,300),(3,5),(4,500),(5,5)])
        cmds.text(l="")
        cmds.text(l="Publish Menu", align='center')
        cmds.text(l="")
        cmds.text(l="Snap Shot viewer")
        cmds.text(l="")
        cmds.setParent('..')
        cmds.text(l="", h=5)
        cmds.separator(style='in',w=815)
#body
        mlo_ro2 = cmds.rowColumnLayout(nc=5, cat=[1,'both',1], cw=[(1,5),(2,300),(3,5),(4,500),(5,5)])
        cmds.text(l="")
    #left row - snap shot menu
        mlo_ro2_lo1 = cmds.columnLayout()
        cmds.separator(style='in',w=300)
        cmds.text(l="", h=5)
        cmds.rowColumnLayout(nc=3, cw=[(1,80),(2,5),(3,215)])
        cmds.text(l="File Name:")
        cmds.text(l="")
        self.fileName = cmds.optionMenu('fileName', w=210)
        self.fileName_item1 = cmds.menuItem('fileName_item1', l=self.publishNameFile)
        cmds.text(l="Reversion: ")
        cmds.text(l="")
        self.reversionName = cmds.optionMenu('reversionName', w=210)
        self.reversionName_item1 = cmds.menuItem('reversionName_item1', l=self.publishRevName)
        cmds.setParent('..')
        cmds.text(l="", h=5)
        cmds.separator(style='in',w=300)
        cmds.text(l="Comment:")
        cmds.text(l="", h=5)
        cmds.textField('plComment', h=50, w=300)
        cmds.text(l="", h=110)
        cmds.text(l="",h=5)
        mlo_ro2_lo1_ro1 = cmds.rowColumnLayout(nc=3, cat=[1,'both',1], cw=[(1,147.5),(2,5),(3,147.5)])
        cmds.button(l="Publish File", c=self.publishFile)
        cmds.text(l="")
        cmds.button(l="Close", command=self.publishClose)
        cmds.setParent('..')
        cmds.text(l="",h=5)
        cmds.separator(style='in',w=300)
    #end of lef row
        cmds.setParent(mlo_ro2)
        cmds.separator(style='in', hr=False)
        mlo_ro2_lo2 = cmds.columnLayout()
        cmds.image(image=self.imageSnapShotPth, w=500, h=263)
        cmds.separator(style='in', w=500)
        cmds.text(l="", h=5)
        cmds.text(l=self.publishImageName,w=500, align='center')
        cmds.text(l="", h=5)
        cmds.separator(style='in', w=500)      
    #end of right row
#show snap shot UI
        cmds.showWindow('plWinID')

    def screenShotImage(self, path):
        view = omui.M3dView.active3dView()
        image = om.MImage()
        view.readColorBuffer( image, True )
        image.resize( 500, 280 )
        image.writeToFile( path, 'jpg' )

    def DAMGopenLoadFilesUI(self):
        title = "Open/Load File Window"
        self.save_ssExt = [f for f in os.listdir(self.snapShotPth) if f.endswith('.ma')]
        self.save_ssImg = [f for f in os.listdir(self.snapShotPth) if f.endswith('.jpg')]

        if cmds.window('openFileUI',q=True, exists=True):
            cmds.deleteUI(title)

        cmds.window('openFileUI', t=title, rtf=True)
        self.mlo = cmds.columnLayout()
#header
        cmds.text(l="",h=5)
        cmds.separator(style='in', w=805)
        cmds.text(l="", h=5)
        self.mlo_ro1 = cmds.rowColumnLayout(nc=3, cat=[1,'both',1], cw=[(1,300),(2,5),(3,500)])
        cmds.text(l="File Name", align='center', w=300)
        cmds.text(l="")
        cmds.text(l="File viewer", align='center', w=500)
        cmds.setParent('..')
        cmds.text(l="",h=5)
        cmds.separator(style='in', w=805)
        cmds.text(l="", h=5)
#body
    #left row
        self.mlo_ro2 = cmds.rowColumnLayout(nc=3, cat=[1,'both',1], cw=[(1,300),(2,5),(3,500)])
        self.mlo_ro2_lo1 = cmds.columnLayout()
        self.ssFile_Menu = cmds.optionMenu('ssFileMenu', l="Files", cc=self.refreshImage)
        for i in range(len(self.save_ssExt)):
            cmds.menuItem(l=self.save_ssExt[i])
            i += 1
        cmds.separator(style='in', w = 300, h=20)
        cmds.rowColumnLayout(nc=3, cw=[(1,5),(2,290),(3,5)])
        cmds.text(l="")
        cmds.text( 'comment', l="", h=20 )
        cmds.text(l="")
        cmds.setParent('..')

        cmds.text(l="", h=185)
        self.mlo_ro2_lo1_ro1 = cmds.rowColumnLayout(nc=3, cat=[1,'both',1], cw=[(1,147.5),(2,5),(3,147.5)])
        cmds.button(l="Load File", command=self.damgOpenFile)
        cmds.text(l="")
        cmds.button(l="Close", command=self.damgCloseFile)
        cmds.setParent(self.mlo_ro2)
    #separator in middle
        cmds.separator(style='in', hr=False)
    #right row
        mlo_ro1_lo2 = cmds.columnLayout()
        value = (cmds.optionMenu('ssFileMenu', query=True, value=True)).split('.ma')[0] + ".jpg"
        if value=="":
            cmds.image(self.imageDisplay, e=True, vis=False)
            cmds.text(self.viewText, e=True, vis=True)
        else:
            self.imageDisplay = cmds.image(image=self.snapShotPth + "/" + value)
            self.viewText = cmds.text( l="No data to show", align='center', w=410, h=231, vis=False )
        cmds.setParent(self.mlo)
        cmds.text(l="", h=5)
        cmds.separator(style='in', w=805)
        cmds.text(l="", h=5)
        self.refreshImage()

        cmds.showWindow( 'openFileUI' )

    def publishFile(self, *args, **info):
        cmds.file(save=True, type='mayaAscii')
        shutil.copy2(self.fileSavePth, self.filePublishPth)
        cmds.file(rename=str(self.publishNameFile + ".ma"))
        cmds.file(save=True, type='mayaAscii')

        name = self.publishNameFile.split('.ma')[0] + "_r001"
        infoFile = os.path.join( self.snapShotPth, '%s.comment' % name )

        info['Name'] = name + ".ma"
        info['Comment'] = cmds.textField('plComment', q=True, tx=True)
        info['SnapShot'] = self.fileSnapShotPth
        info['Image'] = self.imageSnapShotPth

        shutil.copy2(self.fileSavePth, self.snapShotPth + "/" + name + ".ma")
        if cmds.window('plWinID', exists=True):
            cmds.deleteUI('plWinID')
    
    def publishClose(self, *args):
        if os.path.exists(self.imageSnapShotPth) is True:
            cmds.sysFile(self.imageSnapShotPth, delete=True)
        if os.path.exists(self.imagepublishPth) is True:
            cmds.sysFile(self.imagepublishPth, delete=True)
        if cmds.window('plWinID', exists=True):
            cmds.deleteUI('plWinID')

    def snapShotSaveFile(self, *args, **info):
        name = self.reverFileName.split('.ma')[0]
        infoFile = os.path.join(self.snapShotPth, '%s.comment' % name)

        info['Name'] = self.reverFileName
        info['Comment'] = cmds.textField('ssComment', q=True, tx=True)
        info['SnapShot'] = self.fileSnapShotPth
        info['Image'] = self.imageSnapShotPth

        cmds.file(rename=self.verFileName)
        cmds.file(save=True, type='mayaAscii')
        shutil.copy2(self.fileSavePth, self.fileSnapShotPth)

        with open(infoFile, 'w') as f:
            json.dump(info, f, indent=4)

        if cmds.window('ssWinID', exists=True):
            cmds.deleteUI('ssWinID')

    def snapShotClose(self, *args):
        if os.path.exists(self.imageSnapShotPth) is True:
            cmds.sysFile(self.imageSnapShotPth, delete=True)
        if os.path.exists(self.imagepublishPth) is True:
            cmds.sysFile(self.imagepublishPth, delete=True)
        if cmds.window('ssWinID', exists=True):
            cmds.deleteUI('ssWinID')

    def refreshImage(self, *args):
        infoFile = (cmds.optionMenu('ssFileMenu', query=True, value=True)).split('.ma')[0] + ".comment"
        if os.path.exists(self.snapShotPth + "/" +infoFile):
            with open( self.snapShotPth + "/" + infoFile, 'r' ) as f:
                rawInfo = json.load(f)
            comment = rawInfo['Comment']
            image = rawInfo['Image']
        else:
            comment = "No comment"
            image = self.snapShotPth + "/" + (cmds.optionMenu( 'ssFileMenu', query=True, value=True )).split( '.ma' )[ 0 ] + ".jpg"

        cmds.image(self.imageDisplay, e=True, image=image)
        cmds.text( 'comment', e=True, l=comment, align='left')

    def damgOpenFile(self, *args):
        cmds.file(new=True, f=True)
        value = cmds.optionMenu('ssFileMenu', query=True, value=True)
        cmds.file(self.snapShotPth + "/" + value, open=True)
        cmds.file(rename=self.verFileName)
        cmds.file(save=True, type='mayaAscii')
        if cmds.window('openFileUI', exists=True):
            cmds.deleteUI('openFileUI')

    def damgCloseFile(self, *args):
        if cmds.window('openFileUI', exists=True):
            cmds.deleteUI('openFileUI')
