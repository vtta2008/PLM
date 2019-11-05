# -*- coding: utf-8 -*-
"""

Script Name: QImageViewer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore import QDir, Qt, QSize
from PyQt5.QtGui import QImage, QPainter, QPalette, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,
        QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
import os

class ImageViewer(QMainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()

        self.myimage = QImage()
        self.filename = ""
        self.scaleFactor = 1.778 #0.56

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        mp = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setSizePolicy(mp)
        self.imageLabel.setScaledContents(True)
        self.setCentralWidget(self.imageLabel)

        self.setWindowTitle("Image Viewer")
        w = 400
        h = int(400 / self.scaleFactor)
        self.resize(w, h)
        self.move(0, 0)

    def resizeEvent(self, event):
        if not self.myimage.isNull():
           self.updateView()

    def updateView(self):
        if self.scaleFactor < 1:
            self.imageLabel.resize(self.height() * self.scaleFactor, self.height())
        else:
            self.imageLabel.resize(self.width(), (self.width() / self.scaleFactor))
        w = self.imageLabel.width()
        h = self.imageLabel.height()
        self.resize(w, h)

    def loadFile(self, fileName):
        if self.filename:
            self.myimage = QImage(self.filename)
            if self.myimage.isNull():
                QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % self.filename)
                return
            self.imageLabel.setPixmap(QPixmap.fromImage(self.myimage))
            self.scaleFactor = int(self.myimage.width()) / int(self.myimage.height())
            f = round(self.scaleFactor, 3)
            if self.scaleFactor < 1:
                self.resize(600 * self.scaleFactor, 600)
            else:
                self.resize(600, 600 / self.scaleFactor)
            self.setWindowTitle(os.path.splitext(str(self.filename))[0].split("/")[-1])


if __name__ == '__main__':

   import sys
   app = QApplication(sys.argv)
   imageViewer = ImageViewer()
   imageViewer.show()
   if len(sys.argv) > 1:
       print(sys.argv[1])
       imageViewer.filename = sys.argv[1]
       imageViewer.loadFile(imageViewer.filename)
   sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:13 AM
# © 2017 - 2018 DAMGteam. All rights reserved