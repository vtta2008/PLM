# -*- coding: utf-8 -*-
"""

Script Name: ToolBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import json
from functools                              import partial
from damg                                   import DAMGLIST

# PyQt5
from PyQt5.QtWidgets                        import QToolBar, QAction

# PLM
from appData                                import SETTING_FILEPTH, ST_FORMAT, __copyright__, mainConfig, ACTIONS_DATA
from ui.uikits.Action                       import Action
from cores.SignalManager                    import SignalManager
from cores.Settings                         import Settings

# -------------------------------------------------------------------------------------------------------------
""" Tool bar class """

class ToolBar(QToolBar):

    Type                                    = 'DAMGUI'
    key                                     = 'ToolBar'
    _name                                   = 'DAMG Tool Bar'
    _copyright                              = __copyright__
    actionData                              = ACTIONS_DATA
    regisActions                            = DAMGLIST()

    with open(mainConfig, 'r') as f:
        appInfo = json.load(f)

    def __init__(self, configKey=None, actions=[], parent=None):
        QToolBar.__init__(self)

        self.parent             = parent
        self.signals            = SignalManager(self)
        self.settings           = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.configKey          = configKey
        self.actions            = actions

        if self.configKey is None or self.configKey == '':
            if self.actions is None or self.actions == []:
                print('CREATEACTIONERROR: Empty key: {0}, {1}'.format(self.configKey, self.actions))
            else:
                self.add_multiple_actions(self.actions)
        else:
            self.add_actions_by_key(self.configKey)

        self.setAccessibleName(self.configKey)
        self.setMinimumWidth((len(self.acts) + 1) * 32)

    def add_multiple_actions(self, actions=[]):
        for key in actions:
            if type(key) == 'str':
                self.addAction(self.create_action(key))
            elif type(key) == type(QAction) or type(key) == type(Action):
                self.regisActions.append(key)
                self.addAction(key)
            else:
                print("DATATYPEERROR: Could not add action: {0}".format(key))

    def create_action(self, key):
        if key in self.appInfo.keys():
            action = Action({

                                'icon': key,
                                'stt': self.appInfo[key][0],
                                'txt': key,
                                'trg': (partial(self.executing.emit, self.appInfo[key][2]))

                            }, self)

            self.regisActions.append(action)
            return action
        else:
            print("KEYACTIONERROR: Could not find key in main config: {0}".format(key))

    def add_actions_by_key(self, key):
        if key in self.actionData.keys():
            apps = self.actionData[key]
            for app in apps:
                self.create_action(app)
        else:
            print("CONFIGKEYERROR: This key is not configed yet: {0}".format(key))

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.configKey)

    def getValue(self, key):
        return self.settings.initValue(key, self.configKey)

    def showEvent(self, event):
        sizeX = self.getValue('width')
        sizeY = self.getValue('height')

        if not sizeX is None and not sizeY is None:
            self.resize(int(sizeX), int(sizeY))

        posX = self.getValue('posX')
        posY = self.getValue('posY')

        if not posX is None and not posX is None:
            self.move(posX, posY)

        if __name__ == '__main__':
            self.show()
        else:
            self.signals.showLayout.emit(self.key, 'show')
            event.ignore()

    def moveEvent(self, event):
        self.setValue('posX', self.x())
        self.setValue('posY', self.y())

    def resizeEvent(self, event):
        self.setValue('width', self.frameGeometry().width())
        self.setValue('height', self.frameGeometry().height())

    def sizeHint(self):
        size = super(ToolBar, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

    def closeEvent(self, event):
        if __name__=='__main__':
            self.close()
        else:
            self.signals.showLayout.emit(self.configKey, 'hide')
            event.ignore()

    def hideEvent(self, event):
        if __name__=='__main__':
            self.hide()
        else:
            self.signals.showLayout.emit(self.configKey, 'hide')
            event.ignore()

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 31/07/2018 - 12:50 AM
# © 2017 - 2018 DAMGteam. All rights reserved