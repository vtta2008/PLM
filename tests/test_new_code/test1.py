# -*- coding: utf-8 -*-
"""

Script Name: test1.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QDockWidget, QListWidget)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)

        dockWidget = QDockWidget('Dock', self)

        self.textEdit = QTextEdit()
        self.textEdit.setFontPointSize(16)

        self.listWidget = QListWidget()
        self.listWidget.addItem('Google')
        self.listWidget.addItem('Facebook')
        self.listWidget.addItem('Microsoft')
        self.listWidget.addItem('Apple')
        self.listWidget.itemDoubleClicked.connect(self.get_list_item)

        dockWidget.setWidget(self.listWidget)
        dockWidget.setFloating(False)

        self.setCentralWidget(self.textEdit)
        self.addDockWidget(Qt.RightDockWidgetArea, dockWidget)

    def get_list_item(self):
        self.textEdit.setPlainText(self.listWidget.currentItem().text())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/13/2020 - 1:54 AM
# © 2017 - 2019 DAMGteam. All rights reserved