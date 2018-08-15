# -*- coding: utf-8 -*-
"""

Script Name: testplm.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QApplication

import sys


class widget(QWidget):

    def __init__(self):
        super(widget, self).__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.cb = QCheckBox('test cb')
        self.cb.setChecked(True)
        self.layout.addWidget(self.cb)




app = QApplication(sys.argv)
win = widget()
win.show()
app.exec_()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 21/07/2018 - 12:23 AM
# © 2017 - 2018 DAMGteam. All rights reserved