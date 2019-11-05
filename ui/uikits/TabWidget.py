# -*- coding: utf-8 -*-
"""

Script Name: TabBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtWidgets                        import QTabWidget
from PyQt5.QtCore                           import Qt

# PLM
from appData                                import SETTING_FILEPTH, ST_FORMAT, __copyright__
from cores.SignalManager                    import LayoutSignals
from cores.Settings                         import Settings
from ui.uikits.Widget                       import Widget
from ui.uikits.GridLayout                   import GridLayout
from ui.uikits.Label                        import Label
from ui.uikits.TabBar                       import TabBar


class TabWidget(QTabWidget):

    Type                                    = 'DAMGUI'
    key                                     = 'TabWidget'
    _name                                   = 'DAMG Tab Widget'
    _copyright                              = __copyright__

    def __init__(self, parent=None):
        QTabWidget.__init__(self)

        self.parent = parent

        self.signals = LayoutSignals(self)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        self.setTabPosition(self.North)
        self.setMovable(True)

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    def getCurrentTab(self):
        return self.tabLst[self.currentIndex()]

    def getCurrentKey(self):
        return self.getCurrentTab().key

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
            try:
                key = self.getValue('currentTab')
            except None:
                key = self.key
            self.signals.showLayout.emit(key, 'show')

    def sizeHint(self):
        size = super(TabWidget, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

    def moveEvent(self, event):
        self.setValue('posX', self.x())
        self.setValue('posY', self.y())

    def resizeEvent(self, event):
        self.setValue('width', self.frameGeometry().width())
        self.setValue('height', self.frameGeometry().height())

    def closeEvent(self, event):
        if __name__ == '__main__':
            self.close()
        else:
            self.signals.showLayout.emit(self.key, 'hide')
            event.ignore()

    def hideEvent(self, event):
        if __name__ == '__main__':
            self.hide()
        else:
            self.signals.showLayout.emit(self.key, 'hide')
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
        self.tabs.setTabBar(TabBar())
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setUsesScrollButtons(True)

        self.layout.addWidget(self.tabs)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 4:39 PM
# © 2017 - 2018 DAMGteam. All rights reserved