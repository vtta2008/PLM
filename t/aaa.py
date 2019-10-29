# -*- coding: utf-8 -*-
"""

Script Name: aaa.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox, QApplication)

import sys

from ui.uikits.ComboBox import ComboBox

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.lbl = QLabel("Ubuntu", self)

        combo = ComboBox({'items': ['Ubuntu', 'Mandriva', 'Fedora', 'Arch', 'Gentoo']}, self)
        # combo = QComboBox(self)
        # combo.addItem("Ubuntu")
        # combo.addItem("Mandriva")
        # combo.addItem("Fedora")
        # combo.addItem("Arch")
        # combo.addItem("Gentoo")

        combo.move(50, 50)
        combo.show()
        self.lbl.move(50, 150)

        combo.activated[str].connect(self.onActivated)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QComboBox')
        self.show()

    def onActivated(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 30/10/2019 - 12:51 AM
# © 2017 - 2018 DAMGteam. All rights reserved