# -*- coding: utf-8 -*-
"""

Script Name: GraphicView.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__
""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QGraphicsView

# PLM
from appData                                import SETTING_FILEPTH, ST_FORMAT
from cores.Settings                         import Settings
from cores.SignalManager                    import SignalManager


class GraphicView(QGraphicsView):

    Type                                    = 'DAMGGRAPHICVIEW'
    key                                     = 'GraphicView'
    _name                                   = 'DAMG Graphic View'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        super(GraphicView, self).__init__(parent)

        self.parent                         = parent
        self.settings                       = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.signals                        = SignalManager()

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    def closeEvent(self, event):
        if self.settings._settingEnable:
            geometry = self.saveGeometry()
            self.setValue('geometry', geometry)


        if __name__ == '__main__':
            self.setValue('showLayout', 'hide')
            self.hide()
        else:
            self.setValue('showLayout', 'hide')
            self.signals.emit('showLayout', self.key, 'hide')

    def hideEvent(self, event):
        if self.settings._settingEnable:
            geometry = self.saveGeometry()
            self.setValue('geometry', geometry)

        if __name__=='__main__':
            self.setValue('showLayout', 'hide')
            self.hide()
        else:
            self.setValue('showLayout', 'hide')
            self.signals.emit('showLayout', self.key, 'hide')

    def showEvent(self, event):

        geometry = self.getValue('geometry', bytes('', 'utf-8'))
        if geometry is not None:
            self.restoreGeometry(geometry)

        if __name__=='__main__':
            self.setValue('showLayout', 'show')
            self.show()
        else:
            self.setValue('showLayout', 'show')
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


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 1:11 AM
# © 2017 - 2018 DAMGteam. All rights reserved