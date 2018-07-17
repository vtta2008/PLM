# -*- coding: utf-8 -*-
"""

Script Name: button.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from functools import partial

from PyQt5.QtWidgets import QPushButton, QLabel, QGroupBox, QGridLayout, QLineEdit, QComboBox, QCheckBox, QAction, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage

from utilities.utils import getAppIcon, getLogo, getAvatar
from appData import center, left, right, SiPoMin, SiPoPre, SiPoMax, SiPoExp, SiPoIgn

PRS = dict(
    password = QLineEdit.Password,
    center = center, left = left, right = right,
    spmin = SiPoMin, spmax = SiPoMax, sppre = SiPoPre, spexp = SiPoExp, spign = SiPoIgn
)

def check_preset(data):
    if data == {}:
        pass
    else:
        return True

class IconPth(QIcon):
    def __init__(self, size=32, name="AboutPlt"):
        super(IconPth, self).__init__()
        self.iconPth = getAppIcon(size, name)
        self.addFile(self.iconPth, QSize(32, 32))

class AppIcon(QIcon):
    def __init__(self, name="Logo", parent=None):
        super(AppIcon, self).__init__(parent)
        sizes = [16, 24, 32, 48, 64, 96, 128, 256, 512]
        self.name =name
        for s in sizes:
            self.addFile(getLogo(s, name), QSize(s, s))

class Label(QLabel):

    def __init__(self, preset={}, parent=None):
        super(Label, self).__init__(parent)
        self.preset = preset
        if check_preset(self.preset):
            self.precedural()

    def precedural(self):
        for key, value in self.preset.items():
            if key == 'txt':
                self.setText(value)
            elif key == 'fnt':
                self.setFont(QFont(value))
            elif key == 'alg':
                self.setAlignment(PRS[value])
            elif key == 'wmin':
                self.setMinimumWidth(value)
            elif key == 'hmin':
                self.setMinimumHeight(value)
            elif key == 'smin':
                self.setMinimumSize(value[0], value[1])
            elif key == 'sizePolicy':
                self.setSizePolicy(PRS[value])
            elif key == 'pxm':
                self.setPixmap(QPixmap.fromImage(QImage(getAvatar(value))))
            elif key == 'scc':
                self.setScaledContents(value)
            elif key == 'sfs':
                self.setFixedSize(value[0], value[1])
            elif key == 'setBuddy':
                self.setBuddy(value)
            elif key == 'link':
                self.setOpenExternalLinks(value)
            else:
                self.setAlignment(center)

    def sizeHint(self):
        size = super(Label, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class LineEdit(QLineEdit):

    def __init__(self, preset={}, parent=None):
        super(LineEdit, self).__init__(parent)
        self.preset = preset
        if check_preset(self.preset):
            self.precedural()

    def precedural(self):
        for key, value in self.preset.items():
            if key == 'mode':
                self.setEchoMode(PRS[value])

    def sizeHint(self):
        size = super(LineEdit, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class Button(QPushButton):

    def __init__(self, preset={}, parent=None):
        super(Button, self).__init__(parent)
        self.preset = preset
        if check_preset(self.preset):
            self.procedural()

    def procedural(self):
        for key, value in self.preset.items():
            if key == 'txt':
                self.setText(value)
            elif key == 'tt':
                self.setToolTip(value)
            elif key == 'cl':
                self.clicked.connect(value)
            elif key == 'emit1':
                self.clicked.connect(partial(value[0], value[1]))
            elif key == 'emit2':
                self.clicked.connect(partial(value[0], value[1][0], value[1][1]))
            elif key == 'icon':
                self.setIcon(IconPth(32, value))
            elif key == 'fix':
                self.setFixedSize(value)
            elif key == 'ics':
                self.setIconSize(value)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class CheckBox(QCheckBox):

    def __init__(self, preset={}, parent=None):
        super(CheckBox, self).__init__(parent)
        self.preset = preset
        if check_preset(self.preset):
            self.procedural()

    def procedural(self):
        for key, value in self.preset.items():
            if key == 'txt':
                self.setText(value)

    def sizeHint(self):
        size = super(CheckBox, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class Action(QAction):

    def __init__(self, preset={}, parent=None):
        super(Action, self).__init__(parent)
        self.preset = preset
        if check_preset(self.preset):
            self.procedural()

    def procedural(self):
        for key, value in self.preset.items():
            if key == 'icon':
                self.setIcon(IconPth(32, value))
            elif key == 'txt':
                self.setText(value)
            elif key == 'trg':
                self.triggered.connect(value)
            elif key == 'shortcut':
                self.setShortcut(value)
            elif key == 'checkable':
                self.setChecked(value)
            elif key == 'enabled':
                self.setDisabled(value)

class ComboBox(QComboBox):

    def __init__(self, preset={}, parent=None):
        super(ComboBox, self).__init__(parent)
        self.preset = preset
        if check_preset(self.preset):
            self.procedural()

    def procedural(self):
        for key, value in self.preset.items():
            if key == 'items':
                for item in value:
                    self.addItem(item)
            elif key == 'editable':
                self.setEditable(value)
            elif key == 'curIndex':
                self.setCurrentIndex(value)


    def sizeHint(self):
        size = super(ComboBox, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class AutoPreset1(QGridLayout):

    def __init__(self, btns=[], parent=None):
        super(AutoPreset1, self).__init__(parent)
        self.btns = btns
        self.buildUI()

    def buildUI(self):
        if not len(self.btns) == 0:
            for i in range(len(self.btns)):
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
                i += 1

    def sizeHint(self):
        size = super(AutoPreset1, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class AutoPreset2(QGridLayout):

    def __init__(self, btns=[], parent=None):
        super(AutoPreset2, self).__init__(parent)
        self.btns = btns
        self.buildUI()

    def buildUI(self):
        if not len(self.btns) == 0:
            for i in range(len(self.btns)):
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
                i += 1

    def sizeHint(self):
        size = super(AutoPreset2, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class AutoPreset3(QGridLayout):

    def __init__(self, imageView, parent=None):
        super(AutoPreset3, self).__init__(parent)
        self.img = imageView
        self.buildUI()

    def buildUI(self):
        if self.img:
            self.addWidget(self.img, 0, 0, 1, 1)

    def sizeHint(self):
        size = super(AutoPreset3, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class GroupBox(QGroupBox):

    def __init__(self, title="Section Title", btns=[], mode="IconGrid", parent=None):
        super(GroupBox, self).__init__(parent)
        self.setTitle(title)
        self.btns = btns
        self.mode = mode

        self.buildUI()

    def buildUI(self):
        if self.mode == "IconGrid":
            self.setLayout(AutoPreset1(self.btns))
        elif self.mode == "BtnGrid":
            self.setLayout(AutoPreset2(self.btns))
        elif self.mode == "ImageView":
            self.setLayout(AutoPreset3(self.btns[0]))

def GroupGrid(txt=None):
    if txt is None:
        grp = QGroupBox()
    else:
        grp = QGroupBox(txt)

    grid = QGridLayout()
    grp.setLayout(grid)
    return grp, grid

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 6:05 AM
# © 2017 - 2018 DAMGteam. All rights reserved