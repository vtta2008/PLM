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

    def sizeHint(self):
        size = super(DockWidget, self).sizeHint()
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
        if __name__=='__main__':
            self.close()
        else:
            self.signals.emit('showLayout', self.key, 'hide')

    def hideEvent(self, event):
        if __name__=='__main__':
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

            if w is None:
                w = self.width()
            if h is None:
                h = self.height()
            if x is None:
                x = 0
            if y is None:
                y = 0
            self.resize(int(w), int(h))
            self.move(int(x), int(h))

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