# -*- coding: utf-8 -*-
"""

Script Name: Configurations.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python


# PyQt5
from PyQt5.QtCore               import QDate, QSize, Qt, pyqtSignal
from PyQt5.QtGui                import QIcon
from PyQt5.QtWidgets            import (QCheckBox, QDateTimeEdit, QGridLayout, QGroupBox,
                                        QHBoxLayout, QLabel, QLineEdit, QListView, QListWidget, QListWidgetItem, QPushButton,
                                        QSpinBox, QStackedWidget, QVBoxLayout)

# PLM
from PLM import __globalServer__, __localServer__
from PLM import (GroupBox, Label, HBoxLayout, ComboBox, VBoxLayout, LineEdit, Button, Widget,
                 CheckBox, )

# -------------------------------------------------------------------------------------------------------------
""" Server """

class ServerConfig(Widget):

    def __init__(self, parent=None):
        super(ServerConfig, self).__init__(parent)

        serverLabel             = Label({'txt':"Server:"})
        serverCombo             = ComboBox({'items': ['Local: {}'.format(__localServer__), 'GlobalSettings: {}'.format(__globalServer__)]})
        serverLayout            = HBoxLayout({'addWidget': [serverLabel, serverCombo]})
        serverConfigLayout      = VBoxLayout({'addLayout': [serverLayout]})
        serverConfigGroup       = GroupBox("Server configuration", [serverConfigLayout], 'setLayout')

        projectLabel            = Label({'txt': "Set Project:"})
        projectPath             = LineEdit()
        projectBtn              = Button({'txt': 'Set Path'})
        projectLayout           = HBoxLayout({'addWidget': [projectLabel, projectPath, projectBtn]})
        projectConfigLayout     = VBoxLayout({'addLayout': [projectLayout]})
        projectConfigGroup      = GroupBox("Project configuration", [projectConfigLayout], 'setLayout')

        teamtLabel              = Label({'txt': "Set Team:"})
        teamPath                = LineEdit()
        teamBtn                 = Button({'txt': 'Set Team'})
        teamLayout              = HBoxLayout({'addWidget': [teamtLabel, teamPath, teamBtn]})
        teamConfigLayout        = VBoxLayout({'addLayout': [teamLayout]})
        TeamConfigGroup         = GroupBox("Project configuration", [teamConfigLayout], 'setLayout')

        mainLayout              = VBoxLayout({'addWidget': [serverConfigGroup, projectConfigGroup, TeamConfigGroup], 'addStretch': 1})

        self.setLayout(mainLayout)

# -------------------------------------------------------------------------------------------------------------
""" Update """

class UpdatePage(Widget):

    def __init__(self, parent=None):
        super(UpdatePage, self).__init__(parent)

        updateGroup         = GroupBox("Package selection")
        systemCheckBox      = CheckBox("Update system")
        appsCheckBox        = CheckBox("Update applications")
        docsCheckBox        = CheckBox("Update documentation")

        packageGroup        = GroupBox("Existing packages")

        packageList         = QListWidget()
        qtItem              = QListWidgetItem(packageList)
        qtItem.setText("Qt")

        qsaItem             = QListWidgetItem(packageList)
        qsaItem.setText("QSA")

        teamBuilderItem     = QListWidgetItem(packageList)
        teamBuilderItem.setText("Teambuilder")

        startUpdateButton   = Button({'txt':"Start update"})

        updateLayout        = VBoxLayout({'addWidget': [systemCheckBox, appsCheckBox, docsCheckBox]})
        updateGroup.setLayout(updateLayout)

        packageLayout       = QVBoxLayout()
        packageLayout.addWidget(packageList)
        packageGroup.setLayout(packageLayout)

        mainLayout          = QVBoxLayout()
        mainLayout.addWidget(updateGroup)
        mainLayout.addWidget(packageGroup)
        mainLayout.addSpacing(12)
        mainLayout.addWidget(startUpdateButton)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)

# -------------------------------------------------------------------------------------------------------------
""" Query """

class QueryPage(Widget):

    key                     = 'QueryPage'

    def __init__(self, parent=None):
        super(QueryPage, self).__init__(parent)

        packagesGroup       = QGroupBox("Look for packages")

        nameLabel           = QLabel("Name:")
        nameEdit            = QLineEdit()

        dateLabel           = QLabel("Released after:")
        dateEdit            = QDateTimeEdit(QDate.currentDate())

        releasesCheckBox    = QCheckBox("Releases")
        upgradesCheckBox    = QCheckBox("Upgrades")

        hitsSpinBox         = QSpinBox()
        hitsSpinBox.setPrefix("Return up to ")
        hitsSpinBox.setSuffix(" results")
        hitsSpinBox.setSpecialValueText("Return only the first result")
        hitsSpinBox.setMinimum(1)
        hitsSpinBox.setMaximum(100)
        hitsSpinBox.setSingleStep(10)

        startQueryButton    = QPushButton("Start query")

        packagesLayout      = QGridLayout()
        packagesLayout.addWidget(nameLabel, 0, 0)
        packagesLayout.addWidget(nameEdit, 0, 1)
        packagesLayout.addWidget(dateLabel, 1, 0)
        packagesLayout.addWidget(dateEdit, 1, 1)
        packagesLayout.addWidget(releasesCheckBox, 2, 0)
        packagesLayout.addWidget(upgradesCheckBox, 3, 0)
        packagesLayout.addWidget(hitsSpinBox, 4, 0, 1, 2)
        packagesGroup.setLayout(packagesLayout)

        mainLayout          = QVBoxLayout()
        mainLayout.addWidget(packagesGroup)
        mainLayout.addSpacing(12)
        mainLayout.addWidget(startQueryButton)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)

# -------------------------------------------------------------------------------------------------------------
""" Config window """

class Configurations(Widget):

    key = 'Configurations'
    cfgReport = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Configurations, self).__init__(parent)

        self.setWindowTitle("Configuration")

        self.contentsWidget = QListWidget()
        self.contentsWidget.setViewMode(QListView.IconMode)
        self.contentsWidget.setIconSize(QSize(96, 84))
        self.contentsWidget.setMovement(QListView.Static)
        self.contentsWidget.setMaximumWidth(128)
        self.contentsWidget.setSpacing(12)

        self.pagesWidget = QStackedWidget()
        self.pagesWidget.addWidget(ServerConfig())
        self.pagesWidget.addWidget(UpdatePage())
        self.pagesWidget.addWidget(QueryPage())

        closeButton = QPushButton("Close")

        self.createIcons()
        self.contentsWidget.setCurrentRow(0)

        closeButton.clicked.connect(self.close)

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.contentsWidget)
        horizontalLayout.addWidget(self.pagesWidget, 1)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(closeButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addStretch(1)
        mainLayout.addSpacing(12)
        mainLayout.addLayout(buttonsLayout)

        self.setLayout(mainLayout)

    def changePage(self, current, previous):
        if not current:
            current = previous

        self.pagesWidget.setCurrentIndex(self.contentsWidget.row(current))

    def createIcons(self):
        configButton = QListWidgetItem(self.contentsWidget)
        configButton.setIcon(QIcon(':/images/_data.png'))
        configButton.setText("Configuration")
        configButton.setTextAlignment(Qt.AlignHCenter)
        configButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        updateButton = QListWidgetItem(self.contentsWidget)
        updateButton.setIcon(QIcon(':/images/update.png'))
        updateButton.setText("Update")
        updateButton.setTextAlignment(Qt.AlignHCenter)
        updateButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        queryButton = QListWidgetItem(self.contentsWidget)
        queryButton.setIcon(QIcon(':/images/query.png'))
        queryButton.setText("Query")
        queryButton.setTextAlignment(Qt.AlignHCenter)
        queryButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        self.contentsWidget.currentItemChanged.connect(self.changePage)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 5:46 AM
# © 2017 - 2018 DAMGteam. All rights reserved