# -*- coding: utf-8 -*-
"""

Script Name: Widget.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __buildtins__ import __copyright__

""" Import """

# PyQt5
from PyQt5.QtGui                            import QTextTableFormat, QTextCharFormat
from PyQt5.QtWidgets                        import QTextEdit, QDockWidget

# PLM
from appData                                import right, datetTimeStamp, SETTING_FILEPTH, ST_FORMAT
from toolkits.Core                          import Settings, SignalManager

# -------------------------------------------------------------------------------------------------------------
""" Dock widget """

class NoteStamp(QTextTableFormat):
    def __init__(self):
        super(NoteStamp, self).__init__()
        self.setBorder(1)
        self.setCellPadding(4)
        self.setAlignment(right)

class DockStamp(QTextEdit):

    def __init__(self, parent=None):
        super(DockStamp, self).__init__(parent)

        self.buildStamp()

    def buildStamp(self):

        cursor                          = self.textCursor()
        frame                           = cursor.currentFrame()
        frameFormat                     = frame.frameFormat()
        frameFormat.setPadding(1)
        frame.setFrameFormat(frameFormat)

        cursor.insertTable(1, 1, NoteStamp())
        cursor.insertText(datetTimeStamp, QTextCharFormat())
        self.resize(250, 100)

class DockWidget(QDockWidget):

    Type                                    = 'DAMGUI'
    key                                     = 'DockWidget'
    _name                                   = 'DAMG Dock Widget'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        super(DockWidget, self).__init__(parent)

        self.parent                         = parent
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.signals = SignalManager(self)

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

        if __name__ == '__main__':
            self.setValue('showLayout', 'hide')
            self.hide()
        else:
            self.setValue('showLayout', 'hide')
            self.signals.emit('showLayout', self.key, 'hide')

    def showEvent(self, event):

        geometry = self.getValue('geometry', bytes('', 'utf-8'))
        if geometry is not None:
            self.restoreGeometry(geometry)

        if __name__ == '__main__':
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
# Created by panda on 18/07/2018 - 10:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved