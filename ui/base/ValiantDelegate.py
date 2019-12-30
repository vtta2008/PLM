# -*- coding: utf-8 -*-
"""

Script Name: ValiantDelegate.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore import QRegExp, Qt, QByteArray, QDate, QDateTime, QPoint, QRect, QSize, QTime
from PyQt5.QtGui import QRegExpValidator, QValidator, QColor
from PyQt5.QtWidgets import QStyleOptionViewItem, QStyle

from devkit.Widgets.LineEdit import LineEdit


from devkit.Widgets import ItemDelegate

class VariantDelegate(ItemDelegate):

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

        lineEdit = LineEdit(parent)
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
# Created by panda on 29/11/2019 - 4:25 AM
# © 2017 - 2018 DAMGteam. All rights reserved