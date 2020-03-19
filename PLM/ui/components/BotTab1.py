# -*- coding: utf-8 -*-
"""

Script Name: BotTab1.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PLM.commons.Widgets    import Widget, GridLayout, CheckBox
from PLM.commons            import DAMGDICT, DAMGLIST
from PLM.utils              import str2bool

class BotTab1(Widget):

    key = 'BotTab1'
    checkboxes = DAMGDICT()
    cbs = DAMGLIST()

    def __init__(self, parent=None):
        super(BotTab1, self).__init__(parent)

        self.parent                         = parent
        self.layout                         = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.recieveSignalCB                = CheckBox('Recieve')
        self.blockSignalCB                  = CheckBox('Block')
        self.commandCB                      = CheckBox('Command')
        self.registLayoutCB                 = CheckBox('Register')
        self.allTrackingCB                  = CheckBox('All')

        self.allTrackingCB.stateChanged.connect(self.changeAllCB)

        x = 0
        y = 0
        w = 1
        h = 1

        for cb in [self.recieveSignalCB, self.blockSignalCB, self.commandCB, self.registLayoutCB, self.allTrackingCB]:
            cb.key = '{0}_{1}_CheckBox_{2}'.format(self.parent.key, self.key, cb.text())
            cb._name = '{0} {1} Check Box: {2}'.format(self.parent.key, self.key, cb.text())
            cb.settings._settingEnable = True
            state = cb.getValue('checkState')

            if state is None:
                state = False

            cb.setValue('checkState', state)
            cb.setChecked(str2bool(state))
            self.checkboxes.add(cb.key, cb)
            self.cbs.append(cb)

            self.layout.addWidget(cb, x, y, w, h)
            y += 1
            if y == 4:
                x += 1
                y = 0

    def set_tooltip(self):

        self.recieveSignalCB.setToolTip('Tracking Signal recieved')
        self.blockSignalCB.setToolTip('Tracking Signal is blocked')
        self.commandCB.setToolTip('Tracking Command working')
        self.registLayoutCB.setToolTip('Tracking layout is registed')

    def changeAllCB(self, bool):
        for cb in self.cbs:
            cb.setChecked(bool)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 11/11/2019 - 12:19 PM
# © 2017 - 2018 DAMGteam. All rights reserved