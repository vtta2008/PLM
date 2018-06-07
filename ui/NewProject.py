#!/usr/bin/env python3
# -*-coding:utf-8 -*
"""

Script Name: ProdFolder.py

Author: Do Trinh/Jimmy - 3D artist, leader DAMG team.

Description:
    This script is main file to create folder structure in pipeline

"""
# -------------------------------------------------------------------------------------------------------------

import logging
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui import uirc as rc

# -------------------------------------------------------------------------------------------------------------
# VARIABLES
# -------------------------------------------------------------------------------------------------------------
DESKTOPPTH = os.path.join(os.environ['HOMEPATH'], 'desktop')

PRODPROFILE = dict(name=['mwm', 'Midea Wasing Machine'])
WINPROFILE = dict(prodpthUI=['ProdPthUI', 'Create New Project', 'SET UP NEW PROJECT'])

APPS = ['maya', 'zbrush', 'mari', 'nuke', 'photoshop', 'houdini', 'after effects']

MASTER = ['assets', 'sequences', 'deliverables', 'documents', 'editorial', 'sound', 'resources', 'RnD']
TASKS = ['art', 'plt_model', 'rigging', 'surfacing']
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

class ItemWidget(QWidget):

    def __init__(self, section, name="", parent=None):
        super(ItemWidget, self).__init__(parent)
        self.section = section

        self.item = QLabel(name)
        button = QPushButton('Change')
        button.clicked.connect(self.setText)
        layout = QHBoxLayout()
        layout.addWidget(self.item)
        layout.addWidget(button)

        self.setLayout(layout)

    def setText(self):
        text, ok = QInputDialog.getText(self, "Change To",
                                        "%s name:" % self.section, QLineEdit.Normal, self.item.text())
        if ok and text != '':
            self.item.setText(text)


class NewProject(QDialog):

    info = {}

    def __init__(self, id='Create New Project', icon=rc.IconPth('New Project'), parent=None):
        super(NewProject, self).__init__(parent)

        self.setWindowTitle(id)
        self.setWindowIcon(QIcon(icon))
        # self.setFixedSize(600, 800)

        central_widget = QWidget(self)
        self.layout = QGridLayout(self)
        central_widget.setLayout(self.layout)

        self.buildUI()

    def buildUI(self):

        MESSAGE = """DUE TO THE POSSIBILITY TO USE ONLINE RENDER SERVICE SETTING PATH TO E DRIVE 
        IS ALWAYS PREFERABLE IF YOU DO NOT USE THAT KIND OF SERVICE, NEVER MIND"""

        headerGroupBox = QGroupBox()
        headerLayout = QGridLayout()
        titleLabel = QLabel('SET UP NEW PROJECT')
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setMinimumHeight(20)
        headerLayout.addWidget(titleLabel, 0,0,Qt.AlignCenter)
        headerGroupBox.setLayout(headerLayout)
        self.layout.addWidget(headerGroupBox, 0,0,1,4)

        projInfoGroupBox = QGroupBox('Project Info')
        projInfoLayout = QGridLayout()
        projNameLable = self.makeQLabel('Project Name')
        self.projNameField = QLineEdit('Voxel Picture Project')
        projAbbreviated = self.makeQLabel('Abbreviated as')
        self.projAbbrevName = QLineEdit('vxp')
        setPthBtn = QPushButton('Set Path')
        setPthBtn.clicked.connect(self.onSetPthBtnClicked)
        self.projPathField = QLineEdit("E:/")

        noticeGroupBox = QGroupBox('NOTE!!!')
        noticeLayout = QGridLayout()
        noticeQlabel = self.makeQLabel(MESSAGE)
        noticeGroupBox.setLayout(noticeLayout)

        projDetailsGroupBox = QGroupBox('Project Details')
        projDetailsLayout = QGridLayout()
        prjModeLabel = self.makeQLabel('Project Mode')
        self.projModeComboBox = QComboBox()
        self.projModeComboBox.addItem('Studio Mode')
        self.projModeComboBox.addItem('Group Mode')

        characterLabel = self.makeQLabel('Character: ')
        environmentLabel = self.makeQLabel('Environment: ')
        sequencesLabel = self.makeQLabel('Sequences: ')
        propsLabel = self.makeQLabel('Props: ')

        self.number_of_character = QIntValidator()
        self.characterIntField = QLineEdit('1')
        self.characterIntField.setValidator(self.number_of_character)
        self.characterIntField.textChanged.connect(self.onCharacterIntFieldChanged)

        self.number_of_environment = QIntValidator()
        self.environmentIntField = QLineEdit('1')
        self.environmentIntField.setValidator(self.number_of_environment)
        self.environmentIntField.textChanged.connect(self.onEnvironmentIntFieldChanged)

        self.number_of_props = QIntValidator()
        self.propsIntField = QLineEdit('1')
        self.propsIntField.setValidator(self.number_of_props)
        self.propsIntField.textChanged.connect(self.onPropsIntFieldChanged)

        self.number_of_sequences = QIntValidator()
        self.sequencesIntField = QLineEdit('1')
        self.sequencesIntField.setValidator(self.number_of_sequences)
        self.sequencesIntField.textChanged.connect(self.onSequencesIntFieldChanged)

        projDetailsGroupBox.setLayout(projDetailsLayout)
        characterListGroupBox = QGroupBox('Character List')
        characterListLayout = QHBoxLayout()
        self.characterListWidget = QListWidget()
        characterListLayout.addWidget(self.characterListWidget)
        characterListGroupBox.setLayout(characterListLayout)


        environmentListGroupBox = QGroupBox('Environment List')
        environmentListLayout = QHBoxLayout()
        self.environmentListWidget = QListWidget()
        environmentListLayout.addWidget(self.environmentListWidget)
        environmentListGroupBox.setLayout(environmentListLayout)


        propsListGroupBox = QGroupBox('Props List')
        propsListLayout = QHBoxLayout()
        self.propsListWidget = QListWidget()

        sequencesListGroupBox = QGroupBox('Sequences List')
        sequencesListLayout = QHBoxLayout()
        self.sequencesListWidget = QListWidget()
        sequencesListLayout.addWidget(self.sequencesListWidget)
        sequencesListGroupBox.setLayout(sequencesListLayout)
        propsListLayout.addWidget(self.propsListWidget)
        propsListGroupBox.setLayout(propsListLayout)

        buttonGroupBox = QGroupBox()
        buttonGroupLayout = QGridLayout()
        checkPrjListBtn = QPushButton('Project List')
        checkCrewListBtn = QPushButton('Crews List')
        createPrjBtn = QPushButton('Create Project')
        cancelBtn = QPushButton('Cancel')
        buttonGroupBox.setLayout(buttonGroupLayout)

        projInfoLayout.addWidget(projNameLable, 0,0,1,1)
        projInfoLayout.addWidget(self.projNameField, 0,1,1,1)
        projInfoLayout.addWidget(projAbbreviated, 0,2,1,1)
        projInfoLayout.addWidget(self.projAbbrevName, 0,3,1,1)
        projInfoLayout.addWidget(setPthBtn, 1,0,1,1)
        projInfoLayout.addWidget(self.projPathField, 1,1,1,3)
        projInfoGroupBox.setLayout(projInfoLayout)
        self.layout.addWidget(projInfoGroupBox, 1, 0, 2, 4)
        noticeLayout.addWidget(noticeQlabel, 0,0,1,4)
        self.layout.addWidget(noticeGroupBox, 3,0,2,4)
        projDetailsLayout.addWidget(prjModeLabel, 0,0,1,1)
        projDetailsLayout.addWidget(self.projModeComboBox, 0,1,1,1)
        projDetailsLayout.addWidget(characterLabel, 1,0,1,1)
        projDetailsLayout.addWidget(self.characterIntField, 2,0,1,1)
        projDetailsLayout.addWidget(environmentLabel, 1,1,1,1)
        projDetailsLayout.addWidget(self.environmentIntField, 2,1,1,1)
        projDetailsLayout.addWidget(propsLabel, 1,2,1,1)
        projDetailsLayout.addWidget(self.propsIntField, 2,2,1,1)
        projDetailsLayout.addWidget(sequencesLabel, 1,3,1,1)
        projDetailsLayout.addWidget(self.sequencesIntField, 2,3,1,1)
        buttonGroupLayout.addWidget(checkPrjListBtn, 0, 0)
        buttonGroupLayout.addWidget(checkCrewListBtn, 0, 1)
        buttonGroupLayout.addWidget(createPrjBtn, 0, 2)
        buttonGroupLayout.addWidget(cancelBtn, 0, 3)
        self.layout.addWidget(projDetailsGroupBox, 5,0,3,4)
        self.layout.addWidget(characterListGroupBox, 8,0,1,1)
        self.layout.addWidget(environmentListGroupBox, 8,1,1,1)
        self.layout.addWidget(propsListGroupBox, 8,2,1,1)
        self.layout.addWidget(sequencesListGroupBox, 8,3,1,1)
        self.layout.addWidget(buttonGroupBox, 9,0,1,4)

        self.setLayout(self.layout)

    def makeQLabel(self, text, align='c'):
        if align == 'l':
            al = Qt.AlignLeft
        elif align == 'r':
            al = Qt.AlignRight
        else:
            al = Qt.AlignCenter

        label = QLabel(text)
        label.setAlignment(al)
        return label

    def onSetPthBtnClicked(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                                                     "Set production path",
                                                     self.projPathField.text(), options=options)
        if directory:
            self.projPathField.setText(directory)

    def onCharacterIntFieldChanged(self):
        char_section = 'Character'
        char_value = int(self.characterIntField.text())
        if char_value < 10:
            cz = 1
        elif char_value < 100:
            cz = 2
        elif char_value < 1000:
            cz = 3
        else:
            cz = 4
        self.characterListWidget.clear()
        for i in range(char_value):
            char_name = '%s_%s' % (char_section, str(i+1).zfill(cz))
            char_item = QListWidgetItem(self.characterListWidget)
            char_item_widget = ItemWidget(char_section, char_name)
            char_item.setSizeHint(char_item_widget.sizeHint())
            self.characterListWidget.addItem(char_item)
            self.characterListWidget.setItemWidget(char_item, char_item_widget)

    def onEnvironmentIntFieldChanged(self):
        env_section = 'Environment'
        env_value = int(self.environmentIntField.text())
        if env_value < 10:
            ez = 1
        elif env_value < 100:
            ez = 2
        elif env_value < 1000:
            ez = 3
        else:
            ez = 4
        self.environmentListWidget.clear()
        for i in range(env_value):
            env_name = "%s_%s" % (env_section, str(i+1).zfill(ez))
            env_item = QListWidgetItem(self.environmentListWidget)
            env_item_widget = ItemWidget(env_section, env_name)
            env_item.setSizeHint(env_item_widget.sizeHint())
            self.environmentListWidget.addItem(env_item)
            self.environmentListWidget.setItemWidget(env_item, env_item_widget)

    def onPropsIntFieldChanged(self):
        section = 'Props'
        value = int(self.propsIntField.text())
        if value < 10:
            z = 1
        elif value < 100:
            z = 2
        elif value < 1000:
            z = 3
        else:
            z = 4
        self.propsListWidget.clear()

        for i in range(value):
            name = '%s_%s' % (section,str(i+1).zfill(z))
            item = QListWidgetItem(self.propsListWidget)
            item_widget = ItemWidget(section, name)
            item.setSizeHint(item_widget.sizeHint())
            self.propsListWidget.addItem(item)
            self.propsListWidget.setItemWidget(item, item_widget)

    def onSequencesIntFieldChanged(self):
        section = 'Sequences'
        value = int(self.sequencesIntField.text())
        if value < 10:
            z = 1
        elif value < 100:
            z = 2
        elif value < 1000:
            z = 3
        else:
            z = 4
        self.sequencesListWidget.clear()

        for i in range(value):
            name = '%s_%s' % (section,str(i+1).zfill(z))
            item = QListWidgetItem(self.sequencesListWidget)
            item_widget = ItemWidget(section, name)
            item.setSizeHint(item_widget.sizeHint())
            self.sequencesListWidget.addItem(item)
            self.sequencesListWidget.setItemWidget(item, item_widget)

    # def setPth(self, *args):
    #     pth = cmds.fileDialog2(cap='set production path', fm=3, okc='Set')
    #     dir = self.getDirFromUnicode(pth[0])
    #     cmds.textField(self.setPath, edit=True, tx=dir)
    #
    # def createProject(self, *args):
    #     prjName = cmds.textField(self.prodName, q=True, tx=True)
    #     setPth = cmds.textField(self.setPath, q=True, tx=True)
    #     self.rootPth = os.path.join(setPth, prjName)
    #
    #     if os.path.exists(self.rootPth):
    #         cmds.confirmDialog(t='Opps',
    #                            m='The path: %s\nis NOT EMPTY or:\nthis NAME has been USED for another project\n'
    #                              'please choose another name' % self.rootPth, b='Ok')
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
    #     # Create content by set mode
    #     if self.modeSetting == 'Studio Mode':
    #         self.prjStudioMode()
    #     elif self.modeSetting == 'Group Mode':
    #         self.prjGroupMode()
    #
    # def prjStudioMode(self, *args):
    #     # Create master folder
    #     os.mkdir(self.rootPth)
    #     # Create content of master Folder
    #     master = ['assets', 'sequences', 'deliverables', 'documents', 'editorial', 'sound', 'resources', 'RnD']
    #     steps = ['publish', 'review', 'work']
    #     mayaFolders = ['scenes', 'sourceimages', 'images', 'movie', 'alembic', 'reference']
    #
    #     for f in master:
    #         contentMasterPth = os.path.join(self.rootPth, f)
    #         os.mkdir(contentMasterPth)
    #
    #     # Assets content
    #     assetsTasks = ['art', 'plt_model', 'surfacing', 'rigging']
    #     assetsSections = ['characters', 'environment', 'props']
    #
    #     assetsPth = os.path.join(self.rootPth, 'assets')
    #     for section in assetsSections:
    #         assetsSectionsPth = os.path.join(assetsPth, section)
    #         os.mkdir(assetsSectionsPth)
    #         if section == 'characters':
    #             for i in range(self.numOfChar):
    #                 charName = 'char' + str(i + 1)
    #                 folCharName = cmds.textField(charName, q=True, tx=True)
    #                 if folCharName == "" or folCharName == None:
    #                     folCharName = 'character_' + str(i + 1)
    #                 folCharPth = os.path.join(assetsSectionsPth, folCharName)
    #                 os.mkdir(folCharPth)
    #                 for task in assetsTasks:
    #                     assetsTaskPth = os.path.join(folCharPth, task)
    #                     os.mkdir(assetsTaskPth)
    #                     for step in steps:
    #                         assetsTaskStepPth = os.path.join(assetsTaskPth, step)
    #                         os.mkdir(assetsTaskStepPth)
    #                     assetsWorkTaskPth = os.path.join(assetsTaskPth, 'work')
    #                     if task == 'art':
    #                         apps = ['photoshop', 'maya']
    #                     elif task == 'plt_model':
    #                         apps = ['zbrush', 'maya', 'mudbox', 'houdini']
    #                     elif task == 'surfacing':
    #                         apps = ['mari', 'maya', 'substance', 'photoshop']
    #                     elif task == 'rigging':
    #                         apps = ['maya']
    #
    #                     for app in apps:
    #                         appPth = os.path.join(assetsWorkTaskPth, app)
    #                         os.mkdir(appPth)
    #                         if app == 'maya':
    #                             for f in mayaFolders:
    #                                 mayaPth = os.path.join(appPth, f)
    #                                 os.mkdir(mayaPth)
    #                 i += 1
    #         elif section == 'environment':
    #             for i in range(self.numOfEnv):
    #                 envName = 'env' + str(i + 1)
    #                 folEnvName = cmds.textField(envName, q=True, tx=True)
    #                 if folEnvName == "" or folEnvName == None:
    #                     folEnvName = 'env_' + str(i + 1)
    #                 folEnvPth = os.path.join(assetsSectionsPth, folEnvName)
    #                 os.mkdir(folEnvPth)
    #                 for task in assetsTasks:
    #                     assetsTaskPth = os.path.join(folEnvPth, task)
    #                     os.mkdir(assetsTaskPth)
    #                     for step in steps:
    #                         assetsTaskStepPth = os.path.join(assetsTaskPth, step)
    #                         os.mkdir(assetsTaskStepPth)
    #                     assetsWorkTaskPth = os.path.join(assetsTaskPth, 'work')
    #                     if task == 'art':
    #                         apps = ['photoshop', 'maya']
    #                     elif task == 'plt_model':
    #                         apps = ['zbrush', 'maya', 'mudbox', 'houdini']
    #                     elif task == 'surfacing':
    #                         apps = ['mari', 'maya', 'substance', 'photoshop']
    #                     elif task == 'rigging':
    #                         apps = ['maya']
    #
    #                     for app in apps:
    #                         appPth = os.path.join(assetsWorkTaskPth, app)
    #                         os.mkdir(appPth)
    #                         if app == 'maya':
    #                             for f in mayaFolders:
    #                                 mayaPth = os.path.join(appPth, f)
    #                                 os.mkdir(mayaPth)
    #                 i += 1
    #         elif section == 'props':
    #             for i in range(self.numOfProps):
    #                 propsName = 'props' + str(i + 1)
    #                 folPropsName = cmds.textField(propsName, q=True, tx=True)
    #                 print type(folPropsName)
    #
    #                 if folPropsName == "" or folPropsName == None:
    #                     folPropsName = 'props_' + str(i + 1)
    #
    #                 folPropsPth = os.path.join(assetsSectionsPth, folPropsName)
    #
    #                 print folPropsPth + ' 4'
    #
    #                 os.mkdir(folPropsPth)
    #                 for task in assetsTasks:
    #                     assetsTaskPth = os.path.join(folPropsPth, task)
    #                     os.mkdir(assetsTaskPth)
    #                     for step in steps:
    #                         assetsTaskStepPth = os.path.join(assetsTaskPth, step)
    #                         os.mkdir(assetsTaskStepPth)
    #                     assetsWorkTaskPth = os.path.join(assetsTaskPth, 'work')
    #                     if task == 'art':
    #                         apps = ['photoshop', 'maya']
    #                     elif task == 'plt_model':
    #                         apps = ['zbrush', 'maya', 'mudbox', 'houdini']
    #                     elif task == 'surfacing':
    #                         apps = ['mari', 'maya', 'substance', 'photoshop']
    #                     elif task == 'rigging':
    #                         apps = ['maya']
    #
    #                     for app in apps:
    #                         appPth = os.path.join(assetsWorkTaskPth, app)
    #                         os.mkdir(appPth)
    #                         if app == 'maya':
    #                             for f in mayaFolders:
    #                                 mayaPth = os.path.join(appPth, f)
    #                                 os.mkdir(mayaPth)
    #                 i += 1
    #
    #     # Sequences content
    #
    #     seqTask = ['anim', 'comp', 'fx', 'layout', 'lighting']
    #
    #     sequencesPth = os.path.join(self.rootPth, 'sequences')
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
    #             seqTaskWorkPth = os.path.join(seqTaskPth, 'work')
    #             if task == 'anim':
    #                 apps = ['maya', 'after effect', 'houdini']
    #             elif task == 'comp':
    #                 apps = ['nuke', 'after effect', 'photoshop']
    #             elif task == 'fx':
    #                 apps = ['maya', 'houdini']
    #             elif task == 'layout':
    #                 apps = ['maya']
    #             elif task == 'lighting':
    #                 apps = ['maya']
    #
    #             for app in apps:
    #                 appPth = os.path.join(seqTaskWorkPth, app)
    #                 os.mkdir(appPth)
    #                 if app == 'maya':
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


def main():
    app = QApplication(sys.argv)
    window = NewProject()
    window.show()
    app.exec_()

if __name__=="__main__":
    main()