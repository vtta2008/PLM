# -*- coding: utf-8 -*-
"""

Script Name: ProgressUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import sys

from PLM.configs                        import ERROR_LAYOUT_COMPONENT
from PLM.cores                          import StyleSheet
from PLM.commons.Widgets                import MessageBox
from PLM.commons.Widgets.ProgressBar    import ProgressBar

class PotionLoading(ProgressBar):

    key                                 = 'ProgressUI'
    _name                               = 'DAMG Progress UI'

    def __init__(self, parent=None):
        super(PotionLoading, self).__init__(parent)

        self.parent                     = parent

        if not self.parent:
            MessageBox(self, 'Loading Layout Component', 'critical', ERROR_LAYOUT_COMPONENT)
            sys.exit()
        else:
            self.num                    = self.parent.num
            self.pix                    = self.parent.pix
            self.setMinimum(0)
            self.setMaximum(self.num*10)
            self.setGeometry(50, self.pix.height() - 50, self.pix.width() - 100, 20)
            self.setTextVisible(True)
            self.setStyleSheet(StyleSheet.progressBar())

    def start(self):
        self.show()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/20/2020 - 9:26 AM
# © 2017 - 2019 DAMGteam. All rights reserved