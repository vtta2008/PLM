#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: uirc.py
Author: Do Trinh/Jimmy - 3D artist.
Description: This script is the place for every ui elements

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
print("Import from modules: {file}".format(file=__name__))
print("Directory: {path}".format(path=__file__.split(__name__)[0]))
__root__ = "PLT_RT"
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, os

# PyQt5
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QSettings
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QFrame, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QSizePolicy, QSlider,
                             QLineEdit, )

# Plt
from utilities import variables as var

# -------------------------------------------------------------------------------------------------------------
""" Varialbes """

# String
TXT = "plt" # String by default

# Value, Nummber, Float, Int ...
UNIT = 60   # Base Unit
MARG = 5    # Content margin
BUFF = 10   # Buffer size
SCAL = 1    # Scale value
STEP = 1    # Step value changing
VAL = 1     # Default value
MIN = 0     # Minimum value
MAX = 1000  # Maximum value
WMIN = 50   # Minimum width
HMIN = 20   # Minimum height

# Alignment
ALGC = Qt.AlignCenter
ALGR = Qt.AlignRight
ALGL = Qt.AlignLeft
HORZ = Qt.Horizontal
VERT = Qt.Vertical

# Style
frameStyle = QFrame.Sunken | QFrame.Panel

# Data set
DATASET = [UNIT, MARG, BUFF, SCAL, STEP, VAL, MIN, MAX, WMIN, HMIN, ALGC, HORZ]   # SliderTemplate

# Path

# -------------------------------------------------------------------------------------------------------------
""" QLabel """

class tpLabel(QLabel):

    def __init__(self, dataSet=DATASET, parent=None):
        super(tpLabel, self).__init__(parent)
        self.text = dataSet[0]
        self.wmin = dataSet[1]
        self.hmin = dataSet[2]
        self.align = dataSet[3]
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

    def loadSettings(self):
        self.setText(self.text)
        self.setMinimumWidth(self.lbW)
        self.setMinimumHeight(self.hmin)
        self.setAlignment(self.align)

class tpSlider(QSlider):

    def __init__(self, dataSet=DATASET, parent=None):
        super(tpSlider, self).__init__(parent)

        self.set
        self.setMinimum()
        self.setMaximum()
        self.setSingleStep()
        self.setValue()


# -------------------------------------------------------------------------------------------------------------
""" A spacer line to be able to add between layouts """

class QSpacer(QWidget):

    def __init__(self, lineW=MARG, parent=None):
        super(QSpacer, self).__init__(parent)
        self.lineW = lineW
        self.layout = QVBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.show()

    def buildUI(self):
        Separador = QFrame()
        Separador.setFrameShape(QFrame.HLine)
        Separador.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        Separador.setLineWidth(self.lineW)
        self.layout.addWidget(Separador)

# -------------------------------------------------------------------------------------------------------------
""" Layout template """

class SliderTemplate(QWidget):

    valueChangeSig = pyqtSignal(float)

    def __init__(self, setData=SLIDER_DS, parent=None):
        super(SliderTemplate, self).__init__(parent)

        self.txt = setData[0]
        self.min = setData[1]
        self.max = setData[2]
        self.step = setData[3]
        self.val = setData[4]

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.label = tpLabel(text=self.txt + ": ")

        self.slider = tpSlider()
        self.slider.setMinimum(int(self.min))
        self.slider.setMaximum(int(self.max))
        self.slider.setSingleStep(int(self.step))
        self.slider.setValue(int(self.val))

        self.numField = QLineEdit()
        self.numField.setValidator(QIntValidator(0, 999, self))
        self.numField.setText("0")
        self.numField.setFixedSize(30,20)
        self.numField.setText(str(self.val))

        self.slider.valueChanged.connect(self.set_value)
        self.numField.textChanged.connect(self.set_slider)

        self.layout.addWidget(self.label, 0, 0, 1, 1)
        self.layout.addWidget(self.numField, 0, 1, 1, 1)
        self.layout.addWidget(self.slider, 0, 2, 1, 1)

    def set_value(self):
        val = self.slider.value()
        self.numField.setText(str(val))

    def set_slider(self):
        val = self.numField.text()
        if val == "" or val == None:
            val = "0"
        self.slider.setValue(float(val))

    def changeEvent(self, event):
        self.settings.setValue("{name}Value".format(name=self.txt), float)
        self.valueChangeSig.emit(self.slider.value())

# -------------------------------------------------------------------------------------------------------------
""" Unit setting Layout """

class UnitSettingLayout(QWidget):

    stepChangeSig = pyqtSignal(float)
    valueChangeSig = pyqtSignal(float)
    minChangeSig = pyqtSignal(float)
    maxChangeSig = pyqtSignal(float)

    def __init__(self, parent=None):
        super(UnitSettingLayout, self).__init__(parent)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.stepVal = QLineEdit("1")
        self.valueVal = QLineEdit("1")
        self.minVal = QLineEdit("0")
        self.maxVal = QLineEdit("1000")

        self.stepVal.setValidator(QIntValidator(0, 999, self))
        self.valueVal.setValidator(QIntValidator(0, 999, self))
        self.minVal.setValidator(QIntValidator(0, 999, self))
        self.maxVal.setValidator(QIntValidator(0, 999, self))

        self.stepVal.textChanged.connect(self.set_step)
        self.valueVal.textChanged.connect(self.set_value)
        self.minVal.textChanged.connect(self.set_min)
        self.maxVal.textChanged.connect(self.set_max)

        self.layout.addWidget(Clabel("STEP: "), 0,0,1,1)
        self.layout.addWidget(Clabel("VALUE: "), 1,0,1,1)
        self.layout.addWidget(Clabel("MIN: "), 2,0,1,1)
        self.layout.addWidget(Clabel("MAX: "), 3,0,1,1)

        self.layout.addWidget(self.stepVal, 0, 1, 1, 1)
        self.layout.addWidget(self.valueVal, 1, 1, 1, 1)
        self.layout.addWidget(self.minVal, 2, 1, 1, 1)
        self.layout.addWidget(self.maxVal, 3, 1, 1, 1)

    def set_step(self):
        val = float(self.stepVal.text())
        self.stepChangeSig.emit(val)
        self.settings.setValue("stepSetting", float)

    def set_value(self):
        val = float(self.valueVal.text())
        self.valueChangeSig.emit(float(val))
        self.settings.setValue("valueSetting", float)

    def set_min(self):
        val = float(self.minVal.text())
        self.minChangeSig.emit(float(val))
        self.settings.setValue("minSetting", float)

    def set_max(self):
        val = float(self.maxVal.text())
        self.maxChangeSig.emit(float(val))
        self.settings.setValue("maxSetting", float)

    def changeEvent(self, event):
        pass