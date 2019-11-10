# -*- coding: utf-8 -*-
"""

Script Name: Widget.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtGui                        import QTextTableFormat, QTextCharFormat
from PyQt5.QtWidgets                    import QTextEdit, QDockWidget, QApplication

# PLM
from appData                            import right, datetTimeStamp, SETTING_FILEPTH, ST_FORMAT, __copyright__
from ui.SignalManager import SignalManager
from cores.Loggers                      import Loggers
from cores.Settings                     import Settings

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

        cursor              = self.textCursor()
        frame               = cursor.currentFrame()
        frameFormat         = frame.frameFormat()
        frameFormat.setPadding(1)
        frame.setFrameFormat(frameFormat)

        cursor.insertTable(1, 1, NoteStamp())
        cursor.insertText(datetTimeStamp, QTextCharFormat())
        self.resize(250, 100)


class DockWidget(QDockWidget):

    # self.content = DockStamp(self)
    # self.setWidget(self.content)
    # cursor = self.content.textCursor()
    # cursor.insertBlock()
    # cursor.insertText("Note info")

    Type                                    = 'DAMGUI'
    key                                     = 'DockWidget'
    _name                                   = 'DAMG Dock Widget'
    _copyright                              = __copyright__

    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.parent = parent
        self._name = self.__class__.__name__
        self.signals = SignalManager(self)
        self.logger = Loggers(self.__class__.__name__)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

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

    def moveEvent(self, event):
        self.setValue('posX', self.x())
        self.setValue('posY', self.y())

    def resizeEvent(self, event):
        self.setValue('width', self.frameGeometry().width())
        self.setValue('height', self.frameGeometry().height())

    def sizeHint(self):
        size = super(DockWidget, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

    def closeEvent(self, event):
        if __name__ == '__main__':
            self.close()
        else:
            self.signals.emit('showLayout', self.key, 'hide')
            event.ignore()

    def hideEvent(self, event):
        if __name__ == '__main__':
            self.hide()
        else:
            self.signals.emit('showLayout', self.key, 'hide')
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


def main():
    app = QApplication(sys.argv)
    layout = DockWidget()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 10:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved