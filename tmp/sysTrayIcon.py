#! /usr/bin/env python

from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtGui import QIcon, QWheelEvent
from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QAction
import socket

from utilities import utils as func

UDP_IP = "192.168.1.1"
UDP_PORT = 20118

class RightClickMenu(QMenu):
    def __init__(self, parent=None):
        QMenu.__init__(self, "File", parent)

        icon = QIcon("system-shutdown")
        offAction = QAction(icon, "&Off", self)
        offAction.triggered.connect(lambda : sendudp("s53905\n"))
        self.addAction(offAction)

        icon = QIcon("view-statistics")
        fmAction = QAction(icon, "&FM", self)
        fmAction.triggered.connect(lambda : sendudp("s32113\n"))
        self.addAction(fmAction)

        icon = QIcon("view-split-left-right")
        pcAction = QAction(icon, "&PC", self)
        pcAction.triggered.connect(lambda : sendudp("s32401\n"))
        self.addAction(pcAction)

        icon = QIcon("text-speak")
        muteAction = QAction(icon, "&Mute", self)
        muteAction.triggered.connect(lambda : sendudp("s3641\n"))
        self.addAction(muteAction)

        icon = QIcon("go-up")
        volupAction = QAction(icon, "Vol &Up", self)
        volupAction.triggered.connect(lambda : sendudp("s51153\n"))
        self.addAction(volupAction)

        icon = QIcon("go-down")
        voldownAction = QAction(icon, "Vol &Down", self)
        voldownAction.triggered.connect(lambda : sendudp("s53201\n"))
        self.addAction(voldownAction)

        icon = QIcon("media-skip-forward")
        chupAction = QAction(icon, "Ch U&p", self)
        chupAction.triggered.connect(lambda : sendudp("s3150\n"))
        self.addAction(chupAction)

        icon = QIcon("media-skip-backward")
        chdownAction = QAction(icon, "Ch D&own", self)
        chdownAction.triggered.connect(lambda : sendudp("s32198\n"))
        self.addAction(chdownAction)

        icon = QIcon("application-exit")
        exitAction = QAction(icon, "&Exit", self)
        exitAction.triggered.connect(lambda : QApplication.exit(0))
        self.addAction(exitAction)

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QIcon(func.get_icon('Logo')))
        self.click_menu = RightClickMenu()
        self.setContextMenu(self.click_menu)

        self.activated.connect(self.onTrayIconActivated)

        class SystrayWheelEventObject(QObject):
            def eventFilter(self, object, event):
                if type(event)== QWheelEvent:
                    if event.delta() > 0:
                        sendudp("s51153\n")
                    else:
                        sendudp("s53201\n")
                    event.accept()
                    return True
                return False

        self.eventObj=SystrayWheelEventObject()
        self.installEventFilter(self.eventObj)

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            sendudp("s3641\n")

    def welcome(self):
        self.showMessage("Hello", "I should be aware of both buttons")

    def show(self):
        QSystemTrayIcon.show(self)
        QTimer.singleShot(100, self.welcome)

def sendudp(value):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.sendto(bytes(value, 'UTF-8'), (UDP_IP, UDP_PORT))

if __name__ == "__main__":
    app = QApplication([])
    tray = SystemTrayIcon()
    tray.show()
    app.exec_()