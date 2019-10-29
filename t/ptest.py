#!/usr/bin/env python

# Python
import sys

# PyQt5
from PyQt5.QtWidgets import QApplication, QStackedWidget, QWidget, QComboBox
from PyQt5.QtCore import pyqtProperty, pyqtSlot, pyqtSignal, QSize

# PLM
from appData            import __globalServer__, __localPort__, __localHost__
from uikits.Label import Label
# from uikits.ComboBox import ComboBox
from uikits.VBoxLayout import VBoxLayout
from uikits.Icon import AppIcon
from uikits.HBoxLayout import HBoxLayout
from uikits.MessageBox import MessageBox
from uikits.Button   import Button
from uikits.Widget   import Widget


class ServerConfigPage1(Widget):
    key = "ServerConfigPage1"
    name = "Local server"

    def __init__(self, parent=None):
        super(ServerConfigPage1, self).__init__(parent)

        self.setObjectName(self.key)
        self.setWindowTitle(self.name)

        self.ip = Label({'txt': __localHost__})
        self.port = Label({'txt': __localPort__})

        self.layout = VBoxLayout({'addWidget': [self.ip, self.port]})
        self.setLayout(self.layout)


class ServerConfigPage2(Widget):
    key = "ServerConfigPage2"
    name = "Online server"

    def __init__(self, parent=None):
        super(ServerConfigPage2, self).__init__(parent)

        self.setObjectName(self.key)
        self.setWindowTitle(self.name)

        self.url = Label({'txt': __globalServer__})

        self.layout = VBoxLayout({'addWidget': [self.url]})
        self.setLayout(self.layout)


class ServerConfig(Widget):

    currentIndexChanged = pyqtSignal(int)
    pageTitleChanged = pyqtSignal(str)
    sendToSetting = pyqtSignal(str, str, str)

    key = "ServerConfig"

    def __init__(self, settings, parent=None):
        super(ServerConfig, self).__init__(parent)

        self.setWindowTitle("Server Configuration")
        self.setWindowIcon(AppIcon(32, self.key))
        self.settings = settings

        self.comboBox = QComboBox({'setObjName': self.key})
        self.stackWidget = QStackedWidget()
        self.comboBox.activated.connect(self.setCurrentIndex)

        self.btnOk = Button({'txt': 'Config'})
        self.btnOk.clicked.connect(self.get_chose_option)
        self.btnQuit = Button({'txt': 'Quit'})
        self.btnQuit.clicked.connect(self.close)
        self.HboxLayout = HBoxLayout({'addWidget': [self.btnOk, self.btnQuit]})

        self.addPage(ServerConfigPage1())
        self.addPage(ServerConfigPage2())

        self.layout = VBoxLayout({'addWidget': [self.comboBox, self.stackWidget],'addLayout': [self.HboxLayout]})
        self.setLayout(self.layout)

    def get_chose_option(self):
        index = self.getCurrentIndex()
        widget = self.stackWidget.widget(index)
        print("widget index: {0} - widget name: {1}".format(index, widget.name))
        print("send to setting: ServerConfig, {0}, {1}".format(widget.name, None))
        self.sendToSetting.emit("ServerConfig", widget.name, None)
        self.settings.initSetValue("ServerConfig", widget.name, None)

    def sizeHint(self):
        return QSize(200, 150)

    @pyqtSlot(int)
    def setCurrentIndex(self, index):
        if index != self.getCurrentIndex():
            self.stackWidget.setCurrentIndex(index)
            self.comboBox.setCurrentIndex(index)
            self.currentIndexChanged.emit(index)

    def count(self):
        return self.stackWidget.count()

    def widget(self, index):
        return self.stackWidget.widget(index)

    @pyqtSlot(QWidget)
    def addPage(self, page):
        self.insertPage(self.count(), page)

    @pyqtSlot(int, QWidget)
    def insertPage(self, index, page):
        page.setParent(self.stackWidget)
        self.stackWidget.insertWidget(index, page)
        title = page.windowTitle()
        if title == "":
            title = "Page %d" % (self.comboBox.count() + 1)
            page.setWindowTitle(title)
        self.comboBox.insertItem(index, title)

    @pyqtSlot(int)
    def removePage(self, index):
        widget = self.stackWidget.widget(index)
        self.stackWidget.removeWidget(widget)
        self.comboBox.removeItem(index)

    def getPageTitle(self):
        cw = self.stackWidget.currentWidget()
        return cw.windowTitle() if cw is not None else ''

    @pyqtSlot(str)
    def setPageTitle(self, newTitle):
        cw = self.stackWidget.currentWidget()
        if cw is not None:
            self.comboBox.setItemText(self.getCurrentIndex(), newTitle)
            cw.setWindowTitle(newTitle)
            self.pageTitleChanged.emit(newTitle)

    def getCurrentIndex(self):
        return self.stackWidget.currentIndex()

    @pyqtSlot(int)
    def setCurrentIndex(self, index):
        if index != self.getCurrentIndex():
            self.stackWidget.setCurrentIndex(index)
            self.comboBox.setCurrentIndex(index)
            self.currentIndexChanged.emit(index)

    def closeEvent(self, QCloseEvent):
        messBox = MessageBox(self, 'Sure?', 'question', 'Are you sure?', 'yes_no')
        if messBox.Yes:
            self.close()
        else:
            pass

    pageTitle = pyqtProperty(str, fget=getPageTitle, fset=setPageTitle, stored=False)
    currentIndex = pyqtProperty(int, fget=getCurrentIndex, fset=setCurrentIndex)

if __name__ == '__main__':
    from PyQt5.QtCore import QSettings

    app = QApplication(sys.argv)
    widget = ServerConfig(QSettings)
    widget.addPage(ServerConfigPage1())
    widget.addPage(ServerConfigPage2())
    widget.show()
    sys.exit(app.exec_())