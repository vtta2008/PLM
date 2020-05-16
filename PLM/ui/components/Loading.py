# -*- coding: utf-8 -*-
"""

Script Name: Loading.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

from PLM.ui.framework.Widgets import MessageBox, ProgressBar
from PLM.configs                        import ERROR_LAYOUT_COMPONENT
from PLM.cores                          import StyleSheet



class LoadingBar(ProgressBar):

    key                                 = 'ProgressUI'
    _name                               = 'DAMG Progress UI'

    def __init__(self, parent=None):
        super(LoadingBar, self).__init__(parent)

        self.parent                     = parent

        if not self.parent:
            MessageBox(self, 'Loading Layout Component', 'critical', ERROR_LAYOUT_COMPONENT)
            sys.exit()
        else:
            self.num                    = self.parent.num
            self.pix                    = self.parent.splashPix
            self.setMinimum(0)
            self.setMaximum(100)

            self.setGeometry((self.pix.width()-self.width())/2 + 115, self.pix.height() - 115, self.pix.width()/10, 10)
            self.setTextVisible(False)
            self.setStyleSheet(StyleSheet.progressBar())



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/25/2020 - 7:27 PM
# © 2017 - 2019 DAMGteam. All rights reserved