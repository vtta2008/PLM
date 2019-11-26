# -*- coding: utf-8 -*-
"""

Script Name: GlobalSetting.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals


from PyQt5.QtCore                   import Qt
from bin.dependencies.damg.damg import DAMG
from appData                        import SiPoExp


class GlobalSetting(DAMG):

    key = 'GlobalSetting'
    Type = 'DAMG Global Setting'
    _name = 'Global Setting'

    def __init__(self, layouts):
        super(GlobalSetting, self).__init__(self)

        self.layouts = layouts
        self.globalSetting(self.layouts)

    def globalSetting(self, layouts):

        for layout in layouts:

            if layout.key == 'PipelineManager':
                # print('start applying individual setting to: {0}'.format(layout))
                layout.setFixedWidth(500)
                # print('{0} has been set fix width: 500'.format(layout.key))
                # layout.setWindowFlags(STAY_ON_TOP)
                # pass

            if layout.key == 'TobTab' and layout.key == 'BotTab':
                # print('start applying individual setting to: {0}'.format(layout))
                layout.setMovable(True)
                layout.setElideMode(Qt.ElideRight)
                layout.setUsesScrollButtons(True)
                # print('{0} has been set movable: True, ElideMode: right, use scroll okButton: True'.format(layout.key))
                pass
            try:
                # print('Try applying globalsetting content margin to: {0}'.format(layout))
                layout.setContentMargin(1, 1, 1, 1)
            except AttributeError:
                # print('Failed, {0} does not have contenmargin attribute'.format(layout))
                pass
            else:
                # print('{0} has been set content margin: 1,1,1,1'.format(layout.key))
                pass
            try:
                # print('Try applying globalsetting size policy to: {0}'.format(layout))
                layout.setSizePolicy(SiPoExp, SiPoExp)
            except AttributeError:
                # print('Failed, {0} does not have sizepolicy attribute'.format(layout))
                pass
            else:
                # print('{0} has been set size policy: SiPoExp, SiPoExp'.format(layout.key))
                pass

            try:
                # print('Try applying globalsetting spacing to: {0}'.format(layout))
                layout.setSpacing(2)
            except AttributeError:
                # print('Failed, {0} does not have spacing attribute'.format(layout))
                pass
            else:
                # print('{0} has been set spacing: 2'.format(layout.key))
                pass
        return layouts

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 8/11/2019 - 9:33 AM
# © 2017 - 2018 DAMGteam. All rights reserved