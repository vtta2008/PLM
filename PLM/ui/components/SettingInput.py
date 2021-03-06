# -*- coding: utf-8 -*-
"""

Script Name: SettingInput.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------


from PySide2.QtWidgets        import QAbstractItemView, QHeaderView, QTableWidgetItem

from pyPLM.Widgets import Widget, ComboBox, Label, GroupGrid, GridLayout, TableWidget
from PLM.options import INI, NATIVE, USER_SCOPE, SYS_SCOPE, ITEMENABLE
from pyPLM.settings import RegSettings


class SettingInput(Widget):

    key                     = "SettingInput"

    def __init__(self, settings, parent=None):
        super(SettingInput, self).__init__(parent)

        self.settings = settings

        self.formatComboBox = ComboBox()
        self.formatComboBox.addItem('INI')
        self.formatComboBox.addItem('Native')

        self.scopeComboBox = ComboBox()
        self.scopeComboBox.addItem('User')
        self.scopeComboBox.addItem('System')

        self.organizationComboBox = ComboBox()
        self.organizationComboBox.addItem('DAMGteam')
        self.organizationComboBox.setEditable(True)

        self.applicationComboBox = ComboBox()
        self.applicationComboBox.addItem('PLM')
        self.applicationComboBox.setEditable(True)
        self.applicationComboBox.setCurrentIndex(0)


        for cb in [self.formatComboBox, self.scopeComboBox, self.organizationComboBox, self.applicationComboBox]:
            cb.currentIndexChanged.connect(self.updateLocationsTable)

        formatLabel         = Label({'txt': "&Format: ", 'buddy': self.formatComboBox})
        scopeLabel          = Label({'txt': "&Scope:", 'buddy': self.scopeComboBox})
        organizationLabel   = Label({'txt': "&Organization:", 'buddy': self.organizationComboBox})
        applicationLabel    = Label({'txt': "&Application:", 'buddy': self.applicationComboBox})

        grpBox              = GroupGrid("Setting Locations")
        grid                = grpBox.layout

        self.locationsTable = TableWidget()
        self.locationsTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.locationsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.locationsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.locationsTable.setColumnCount(2)
        self.locationsTable.setHorizontalHeaderLabels(("Location", "Access"))
        self.locationsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.locationsTable.horizontalHeader().resizeSection(1, 180)
        self.locationsTable.setMinimumHeight(180)

        self.formatComboBox.activated.connect(self.updateLocationsTable)
        self.scopeComboBox.activated.connect(self.updateLocationsTable)
        self.organizationComboBox.lineEdit().editingFinished.connect(self.updateLocationsTable)
        self.applicationComboBox.lineEdit().editingFinished.connect(self.updateLocationsTable)

        self.layout = GridLayout()

        grid.addWidget(formatLabel, 1, 0)
        grid.addWidget(self.formatComboBox, 1, 1)
        grid.addWidget(scopeLabel, 2, 0)
        grid.addWidget(self.scopeComboBox, 2, 1)
        grid.addWidget(organizationLabel, 3, 0)
        grid.addWidget(self.organizationComboBox, 3, 1)
        grid.addWidget(applicationLabel, 4, 0)
        grid.addWidget(self.applicationComboBox, 4, 1)
        grid.addWidget(self.locationsTable, 0, 2, 6, 4)

        self.updateLocationsTable()
        self.layout.addWidget(grpBox)

        self.setLayout(self.layout)

    def format(self):
        if self.formatComboBox.currentIndex() == 0:
            return NATIVE
        else:
            return INI

    def scope(self):
        if self.scopeComboBox.currentIndex() == 0:
            return USER_SCOPE
        else:
            return SYS_SCOPE

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
                if self.scope() == SYS_SCOPE:
                    continue
                actualScope = USER_SCOPE
            else:
                actualScope = SYS_SCOPE

            for j in range(2):
                if j == 0:
                    if not self.application():
                        continue

                actApp = self.application()

                settings = RegSettings(self.format(), actualScope, self.organization(), actApp)

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
                    # self.buttonBox.okButton(QDialogButtonBox.Ok).setDisabled(disable)
                else:
                    item1.setText("Read-only fallback")

                if disable:
                    item0.setFlags(item0.flags() & ~ITEMENABLE)
                    item1.setFlags(item1.flags() & ~ITEMENABLE)

                self.locationsTable.setItem(row, 0, item0)
                self.locationsTable.setItem(row, 1, item1)
        self.locationsTable.setUpdatesEnabled(True)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 29/11/2019 - 4:42 AM
# © 2017 - 2018 DAMGteam. All rights reserved