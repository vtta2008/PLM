#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Calendar.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is a calendar

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtCore import QDate, QLocale, Qt
from PyQt5.QtGui import QFont, QTextCharFormat
from PyQt5.QtWidgets import (QApplication, QCalendarWidget, QCheckBox,
                             QComboBox, QDateEdit, QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                             QLayout)

# Plt
from appData                    import SiPoMin
from ui.uikits.Widget           import Widget
from ui.uikits.GridLayout       import GridLayout
from ui.uikits.Icon             import AppIcon
# -------------------------------------------------------------------------------------------------------------
""" Clendar """

class Calendar(Widget):

    key = 'Calendar'

    def __init__(self, parent=None):
        super(Calendar, self).__init__(parent)

        self.setWindowIcon(AppIcon(32, self.key))
        self.setWindowTitle(self.key)
        self.buildUI()

    def buildUI(self):
        self.layout = GridLayout()

        self.createPreviewGroupBox()
        self.createGeneralOptionsGroupBox()
        self.createDatesGroupBox()
        self.createTextFormatsGroupBox()

        self.layout.addWidget(self.previewGroupBox, 0, 0)
        self.layout.addWidget(self.generalOptionsGroupBox, 0, 1)
        self.layout.addWidget(self.datesGroupBox, 1, 0)
        self.layout.addWidget(self.textFormatsGroupBox, 1, 1)

        self.layout.setSpacing(2)
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setSizePolicy(SiPoMin, SiPoMin)

        self.setLayout(self.layout)

    def localeChanged(self, index):
        self.calendar.setLocale(self.localeCombo.itemData(index))

    def firstDayChanged(self, index):
        self.calendar.setFirstDayOfWeek(Qt.DayOfWeek(self.firstDayCombo.itemData(index)))

    def selectionModeChanged(self, index):
        self.calendar.setSelectionMode(QCalendarWidget.SelectionMode(
            self.selectionModeCombo.itemData(index)))

    def horizontalHeaderChanged(self, index):
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat(
                self.horizontalHeaderCombo.itemData(index)))

    def verticalHeaderChanged(self, index):
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat(
                self.verticalHeaderCombo.itemData(index)))

    def selectedDateChanged(self):
        self.currentDateEdit.setDate(self.calendar.selectedDate())

    def minimumDateChanged(self, date):
        self.calendar.setMinimumDate(date)
        self.maximumDateEdit.setDate(self.calendar.maximumDate())

    def maximumDateChanged(self, date):
        self.calendar.setMaximumDate(date)
        self.minimumDateEdit.setDate(self.calendar.minimumDate())

    def weekdayFormatChanged(self):
        format = QTextCharFormat()
        format.setForeground(Qt.GlobalColor(self.weekdayColorCombo.itemData(
                    self.weekdayColorCombo.currentIndex())))

        self.calendar.setWeekdayTextFormat(Qt.Monday, format)
        self.calendar.setWeekdayTextFormat(Qt.Tuesday, format)
        self.calendar.setWeekdayTextFormat(Qt.Wednesday, format)
        self.calendar.setWeekdayTextFormat(Qt.Thursday, format)
        self.calendar.setWeekdayTextFormat(Qt.Friday, format)

    def weekendFormatChanged(self):
        format = QTextCharFormat()
        format.setForeground(Qt.GlobalColor(self.weekendColorCombo.itemData(
                    self.weekendColorCombo.currentIndex())))

        self.calendar.setWeekdayTextFormat(Qt.Saturday, format)
        self.calendar.setWeekdayTextFormat(Qt.Sunday, format)

    def reformatHeaders(self):
        text = self.headerTextFormatCombo.currentText()
        format = QTextCharFormat()

        if text == "Bold":
            format.setFontWeight(QFont.Bold)
        elif text == "Italic":
            format.setFontItalic(True)
        elif text == "Green":
            format.setForeground(Qt.green)

        self.calendar.setHeaderTextFormat(format)

    def reformatCalendarPage(self):
        if self.firstFridayCheckBox.isChecked():
            firstFriday = QDate(self.calendar.yearShown(), self.calendar.monthShown(), 1)

            while firstFriday.dayOfWeek() != Qt.Friday:
                firstFriday = firstFriday.addDays(1)

            firstFridayFormat = QTextCharFormat()
            firstFridayFormat.setForeground(Qt.blue)

            self.calendar.setDateTextFormat(firstFriday, firstFridayFormat)

        # May 1st in Red takes precedence.
        if self.mayFirstCheckBox.isChecked():
            mayFirst = QDate(self.calendar.yearShown(), 5, 1)

            mayFirstFormat = QTextCharFormat()
            mayFirstFormat.setForeground(Qt.red)

            self.calendar.setDateTextFormat(mayFirst, mayFirstFormat)

    def createPreviewGroupBox(self):
        self.previewGroupBox = QGroupBox("Preview")

        self.calendar = QCalendarWidget()
        self.calendar.setMinimumDate(QDate(1900, 1, 1))
        self.calendar.setMaximumDate(QDate(3000, 1, 1))
        self.calendar.setGridVisible(True)
        self.calendar.currentPageChanged.connect(self.reformatCalendarPage)

        self.previewLayout = QGridLayout()
        self.previewLayout.addWidget(self.calendar, 0, 0, Qt.AlignCenter)
        self.previewGroupBox.setLayout(self.previewLayout)

    def createGeneralOptionsGroupBox(self):
        self.generalOptionsGroupBox = QGroupBox("General Options")
        self.localeCombo = QComboBox()

        curLocaleIndex = -1
        lang_country = {}
        for lid in range(QLocale.C, QLocale.LastLanguage + 1):
            lang = (QLocale(lid).nativeLanguageName())
            country = u' '.join(QLocale(lid).nativeCountryName()).encode('utf-8').strip()
            lang_country[country] = [lang, lid]
            lid += 1

        countries = sorted(list(set([c for c in lang_country])))
        countries.remove(countries[0])
        for country in countries:
            lang = lang_country[country][0]
            label = "%s - %s" % ((u' '.join(lang).encode('Utf-8').strip()), country)
            locale = QLocale(lang_country[country][1])

            if self.locale().language() == lang and self.locale().country() == country:
                curLocaleIndex = lang_country[country][1]

            self.localeCombo.addItem(label, locale)

        if curLocaleIndex != -1:
            self.localeCombo.setCurrentIndex(curLocaleIndex)

        self.localeLabel = QLabel("&Locale")
        self.localeLabel.setBuddy(self.localeCombo)

        self.firstDayCombo = QComboBox()
        self.firstDayCombo.addItem("Sunday", Qt.Sunday)
        self.firstDayCombo.addItem("Monday", Qt.Monday)
        self.firstDayCombo.addItem("Tuesday", Qt.Tuesday)
        self.firstDayCombo.addItem("Wednesday", Qt.Wednesday)
        self.firstDayCombo.addItem("Thursday", Qt.Thursday)
        self.firstDayCombo.addItem("Friday", Qt.Friday)
        self.firstDayCombo.addItem("Saturday", Qt.Saturday)

        self.firstDayLabel = QLabel("Wee&k starts on:")
        self.firstDayLabel.setBuddy(self.firstDayCombo)

        self.selectionModeCombo = QComboBox()
        self.selectionModeCombo.addItem("Single selection",
                                        QCalendarWidget.SingleSelection)
        self.selectionModeCombo.addItem("None",
                                        QCalendarWidget.NoSelection)
        self.selectionModeLabel = QLabel("&Selection fn:")
        self.selectionModeLabel.setBuddy(self.selectionModeCombo)

        self.gridCheckBox = QCheckBox("&Grid")
        self.gridCheckBox.setChecked(self.calendar.isGridVisible())

        self.navigationCheckBox = QCheckBox("&Navigation bar")
        self.navigationCheckBox.setChecked(True)

        self.horizontalHeaderCombo = QComboBox()
        self.horizontalHeaderCombo.addItem("Single letter day names", QCalendarWidget.SingleLetterDayNames)
        self.horizontalHeaderCombo.addItem("Short day names", QCalendarWidget.ShortDayNames)
        self.horizontalHeaderCombo.addItem("Long day names", QCalendarWidget.LongDayNames)
        self.horizontalHeaderCombo.addItem("None", QCalendarWidget.NoHorizontalHeader)
        self.horizontalHeaderCombo.setCurrentIndex(1)

        self.horizontalHeaderLabel = QLabel("&Horizontal header:")
        self.horizontalHeaderLabel.setBuddy(self.horizontalHeaderCombo)

        self.verticalHeaderCombo = QComboBox()
        self.verticalHeaderCombo.addItem("ISO week numbers", QCalendarWidget.ISOWeekNumbers)
        self.verticalHeaderCombo.addItem("None", QCalendarWidget.NoVerticalHeader)

        self.verticalHeaderLabel = QLabel("&Vertical header:")
        self.verticalHeaderLabel.setBuddy(self.verticalHeaderCombo)

        self.localeCombo.currentIndexChanged.connect(self.localeChanged)
        self.firstDayCombo.currentIndexChanged.connect(self.firstDayChanged)
        self.selectionModeCombo.currentIndexChanged.connect(self.selectionModeChanged)
        self.gridCheckBox.toggled.connect(self.calendar.setGridVisible)
        self.navigationCheckBox.toggled.connect(self.calendar.setNavigationBarVisible)
        self.horizontalHeaderCombo.currentIndexChanged.connect(self.horizontalHeaderChanged)
        self.verticalHeaderCombo.currentIndexChanged.connect(self.verticalHeaderChanged)

        checkBoxLayout = QHBoxLayout()
        checkBoxLayout.addWidget(self.gridCheckBox)
        checkBoxLayout.addStretch()
        checkBoxLayout.addWidget(self.navigationCheckBox)

        outerLayout = QGridLayout()
        outerLayout.addWidget(self.localeLabel, 0, 0, 1, 1)
        outerLayout.addWidget(self.localeCombo, 0, 1, 1, 1)
        outerLayout.addWidget(self.firstDayLabel, 1, 0, 1, 1)
        outerLayout.addWidget(self.firstDayCombo, 1, 1, 1, 1)
        outerLayout.addWidget(self.selectionModeLabel, 2, 0, 1, 1)
        outerLayout.addWidget(self.selectionModeCombo, 2, 1, 1, 1)
        outerLayout.addLayout(checkBoxLayout, 3, 0, 1, 2)
        outerLayout.addWidget(self.horizontalHeaderLabel, 5, 0, 1, 1)
        outerLayout.addWidget(self.horizontalHeaderCombo, 5, 1, 1, 1)
        outerLayout.addWidget(self.verticalHeaderLabel, 6, 0, 1, 1)
        outerLayout.addWidget(self.verticalHeaderCombo, 6, 1, 1, 1)
        self.generalOptionsGroupBox.setLayout(outerLayout)

        self.firstDayChanged(self.firstDayCombo.currentIndex())
        self.selectionModeChanged(self.selectionModeCombo.currentIndex())
        self.horizontalHeaderChanged(self.horizontalHeaderCombo.currentIndex())
        self.verticalHeaderChanged(self.verticalHeaderCombo.currentIndex())

    def createDatesGroupBox(self):
        self.datesGroupBox = QGroupBox(self.tr("Dates"))

        self.minimumDateEdit = QDateEdit()
        self.minimumDateEdit.setDisplayFormat('MMM d yyyy')
        self.minimumDateEdit.setDateRange(self.calendar.minimumDate(), self.calendar.maximumDate())
        self.minimumDateEdit.setDate(self.calendar.minimumDate())

        self.minimumDateLabel = QLabel("&Minimum Date:")
        self.minimumDateLabel.setBuddy(self.minimumDateEdit)

        self.currentDateEdit = QDateEdit()
        self.currentDateEdit.setDisplayFormat('MMM d yyyy')
        self.currentDateEdit.setDate(self.calendar.selectedDate())
        self.currentDateEdit.setDateRange(self.calendar.minimumDate(), self.calendar.maximumDate())

        self.currentDateLabel = QLabel("&Current Date:")
        self.currentDateLabel.setBuddy(self.currentDateEdit)

        self.maximumDateEdit = QDateEdit()
        self.maximumDateEdit.setDisplayFormat('MMM d yyyy')
        self.maximumDateEdit.setDateRange(self.calendar.minimumDate(), self.calendar.maximumDate())
        self.maximumDateEdit.setDate(self.calendar.maximumDate())

        self.maximumDateLabel = QLabel("Ma&ximum Date:")
        self.maximumDateLabel.setBuddy(self.maximumDateEdit)

        self.currentDateEdit.dateChanged.connect(self.calendar.setSelectedDate)
        self.calendar.selectionChanged.connect(self.selectedDateChanged)
        self.minimumDateEdit.dateChanged.connect(self.minimumDateChanged)
        self.maximumDateEdit.dateChanged.connect(self.maximumDateChanged)

        dateBoxLayout = QGridLayout()
        dateBoxLayout.addWidget(self.currentDateLabel, 1, 0)
        dateBoxLayout.addWidget(self.currentDateEdit, 1, 1)
        dateBoxLayout.addWidget(self.minimumDateLabel, 0, 0)
        dateBoxLayout.addWidget(self.minimumDateEdit, 0, 1)
        dateBoxLayout.addWidget(self.maximumDateLabel, 2, 0)
        dateBoxLayout.addWidget(self.maximumDateEdit, 2, 1)
        dateBoxLayout.setRowStretch(3, 1)

        self.datesGroupBox.setLayout(dateBoxLayout)

    def createTextFormatsGroupBox(self):
        self.textFormatsGroupBox = QGroupBox("Text Formats")

        self.weekdayColorCombo = self.createColorComboBox()
        self.weekdayColorCombo.setCurrentIndex(self.weekdayColorCombo.findText("Black"))

        self.weekdayColorLabel = QLabel("&Weekday color:")
        self.weekdayColorLabel.setBuddy(self.weekdayColorCombo)

        self.weekendColorCombo = self.createColorComboBox()
        self.weekendColorCombo.setCurrentIndex(self.weekendColorCombo.findText("Red"))

        self.weekendColorLabel = QLabel("Week&end color:")
        self.weekendColorLabel.setBuddy(self.weekendColorCombo)

        self.headerTextFormatCombo = QComboBox()
        self.headerTextFormatCombo.addItem("Bold")
        self.headerTextFormatCombo.addItem("Italic")
        self.headerTextFormatCombo.addItem("Plain")

        self.headerTextFormatLabel = QLabel("&Header text:")
        self.headerTextFormatLabel.setBuddy(self.headerTextFormatCombo)

        self.firstFridayCheckBox = QCheckBox("&First Friday in blue")

        self.mayFirstCheckBox = QCheckBox("May &1 in red")

        self.weekdayColorCombo.currentIndexChanged.connect(self.weekdayFormatChanged)
        self.weekendColorCombo.currentIndexChanged.connect(self.weekendFormatChanged)
        self.headerTextFormatCombo.currentIndexChanged.connect(self.reformatHeaders)
        self.firstFridayCheckBox.toggled.connect(self.reformatCalendarPage)
        self.mayFirstCheckBox.toggled.connect(self.reformatCalendarPage)

        checkBoxLayout = QHBoxLayout()
        checkBoxLayout.addWidget(self.firstFridayCheckBox)
        checkBoxLayout.addStretch()
        checkBoxLayout.addWidget(self.mayFirstCheckBox)

        outerLayout = QGridLayout()
        outerLayout.addWidget(self.weekdayColorLabel, 0, 0, 1, 1)
        outerLayout.addWidget(self.weekdayColorCombo, 0, 1, 1, 1)
        outerLayout.addWidget(self.weekendColorLabel, 1, 0, 1, 1)
        outerLayout.addWidget(self.weekendColorCombo, 1, 1, 1, 1)
        outerLayout.addWidget(self.headerTextFormatLabel, 2, 0, 1, 1)
        outerLayout.addWidget(self.headerTextFormatCombo, 2, 1, 1, 1)
        outerLayout.addLayout(checkBoxLayout, 3, 0, 1, 2)
        self.textFormatsGroupBox.setLayout(outerLayout)

        self.weekdayFormatChanged()
        self.weekendFormatChanged()

        self.reformatHeaders()
        self.reformatCalendarPage()

    def createColorComboBox(self):
        comboBox = QComboBox()
        comboBox.addItem("Red", Qt.red)
        comboBox.addItem("Blue", Qt.blue)
        comboBox.addItem("Black", Qt.black)
        comboBox.addItem("Magenta", Qt.magenta)
        return comboBox

def main():
    calendar = QApplication(sys.argv)
    window = Calendar()
    window.show()
    calendar.exec_()

if __name__ == '__main__':
    main()