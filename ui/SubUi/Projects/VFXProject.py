#!/usr/bin/env python3
# -*-coding:utf-8 -*
"""

Script Name: ProdFolder.py

Author: Do Trinh/Jimmy - 3D artist, leader DAMG team.

Description:
    This script is main file to create folder structure in pipeline

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
from functools import partial

# PyQt5
from PyQt5.QtWidgets            import (QGroupBox, QInputDialog, QComboBox, QFileDialog, QListWidget, QListWidgetItem)

# PLM
from devkit.Widgets           import Widget, Label, HBoxLayout, Button, GridLayout, LineEdit, VBoxLayout

# -------------------------------------------------------------------------------------------------------------
""" Sub class """

class ItemWidget(Widget):

    key = "ItemWidget"

    def __init__(self, section, name="", parent=None):
        super(ItemWidget, self).__init__(parent)

        self.section            = section
        self.item               = Label({'txt': name})
        self.setLayout(
                        HBoxLayout({'addWidget': [self.item,
                                                  Button({'txt' :"Edit", 
                                                          'stt' :"Edit character name", 
                                                          'cl'  : self.setText})]
                                   })
                        )

    def setText(self):
        text, ok = QInputDialog.getText(self, "Change To", "{0} name:".format(self.section), LineEdit.Normal, self.item.text())
        if ok and text != "":
            self.item.setText(text)

# -------------------------------------------------------------------------------------------------------------
""" Create Project Window """

class VFXProject(Widget):

    info                        = {}
    key                         = 'VFXProject'

    def __init__(self, parent=None):
        super(VFXProject, self).__init__(parent)

        self.layout = GridLayout(self)
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        MESSAGE = "DUE TO THE POSSIBILITY OF USING RENDER FARM SERVICE, PLEAE SET PROJECT PATH TO E DRIVE\n " \
                  "IF YOU DO NOT USE RENDER FARM, DRIVE E IS STILL PREFER."

        TITLE = "SET UP NEW PROJECT"

        # Title
        headGrp, headGrid = self.styleGB()
        headGrid.addWidget(Label({'txt': TITLE}))

        # Project Info
        prjInfGrp, prjInfGrid   = self.styleGB("Project Info")
        self.prjLong            = LineEdit({'txt': "DAMG team project"})
        self.prjShort           = LineEdit({'txt': "damg"})
        self.prjPth             = LineEdit({'txt': "E:/"})

        setPthBtn = Button({'txt': "Set Path", 'stt': "Set project path", 'cl': self.onSetPthBtnClicked})

        prjInfGrid.addWidget(Label({'txt': "Project Name"}), 0, 0, 1, 1)
        prjInfGrid.addWidget(self.prjLong, 0, 1, 1, 1)
        prjInfGrid.addWidget(Label({'txt': "Abbreviated as"}), 0, 2, 1, 1)
        prjInfGrid.addWidget(self.prjShort, 0, 3, 1, 1)
        prjInfGrid.addWidget(setPthBtn, 1, 0, 1, 1)
        prjInfGrid.addWidget(self.prjPth, 1, 1, 1, 3)

        # Notice!!!
        noticeGrp, noticeGrid = self.styleGB("NOTE!!!")
        noticeGrid.addWidget(Label({'txt': MESSAGE}), 0, 0, 1, 4)

        # Project details
        prjDetailGrp, prjDetailGrid = self.styleGB("Project Details")

        self.prjMode            = QComboBox()
        self.prjMode.addItem("Studio Mode")
        self.prjMode.addItem("Group Mode")

        self.numOfChar          = LineEdit({'txt': "1", 'validator': 'int'})
        self.numOfChar.textChanged.connect(partial(self.populate_lst, "char"))

        self.numOfEnv           = LineEdit({'txt': "1", 'validator': 'int'})
        self.numOfEnv.textChanged.connect(partial(self.populate_lst, "env"))

        self.numOfProp          = LineEdit({'txt': "1", 'validator': 'int'})
        self.numOfProp.textChanged.connect(partial(self.populate_lst, "prop"))

        self.numOfSeq           = LineEdit({'txt': "1", 'validator': 'int'})
        self.numOfSeq.textChanged.connect(partial(self.populate_lst, "seq"))

        prjDetailGrid.addWidget(Label({'txt':"Project Mode"}), 0,0,1,1)
        prjDetailGrid.addWidget(self.prjMode, 0, 1, 1, 1)
        prjDetailGrid.addWidget(Label({'txt':"Character: "}), 1,0,1,1)
        prjDetailGrid.addWidget(self.numOfChar, 2, 0, 1, 1)
        prjDetailGrid.addWidget(Label({'txt':"Environment: "}), 1,1,1,1)
        prjDetailGrid.addWidget(self.numOfEnv, 2, 1, 1, 1)
        prjDetailGrid.addWidget(Label({'txt':"Props: "}), 1,2,1,1)
        prjDetailGrid.addWidget(self.numOfProp, 2, 2, 1, 1)
        prjDetailGrid.addWidget(Label({'txt':"Sequences: "}), 1,3,1,1)
        prjDetailGrid.addWidget(self.numOfSeq, 2, 3, 1, 1)

        # Asset details
        charGrp, self.charLst   = self.styleGBLst("Character List")
        envGrp, self.envLst     = self.styleGBLst("Environment List")
        propGrp, self.propLst   = self.styleGBLst("Props List")

        # Shot details
        seqGrp, self.seqLst     = self.styleGBLst("Sequences List")

        # Buttons
        btnGrp, btnGrid         = self.styleGB()

        prjLstBtn               = Button({'txt': "Project List", 'stt': "Project List"})
        crewLstBtn              = Button({'txt': "Crews List", 'stt': "Crews List"})
        newPrjBtn               = Button({'txt': "Create Project", 'stt': "Create New Project"})
        cancelBtn               = Button({'txt': "Cancel", 'stt': "Cancel"})

        btnGrid.addWidget(prjLstBtn, 0, 0)
        btnGrid.addWidget(crewLstBtn, 0, 1)
        btnGrid.addWidget(newPrjBtn, 0, 2)
        btnGrid.addWidget(cancelBtn, 0, 3)

        self.layout.addWidget(headGrp, 0, 0, 1, 4)
        self.layout.addWidget(prjInfGrp, 1, 0, 2, 4)
        self.layout.addWidget(noticeGrp, 3, 0, 1, 4)
        self.layout.addWidget(prjDetailGrp, 5,0,3,4)
        self.layout.addWidget(charGrp, 8,0,1,1)
        self.layout.addWidget(envGrp, 8,1,1,1)
        self.layout.addWidget(propGrp, 8,2,1,1)
        self.layout.addWidget(seqGrp, 8,3,1,1)
        self.layout.addWidget(btnGrp, 9,0,1,4)

        sections = ["char", "env", "prop", "seq"]
        for section in sections:
            self.populate_lst(section)

    def getZ(self, value):
        if value < 10:
            z = 1
        elif value < 100:
            z = 2
        elif value < 1000:
            z = 3
        else:
            z = 4
        return z

    def styleGB(self, title="", tl="grid"):
        if title == "":
            grpBox = QGroupBox()
        else:
            grpBox = QGroupBox(title)

        if tl.lower() == "grid":
            layout = GridLayout()
        elif tl.lower() == "hbox":
            layout = HBoxLayout()
        elif tl.lower() == "vbox":
            layout = VBoxLayout()

        grpBox.setLayout(layout)

        return grpBox, layout

    def styleGBLst(self, title=""):
        grpBox, hbox = self.styleGB(title, "hbox")
        listWidget = QListWidget()
        hbox.addWidget(listWidget)

        return grpBox, listWidget

    def onSetPthBtnClicked(self):
        opts = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        dir = QFileDialog.getExistingDirectory(self, "Set production path", self.prjPth.text(), options=opts)

        if dir:
            self.prjPth.setText(dir)
        else:
            self.logger.debug("You should set a valid path")

    def populate_lst(self, name="char"):
        if name.lower() == "char":
            lst = self.charLst
            value = int(self.numOfChar.text())
        elif name.lower() == "env":
            lst = self.envLst
            value = int(self.numOfEnv.text())
        elif name.lower() == "prop":
            lst = self.propLst
            value = int(self.numOfProp.text())
        elif name.lower() == "seq":
            lst = self.seqLst
            value = int(self.numOfSeq.text())
        else:
            lst = None
            value = 0

        lst.clear()
        z = self.getZ(value)

        for i in range(value):
            item = QListWidgetItem(lst)
            itemWidget = ItemWidget(name.lower(), "{0}_{1}".format(name.lower(), str(i+1).zfill(z)))
            item.setSizeHint(itemWidget.sizeHint())
            lst.addItem(item)
            lst.setItemWidget(item, itemWidget)

    # def setPth(self, *args):
    #     pth = cmds.fileDialog2(cap="set production path", fn=3, okc="Set")
    #     dir = self.getDirFromUnicode(pth[0])
    #     cmds.textField(self.setPath, edit=True, tx=dir)
    #
    # def createProject(self, *args):
    #     prjName = cmds.textField(self.prodName, q=True, tx=True)
    #     setPth = cmds.textField(self.setPath, q=True, tx=True)
    #     self.rootPth = os.path.join(setPth, prjName)
    #
    #     if os.path.exists(self.rootPth):
    #         cmds.confirmDialog(t="Opps",
    #                            m="The path: %s\nis NOT EMPTY or:\nthis NAME has been USED for another project\n"
    #                              "please choose another name" % self.rootPth, b="Ok")
    #         sys.exit()
    #
    #     self.shortName = cmds.textField(self.prodShort, q=True, tx=True)
    #
    #     self.modeSetting = cmds.optionMenu(self.setMode, q=True, v=True)
    #
    #     self.numSeq = cmds.intField(self.numShot, q=True, v=True)
    #     self.numOfChar = cmds.intField(self.numChar, q=True, v=True)
    #     self.numOfEnv = cmds.intField(self.numEnv, q=True, v=True)
    #     self.numOfProps = cmds.intField(self.numProps, q=True, v=True)
    #
    #     # Create content by set fn
    #     if self.modeSetting == "Studio Mode":
    #         self.prjStudioMode()
    #     elif self.modeSetting == "Group Mode":
    #         self.prjGroupMode()
    #
    # def prjStudioMode(self, *args):
    #     # Create master folder
    #     os.mkdir(self.rootPth)
    #     # Create content of master Folder
    #     master = ["assets", "sequences", "deliverables", "docs", "editorial", "sound", "rcs", "RnD"]
    #     steps = ["publish", "review", "work"]
    #     mayaFolders = ["scenes", "sourceimages", "images", "movie", "alembic", "reference"]
    #
    #     for f in master:
    #         contentMasterPth = os.path.join(self.rootPth, f)
    #         os.mkdir(contentMasterPth)
    #
    #     # Assets content
    #     assetsTasks = ["art", "plt_model", "surfacing", "rigging"]
    #     assetsSections = ["characters", "environment", "props"]
    #
    #     assetsPth = os.path.join(self.rootPth, "assets")
    #     for section in assetsSections:
    #         assetsSectionsPth = os.path.join(assetsPth, section)
    #         os.mkdir(assetsSectionsPth)
    #         if section == "characters":
    #             for i in range(self.numOfChar):
    #                 charName = "char" + str(i + 1)
    #                 folCharName = cmds.textField(charName, q=True, tx=True)
    #                 if folCharName == "" or folCharName == None:
    #                     folCharName = "character_" + str(i + 1)
    #                 folCharPth = os.path.join(assetsSectionsPth, folCharName)
    #                 os.mkdir(folCharPth)
    #                 for task in assetsTasks:
    #                     assetsTaskPth = os.path.join(folCharPth, task)
    #                     os.mkdir(assetsTaskPth)
    #                     for step in steps:
    #                         assetsTaskStepPth = os.path.join(assetsTaskPth, step)
    #                         os.mkdir(assetsTaskStepPth)
    #                     assetsWorkTaskPth = os.path.join(assetsTaskPth, "work")
    #                     if task == "art":
    #                         apps = ["photoshop", "maya"]
    #                     elif task == "plt_model":
    #                         apps = ["zbrush", "maya", "mudbox", "houdini"]
    #                     elif task == "surfacing":
    #                         apps = ["mari", "maya", "substance", "photoshop"]
    #                     elif task == "rigging":
    #                         apps = ["maya"]
    #
    #                     for app in apps:
    #                         appPth = os.path.join(assetsWorkTaskPth, app)
    #                         os.mkdir(appPth)
    #                         if app == "maya":
    #                             for f in mayaFolders:
    #                                 mayaPth = os.path.join(appPth, f)
    #                                 os.mkdir(mayaPth)
    #                 i += 1
    #         elif section == "environment":
    #             for i in range(self.numOfEnv):
    #                 envName = "env" + str(i + 1)
    #                 folEnvName = cmds.textField(envName, q=True, tx=True)
    #                 if folEnvName == "" or folEnvName == None:
    #                     folEnvName = "env_" + str(i + 1)
    #                 folEnvPth = os.path.join(assetsSectionsPth, folEnvName)
    #                 os.mkdir(folEnvPth)
    #                 for task in assetsTasks:
    #                     assetsTaskPth = os.path.join(folEnvPth, task)
    #                     os.mkdir(assetsTaskPth)
    #                     for step in steps:
    #                         assetsTaskStepPth = os.path.join(assetsTaskPth, step)
    #                         os.mkdir(assetsTaskStepPth)
    #                     assetsWorkTaskPth = os.path.join(assetsTaskPth, "work")
    #                     if task == "art":
    #                         apps = ["photoshop", "maya"]
    #                     elif task == "plt_model":
    #                         apps = ["zbrush", "maya", "mudbox", "houdini"]
    #                     elif task == "surfacing":
    #                         apps = ["mari", "maya", "substance", "photoshop"]
    #                     elif task == "rigging":
    #                         apps = ["maya"]
    #
    #                     for app in apps:
    #                         appPth = os.path.join(assetsWorkTaskPth, app)
    #                         os.mkdir(appPth)
    #                         if app == "maya":
    #                             for f in mayaFolders:
    #                                 mayaPth = os.path.join(appPth, f)
    #                                 os.mkdir(mayaPth)
    #                 i += 1
    #         elif section == "props":
    #             for i in range(self.numOfProps):
    #                 propsName = "props" + str(i + 1)
    #                 folPropsName = cmds.textField(propsName, q=True, tx=True)
    #                 print type(folPropsName)
    #
    #                 if folPropsName == "" or folPropsName == None:
    #                     folPropsName = "props_" + str(i + 1)
    #
    #                 folPropsPth = os.path.join(assetsSectionsPth, folPropsName)
    #
    #                 print folPropsPth + " 4"
    #
    #                 os.mkdir(folPropsPth)
    #                 for task in assetsTasks:
    #                     assetsTaskPth = os.path.join(folPropsPth, task)
    #                     os.mkdir(assetsTaskPth)
    #                     for step in steps:
    #                         assetsTaskStepPth = os.path.join(assetsTaskPth, step)
    #                         os.mkdir(assetsTaskStepPth)
    #                     assetsWorkTaskPth = os.path.join(assetsTaskPth, "work")
    #                     if task == "art":
    #                         apps = ["photoshop", "maya"]
    #                     elif task == "plt_model":
    #                         apps = ["zbrush", "maya", "mudbox", "houdini"]
    #                     elif task == "surfacing":
    #                         apps = ["mari", "maya", "substance", "photoshop"]
    #                     elif task == "rigging":
    #                         apps = ["maya"]
    #
    #                     for app in apps:
    #                         appPth = os.path.join(assetsWorkTaskPth, app)
    #                         os.mkdir(appPth)
    #                         if app == "maya":
    #                             for f in mayaFolders:
    #                                 mayaPth = os.path.join(appPth, f)
    #                                 os.mkdir(mayaPth)
    #                 i += 1
    #
    #     # Sequences content
    #
    #     seqTask = ["anim", "comp", "fx", "layout", "lighting"]
    #
    #     sequencesPth = os.path.join(self.rootPth, "sequences")
    #     for i in range(self.numSeq):
    #         folName = self.shortName + "_" + "shot_" + str(i + 1)
    #         seqPth = os.path.join(sequencesPth, folName)
    #         os.mkdir(seqPth)
    #         for task in seqTask:
    #             seqTaskPth = os.path.join(seqPth, task)
    #             os.mkdir(seqTaskPth)
    #             for step in steps:
    #                 seqTaskStepPth = os.path.join(seqTaskPth, step)
    #                 os.mkdir(seqTaskStepPth)
    #             seqTaskWorkPth = os.path.join(seqTaskPth, "work")
    #             if task == "anim":
    #                 apps = ["maya", "after effect", "houdini"]
    #             elif task == "comp":
    #                 apps = ["nuke", "after effect", "photoshop"]
    #             elif task == "fx":
    #                 apps = ["maya", "houdini"]
    #             elif task == "layout":
    #                 apps = ["maya"]
    #             elif task == "lighting":
    #                 apps = ["maya"]
    #
    #             for app in apps:
    #                 appPth = os.path.join(seqTaskWorkPth, app)
    #                 os.mkdir(appPth)
    #                 if app == "maya":
    #                     for f in mayaFolders:
    #                         mayaPth = os.path.join(appPth, f)
    #                         os.mkdir(mayaPth)
    #         i += 1
    #
    # def prjGroupMode(self, *args):
    #     pass
    #
    # def getDirFromUnicode(self, path, *args):
    #     for dirpath, dirnames, filenames in os.walk(path):
    #         return dirpath


