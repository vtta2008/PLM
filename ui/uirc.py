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
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QSettings, QObject
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QFrame, QLabel, QGridLayout, QPushButton, QAction, QApplication, QGroupBox, QToolBar,
                             QGraphicsView, QHBoxLayout, QGraphicsScene, QMessageBox, QTabWidget, QWidget, QTabBar,
                             QVBoxLayout, )

# Plt
import appData as app
from utilities import variables as var
from utilities import sql_local as usql
from utilities import utils as func
from utilities import message as mess

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# String
TXT = "No Text" # String by default

# Value, Nummber, Float, Int ...
UNIT = 60   # Base Unit
MARG = 5    # Content margin
BUFF = 10   # Buffer size
SCAL = 1    # Scale value
STEP = 1    # Step value changing
VAL = 1     # Default value
WLINE = 3   # Line width
MIN = 0     # Minimum value
MAX = 1000  # Maximum value
WMIN = 50   # Minimum width
HMIN = 20   # Minimum height

ICON_SIZE = 30
ICON_BUFFRATE = 10
ICON_BUFFREGION = -1
ICON_BUFF = ICON_BUFFREGION*(ICON_SIZE*ICON_BUFFRATE/100)
ICON_SET_SIZE = QSize(ICON_SIZE + ICON_BUFF, ICON_SIZE + ICON_BUFF)

# Alignment
ALGC = Qt.AlignCenter
ALGR = Qt.AlignRight
ALGL = Qt.AlignLeft
HORZ = Qt.Horizontal
VERT = Qt.Vertical

# Style
frameStyle = QFrame.Sunken | QFrame.Panel

# Path
pth = os.path.join(os.getenv(app.__envKey__), 'appData', 'config', 'main.json')
with open(pth, 'r') as f:
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
            usql.insert_timeLog("Log out")
            QApplication.instance().quit()
        elif funcName == "open_cmd":
            func.open_cmd()

# -------------------------------------------------------------------------------------------------------------
""" UI resource preset """

class IconBtnProcess(QPushButton):

    consoleSig = pyqtSignal(str)

    def __init__(self, key, parent=None):
        super(IconBtnProcess, self).__init__(parent)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.key = key

        self.buildUI()

    def buildUI(self):
        self.setToolTip(APPINFO[self.key][0])
        self.setIcon(QIcon(APPINFO[self.key][1]))
        self.setFixedSize(ICON_SIZE, ICON_SIZE)
        self.setIconSize(ICON_SET_SIZE)
        self.clicked.connect(partial(self.on_icon_btn_clicked, APPINFO[self.key][2]))

        self.applySetting()

    def on_icon_btn_clicked(self, data):
        Run(data)

    def applySetting(self):
        pass

class IconBtnLoadLayout(QPushButton):

    consoleSig = pyqtSignal(bool)

    def __init__(self, key=None, parent=None):
        super(IconBtnLoadLayout, self).__init__(parent)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.key = key

        self.buildUI()

    def buildUI(self):
        self.setToolTip(APPINFO[self.key][0])
        self.setIcon(QIcon(APPINFO[self.key][1]))
        self.setFixedSize(ICON_SIZE, ICON_SIZE)
        self.setIconSize(ICON_SET_SIZE)
        self.clicked.connect(self.on_icon_btn_clicked)

        self.applySetting()

    def on_icon_btn_clicked(self):
        self.settings.setValue(self.key, True)
        self.consoleSig.emit(True)

    def applySetting(self):
        pass

class ActionProcess(QAction):

    consoleSig = pyqtSignal(str)

    def __init__(self, key, parent=None):
        super(ActionProcess, self).__init__(parent)
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
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

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
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

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
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

class AutoArrangeIconGrid(QGridLayout):

    def __init__(self, btns=[], parent=None):
        super(AutoArrangeIconGrid, self).__init__(parent)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.btns = btns

        self.buildUI()

    def buildUI(self):
        if not len(self.btns) == 0:
            for i in range(len(self.btns)):
                if str(type(self.btns[i])) in ["<class 'ui.uirc.IconBtnProcess'>", "<class 'ui.uirc.IconBtnLoadLayout'>"]:
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

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
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

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

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

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
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

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
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

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.setTitle(title)

        self.layout = subLayout
        self.setLayout(self.layout)

        self.applySetting()

    def applySetting(self):
        pass

class AutoSectionLayoutGrp(QGroupBox):

    def __init__(self, title="Section Title", subLayout=None, parent=None):
        super(AutoSectionLayoutGrp, self).__init__(parent)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.setTitle(title)

        if subLayout == None or len(subLayout) == 0 or str(type(subLayout)) in ["Class <'Label'>", "Class <'QLabel'>",]:
            subLayout = Label(mess.WAIT_LAYOUT_COMPLETE)
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
""" Tab layout """

class TabBar(QTabBar):
    def tabSizeHint(self, index):
        size = QTabBar.tabSizeHint(self, index)
        w = int(self.width()/self.count())
        return QSize(w, size.height())

class TabBodyDemo(QWidget):
    def __init__(self, text):
        super(TabBodyDemo, self).__init__()

        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)

        self.button = QPushButton(text)
        self.hbox.addWidget(self.button)

class TabWidget (QWidget):
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)

        self.button = QPushButton("Add tab")
        self.button.clicked.connect(self.buttonClicked)

        self.tabs = QTabWidget()
        self.tabs.setTabBar(TabBar())
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setUsesScrollButtons(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)

        self.tabs.addTab(TabBodyDemo("Very big titleeeeeeeeee"),
                         "Very big titleeeeeeeeeeee")
        self.tabs.addTab(TabBodyDemo("smalltext"), "smalltext")
        self.tabs.addTab(TabBodyDemo("smalltext2"), "smalltext2")

        vbox = QVBoxLayout()
        vbox.addWidget(self.button)
        vbox.addWidget(self.tabs)
        self.setLayout(vbox)

        self.resize(600, 600)

    def closeTab(self, index):
        tab = self.tabs.widget(index)
        tab.deleteLater()
        self.tabs.removeTab(index)

    def buttonClicked(self):
        self.tabs.addTab(TabBodyDemo("smalltext2"), "smalltext2")

# -------------------------------------------------------------------------------------------------------------
""" UI element """

class Label(QLabel):

    def __init__(self, txt=TXT, wmin=WMIN, alg = None, font=None, parent=None):
        super(Label, self).__init__(parent)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

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

class ImageUI(QGraphicsView):

    def __init__(self, icon="", size=None, parent=None):
        super(ImageUI, self).__init__(parent)

        if not os.path.exists(func.get_icon(icon)):
            QMessageBox.Critical(self, "Key Error", mess.PTH_NOT_EXSIST)
            sys.exit(1)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.pixmap = QPixmap(func.get_icon(icon))

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
        self.aspectRatioMode = app.keepARM
        self.setSizePolicy(app.SiPoMin, app.SiPoMin)
        self.resize(self.size[0], self.size[1])

# -------------------------------------------------------------------------------------------------------------
