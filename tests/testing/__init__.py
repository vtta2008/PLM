# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------


# Python
import sys

# PyQt5
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QTextCharFormat
from PySide2.QtWidgets import (QApplication, QComboBox, QDateEdit, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLayout)




# Plt
from PLM.options import (SiPoMin, center, SingleSelection, NoSelection, DayOfWeek, Sunday, Monday, Tuesday, Wednesday,
                         Thursday, Friday, Saturday, SingleLetterDay, LongDay, ShortDay, NoHoriHeader, NoVertHeader,
                         IsoWeekNum, SelectMode, HoriHeaderFm, VertHeaderFm)
from bin.Core import Date, Locale
from bin.Widgets import GridLayout, Widget, GroupGrid, CalendarWidget, GroupCombo, Label, ComboBox, CheckBox, HBoxLayout
from bin.Gui import AppIcon


# -------------------------------------------------------------------------------------------------------------
""" Clendar """

maxDate = Date(1900, 1, 1)
minDate = Date(3000, 1, 1)



class GeneralOption(GroupCombo):

    key                             = 'GeneralOption'

    def __init__(self, title='', calendar=None):
        super(GeneralOption, self).__init__("", calendar)

        self._title                 = title
        self.calendar               = calendar

        curLocaleIndex              = -1
        lang_country                = {}
        locales                     = Locale.matchingLocales(Locale.AnyLanguage, Locale.AnyScript, Locale.AnyCountry)

        id = 0
        for i in locales:
            l = i.nativeLanguageName()
            s = Locale.scriptToString(i.script())
            c = i.nativeCountryName()
            if not l == "" and not c == "":
                lang_country[c] = [l, s, id]
            id += 1

        countries = sorted(list(set([c for c in lang_country])))
        countries.remove(countries[0])

        for country in countries:
            lang = lang_country[country][0]
            label = "{0} - {1}".format(lang, country)
            locale = lang_country[country][2]

            if self.locale().language() == lang and self.locale().country() == country:
                curLocaleIndex = lang_country[country][2]

            self.layout.addItem(label, locale)

        if curLocaleIndex != -1:
            self.layout.setCurrentIndex(curLocaleIndex)

        self.layout.currentIndexChanged.connect(self.localeChanged)


        horiPreset = {'2items': [["Single letter day names", SingleLetterDay], ["Short day names", ShortDay],
                        ["Long day names", LongDay], ["None", NoHoriHeader]], 'curIndex': 1,
                      'curIndexChange': self.horiHeaderChange}

        firstDayPreset = {'2items': [['Sunday', Sunday], ['Monday', Monday], ['Tuesday', Tuesday], ['Wednesday', Wednesday],
                                     ['Thursday', Thursday], ['Friday', Friday], ['Saturday', Saturday]],
                                    'curIndexChange': self.firstDayChanged}

        self.firstDayCB             = ComboBox(firstDayPreset)
        self.selectModeCB           = ComboBox({'2items': [['single', SingleSelection], ['None', NoSelection]],
                                                'curIndexChange': self.selectionModeChanged})
        self.horiHeadCB             = ComboBox(horiPreset)
        self.vertHeaderCB           = ComboBox({'2items': [["ISO week numbers", IsoWeekNum], ["None", NoVertHeader]],
                                                'curIndexChange': self.vertHeaderChange})

        self.gridCB                 = CheckBox("&Grid", {'check': bool(self.calendar.isGridVisible), 'toggle': self.calendar.setGridVisible})

        self.navigateCB             = CheckBox("&Navigation bar", {'check': True, 'toggle': self.calendar.setNavigationBarVisible})


        self.localeLabel            = Label({'txt': '&Locale', 'buddy': self.layout})
        self.firstDayLabel          = Label({'txt': '"Wee&k starts on:"', 'buddy': self.firstDayCB})
        self.selectModeLabel        = Label({'txt': '&Selection fn:', 'buddy': self.selectModeCB})
        self.horiHeadLabel          = Label({'txt': '&Horizontal header:', 'buddy': self.horiHeadCB})
        self.verticalHeaderLabel    = Label({'txt': '&Vertical header:', 'buddy': self.vertHeaderCB})


        checkBoxLayout = HBoxLayout({'addWidget': [self.gridCB, self.navigateCB], 'stretch': None})

        outerLayout = QGridLayout()
        outerLayout.addWidget(self.localeLabel, 0, 0, 1, 1)
        outerLayout.addWidget(self.layout, 0, 1, 1, 1)
        outerLayout.addWidget(self.firstDayLabel, 1, 0, 1, 1)
        outerLayout.addWidget(self.firstDayCB, 1, 1, 1, 1)
        outerLayout.addWidget(self.selectModeLabel, 2, 0, 1, 1)
        outerLayout.addWidget(self.selectModeCB, 2, 1, 1, 1)

        outerLayout.addLayout(checkBoxLayout, 3, 0, 1, 2)

        outerLayout.addWidget(self.horiHeadCB, 5, 0, 1, 1)
        outerLayout.addWidget(self.horiHeadLabel, 5, 1, 1, 1)
        outerLayout.addWidget(self.verticalHeaderLabel, 6, 0, 1, 1)
        outerLayout.addWidget(self.vertHeaderCB, 6, 1, 1, 1)

        self.layout.setLayout(outerLayout)

        self.firstDayChanged(self.firstDayCB.currentIndex())
        self.selectionModeChanged(self.selectModeCB.currentIndex())
        self.horiHeaderChange(self.horiHeadCB.currentIndex())
        self.vertHeaderChange(self.vertHeaderCB.currentIndex())

    def localeChanged(self, index):
        self.calendar.setLocale(self.itemData(index))

    def firstDayChanged(self, index):
        self.calendar.setFirstDayOfWeek(DayOfWeek(self.firstDayCB.itemData(index)))

    def selectionModeChanged(self, index):
        self.calendar.setSelectionMode(SelectMode(self.selectModeCB.itemData(index)))

    def horiHeaderChange(self, index):
        self.calendar.setHorizontalHeaderFormat(HoriHeaderFm(self.horiHeadCB.itemData(index)))

    def vertHeaderChange(self, index):
        self.calendar.setVerticalHeaderFormat(VertHeaderFm(self.vertHeaderCB.itemData(index)))

class Calendar(Widget):

    key                             = 'Calendar'

    def __init__(self, parent=None):
        super(Calendar, self).__init__(parent)

        self.setWindowIcon(AppIcon(32, self.key))
        self.setWindowTitle(self.key)

        self.layout                 = GridLayout(self)
        self.calendar               = CalendarWidget(self)
        self.generalOpt             = GeneralOption(title="General Options", calendar=self.calendar)

        self.setLayout(self.layout)
        self.applySetting()
        self.buildUI()

    def buildUI(self):

        self.previewGB = GroupGrid("Preview", self)
        self.previewGB.layout.addWidget(self.calendar, 0, 0, center)

        self.createGeneralOptionsGroupBox()
        self.createDatesGroupBox()
        self.createTextFormatsGroupBox()

        self.calendar.currentPageChanged.connect(self.reformatCalendarPage)

        self.layout.addWidget(self.previewGB, 0, 0)
        self.layout.addWidget(self.generalOpt, 0, 1)
        self.layout.addWidget(self.datesGroupBox, 1, 0)
        self.layout.addWidget(self.textFormatsGroupBox, 1, 1)

        self.layout.setSpacing(2)
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setSizePolicy(SiPoMin, SiPoMin)

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
        format.setForeground(Qt.GlobalColor(self.weekdayColorCombo.itemData(self.weekdayColorCombo.currentIndex())))

        self.calendar.setWeekdayTextFormat(Qt.Monday, format)
        self.calendar.setWeekdayTextFormat(Qt.Tuesday, format)
        self.calendar.setWeekdayTextFormat(Qt.Wednesday, format)
        self.calendar.setWeekdayTextFormat(Qt.Thursday, format)
        self.calendar.setWeekdayTextFormat(Qt.Friday, format)

    def weekendFormatChanged(self):
        format = QTextCharFormat()
        format.setForeground(Qt.GlobalColor(self.weekendColorCombo.itemData(self.weekendColorCombo.currentIndex())))

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
            firstFriday = Date(self.calendar.yearShown(), self.calendar.monthShown(), 1)

            while firstFriday.dayOfWeek() != Qt.Friday:
                firstFriday = firstFriday.addDays(1)

            firstFridayFormat = QTextCharFormat()
            firstFridayFormat.setForeground(Qt.blue)

            self.calendar.setDateTextFormat(firstFriday, firstFridayFormat)

        # May 1st in Red takes precedence.
        if self.mayFirstCheckBox.isChecked():
            mayFirst = Date(self.calendar.yearShown(), 5, 1)

            mayFirstFormat = QTextCharFormat()
            mayFirstFormat.setForeground(Qt.red)

            self.calendar.setDateTextFormat(mayFirst, mayFirstFormat)

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

        self.firstFridayCheckBox = CheckBox("&First Friday in blue")

        self.mayFirstCheckBox = CheckBox("May &1 in red")

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

    def applySetting(self):
        self.calendar.setMinimumDate(minDate)
        self.calendar.setMaximumDate(maxDate)
        self.calendar.setGridVisible(True)

def main():
    calendar = QApplication(sys.argv)
    window = Calendar()
    window.show()
    calendar.exec_()


if __name__ == '__main__':
    main()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/16/2020 - 2:17 AM
# © 2017 - 2019 DAMGteam. All rights reserved