import random

from PyQt5.QtCore import QByteArray, QDataStream, QIODevice
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QHBoxLayout,
                             QMessageBox, QPushButton, QVBoxLayout)
from PyQt5.QtNetwork import QLocalServer


class Server(QDialog):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)

        statusLabel = QLabel()
        statusLabel.setWordWrap(True)
        quitButton = QPushButton("Quit")
        quitButton.setAutoDefault(False)

        self.fortunes = (
            "You've been leading a dog's life. Stay off the furniture.",
            "You've got to think about tomorrow.",
            "You will be surprised by a loud noise.",
            "You will feel hungry again in another hour.",
            "You might have mail.",
            "You cannot kill time without injuring eternity.",
            "Computers are not intelligent. They only think they are.",
        )

        self.server = QLocalServer()
        if not self.server.listen('fortune'):
            QMessageBox.critical(self, "Fortune Server",
                                 "Unable to start the server: %s." % self.server.errorString())
            self.close()
            return

        statusLabel.setText("The server is running.\nRun the Fortune Client "
                            "example now.")

        quitButton.clicked.connect(self.close)
        self.server.newConnection.connect(self.sendFortune)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle("Fortune Server")

    def sendFortune(self):
        block = QByteArray()
        out = QDataStream(block, QIODevice.WriteOnly)
        out.setVersion(QDataStream.Qt_4_0)
        out.writeUInt16(0)
        out.writeQString(random.choice(self.fortunes))
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)

        clientConnection = self.server.nextPendingConnection()
        clientConnection.disconnected.connect(clientConnection.deleteLater)
        clientConnection.write(block)
        clientConnection.flush()
        clientConnection.disconnectFromServer()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    server = Server()
    server.show()
    sys.exit(app.exec_())