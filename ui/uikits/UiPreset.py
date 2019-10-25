# -*- coding: utf-8 -*-
"""

Script Name: button.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python


# PyQt5
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QCheckBox, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage

# PLM
from appData import center, left, right, SiPoMin, SiPoPre, SiPoMax, SiPoExp, SiPoIgn, appIconCfg
from utils.utils import get_app_icon, get_logo_icon, get_avatar_icon, data_handler

PRS = dict( password = QLineEdit.Password,  center = center , left  = left   , right  = right, spmin = SiPoMin,
            spmax    = SiPoMax           ,  sppre  = SiPoPre, spexp = SiPoExp, spign  = SiPoIgn,  )

def check_preset(data):
    if data == {}:
        pass
    else:
        return True

class IconPth(QIcon):

    def __init__(self, size=32, name="AboutPlt"):
        super(IconPth, self).__init__()

        self._found = False
        self.iconSize = size
        self.iconName = name

        iconInfo = data_handler(filePath=appIconCfg)
        for icon in iconInfo.keys():
            if self.iconName == icon:
                self._found = True

        if self._found:
            self.iconPth = get_app_icon(self.iconSize, self.iconName)
            self.addFile(self.iconPth, QSize(self.iconSize, self.iconSize))
        else:
            # raise FileNotFoundError("Could not find icon name: {0}".format(self.iconName))
            print("FILENOTFOUNDERROR: {0}: Could not find icon name: {1}".format(__name__, self.iconName))

class AppIcon(QIcon):
    def __init__(self, name="Logo", parent=None):
        super(AppIcon, self).__init__(parent)
        sizes = [16, 24, 32, 48, 64, 96, 128, 256, 512]
        self.name =name
        for s in sizes:
            self.addFile(get_logo_icon(s, name), QSize(s, s))

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
                self.setPixmap(QPixmap.fromImage(QImage(get_avatar_icon(value))))
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
            if key == 'fn':
                self.setEchoMode(PRS[value])

    # def sizeHint(self):
    #     size = super(LineEdit, self).sizeHint()
    #     size.setHeight(size.height())
    #     size.setWidth(max(size.width(), size.height()))
    #     return size

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
            elif key == 'setObjName':
                self.setObjectName(value)

    def sizeHint(self):
        size = super(ComboBox, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class VBoxLayout(QVBoxLayout):

    def __init__(self, preset={}, parent=None):
        super(VBoxLayout, self).__init__(parent)
        self.preset = preset

        if check_preset(self.preset):
            self.procedural()

    def procedural(self):
        for key, value in self.preset.items():
            if key == 'addWidget':
                for widget in value:
                    self.addWidget(widget)
            elif key == 'addLayout':
                for layout in value:
                    self.addLayout(layout)
            elif key == 'addStretch':
                self.setStretch(value, 0)

    def sizeHint(self):
        size = super(VBoxLayout, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class HBoxLayout(QHBoxLayout):

    def __init__(self, preset={}, parent=None):
        super(HBoxLayout, self).__init__(parent)
        self.preset = preset

        if check_preset(self.preset):
            self.procedural()

    def procedural(self):
        for key, value in self.preset.items():
            if key == 'addWidget':
                for widget in value:
                    self.addWidget(widget)
            elif key == 'addLayout':
                for layout in value:
                    self.addLayout(layout)

    def sizeHint(self):
        size = super(HBoxLayout, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class Widget(QWidget):

    def __init__(self, preset={}, parent=None):
        super(Widget, self).__init__(parent)

        self.preset = preset

        if check_preset(self.preset):
            self.procedural()

    def procedural(self):
        for key, value in self.preset.items():
            if key == 'setLayout':
                for layout in value:
                    self.setLayout(layout)

    def sizeHint(self):
        size = super(Widget, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 6:05 AM
# © 2017 - 2018 DAMGteam. All rights reserved