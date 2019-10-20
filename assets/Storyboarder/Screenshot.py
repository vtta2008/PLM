#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script Name: Screenshot.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script will create a new layout with image is desktop screenshot.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
from functools import partial

# PyQt5
from PyQt5.QtCore import Qt, QDir, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QGridLayout, QFileDialog, QApplication, QGroupBox, QSpinBox, QCheckBox,
                             QHBoxLayout, QLabel, QSizePolicy, )

from damgteam.core import keepARM
from ui.uikits.Button import Button
# PLM
from ui.uikits.UiPreset import IconPth


class Screenshot(QWidget):

    key = 'screenShot'
    showLayout = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(Screenshot, self).__init__(parent)
        self.setWindowIcon(IconPth(32, "Screenshot"))
        self.resize(960, 540)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

        self.shootScreen()
        self.delaySpinBox.setValue(5)

    def buildUI(self):
        self.screenshotLabel = QLabel()
        self.screenshotLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.screenshotLabel.setAlignment(Qt.AlignCenter)
        self.screenshotLabel.setMinimumSize(240, 160)
        self.createOptionsGroupBox()
        self.createButtonsLayout()

        self.layout.addWidget(self.screenshotLabel,0,0,9,16)
        self.layout.addWidget(self.optionsGroupBox,10,0,1,16)
        self.layout.addLayout(self.buttonsLayout, 11,0,1,16)

    def resizeEvent(self, event):
        scaledSize = self.originalPixmap.size()
        scaledSize.scale(self.screenshotLabel.size(), keepARM)
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

        optionsGroupBoxLayout = QGridLayout()
        optionsGroupBoxLayout.addWidget(self.delaySpinBoxLabel, 0, 0)
        optionsGroupBoxLayout.addWidget(self.delaySpinBox, 0, 1)
        optionsGroupBoxLayout.addWidget(self.hideThisWindowCheckBox, 1, 0, 1, 2)
        self.optionsGroupBox.setLayout(optionsGroupBoxLayout)

    def createButtonsLayout(self):
        self.newScreenshotButton = Button({'txt': "New Screenshot", 'cl': self.newScreenshot})
        self.saveScreenshotButton = Button({'txt': "Save Screenshot", 'cl': self.saveScreenshot})
        self.quitScreenshotButton = Button({'txt': "Quit", 'cl': partial(self.showLayout.emit, self.key, 'hide')})

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addStretch()
        self.buttonsLayout.addWidget(self.newScreenshotButton)
        self.buttonsLayout.addWidget(self.saveScreenshotButton)
        self.buttonsLayout.addWidget(self.quitScreenshotButton)

    def updateScreenshotLabel(self):
        self.screenshotLabel.setPixmap(self.originalPixmap.scaled(
                self.screenshotLabel.size(), Qt.KeepAspectRatio,
                Qt.SmoothTransformation))

    def hideEvent(self, event):
        # self.specs.showState.emit(False)
        pass

    def closeEvent(self, event):
        self.showLayout.emit(self.key, 'hide')
        event.ignore()

def main():
    app = QApplication(sys.argv)
    screenshot = Screenshot()
    screenshot.show()
    app.exec_()

if __name__ == '__main__':
    main()