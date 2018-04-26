from PyQt5.QtCore import QDataStream, QTimer
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox,
                             QGridLayout, QLabel, QLineEdit, QMessageBox, QPushButton)
from PyQt5.QtNetwork import QLocalSocket


class Client(QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        self.blockSize = 0
        self.currentFortune = None

        hostLabel = QLabel("&Server name:")
        self.hostLineEdit = QLineEdit("fortune")
        hostLabel.setBuddy(self.hostLineEdit)

        self.statusLabel = QLabel(
            "This examples requires that you run the Fortune Server "
            "example as well.")
        self.statusLabel.setWordWrap(True)

        self.getFortuneButton = QPushButton("Get Fortune")
        self.getFortuneButton.setDefault(True)

        quitButton = QPushButton("Quit")
        buttonBox = QDialogButtonBox()
        buttonBox.addButton(self.getFortuneButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(quitButton, QDialogButtonBox.RejectRole)

        self.socket = QLocalSocket()

        self.hostLineEdit.textChanged.connect(self.enableGetFortuneButton)
        self.getFortuneButton.clicked.connect(self.requestNewFortune)
        quitButton.clicked.connect(self.close)
        self.socket.readyRead.connect(self.readFortune)
        self.socket.error.connect(self.displayError)

        mainLayout = QGridLayout()
        mainLayout.addWidget(hostLabel, 0, 0)
        mainLayout.addWidget(self.hostLineEdit, 0, 1)
        mainLayout.addWidget(self.statusLabel, 2, 0, 1, 2)
        mainLayout.addWidget(buttonBox, 3, 0, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle("Fortune Client")
        self.hostLineEdit.setFocus()

    def requestNewFortune(self):
        self.getFortuneButton.setEnabled(False)
        self.blockSize = 0
        self.socket.abort()
        self.socket.connectToServer(self.hostLineEdit.text())

    def readFortune(self):
        ins = QDataStream(self.socket)
        ins.setVersion(QDataStream.Qt_4_0)

        if self.blockSize == 0:
            if self.socket.bytesAvailable() < 2:
                return
            self.blockSize = ins.readUInt16()

        if ins.atEnd():
            return

        nextFortune = ins.readQString()
        if nextFortune == self.currentFortune:
            QTimer.singleShot(0, self.requestNewFortune)
            return

        self.currentFortune = nextFortune
        self.statusLabel.setText(self.currentFortune)
        self.getFortuneButton.setEnabled(True)

    def displayError(self, socketError):
        errors = {
            QLocalSocket.ServerNotFoundError:
                "The host was not found. Please check the host name and port "
                "settings.",

            QLocalSocket.ConnectionRefusedError:
                "The connection was refused by the peer. Make sure the "
                "fortune server is running, and check that the host name and "
                "port settings are correct.",

            QLocalSocket.PeerClosedError:
                None,
        }

        msg = errors.get(socketError,
                         "The following error occurred: %s." % self.socket.errorString())
        if msg is not None:
            QMessageBox.information(self, "Fortune Client", msg)

        self.getFortuneButton.setEnabled(True)

    def enableGetFortuneButton(self):
        self.getFortuneButton.setEnabled(self.hostLineEdit.text() != "")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())