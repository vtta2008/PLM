import random

from PyQt5.QtCore import QByteArray, QDataStream, QIODevice, QSettings
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
                             QMessageBox, QPushButton, QVBoxLayout)
from PyQt5.QtNetwork import (QHostAddress, QNetworkConfiguration,
                             QNetworkConfigurationManager, QNetworkInterface, QNetworkSession,
                             QTcpServer)


class Server(QDialog):
    FORTUNES = (
        "You've been leading a dog's life. Stay off the furniture.",
        "You've got to think about tomorrow.",
        "You will be surprised by a loud noise.",
        "You will feel hungry again in another hour.",
        "You might have mail.",
        "You cannot kill time without injuring eternity.",
        "Computers are not intelligent. They only think they are.")

    def __init__(self, parent=None):
        super(Server, self).__init__(parent)

        self.tcpServer = None
        self.networkSession = None

        self.statusLabel = QLabel()
        quitButton = QPushButton("Quit")
        quitButton.setAutoDefault(False)

        manager = QNetworkConfigurationManager()
        if manager.capabilities() & QNetworkConfigurationManager.NetworkSessionRequired:
            settings = QSettings(QSettings.UserScope, 'QtProject')
            settings.beginGroup('QtNetwork')
            id = settings.value('DefaultNetworkConfiguration', '')
            settings.endGroup()

            config = manager.configurationFromIdentifier(id)
            if config.state() & QNetworkConfiguration.Discovered == 0:
                config = manager.defaultConfiguration()

            self.networkSession = QNetworkSession(config, self)
            self.networkSession.opened.connect(self.sessionOpened)

            self.statusLabel.setText("Opening network session.")
            self.networkSession.open()
        else:
            self.sessionOpened()

        quitButton.clicked.connect(self.close)
        self.tcpServer.newConnection.connect(self.sendFortune)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle("Fortune Server")

    def sessionOpened(self):
        if self.networkSession is not None:
            config = self.networkSession.configuration()

            if config.type() == QNetworkConfiguration.UserChoice:
                id = self.networkSession.sessionProperty('UserChoiceConfiguration')
            else:
                id = config.identifier()

            settings = QSettings(QSettings.UserScope, 'QtProject')
            settings.beginGroup('QtNetwork')
            settings.setValue('DefaultNetworkConfiguration', id)
            settings.endGroup();

        self.tcpServer = QTcpServer(self)
        if not self.tcpServer.listen():
            QMessageBox.critical(self, "Fortune Server",
                                 "Unable to start the server: %s." % self.tcpServer.errorString())
            self.close()
            return

        for ipAddress in QNetworkInterface.allAddresses():
            if ipAddress != QHostAddress.LocalHost and ipAddress.toIPv4Address() != 0:
                break
        else:
            ipAddress = QHostAddress(QHostAddress.LocalHost)

        ipAddress = ipAddress.toString()

        self.statusLabel.setText("The server is running on\n\nIP: %s\nport %d\n\n"
                                 "Run the Fortune Client example now." % (ipAddress, self.tcpServer.serverPort()))

    def sendFortune(self):
        fortune = self.FORTUNES[random.randint(0, len(self.FORTUNES) - 1)]

        block = QByteArray()
        out = QDataStream(block, QIODevice.WriteOnly)
        out.setVersion(QDataStream.Qt_4_0)
        out.writeUInt16(0)
        out.writeQString(fortune)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)

        clientConnection = self.tcpServer.nextPendingConnection()
        clientConnection.disconnected.connect(clientConnection.deleteLater)

        clientConnection.write(block)
        clientConnection.disconnectFromHost()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    server = Server()
    random.seed(None)
    sys.exit(server.exec_())