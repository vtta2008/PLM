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
from PySide2.QtGui import QTextCharFormat
from PySide2.QtWidgets import (QApplication, QLayout)

# Plt
from PLM.options import (SiPoMin, center, SingleSelection, NoSelection, DayOfWeek, Sunday, Monday, Tuesday, Wednesday,
                         Thursday, Friday, Saturday, SingleLetterDay, LongDay, ShortDay, NoHoriHeader, NoVertHeader,
                         IsoWeekNum, SelectMode, HoriHeaderFm, VertHeaderFm, TEXT_BOLD, GlobalColor, GREEN, BLUE, RED,
                         BLACK, MAGENTA)
from pyPLM.Core import Date, Locale
from pyPLM.Widgets import (GridLayout, Widget, GroupGrid, CalendarWidget, GroupCombo, Label, ComboBox, CheckBox,
                           HBoxLayout, DateEdit)
from pyPLM.Gui import AppIcon


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

        outerLayout = GridLayout()
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



class DateOption(GroupGrid):

    key = 'DateOption'

    def __init__(self, title=None, calendar=None):
        super(DateOption, self).__init__(calendar)

        self.calendar = calendar

        self.minDateEdit = DateEdit(None, {'dispfm': 'MMM d yyyy',
                                           'dateRange': [self.calendar.minimumDate(), self.calendar.maximumDate()],
                                           'date': self.calendar.minimumDate()})

        self.curDateEdit = DateEdit(None, {'dispfm': 'MMM d yyyy',
                                           'dateRange': [self.calendar.minimumDate(), self.calendar.maximumDate()],
                                           'date': self.calendar.selectedDate()})

        self.maxDateEdit = DateEdit(None, {'dispfm': 'MMM d yyyy',
                                           'dateRange': [self.calendar.minimumDate(), self.calendar.maximumDate()],
                                           'date': self.calendar.maxDateEdit})

        self.minDateLabel = Label({'txt': "&Minimum Date:", 'buddy': self.minDateEdit})
        self.curDateLabel = Label({'txt': '&Current Date:', 'buddy': self.curDateEdit})
        self.maxDateLabel = Label({'txt': '&Maximum Date:', 'buddy': self.maxDateEdit})

        self.curDateEdit.dateChanged.connect(self.calendar.setSelectedDate)
        self.calendar.selectionChanged.connect(self.selectedDateChanged)
        self.minDateEdit.dateChanged.connect(self.minimumDateChanged)
        self.maximumDateEdit.dateChanged.connect(self.maximumDateChanged)

        self.layout.addWidget(self.curDateLabel, 1, 0)
        self.layout.addWidget(self.curDateEdit, 1, 1)
        self.layout.addWidget(self.minDateLabel, 0, 0)
        self.layout.addWidget(self.minDateEdit, 0, 1)
        self.layout.addWidget(self.maxDateLabel, 2, 0)
        self.layout.addWidget(self.maxDateEdit, 2, 1)
        self.layout.setRowStretch(3, 1)



class TextOption(GroupGrid):

    key = 'TextOption'

    def __init__(self, title=None, calendar=None):
        super(TextOption, self).__init__(calendar)

        self._title = title
        self.calendar = calendar

        self.weekdayColorCB = ComboBox({'2items': [["Red", RED], ["Blue", BLUE], ["Black", BLACK], ["Magenta", MAGENTA]],
                                        'curIndex': self.weekdayColorCB.findText("Black"),
                                        'curIndexChange': self.weekdayFormatChanged})

        self.weekendColorCB = ComboBox({'2items': [["Red", RED], ["Blue", BLUE], ["Black", BLACK], ["Magenta", MAGENTA]],
                                        'curIndex': self.weekendColorCB.findText("Red"),
                                        'curIndexChange': self.weekendFormatChanged})

        self.headerTxtfmCB = ComboBox({'items': ['Bold', 'Italic', 'Plain'], 'curIndexChange': self.reformatHeaders})

        self.weekdayColorLabel = Label({'txt': "&Weekday color:", 'buddy': self.weekdayColorCB})
        self.weekendColorLabel = Label({'txt': "Week&end color:", 'buddy': self.weekendColorCB})
        self.headerTxtfmLabel = Label({'txt': "&Header text:", 'buddy': self.headerTxtfmCB})

        self.firstFridayCB = CheckBox("&First Friday in blue", {'toggle': self.reformatCalendarPage})
        self.mayFirstCB = CheckBox("May &1 in red", {'toggle': self.reformatCalendarPage})

        self.layout.addWidget(self.weekdayColorLabel, 0, 0, 1, 1)
        self.layout.addWidget(self.weekdayColorCB, 0, 1, 1, 1)
        self.layout.addWidget(self.weekendColorLabel, 1, 0, 1, 1)
        self.layout.addWidget(self.weekendColorCB, 1, 1, 1, 1)
        self.layout.addWidget(self.headerTxtfmLabel, 2, 0, 1, 1)
        self.layout.addWidget(self.headerTxtfmCB, 2, 1, 1, 1)
        self.layout.addLayout(HBoxLayout(None, {'addWidget': [self.firstFridayCB, self.mayFirstCB]}), 3, 0, 1, 2)

        self.calendar.currentPageChanged.connect(self.reformatCalendarPage)

        self.weekdayFormatChanged()
        self.weekendFormatChanged()

        self.reformatHeaders()
        self.reformatCalendarPage()

    def reformatCalendarPage(self):
        if self.firstFridayCB.isChecked():
            firstFriday = Date(self.calendar.yearShown(), self.calendar.monthShown(), 1)

            while firstFriday.dayOfWeek() != Friday:
                firstFriday = firstFriday.addDays(1)

            firstFridayFormat = QTextCharFormat()
            firstFridayFormat.setForeground(BLUE)

            self.calendar.setDateTextFormat(firstFriday, firstFridayFormat)

        # May 1st in Red takes precedence.
        if self.mayFirstCB.isChecked():
            mayFirst = Date(self.calendar.yearShown(), 5, 1)

            mayFirstFormat = QTextCharFormat()
            mayFirstFormat.setForeground(RED)

            self.calendar.setDateTextFormat(mayFirst, mayFirstFormat)


    def reformatHeaders(self):
        text = self.headerTxtfmCB.currentText()
        format = QTextCharFormat()

        if text == "Bold":
            format.setFontWeight(TEXT_BOLD)
        elif text == "Italic":
            format.setFontItalic(True)
        elif text == "Green":
            format.setForeground(GREEN)

        self.calendar.setHeaderTextFormat(format)


    def selectedDateChanged(self):
        self.curDateEdit.setDate(self.calendar.selectedDate())


    def minimumDateChanged(self, date):
        self.calendar.setMinimumDate(date)
        self.maximumDateEdit.setDate(self.calendar.maximumDate())

    def maximumDateChanged(self, date):
        self.calendar.setMaximumDate(date)
        self.minDateEdit.setDate(self.calendar.minimumDate())

    def weekdayFormatChanged(self):
        format = QTextCharFormat()
        format.setForeground(GlobalColor(self.weekdayColorCB.itemData(self.weekdayColorCB.currentIndex())))

        self.calendar.setWeekdayTextFormat(Monday, format)
        self.calendar.setWeekdayTextFormat(Tuesday, format)
        self.calendar.setWeekdayTextFormat(Wednesday, format)
        self.calendar.setWeekdayTextFormat(Thursday, format)
        self.calendar.setWeekdayTextFormat(Friday, format)

    def weekendFormatChanged(self):
        format = QTextCharFormat()
        format.setForeground(GlobalColor(self.weekendColorCB.itemData(self.weekendColorCB.currentIndex())))

        self.calendar.setWeekdayTextFormat(Saturday, format)
        self.calendar.setWeekdayTextFormat(Sunday, format)



class Calendar(Widget):

    key                             = 'Calendar'

    def __init__(self, parent=None):
        super(Calendar, self).__init__(parent)

        self.setWindowIcon(AppIcon(32, self.key))
        self.setWindowTitle(self.key)

        self.layout                 = GridLayout(self)
        self.previewGB              = GroupGrid("Preview", self)
        self.calendar               = CalendarWidget(self)

        self.previewGB.layout.addWidget(self.calendar, 0, 0, center)

        self.generalOpt             = GeneralOption(title="General Options", calendar=self.calendar)
        self.dateOpt                = DateOption(title=self.tr("Dates"), calendar=self.calendar)
        self.textOptGB              = TextOption(title="Text Formats", calendar=self.calendar)

        self.setLayout(self.layout)
        self.applySetting()
        self.buildUI()

        self.createTextFormatsGroupBox()

        self.layout.addWidget(self.previewGB, 0, 0)
        self.layout.addWidget(self.generalOpt, 0, 1)
        self.layout.addWidget(self.datesGroupBox, 1, 0)
        self.layout.addWidget(self.textOptGB, 1, 1)

        # self.textOptGB.setLayout(outerLayout)

    def applySetting(self):

        self.calendar.setMinimumDate(minDate)
        self.calendar.setMaximumDate(maxDate)
        self.calendar.setGridVisible(True)

        self.layout.setSpacing(2)
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setSizePolicy(SiPoMin, SiPoMin)





if __name__ == '__main__':
    calendar = QApplication(sys.argv)
    window = Calendar()
    window.show()
    calendar.exec_()