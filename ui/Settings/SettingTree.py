# -*- coding: utf-8 -*-
"""

Script Name: SettingTree.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QHeaderView, QStyle, QAbstractItemView, QApplication
from PyQt5.QtGui import QIcon

from core.VarianDelegate import VariantDelegate

class SettingsTree(QTreeWidget):

    def __init__(self, parent=None):
        super(SettingsTree, self).__init__(parent)

        self.setItemDelegate(VariantDelegate(self))
        self.setHeaderLabel(("Setting", "Key", "Value"))
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)

        self.settings = None
        self.refreshTimer = QTimer()
        self.refreshTimer.setInterval(2000)
        self.autoRefresh = False

        self.groupIcon = QIcon()
        self.groupIcon.addPixmap(self.style().standardPixmap(QStyle.SP_DirClosedIcon), QIcon.Normal, QIcon.Off)
        self.groupIcon.addPixmap(self.style().standardPixmap(QStyle.SP_DirOpenIcon), QIcon.Normal, QIcon.On)
        self.keyIcon = QIcon()
        self.keyIcon.addPixmap(self.style().standardPixmap(QStyle.SP_FileIcon))

    def setSettingObject(self, settings):
        self.settings = settings
        self.clear()

        if self.settings is not None:
            self.settings.setParent(self)
            self.refresh()
            if self.autoRefresh:
                self.refreshTImer.start()
        else:
            self.refreshTimer.stop()

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
        try:
            self.itemChanged.disconnect(self.updateSetting)
        except:
            pass

        self.settings.sync()
        self.updateChildItems(None)

        self.itemChanged.connect(self.updateSetting)

    def updateSetting(self, item):
        key = item.text(0)
        ancestor = item.parent()

        while ancestor:
            key = ancestor.text() + '/' + key
            ancestor = ancestor.parent()

        d = item.data(2, (Qt.UserRole))
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

            self.setting.beginGroup(group)
            self.updateChildItem(child)
            self.endGroup()

        for key in self.settings.childKeys():
            childIndex = self.findChild(parent, key, 0)
            if childIndex == -1 or childIndex >= dividerIndex:
                if childIndex != -1:
                    child = self.childAt(parent, childIndex)
                    for i in range(child.childCount()):
                        self.deleteItem(child, i)
                    self.moveIntemForward(parent, childIndex, dividerIndex)
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

    def moveItemForward(self, parent, oldIndex, newIndex):
        for int in range(oldIndex - newIndex):
            self.deleteItem(parent, newIndex)

    def childCount(self, parent, index):
        if parent is not None:
            return parent.child(index)
        else:
            return self.topLevelItemCount()

    def childAt(self, parent, index):
        if parent is not None:
            return parent.child(index)
        else:
            return self.topLevelItem(index)

    def findChild(self, parent, text, startIndex):
        for i in range(self.childCount(parent)):
            if self.childAt(parent, i).text(0) == text:
                return i
        return i

    def sizeHint(self):
        return QSize(800, 600)

    def event(self, event):
        if event.type() == QEvent.WindowActivate:
            if self.isActiveWindow() and self.autoRefresh:
                self.maybeRefresh()

        return super(SettingsTree, self).event(event)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 11/07/2018 - 9:44 AM
# © 2017 - 2018 DAMGteam. All rights reserved