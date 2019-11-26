# -*- coding: utf-8 -*-
"""

Script Name: SettingUI.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
import sys

# PyQt5
from PyQt5.QtCore       import (QByteArray, QDate, QDateTime, QEvent, QPoint, QRect, QRegExp, QSettings, QSize, Qt, 
                                QTime, QTimer)
from PyQt5.QtGui        import QColor, QIcon, QRegExpValidator, QValidator
from PyQt5.QtWidgets    import (QAbstractItemView, QAction, QMenuBar, QFileDialog, QGridLayout,
                                QHeaderView, QInputDialog, QItemDelegate, QLineEdit, QStyle, QComboBox,
                                QStyleOptionViewItem, QTableWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem)

# PLM
from appData                           import __organization__, __appname__, SETTING_FILEPTH, INI
from ui.uikits.Action                  import Action
from ui.uikits.MenuBar                 import MenuBar
from ui.uikits.Label                   import Label
from ui.uikits.Widget                  import Widget
from ui.uikits.GridLayout              import GridLayout
from ui.uikits.GroupBox                import GroupGrid

# -------------------------------------------------------------------------------------------------------------
""" Setting Manager """

class SettingUI(Widget):

    key = 'SettingUI'


    def __init__(self, parent=None):
        super(SettingUI, self).__init__(parent)

        self.parent = parent
        self.menubar = QMenuBar(self)
        self.regValue = SettingOutput(self.settings)
        self.regInfo = SettingInput(self.settings)

        self.createMenus()

        self.layout = GridLayout()
        self.layout.addWidget(self.menubar, 0, 0, 1, 1)
        self.layout.addWidget(self.regInfo, 1, 0, 1, 1)
        self.layout.addWidget(self.regValue, 2, 0, 1, 1)

        self.setLayout(self.layout)

        self.autoRefreshAct.setChecked(True)
        self.fallbacksAct.setChecked(True)

        self.setWindowTitle("PLM settings")

    def openSettings(self):
        if not self.settings:
            self.settings = QSettings(self.regInfo.format(), self.regInfo.scope(), self.regInfo.organization(), self.regInfo.application())
        self.setSettingsObject(self.settings)
        self.fallbacksAct.setEnabled(True)

    def openIniFile(self):
        if not os.path.exists(self.settings.settingFile):
            fileName, _ = QFileDialog.getOpenFileName(self, "Open INI File", '', "INI Files (*.ini *.conf)")

            if fileName:
                self.settings._settingFile = fileName
        else:
            self.settings._settingFile = SETTING_FILEPTH['app']
            self.setSettingsObject(self.settings)
            self.fallbacksAct.setEnabled(False)

    def openPropertyList(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Property List", '', "Property List Files (*.plist)")

        if fileName:
            self.settings.set_format(QSettings.NativeFormat)
            self.setSettingsObject(self.settings)
            self.fallbacksAct.setEnabled(False)

    def openRegistryPath(self):
        path, ok = QInputDialog.getText(self, "Open Registry Path",
                                        "Enter the path in the Windows registry:", QLineEdit.Normal,
                                        'HKEY_CURRENT_USER\\Software\\{0}\\{1}'.format(__organization__, __appname__))

        if ok and path != '':
            settings = QSettings(path, QSettings.NativeFormat)
            self.setSettingsObject(settings)
            self.fallbacksAct.setEnabled(False)

    def createActions(self):
        self.openSettingsAct = QAction("&Open Application Settings...", self, shortcut="Ctrl+O", triggered=self.openSettings)
        # self.openSettingsAct = Action({'shortcut': "Ctrl+O", 'tt': "&Open Application Settings...", 'trg': self.openSettings}, self )

        self.openIniFileAct = QAction("Open I&NI File...", self, shortcut="Ctrl+N", triggered=self.openIniFile)
        self.openPropertyListAct = QAction("Open Mac &Property List...", self, shortcut="Ctrl+P",
                                           triggered=self.openPropertyList)
        self.openRegistryPathAct = QAction("Open Windows &Registry Path...", self, shortcut="Ctrl+G",
                                           triggered=self.openRegistryPath)
        self.refreshAct = QAction("&Refresh", self, shortcut="Ctrl+R", enabled=False, triggered=self.regValue.refresh)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.autoRefreshAct = QAction("&Auto-Refresh", self, shortcut="Ctrl+A", checkable=True, enabled=False)
        self.fallbacksAct = QAction("&Fallbacks", self, shortcut="Ctrl+F", checkable=True, enabled=False,  triggered=self.regValue.setFallbacksEnabled)

        if sys.platform != 'darwin':
            self.openPropertyListAct.setEnabled(False)

        if sys.platform != 'win32':
            self.openRegistryPathAct.setEnabled(False)

        self.autoRefreshAct.triggered.connect(self.regValue.setAutoRefresh)
        self.autoRefreshAct.triggered.connect(self.refreshAct.setDisabled)

    def createMenus(self):
        self.createActions()
        self.fileMenu = self.menubar.addMenu("&File")
        self.fileMenu.addAction(self.openSettingsAct)
        self.fileMenu.addAction(self.openIniFileAct)
        self.fileMenu.addAction(self.openPropertyListAct)
        self.fileMenu.addAction(self.openRegistryPathAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.refreshAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.optionsMenu = self.menubar.addMenu("&Options")
        self.optionsMenu.addAction(self.autoRefreshAct)
        self.optionsMenu.addAction(self.fallbacksAct)

    def setSettingsObject(self, settings):
        settings.setFallbacksEnabled(self.fallbacksAct.isChecked())
        self.regValue.setSettingsObject(settings)

        self.refreshAct.setEnabled(True)
        self.autoRefreshAct.setEnabled(True)

        niceName = settings.fileName()
        niceName.replace('\\', '/')
        niceName = niceName.split('/')[-1]

        if not settings.isWritable():
            niceName += " (read only)"

        self.setWindowTitle("%s - Settings Editor" % niceName)

    def setting_mode(self, filename, fm, parent):
        pass


class SettingInput(Widget):

    key = "SettingInput"

    def __init__(self, settings, parent=None):
        super(SettingInput, self).__init__(parent)

        self.settings = settings

        self.formatComboBox = QComboBox(self)
        self.formatComboBox.addItem('INI')
        self.formatComboBox.addItem('Native')

        self.scopeComboBox = QComboBox(self)
        self.scopeComboBox.addItem('User')
        self.scopeComboBox.addItem('System')

        self.organizationComboBox = QComboBox(self)
        self.organizationComboBox.addItem('DAMGteam')
        self.organizationComboBox.setEditable(True)

        self.applicationComboBox = QComboBox(self)
        self.applicationComboBox.addItem('PLM')
        self.applicationComboBox.setEditable(True)
        self.applicationComboBox.setCurrentIndex(0)


        for cb in [self.formatComboBox, self.scopeComboBox, self.organizationComboBox, self.applicationComboBox]:
            cb.currentIndexChanged.connect(self.updateLocationsTable)

        formatLabel = Label({'txt': "&Format: ", 'setBuddy': self.formatComboBox})
        scopeLabel = Label({'txt': "&Scope:", 'setBuddy': self.scopeComboBox})
        organizationLabel = Label({'txt': "&Organization:", 'setBuddy': self.organizationComboBox})
        applicationLabel = Label({'txt': "&Application:", 'setBuddy': self.applicationComboBox})

        grpBox, grid = GroupGrid("Setting Locations")

        self.locationsTable = QTableWidget()
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

        self.layout = QGridLayout()

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
            return QSettings.NativeFormat
        else:
            return INI

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
                    # self.buttonBox.okButton(QDialogButtonBox.Ok).setDisabled(disable)
                else:
                    item1.setText("Read-only fallback")

                if disable:
                    item0.setFlags(item0.flags() & ~Qt.ItemIsEnabled)
                    item1.setFlags(item1.flags() & ~Qt.ItemIsEnabled)

                self.locationsTable.setItem(row, 0, item0)
                self.locationsTable.setItem(row, 1, item1)
        self.locationsTable.setUpdatesEnabled(True)


class SettingOutput(QTreeWidget):

    key = "SettingOutput"

    def __init__(self, settings, parent=None):
        super(SettingOutput, self).__init__(parent)

        self.setItemDelegate(VariantDelegate(self))

        self.setHeaderLabels(("Setting", "Type", "Value"))
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header().setSectionResizeMode(2, QHeaderView.Stretch)

        self.settings = settings
        self.refreshTimer = QTimer()
        self.refreshTimer.setInterval(2000)
        self.autoRefresh = False

        self.groupIcon = QIcon()
        self.groupIcon.addPixmap(self.style().standardPixmap(QStyle.SP_DirClosedIcon), QIcon.Normal, QIcon.Off)
        self.groupIcon.addPixmap(self.style().standardPixmap(QStyle.SP_DirOpenIcon), QIcon.Normal, QIcon.On)
        self.keyIcon = QIcon()
        self.keyIcon.addPixmap(self.style().standardPixmap(QStyle.SP_FileIcon))

        self.refreshTimer.timeout.connect(self.maybeRefresh)

    def setSettingsObject(self, settings):
        self.settings = settings
        self.clear()

        if self.settings is not None:
            self.settings.setParent(self)
            self.refresh()
            if self.autoRefresh:
                self.refreshTimer.start()
        else:
            self.refreshTimer.stop()

    def sizeHint(self):
        return QSize(800, 600)

    def setAutoRefresh(self, autoRefresh):
        self.autoRefresh = autoRefresh

        if self.settings is not None:
            if self.autoRefresh:
                self.maybeRefresh()
                self.refreshTimer.start()
            else:
                self.refreshTimer.stop()

    def setFallbacksEnabled(self, enabled):
        if self.settings is not None:
            self.settings.setFallbacksEnabled(enabled)
            self.refresh()

    def maybeRefresh(self):
        if self.state() != QAbstractItemView.EditingState:
            self.refresh()

    def refresh(self):
        if self.settings is None:
            return

        # The signal_cpu might not be connected.
        try:
            self.itemChanged.disconnect(self.updateSetting)
        except:
            pass

        self.settings.sync()
        self.updateChildItems(None)

        self.itemChanged.connect(self.updateSetting)

    def event(self, event):
        if event.type() == QEvent.WindowActivate:
            if self.isActiveWindow() and self.autoRefresh:
                self.maybeRefresh()

        return super(SettingOutput, self).event(event)

    def updateSetting(self, item):
        key = item.text(0)
        ancestor = item.parent()

        while ancestor:
            key = ancestor.text(0) + '/' + key
            ancestor = ancestor.parent()

        d = item.data(2, Qt.UserRole)
        self.settings.setValue(key, item.data(2, Qt.UserRole))

        if self.autoRefresh:
            self.refresh()

    def updateChildItems(self, parent):
        dividerIndex = 0

        for group in self.settings.childGroups():
            childIndex = self.findChild(parent, group, dividerIndex)
            if childIndex != -1:
                child = self.childAt(parent, childIndex)
                child.setText(1, '')
                child.setText(2, '')
                child.setData(2, Qt.UserRole, None)
                self.moveItemForward(parent, childIndex, dividerIndex)
            else:
                child = self.createItem(group, parent, dividerIndex)

            child.setIcon(0, self.groupIcon)
            dividerIndex += 1

            self.settings.beginGroup(group)
            self.updateChildItems(child)
            self.settings.endGroup()

        for key in self.settings.childKeys():
            childIndex = self.findChild(parent, key, 0)
            if childIndex == -1 or childIndex >= dividerIndex:
                if childIndex != -1:
                    child = self.childAt(parent, childIndex)
                    for i in range(child.childCount()):
                        self.deleteItem(child, i)
                    self.moveItemForward(parent, childIndex, dividerIndex)
                else:
                    child = self.createItem(key, parent, dividerIndex)
                child.setIcon(0, self.keyIcon)
                dividerIndex += 1
            else:
                child = self.childAt(parent, childIndex)

            value = self.settings.value(key)
            if value is None:
                child.setText(1, 'Invalid')
            else:
                child.setText(1, value.__class__.__name__)
            child.setText(2, VariantDelegate.displayText(value))
            child.setData(2, Qt.UserRole, value)

        while dividerIndex < self.childCount(parent):
            self.deleteItem(parent, dividerIndex)

    def createItem(self, text, parent, index):
        after = None

        if index != 0:
            after = self.childAt(parent, index - 1)

        if parent is not None:
            item = QTreeWidgetItem(parent, after)
        else:
            item = QTreeWidgetItem(self, after)

        item.setText(0, text)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        return item

    def deleteItem(self, parent, index):
        if parent is not None:
            item = parent.takeChild(index)
        else:
            item = self.takeTopLevelItem(index)
        del item

    def childAt(self, parent, index):
        if parent is not None:
            return parent.child(index)
        else:
            return self.topLevelItem(index)

    def childCount(self, parent):
        if parent is not None:
            return parent.childCount()
        else:
            return self.topLevelItemCount()

    def findChild(self, parent, text, startIndex):
        for i in range(self.childCount(parent)):
            if self.childAt(parent, i).text(0) == text:
                return i
        return -1

    def moveItemForward(self, parent, oldIndex, newIndex):
        for int in range(oldIndex - newIndex):
            self.deleteItem(parent, newIndex)


class VariantDelegate(QItemDelegate):

    key = "VariantDelegate"

    def __init__(self, parent=None):
        super(VariantDelegate, self).__init__(parent)

        self.boolExp = QRegExp()
        self.boolExp.setPattern('true|false')
        self.boolExp.setCaseSensitivity(Qt.CaseInsensitive)

        self.byteArrayExp = QRegExp()
        self.byteArrayExp.setPattern('[\\x00-\\xff]*')

        self.charExp = QRegExp()
        self.charExp.setPattern('.')

        self.colorExp = QRegExp()
        self.colorExp.setPattern('\\(([0-9]*),([0-9]*),([0-9]*),([0-9]*)\\)')

        self.doubleExp = QRegExp()
        self.doubleExp.setPattern('')

        self.pointExp = QRegExp()
        self.pointExp.setPattern('\\((-?[0-9]*),(-?[0-9]*)\\)')

        self.rectExp = QRegExp()
        self.rectExp.setPattern('\\((-?[0-9]*),(-?[0-9]*),(-?[0-9]*),(-?[0-9]*)\\)')

        self.signedIntegerExp = QRegExp()
        self.signedIntegerExp.setPattern('-?[0-9]*')

        self.sizeExp = QRegExp(self.pointExp)

        self.unsignedIntegerExp = QRegExp()
        self.unsignedIntegerExp.setPattern('[0-9]*')

        self.dateExp = QRegExp()
        self.dateExp.setPattern('([0-9]{,4})-([0-9]{,2})-([0-9]{,2})')

        self.timeExp = QRegExp()
        self.timeExp.setPattern('([0-9]{,2}):([0-9]{,2}):([0-9]{,2})')

        self.dateTimeExp = QRegExp()
        self.dateTimeExp.setPattern(self.dateExp.pattern() + 'T' + self.timeExp.pattern())

    def paint(self, painter, option, index):
        if index.column() == 2:
            value = index.model().data(index, Qt.UserRole)
            if not self.isSupportedType(value):
                myOption = QStyleOptionViewItem(option)
                myOption.state &= ~QStyle.State_Enabled
                super(VariantDelegate, self).paint(painter, myOption, index)
                return

        super(VariantDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        if index.column() != 2:
            return None

        originalValue = index.model().data(index, Qt.UserRole)
        if not self.isSupportedType(originalValue):
            return None

        lineEdit = QLineEdit(parent)
        lineEdit.setFrame(False)

        if isinstance(originalValue, bool):
            regExp = self.boolExp
        elif isinstance(originalValue, float):
            regExp = self.doubleExp
        elif isinstance(originalValue, int):
            regExp = self.signedIntegerExp
        elif isinstance(originalValue, QByteArray):
            regExp = self.byteArrayExp
        elif isinstance(originalValue, QColor):
            regExp = self.colorExp
        elif isinstance(originalValue, QDate):
            regExp = self.dateExp
        elif isinstance(originalValue, QDateTime):
            regExp = self.dateTimeExp
        elif isinstance(originalValue, QTime):
            regExp = self.timeExp
        elif isinstance(originalValue, QPoint):
            regExp = self.pointExp
        elif isinstance(originalValue, QRect):
            regExp = self.rectExp
        elif isinstance(originalValue, QSize):
            regExp = self.sizeExp
        else:
            regExp = QRegExp()

        if not regExp.isEmpty():
            validator = QRegExpValidator(regExp, lineEdit)
            lineEdit.setValidator(validator)

        return lineEdit

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.UserRole)
        if editor is not None:
            editor.setText(self.displayText(value))

    def setModelData(self, editor, model, index):
        if not editor.isModified():
            return

        text = editor.text()
        validator = editor.validator()
        if validator is not None:
            state, text, _ = validator.validate(text, 0)
            if state != QValidator.Acceptable:
                return

        originalValue = index.model().data(index, Qt.UserRole)

        if isinstance(originalValue, QColor):
            self.colorExp.exactMatch(text)
            value = QColor(min(int(self.colorExp.cap(1)), 255),
                           min(int(self.colorExp.cap(2)), 255),
                           min(int(self.colorExp.cap(3)), 255),
                           min(int(self.colorExp.cap(4)), 255))
        elif isinstance(originalValue, QDate):
            value = QDate.fromString(text, Qt.ISODate)
            if not value.isValid():
                return
        elif isinstance(originalValue, QDateTime):
            value = QDateTime.fromString(text, Qt.ISODate)
            if not value.isValid():
                return
        elif isinstance(originalValue, QTime):
            value = QTime.fromString(text, Qt.ISODate)
            if not value.isValid():
                return
        elif isinstance(originalValue, QPoint):
            self.pointExp.exactMatch(text)
            value = QPoint(int(self.pointExp.cap(1)),
                           int(self.pointExp.cap(2)))
        elif isinstance(originalValue, QRect):
            self.rectExp.exactMatch(text)
            value = QRect(int(self.rectExp.cap(1)),
                          int(self.rectExp.cap(2)),
                          int(self.rectExp.cap(3)),
                          int(self.rectExp.cap(4)))
        elif isinstance(originalValue, QSize):
            self.sizeExp.exactMatch(text)
            value = QSize(int(self.sizeExp.cap(1)),
                          int(self.sizeExp.cap(2)))
        elif isinstance(originalValue, list):
            value = text.split(',')
        else:
            value = type(originalValue)(text)

        model.setData(index, self.displayText(value), Qt.DisplayRole)
        model.setData(index, value, Qt.UserRole)

    @staticmethod
    def isSupportedType(value):
        return isinstance(value, (bool, float, int, QByteArray, str, QColor,
                                  QDate, QDateTime, QTime, QPoint, QRect, QSize, list))

    @staticmethod
    def displayText(value):
        if isinstance(value, (bool, int, QByteArray)):
            return str(value)
        if isinstance(value, str):
            return value
        elif isinstance(value, float):
            return '%g' % value
        elif isinstance(value, QColor):
            return '(%u,%u,%u,%u)' % (value.red(), value.green(), value.blue(), value.alpha())
        elif isinstance(value, (QDate, QDateTime, QTime)):
            return value.toString(Qt.ISODate)
        elif isinstance(value, QPoint):
            return '(%d,%d)' % (value.x(), value.y())
        elif isinstance(value, QRect):
            return '(%d,%d,%d,%d)' % (value.x(), value.y(), value.width(), value.height())
        elif isinstance(value, QSize):
            return '(%d,%d)' % (value.width(), value.height())
        elif isinstance(value, list):
            return ','.join(value)
        elif value is None:
            return '<Invalid>'

        return '<%s>' % value

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 11/07/2018 - 1:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved