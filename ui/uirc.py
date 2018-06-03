#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: uirc.py
Author: Do Trinh/Jimmy - 3D artist.
Description: This script is the place for every ui elements

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, os, webbrowser
import json
import subprocess
from functools import partial

# PyQt5
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QIcon, QPixmap, QTextTableFormat, QTextCharFormat
from PyQt5.QtWidgets import (QLabel, QGridLayout, QPushButton, QAction, QApplication, QGroupBox, QToolBar,
                             QGraphicsView, QHBoxLayout, QGraphicsScene, QTabWidget, QWidget, QTabBar,
                             QVBoxLayout, QToolButton, QTextEdit, QDockWidget)

# Plt
import appData as app
from utilities import localSQL as usql
from utilities import utils as func

# Path
with open(app.mainConfig, 'r') as f:
    APPINFO = json.load(f)

# -------------------------------------------------------------------------------------------------------------
""" UI resource with signal """

class Run(QObject):

    def __init__(self, data=None, parent=None):
        super(Run, self).__init__(parent)

        self.data = data

        if "App: " in self.data:
            self.openApp(self.data.split("App: ")[1])
        elif "Url: " in self.data:
            self.openUrl(self.data.split("Url: ")[1])
        elif "Func: " in self.data:
            self.exeFunc(self.data.split("Func: ")[1])
        elif "UI: " in self.data:
            pass

    def openApp(self, pth):
        subprocess.Popen(pth)

    def openUrl(self, url):
        webbrowser.open(url)

    def exeFunc(self, funcName):
        if funcName == "Exit":
            usql.TimeLog("Log out")
            QApplication.instance().quit()
        elif funcName == "open_cmd":
            func.open_cmd()

# -------------------------------------------------------------------------------------------------------------
""" UI resource preset """

class IconPth(QIcon):

    def __init__(self, size=32, name="AboutPlt"):
        super(IconPth, self).__init__()

        self.iconPth = func.getAppIcon(size, name)
        self.buildUI()

    def buildUI(self):
        self.addFile(self.iconPth, QSize(32, 32))
        self.applySetting()

    def applySetting(self):
        pass

class AppIcon(QIcon):

    def __init__(self, name="Logo", parent=None):
        super(AppIcon, self).__init__(parent)

        sizes = [16, 24, 32, 48, 64, 96, 128, 256, 512]

        for s in sizes:
            self.addFile(func.getLogo(s, name), QSize(s, s))

        self.applySetting()

    def applySetting(self):

        pass

class ImageUI(QGraphicsView):

    def __init__(self, icon="", size=None, parent=None):
        super(ImageUI, self).__init__(parent)

        self.settings = app.APPSETTING
        self.pixmap = QPixmap(func.getAppIcon(32, icon))

        if size == None or len(size) == 0:
            self.size = [self.pixmap.width(), self.pixmap.height()]
        else:
            self.size = size

        self.scene = QGraphicsScene()
        self.buildUI()
        self.setScene(self.scene)

    def buildUI(self):
        self.scene.addPixmap(self.pixmap)
        self.applySetting()

    def applySetting(self):
        pass

class Label(QLabel):

    def __init__(self, txt=app.TXT, wmin=app.WMIN, alg = None, font=None, parent=None):
        super(Label, self).__init__(parent)

        self.settings = app.APPSETTING

        if alg == None:
            alg = Qt.AlignCenter

        if font == None:
            font = QFont("Arial, 10")

        self.alg = alg
        self.fnt = font
        self.txt = txt
        self.wmin = wmin

        self.buildText()

    def buildText(self):
        self.setText(self.txt)
        self.applySetting()

    def applySetting(self):
        self.setMinimumWidth(self.wmin)
        self.setAlignment(self.alg)
        self.setFont(self.fnt)
        self.setSizePolicy(app.SiPoMin, app.SiPoMin)
        self.setScaledContents(True)
        self.setWordWrap(True)

class ToolBtn(QToolButton):

    def __init__(self, text, parent=None):
        super(ToolBtn, self).__init__(parent)

        self.settings = app.APPSETTING
        self.setText(text)
        self.applySetting()

    def applySetting(self):
        self.setSizePolicy(app.SiPoExp, app.SiPoPre)

    def sizeHint(self):
        size = super(ToolBtn, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size

class Button(QPushButton):

    def __init__(self, data=[], parent=None):
        super(Button, self).__init__(parent)

        self.data = data
        self.buildUI()

    def buildUI(self):

        self.setText(self.data[0])
        self.setToolTip(self.data[1])
        self.applySetting()

    def applySetting(self):
        self.setSizePolicy(app.SiPoMin, app.SiPoMin)
        self.setMouseTracking(True)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class IconBtnProcess(QPushButton):

    consoleSig = pyqtSignal(str)

    def __init__(self, key, parent=None):
        super(IconBtnProcess, self).__init__(parent)

        self.settings = app.APPSETTING

        self.key = key

        self.buildUI()

    def buildUI(self):

        self.setToolTip(APPINFO[self.key][0])
        self.setIcon(IconPth(32, self.key))
        self.clicked.connect(partial(self.consoleSig.emit, self.key))

        self.applySetting()

    def on_icon_btn_clicked(self, data):
        Run(data)

    def applySetting(self):
        self.setFixedSize(app.BTNICONSIZE)
        self.setIconSize(app.ICONBTNSIZE)
        self.setMouseTracking(True)

class IconBtnLoadLayout(QPushButton):

    consoleSig = pyqtSignal(str)

    def __init__(self, key=None, parent=None):
        super(IconBtnLoadLayout, self).__init__(parent)

        self.settings = app.APPSETTING
        self.key = key

        self.buildUI()

    def buildUI(self):
        self.setToolTip(APPINFO[self.key][0])
        self.setIcon(IconPth(32, self.key))
        self.clicked.connect(partial(self.consoleSig.emit, self.key))

        self.applySetting()

    def on_icon_btn_clicked(self):
        self.settings.setValue(self.key, True)
        self.consoleSig.emit(self.key)

    def applySetting(self):
        self.setFixedSize(app.BTNICONSIZE)
        self.setIconSize(app.ICONBTNSIZE)
        self.setMouseTracking(True)

class ActionProcess(QAction):

    consoleSig = pyqtSignal(str)

    def __init__(self, key, parent=None):
        super(ActionProcess, self).__init__(parent)
        self.settings = app.APPSETTING
        self.key = key
        self.buildUI()

    def buildUI(self):
        self.setIcon(QIcon(APPINFO[self.key][1]))
        self.setText(self.key)
        self.setStatusTip(APPINFO[self.key][0])
        self.triggered.connect(partial(self.on_action_triggered, APPINFO[self.key][2]))

        self.applySetting()

    def on_action_triggered(self, data):
        Run(data)

    def applySetting(self):
        pass

class ActionLoadLayout(QAction):

    consoleSig = pyqtSignal(str)

    def __init__(self, key, parent=None):
        super(ActionLoadLayout, self).__init__(parent)

        self.settings = app.APPSETTING
        self.key = key

        self.buildUI()

    def buildUI(self, key):
        self.setIcon(QIcon(APPINFO[self.key][1]))
        self.setText(key)
        self.setStatusTip(APPINFO[self.key][0])
        self.triggered.connect(self.on_action_triggered)

        self.applySetting()

    def on_action_triggered(self):
        self.settings.setValue(self.key, True)
        self.consoleSig.emit(True)

    def applySetting(self):
        pass

class BatchTBProcess(QToolBar):

    def __init__(self, name="Tool bar name", apps=[], parent=None):
        super(BatchTBProcess, self).__init__(parent)

        self.settings = app.APPSETTING
        self.name = name
        self.layout = parent
        self.apps = apps

        self.buildUI()

    def buildUI(self):
        self.toolBar = self.layout.addToolBar(self.name)

        for key in self.apps:
            if key in APPINFO:
                self.toolBar.addAction(ActionProcess(key, self.layout))

        self.applySetting()

    def applySetting(self):
        pass

# -------------------------------------------------------------------------------------------------------------
""" Dock widget """

class NoteStamp(QTextTableFormat):
    def __init__(self):
        super(NoteStamp, self).__init__()
        self.setBorder(1)
        self.setCellPadding(4)
        self.setAlignment(app.right)

class DockStamp(QTextEdit):

    def __init__(self, parent=None):
        super(DockStamp, self).__init__(parent)

        self.buildStamp()

    def buildStamp(self):

        cursor = self.textCursor()
        frame = cursor.currentFrame()
        frameFormat = frame.frameFormat()
        frameFormat.setPadding(1)
        frame.setFrameFormat(frameFormat)

        cursor.insertTable(1, 1, NoteStamp())
        cursor.insertText(app.datetTimeStamp, QTextCharFormat())

    def applySetting(self):
        self.resize(250, 100)
        self.setSizePolicy(app.SiPoMin, app.SiPoMin)

class DockWidget(QDockWidget):

    def __init__(self, name="Reminder", parent=None):
        super(DockWidget, self).__init__(parent)

        self.setWindowTitle = name
        self.setAllowedAreas(app.dockB | app.dockT)

        self.content = DockStamp(self)
        self.buildUI()
        self.setWidget(self.content)

    def buildUI(self):

        cursor = self.content.textCursor()
        cursor.insertBlock()
        cursor.insertText("Note info")

# -------------------------------------------------------------------------------------------------------------
""" Tab layout element"""

class TabBar(QTabBar):

    def tabSizeHint(self, index):
        size = QTabBar.tabSizeHint(self, index)
        w = int(self.width()/self.count())
        return QSize(w, size.height())

class TabContent(QWidget):

    def __init__(self, layout=None, parent=None):
        super(TabContent, self).__init__(parent)

        if layout is None:
            layout = QGridLayout()
            layout.addWidget(Label())

        self.settings = app.APPSETTING
        self.layout = layout
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.applySetting()

    def applySetting(self):
        self.setSizePolicy(app.SiPoMin, app.SiPoMin)

class TabWidget(QWidget):

    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self.settings = app.APPSETTING
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.tabs = QTabWidget()
        self.tabs.setTabBar(TabBar())
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)

        self.applySetting()

    def applySetting(self):
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setUsesScrollButtons(True)

# -------------------------------------------------------------------------------------------------------------
""" Layout """

class AutoArrangeIconGrid(QGridLayout):

    def __init__(self, btns=[], parent=None):
        super(AutoArrangeIconGrid, self).__init__(parent)

        self.settings = app.APPSETTING

        self.btns = btns

        self.buildUI()

    def buildUI(self):
        if not len(self.btns) == 0:
            for i in range(len(self.btns)):
                if str(type(self.btns[i])) in ["<class 'ui.uirc.IconBtnProcess'>", "<class 'ui.uirc.IconBtnLoadLayout'>", ]:
                    if i == 0:
                        self.addWidget(self.btns[i], 0, 0, 1, 1)
                    elif i == 1:
                        self.addWidget(self.btns[i], 0, 1, 1, 1)
                    elif i == 2:
                        self.addWidget(self.btns[i], 0, 2, 1, 1)
                    elif i == 3:
                        self.addWidget(self.btns[i], 1, 0, 1, 1)
                    elif i == 4:
                        self.addWidget(self.btns[i], 1, 1, 1, 1)
                    elif i == 5:
                        self.addWidget(self.btns[i], 1, 2, 1, 1)
                    elif i == 6:
                        self.addWidget(self.btns[i], 2, 0, 1, 1)
                    elif i == 7:
                        self.addWidget(self.btns[i], 2, 1, 1, 1)
                    elif i == 8:
                        self.addWidget(self.btns[i], 2, 2, 1, 1)
                else:
                    raise TypeError("Type Object is not corrected, expected icon button class")
                i += 1

        self.applySetting()

    def applySetting(self):
        pass

class AutoArrangeBtnGrid(QGridLayout):

    def __init__(self, btns=[], parent=None):
        super(AutoArrangeBtnGrid, self).__init__(parent)

        self.settings = app.APPSETTING
        self.btns = btns
        self.buildUI()

    def buildUI(self):
        if not len(self.btns) == 0:
            for i in range(len(self.btns)):
                if str(type(self.btns[i])) in ["<class 'PyQt5.QtWidgets.QPushButton'>"]:
                    if i == 0:
                        self.addWidget(self.btns[i], 0, 0, 1, 2)
                    elif i == 1:
                        self.addWidget(self.btns[i], 1, 0, 1, 2)
                    elif i == 2:
                        self.addWidget(self.btns[i], 2, 0, 1, 2)
                    elif i == 3:
                        self.addWidget(self.btns[i], 3, 0, 1, 2)
                    elif i == 4:
                        self.addWidget(self.btns[i], 4, 0, 1, 2)
                    elif i == 5:
                        self.addWidget(self.btns[i], 5, 0, 1, 2)
                    elif i == 6:
                        self.addWidget(self.btns[i], 6, 0, 1, 2)
                    elif i == 7:
                        self.addWidget(self.btns[i], 7, 0, 1, 2)
                    elif i == 8:
                        self.addWidget(self.btns[i], 8, 0, 1, 2)
                else:
                    raise TypeError("Type Object is not corrected, expected icon button class")
            i += 1

        self.applySetting()

    def applySetting(self):
        pass

class AutoArrangeImageView(QGridLayout):

    def __init__(self, imageView, parent=None):
        super(AutoArrangeImageView, self).__init__(parent)

        self.settings = app.APPSETTING

        self.img = imageView

        self.buildUI()


    def buildUI(self):

        if self.img:
            if str(type(self.img)) in ["<class 'PyQt5.QtWidgets.QGraphicsView'>", ]:
                self.addWidget(self.img, 0, 0, 1, 1)

        self.applySetting()

    def applySetting(self):
        pass

class AutoSectionBtnGrp(QGroupBox):

    def __init__(self, title="Section Title", btns=[], mode="IconGrid", parent=None):
        super(AutoSectionBtnGrp, self).__init__(parent)

        self.settings = app.APPSETTING
        self.setTitle(title)
        self.btns = btns
        self.mode = mode

        self.buildUI()

    def buildUI(self):
        if self.mode == "IconGrid":
            self.setLayout(AutoArrangeIconGrid(self.btns))
        elif self.mode == "BtnGrid":
            self.setLayout(AutoArrangeBtnGrid(self.btns))
        elif self.mode == "ImageView":
            self.setLayout(AutoArrangeImageView(self.btns[0]))

        self.applySetting()

    def applySetting(self):
        pass

class AutoSectionQMainGrp(QGroupBox):

    def __init__(self, title="Section Title", subLayout=None, parent=None):
        super(AutoSectionQMainGrp, self).__init__(parent)

        self.settings = app.APPSETTING
        self.setTitle(title)
        self.subLayout = subLayout

        self.layout = QHBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.layout.addWidget(self.subLayout)

        self.applySetting()

    def applySetting(self):
        pass

class AutoSectionQGridGrp(QGroupBox):

    def __init__(self, title="Section Title", subLayout=None, parent=None):
        super(AutoSectionQGridGrp, self).__init__(parent)

        self.settings = app.APPSETTING
        self.setTitle(title)

        self.layout = subLayout
        self.setLayout(self.layout)

        self.applySetting()

    def applySetting(self):
        pass

class AutoSectionLayoutGrp(QGroupBox):

    def __init__(self, title="Section Title", subLayout=None, parent=None):
        super(AutoSectionLayoutGrp, self).__init__(parent)

        self.settings = app.APPSETTING
        self.setTitle(title)

        if subLayout == None or len(subLayout) == 0 or str(type(subLayout)) in ["Class <'Label'>", "Class <'QLabel'>",]:
            subLayout = Label(app.WAIT_LAYOUT_COMPLETE)
            self.layout = QGridLayout()
            self.layout.addWidget(subLayout, 0, 0, 1, 1)
        else:
            self.layout = subLayout

        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.applySetting()

    def applySetting(self):
        pass

# -------------------------------------------------------------------------------------------------------------
