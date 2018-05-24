#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: topTab1.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, logging

# PyQt5
from PyQt5.QtCore import QUrl, QSize, QSettings
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QGroupBox

# Plt
import appData as app
from ui import uirc as rc
from utilities import utils as func
from utilities import variables as var

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logPth = os.path.join(app.LOGPTH)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
""" Variables """

ICON_SIZE = 30
ICON_BUFFRATE = 10
ICON_BUFFREGION = -1
ICON_BUFF = ICON_BUFFREGION*(ICON_SIZE*ICON_BUFFRATE/100)
ICON_SET_SIZE = QSize(ICON_SIZE + ICON_BUFF, ICON_SIZE + ICON_BUFF)

def handleLeftClick(x, y):
    row = int(y)
    column = int(x)
    print("Clicked on image pixel (row=" + str(row) + ", column=" + str(column) + ")")

# -------------------------------------------------------------------------------------------------------------
""" topTab1 """

class TopTab1(QWidget):

    def __init__(self, parent=None):
        super(TopTab1, self).__init__(parent)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        for i in app.CONFIG_PQUIP1:
            self.settings.setValue(i, False)

        self.appInfo = func.preset_load_appInfo()
        self.layout = QGridLayout()

        self.buildUI()

        self.setLayout(self.layout)

    def buildUI(self):

        officeBtns = [rc.IconBtnProcess(key) for key in app.CONFIG_OFFICE if key in self.appInfo] or []
        sec1Grp = rc.AutoSectionBtnGrp("Office", officeBtns, "IconGrid")

        devBtns = [rc.IconBtnProcess(key) for key in app.CONFIG_DEV if key in self.appInfo] or []
        sec2Grp = rc.AutoSectionBtnGrp("Dev", devBtns, "IconGrid")

        loaduiLst = [self.calculatorUI, self.calendarUI, self.englishDictionaryUI, self.findFilesUI, self.imageViewerUI,
                     self.noteReminderUI, self.pltBrowserUI, self.screenshotUI, self.textEditorUI]

        pyuiBtns = []
        for key in app.CONFIG_PQUIP1:
            if key in self.appInfo:
                btn = rc.IconBtnLoadLayout(key)
                sig = btn.consoleSig
                sig.connect(loaduiLst[app.CONFIG_PQUIP1.index(key)])
                pyuiBtns.append(btn)

        sec3Grp = rc.AutoSectionBtnGrp("Tools", pyuiBtns, "IconGrid")

        sec4Grp = QGroupBox("CMD")
        sec4Grid = QGridLayout()
        sec4Grp.setLayout(sec4Grid)

        sec5Grp = QGroupBox("CGI")
        sec5Grid = QGridLayout()
        sec5Grp.setLayout(sec5Grid)

        for key in self.appInfo:
            if key == 'Mudbox 2018':
                mudbox18Btn = rc.IconBtnProcess(key)
                sec4Grid.addWidget(mudbox18Btn, 2, 0, 1, 1)
            if key == 'Mudbox 2017':
                mudbox17Btn = rc.IconBtnProcess(key)
                sec4Grid.addWidget(mudbox17Btn, 2, 1, 1, 1)
            if key == '3ds Max 2018':
                max18Btn = rc.IconBtnProcess(key)
                sec4Grid.addWidget(max18Btn, 2, 2, 1, 1)
            if key == '3ds Max 2017':
                max17Btn = rc.IconBtnProcess(key)
                sec4Grid.addWidget(max17Btn, 3, 0, 1, 1)

        self.layout.addWidget(sec1Grp, 0, 0, 2, 3)
        self.layout.addWidget(sec2Grp, 2, 0, 2, 3)
        self.layout.addWidget(sec3Grp, 0, 3, 4, 3)
        self.layout.addWidget(sec4Grp, 0, 6, 2, 2)
        self.layout.addWidget(sec5Grp, 2, 6, 2, 2)

        self.applySetting()

    def calculatorUI(self):
        from ui import Calculator
        app.reload(Calculator)
        layout = Calculator.Calculator()
        layout.show()
        layout.exec_()

    def calendarUI(self):
        from ui import Calendar
        app.reload(Calendar)
        layout = Calendar.Calendar()
        layout.show()
        layout.exec_()

    def englishDictionaryUI(self):
        from ui import EnglishDictionary
        app.reload(EnglishDictionary)
        layout = EnglishDictionary.EnglishDictionary()
        layout.show()
        layout.exec_()

    def findFilesUI(self):
        from ui import FindFiles
        app.reload(FindFiles)
        layout = FindFiles.FindFiles()
        layout.show()
        layout.exec_()

    def imageViewerUI(self):
        from ui import ImageViewer
        app.reload(ImageViewer)
        layout = ImageViewer.ImageViewer()
        layout.show()
        layout.exec_()

    def noteReminderUI(self):
        from ui import NoteReminder
        app.reload(NoteReminder)
        layout = NoteReminder.NoteReminder()
        layout.show()
        layout.exec_()

    def pltBrowserUI(self):
        from ui import PltBrowser
        app.reload(PltBrowser)
        layout = PltBrowser.PltBrowser(QUrl('http://www.google.com.vn'))
        layout.show()
        layout.exec_()

    def screenshotUI(self):
        from ui import Screenshot
        app.reload(Screenshot)
        layout = Screenshot.Screenshot()
        layout.show()
        layout.exec_()

    def textEditorUI(self):
        from ui import TextEditor
        app.reload(TextEditor)
        layout = TextEditor.TextEditor()
        layout.show()
        layout.exec_()

    def applySetting(self):

        self.layout.setSpacing(2)


def main():
    app = QApplication(sys.argv)
    layout = TopTab1()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/05/2018