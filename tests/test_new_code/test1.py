# -*- coding: utf-8 -*-
"""

Script Name: test1.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from PyQt5.QtGui import QFontDatabase, QFont, QFontMetrics, QFontInfo, QRawFont
from PyQt5.QtWidgets import QApplication
import sys





app = QApplication(sys.argv)
dataFont = QFontDatabase()
for family in dataFont.families():
    print(family)
    for style in dataFont.styles(family):
        print(style)



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/13/2020 - 1:54 AM
# © 2017 - 2019 DAMGteam. All rights reserved