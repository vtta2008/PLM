# -*- coding: utf-8 -*-
"""

Script Name: AppSetting.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

import sys
from appData import __organization__, __appname__
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QTableWidget, QAbstractItemView, QHeaderView,
                             QDialogButtonBox, QGridLayout, QTableWidgetItem, QApplication)
from PyQt5.QtCore import QSettings, Qt
from ui.lib.LayoutPreset import ComboBox, Label


class AppSetting(QWidget):

    def __init__(self, parent=None):
        super(AppSetting, self).__init__(parent)

        self.formatComboBox = ComboBox({'items': ["Native", "INI"]})
        self.scopeComboBox = ComboBox({'items': ["User", "System"]})
        self.organizationComboBox = ComboBox({'items':['DAMGteam'], 'editable':True})
        self.applicationComboBox = ComboBox({'items': ['PLM'], 'editable':True, 'curIndex':3})

        formatLabel = Label({'txt':"&Format: ", 'setBuddy': self.scopeComboBox})
        scopeLabel = Label({'txt':"&Scope:", 'setBuddy': self.scopeComboBox})
        organizationLabel = Label({'txt':"&Organization:", 'setBuddy': self.organizationComboBox})
        applicationLabel = Label({'txt':"&Application:", 'setBuddy': self.applicationComboBox})

        self.locationsGroupBox = QGroupBox("Setting Locations")
        self.locationsTable = QTableWidget()
        self.locationsTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.locationsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.locationsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.locationsTable.setColumnCount(2)
        self.locationsTable.setHorizontalHeaderLabels(("Location", "Access"))
        self.locationsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.locationsTable.horizontalHeader().resizeSection(1, 180)

        # self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.formatComboBox.activated.connect(self.updateLocationsTable)
        self.scopeComboBox.activated.connect(self.updateLocationsTable)
        self.organizationComboBox.lineEdit().editingFinished.connect(self.updateLocationsTable)
        self.applicationComboBox.lineEdit().editingFinished.connect(self.updateLocationsTable)
        # self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.rejected.connect(self.reject)

        locationsLayout = QVBoxLayout()
        locationsLayout.addWidget(self.locationsTable)
        self.locationsGroupBox.setLayout(locationsLayout)

        mainLayout = QGridLayout()
        mainLayout.addWidget(formatLabel, 0, 0)
        mainLayout.addWidget(self.formatComboBox, 0, 1)
        mainLayout.addWidget(scopeLabel, 1, 0)
        mainLayout.addWidget(self.scopeComboBox, 1, 1)
        mainLayout.addWidget(organizationLabel, 2, 0)
        mainLayout.addWidget(self.organizationComboBox, 2, 1)
        mainLayout.addWidget(applicationLabel, 3, 0)
        mainLayout.addWidget(self.applicationComboBox, 3, 1)
        mainLayout.addWidget(self.locationsGroupBox, 4, 0, 1, 2)
        # mainLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.setLayout(mainLayout)

        self.updateLocationsTable()

        # self.setWindowTitle("Open Application Settings")
        # self.resize(650, 400)

    def format(self):
        if self.formatComboBox.currentIndex() == 0:
            return QSettings.NativeFormat
        else:
            return QSettings.IniFormat

    def scope(self):
        if self.scopeComboBox.currentIndex() == 0:
            return QSettings.UserScope
        else:
            return QSettings.SystemScope

    def organization(self):
        return self.organizationComboBox.currentText()

    def application(self):
        if self.applicationComboBox.currentText() == "Any":
            return ''

        return self.applicationComboBox.currentText()

    def updateLocationsTable(self):
        self.locationsTable.setUpdatesEnabled(False)
        self.locationsTable.setRowCount(0)

        for i in range(2):
            if i == 0:
                if self.scope() == QSettings.SystemScope:
                    continue

                actualScope = QSettings.UserScope
            else:
                actualScope = QSettings.SystemScope

            for j in range(2):
                if j == 0:
                    if not self.application():
                        continue

                    actualApplication = self.application()
                else:
                    actualApplication = ''

                settings = QSettings(self.format(), actualScope,
                                     self.organization(), actualApplication)

                row = self.locationsTable.rowCount()
                self.locationsTable.setRowCount(row + 1)

                item0 = QTableWidgetItem()
                item0.setText(settings.fileName())

                item1 = QTableWidgetItem()
                disable = not (settings.childKeys() or settings.childGroups())

                if row == 0:
                    if settings.isWritable():
                        item1.setText("Read-write")
                        disable = False
                    else:
                        item1.setText("Read-only")
                    # self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(disable)
                else:
                    item1.setText("Read-only fallback")

                if disable:
                    item0.setFlags(item0.flags() & ~Qt.ItemIsEnabled)
                    item1.setFlags(item1.flags() & ~Qt.ItemIsEnabled)

                self.locationsTable.setItem(row, 0, item0)
                self.locationsTable.setItem(row, 1, item1)

        self.locationsTable.setUpdatesEnabled(True)

# app = QApplication(sys.argv)
# ui = AppSetting()
# ui.show()
# app.exec_()
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 11/07/2018 - 1:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved