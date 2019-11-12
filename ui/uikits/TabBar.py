# -*- coding: utf-8 -*-
"""

Script Name: TabBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtWidgets                        import QTabBar
from PyQt5.QtCore                           import Qt

from appData                                import __copyright__, SETTING_FILEPTH, ST_FORMAT
from ui.SignalManager                       import SignalManager
from cores.Settings                         import Settings
from ui.uikits.Widget                       import Widget
from ui.uikits.GridLayout                   import GridLayout
from ui.uikits.TabWidget                    import TabWidget
from ui.uikits.Label                        import Label

class TabBar(QTabBar):

    Type                                    = 'DAMGUI'
    key                                     = 'TabBar'
    _name                                   = 'DAMG Tab Bar'
    _copyright                              = __copyright__

    def __init__(self, parent=None):
        QTabBar.__init__(self)

        self.parent = parent

        self.signals = SignalManager(self)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        self.values = dict(w = self.width(), h = self.height(), x = self.x(), y = self.y())

    def sizeHint(self):
        size = super(TabBar, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    def moveEvent(self, event):
        if self.settings._settingEnable:
            self.setValue('x', self.x())
            self.setValue('y', self.y())

    def resizeEvent(self, event):
        if self.settings._settingEnable:
            self.setValue('w', self.width())
            self.setValue('h', self.height())

    def closeEvent(self, event):
        if __name__ == '__main__':
            self.close()
        else:
            self.signals.emit('showLayout', self.key, 'hide')

    def hideEvent(self, event):
        if __name__ == '__main__':
            self.hide()
        else:
            if self.settings._settingEnable:
                for key, value in self.values.items():
                    self.setValue(key, value)
            self.signals.emit('showLayout', self.key, 'hide')

    def showEvent(self, event):

        if self.settings._settingEnable:
            w = self.getValue('w')
            h = self.getValue('h')
            x = self.getValue('x')
            y = self.getValue('x')

            vals = [w, h, x, y]

            for i in range(len(vals)):
                if vals[i] is None:
                    key = [k for k in self.values.keys()]
                    value = self.values[key[i]]
                    for index, element in enumerate(vals):
                        if element == vals[i]:
                            vals[index] = value
                    self.setValue(key[i], self.values[key[i]])

            for v in vals:
                if not type(v) in [int]:
                    v = int(v)

            self.resize(vals[0], vals[1])
            self.move(vals[2], vals[3])

        if __name__ == '__main__':
            self.show()
        else:
            self.signals.emit('showLayout', self.key, 'show')

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


class TabContent(Widget):
    key = 'TabContent'

    def __init__(self, layout=None, parent=None):
        super(TabContent, self).__init__(parent)

        if layout is None:
            layout = GridLayout()
            layout.addWidget(Label())

        self.layout = layout
        self.setLayout(self.layout)


class Tabs(Widget):
    key = 'Tabs'

    def __init__(self, parent=None):
        super(Tabs, self).__init__(parent)
        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.tabs = TabWidget()
        tabBar = TabBar()
        self.tabs.setTabBar(tabBar)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setUsesScrollButtons(True)

        content = TabContent()
        tabBar.addAction(content)

        self.layout.addWidget(self.tabs)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 4:39 PM
# © 2017 - 2018 DAMGteam. All rights reserved