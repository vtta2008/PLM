import maya.cmds as cmds
import os, sys

class DAMGfunctionsAppsTransfer():

    def __init__(self):
        if cmds.window("DAMGgo2AppsUI", exists=True):
            cmds.deleteUI('DAMGgo2AppsUI')

        def makeACoolButton(ann, image, command):
            cmds.frameLayout(borderVisible=True, labelVisible=False)
            cmds.symbolButton(ann=ann, i=image, c=command, h=40, w=40)
            cmds.setParent('..')

        self.DAMGgo2AppsUI = cmds.window('DAMGgo2AppsUI', t="DAMG Go to Apps", rtf=True)
        cmds.rowColumnLayout(nc=5, cat=[1,"both",1], cw=[(1,45),(2,45),(3,45),(4,45),(5,45)])

        makeACoolButton('go to Zbrush', "zbrushicon.png", self.openZbrush)
        makeACoolButton('go to Mudbox', "mudboxicon.png", self.openMudbox)
        makeACoolButton('go to Mari', "houdiniicon.png", self.openHoudini)
        makeACoolButton('go to Mari', "mariicon.png", self.openMari)
        makeACoolButton('go to NukeX', "nukexicon.png", self.openNuke)
        makeACoolButton('go to Hiero', "hieroicon.png", self.openHiero)
        makeACoolButton('go to Photoshop', "photoshopicon.png", self.openPhotoshop)
        makeACoolButton('go to Illustrator', "illustratoricon.png", self.openIllustrator)
        makeACoolButton('go to After Effect', "aftereffecticon.png", self.openAfterEffect)
        makeACoolButton('go to Premiere', "premiereicon.png", self.openPremiere)

        cmds.showWindow('DAMGgo2AppsUI')

    def openZbrush(self, *args):
        for r,d,f in os.walk(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Pixologic"):
            for files in f:
                if files == "ZBrush 4R7 64-bit.exe":
                    filepath = os.path.join(r,files)
                    os.startfile(filepath)
                    sys.exit()
                else:
                    for r,d,f in os.walk(r"C:\Apps"):
                        for files in f:
                            if files == "ZBrush 4R7 64-bit.exe":
                                filepath = os.path.join(r,files)
                                os.startfile(filepath)

    def openMudbox(self, *args):
        for r,d,f in os.walk(r"C:\Program Files\Autodesk"):
            for files in f:
                if files == "mudbox.exe":
                    filepath = os.path.join(r,files)
                    os.startfile(filepath)
                    sys.exit()
                else:
                    for r,d,f in os.walk(r"C:\Apps\Autodesk"):
                        for files in f:
                            if files == "mudbox.exe":
                                filepath = os.path.join(r,files)
                                os.startfile(filepath)

    def openHoudini(self, *args):
        for r,d,f in os.walk(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"):
            for files in f:
                if files == "Houdini FX 15.0.393.exe":
                    filepath = os.path.join(r,files)
                    os.startfile(filepath)
                    sys.exit()
                else:
                    for r,d,f in os.walk(r"C:\Apps\Autodesk"):
                        for files in f:
                            if files == "Houdini FX 15.0.393.exe":
                                filepath = os.path.join(r,files)
                                os.startfile(filepath)

    def openMari(self, *args):
        for r,d,f in os.walk(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"):
            for files in f:
                if files == "Mari 3.0v2.exe":
                    filepath = os.path.join(r,files)
                    os.startfile(filepath)
                    sys.exit()
                else:
                    for r,d,f in os.walk(r"C:\Apps"):
                        for files in f:
                            if files == "Mari 3.0v2.exe":
                                filepath = os.path.join(r,files)
                                os.startfile(filepath)

    def openNuke(self, *args):
        for r,d,f in os.walk(r"C:\Program Files"):
            for files in f:
                if files == "Nuke10.0.exe":
                    filepath = os.path.join(r,files)
                    os.startfile(filepath)
                    sys.exit()
                else:
                    for r,d,f in os.walk(r"C:\Apps"):
                        for files in f:
                            if files == "Nuke10.0.exe":
                                filepath = os.path.join(r,files)
                                os.startfile(filepath)

    def openHiero(self, *args):
        for r,d,f in os.walk(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"):
            for files in f:
                if files == "Hiero10.0v4.exe":
                    filepath = os.path.join(r,files)
                    os.startfile(filepath)
                    sys.exit()
                else:
                    for r,d,f in os.walk(r"C:\Apps"):
                        for files in f:
                            if files == "Hiero10.0v4.exe":
                                filepath = os.path.join(r,files)
                                os.startfile(filepath)

    def openPhotoshop(self, *args):
        for r,d,f in os.walk(r"C:\Program Files\Adobe\Adobe Photoshop CC 2015"):
            for files in f:
                if files == "Photoshop.exe":
                    filepath = os.path.join(r,files)
                    os.startfile(filepath)
                    sys.exit()
                else:
                    for r,d,f in os.walk(r"C:\Apps"):
                        for files in f:
                            if files == "Photoshop.exe":
                                filepath = os.path.join(r,files)
                                os.startfile(filepath)

    def openIllustrator(self, *args):
        for r,d,f in os.walk(r"C:\Program Files\Adobe\Adobe Illustrator CC 2014"):
            for files in f:
                if files == "Adobe Illustrator CC 2014.exe":
                    filepath = os.path.join(r,files)
                    os.startfile(filepath)
                    sys.exit()
                else:
                    for r,d,f in os.walk(r"C:\Apps"):
                        for files in f:
                            if files == "Adobe Illustrator CC 2014.exe":
                                filepath = os.path.join(r,files)
                                os.startfile(filepath)

    def openAfterEffect(self, *args):
        for r,d,f in os.walk(r"C:\Program Files\Adobe\Adobe After Effects CC 2014"):
            for files in f:
                if files == "Adobe After Effects CC 2014.exe":
                    filepath = os.path.join(r,files)
                    os.startfile(filepath)
                    sys.exit()
                else:
                    for r,d,f in os.walk(r"C:\Apps"):
                        for files in f:
                            if files == "Adobe After Effects CC 2014.exe":
                                filepath = os.path.join(r,files)
                                os.startfile(filepath)

    def openPremiere(self, *args):
        for r,d,f in os.walk(r"C:\Program Files\Adobe\Adobe Premiere Pro CC 2014"):
            for files in f:
                if files == "Adobe Premiere Pro.exe":
                    filepath = os.path.join(r,files)
                    os.startfile(filepath)
                    sys.exit()
                else:
                    for r,d,f in os.walk(r"C:\Apps"):
                        for files in f:
                            if files == "Adobe Premiere Pro.exe":
                                filepath = os.path.join(r,files)
                                os.startfile(filepath)
