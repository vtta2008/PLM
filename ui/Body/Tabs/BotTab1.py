# -*- coding: utf-8 -*-
"""

Script Name: BotTab1.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals


from ui.uikits.Widget import Widget

class BotTab1(Widget):

    key = 'BotTab1'

    def __init__(self, parent=None):
        super(BotTab1, self).__init__(parent)

        self.parent = parent

    # def eventFilter(self, source, event):
    #     if source in [self.parent]:
    #         if event in [QResizeEvent]:
    #             return True

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 11/11/2019 - 12:19 PM
# © 2017 - 2018 DAMGteam. All rights reserved