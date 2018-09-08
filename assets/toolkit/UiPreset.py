# -*- coding: utf-8 -*-
"""

Script Name: button.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
# PyQt5
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QCheckBox

from app import center, left, right, SiPoMin, SiPoPre, SiPoMax, SiPoExp, SiPoIgn
# PLM
from dock.utils import get_app_icon, get_logo_icon, get_avatar_icon

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

        self.iconPth = get_app_icon(size, name)
        self.addFile(self.iconPth, QSize(32, 32))

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
            if key == 'fm':
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


    def sizeHint(self):
        size = super(ComboBox, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 6:05 AM
# © 2017 - 2018 DAMGteam. All rights reserved