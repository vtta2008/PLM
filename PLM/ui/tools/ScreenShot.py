#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script Name: Screenshot.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script will create a showLayout_new layout with image is desktop screenshot.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

# PyQt5
from PySide2.QtCore               import QDir, QTimer
from PySide2.QtGui                import QPixmap
from PySide2.QtWidgets            import (QFileDialog, QApplication, QGroupBox, QSpinBox, QCheckBox, QLabel)

# PLM
from PLM.options import ASPEC_RATIO, SMOOTH_TRANS
from bin.Widgets import GridLayout, Button, Label, Widget, HBoxLayout
from bin.Gui import AppIcon

class ScreenShot(Widget):

    key = 'ScreenShot'

    def __init__(self, parent=None):
        super(ScreenShot, self).__init__(parent)
        self.setWindowIcon(AppIcon(32, "ScreenShot"))
        self.resize(960, 540)

        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

        self.shootScreen()
        self.delaySpinBox.setValue(5)

    def buildUI(self):
        self.screenshotLabel = Label({'alg': 'center', 'sizePolicy': ['expanding', 'expanding'], 'smin': [240, 160]})
        self.createOptionsGroupBox()
        self.createButtonsLayout()

        self.layout.addWidget(self.screenshotLabel,0,0,9,16)
        self.layout.addWidget(self.optionsGroupBox,10,0,1,16)
        self.layout.addLayout(self.buttonsLayout, 11,0,1,16)

    def resizeEvent(self, event):
        scaledSize = self.originalPixmap.size()
        scaledSize.scale(self.screenshotLabel.size(), ASPEC_RATIO)
        if not self.screenshotLabel.pixmap() or scaledSize != self.screenshotLabel.pixmap().size():
            self.updateScreenshotLabel()

    def newScreenshot(self):
        if self.hideThisWindowCheckBox.isChecked():
            self.hide()

        self.newScreenshotButton.setDisabled(True)

        QTimer.singleShot(self.delaySpinBox.value() * 1000,
                self.shootScreen)

    def saveScreenshot(self):
        format = 'png'
        initialPath = QDir.currentPath() + "/untitled." + format

        fileName, _ = QFileDialog.getSaveFileName(self, "Save As", initialPath, "%s Files (*.%s);;All Files (*)" % (format.upper(), format))

        if fileName:
            self.originalPixmap.save(fileName, format)

    def shootScreen(self):
        if self.delaySpinBox.value() != 0:
            QApplication.instance().beep()

        screen = QApplication.primaryScreen()
        if screen is not None:
            self.originalPixmap = screen.grabWindow(0)
        else:
            self.originalPixmap = QPixmap()

        self.updateScreenshotLabel()

        self.newScreenshotButton.setDisabled(False)
        if self.hideThisWindowCheckBox.isChecked():
            self.show()

    def updateCheckBox(self):
        if self.delaySpinBox.value() == 0:
            self.hideThisWindowCheckBox.setDisabled(True)
        else:
            self.hideThisWindowCheckBox.setDisabled(False)

    def createOptionsGroupBox(self):
        self.optionsGroupBox = QGroupBox("Options")

        self.delaySpinBox = QSpinBox()
        self.delaySpinBox.setSuffix(" s")
        self.delaySpinBox.setMaximum(60)
        self.delaySpinBox.valueChanged.connect(self.updateCheckBox)

        self.delaySpinBoxLabel = QLabel("Screenshot Delay:")

        self.hideThisWindowCheckBox = QCheckBox("Hide This Window")

        optionsGroupBoxLayout = GridLayout()
        optionsGroupBoxLayout.addWidget(self.delaySpinBoxLabel, 0, 0)
        optionsGroupBoxLayout.addWidget(self.delaySpinBox, 0, 1)
        optionsGroupBoxLayout.addWidget(self.hideThisWindowCheckBox, 1, 0, 1, 2)
        self.optionsGroupBox.setLayout(optionsGroupBoxLayout)

    def createButtonsLayout(self):
        self.newScreenshotButton = Button({'txt': "New Screenshot", 'cl': self.newScreenshot})
        self.saveScreenshotButton = Button({'txt': "Save Screenshot", 'cl': self.saveScreenshot})
        self.quitScreenshotButton = Button({'txt': "Quit", 'cl': self.close})
        self.buttonsLayout = HBoxLayout({'addWidget': [self.newScreenshotButton, self.saveScreenshotButton, self.quitScreenshotButton]})
        self.buttonsLayout.addStretch()

    def updateScreenshotLabel(self):
        self.screenshotLabel.setPixmap(self.originalPixmap.scaled(self.screenshotLabel.size(), ASPEC_RATIO, SMOOTH_TRANS))


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 11:31 AM
# © 2017 - 2018 DAMGTEAM. All rights reserved