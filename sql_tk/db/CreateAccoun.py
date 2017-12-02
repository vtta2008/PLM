


import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from tk import appFuncs as func

__center__ = Qt.AlignCenter
__right__ = Qt.AlignRight
__left__ = Qt.AlignLeft
frameStyle = QFrame.Sunken | QFrame.Panel


class NewAccount(QDialog):

    TITLEBLANK = 'If title is blank, it will be considered as a "Tester"'

    def __init__(self, parent=None):
        super(NewAccount, self).__init__(parent)
        self.setWindowTitle("Create New Account")
        self.setWindowIcon(QIcon(func.getIcon('Logo')))

        self.layout = QGridLayout()
        # self.layout.setColumnStretch(1, 1)
        # self.layout.setColumnMinimumWidth(1, 250)

        self.firstnameField = QLineEdit()
        self.lastnameField = QLineEdit()
        self.regisTitle = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.passwordRetype = QLineEdit()
        self.passwordRetype.setEchoMode(QLineEdit.Password)

        self.buildUI()

    def buildUI(self):

        self.layout.addWidget(self.clabel('Register!'),0,0,1,4)
        self.layout.addWidget(self.clabel('Title(modeler, artist, etc.)'),1,0,1,1)
        self.layout.addWidget(self.clabel('First Name'),2,0,1,1)
        self.layout.addWidget(self.clabel('Last Name'),3,0,1,1)

        self.layout.addWidget(self.clabel(self.TITLEBLANK), 4,0,1,4)

        self.layout.addWidget(self.clabel('Password'),5,0,1,1)
        self.layout.addWidget(self.clabel('Re-type password'),6,0,1,1)

        self.layout.addWidget(self.regisTitle,1,1,1,3)
        self.layout.addWidget(self.firstnameField, 2,1,1,3)
        self.layout.addWidget(self.lastnameField,3,1,1,3)
        self.layout.addWidget(self.password, 5, 1, 1, 3)
        self.layout.addWidget(self.passwordRetype,6,1,1,3)

        self.layout.addWidget(self.clabel(''), 7, 0, 1, 4)

        okBtn = QPushButton('Ok')
        okBtn.clicked.connect(self.setOKclciked)

        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(self.close)

        self.layout.addWidget(okBtn,8,0,1,2)
        self.layout.addWidget(cancelBtn,8,2,1,2)

        self.setLayout(self.layout)

    def clabel(self, text):
        label = QLabel(text)
        label.setAlignment(__center__)
        label.setMinimumWidth(50)
        return label

    def setOKclciked(self):


        title = self.regisTitle.text()
        firstname = self.firstnameField.text()
        lastname = self.lastnameField.text()

        password = self.password.text()
        passretype = self.passwordRetype.text()

        check = self.checkMatchPassWord(firstname, lastname, title, password, passretype)

        if not check:
            pass
        else:
            SUCCESS = "%s.%s" % (lastname, firstname)
            self.processNewAcountData(lastname, firstname, title, password)
            QMessageBox.information(self, "Error", SUCCESS, QMessageBox.Retry)


    def checkMatchPassWord(self, firstname, lastname, title, password, passretype):
        NOTMATCH = "Password doesn't match"
        FIRSTNAME = "Firstname cannot be blank"
        LASTNAME = "Lastname cannot be blank"
        if title == "":
            title = 'Tester'
        if firstname == "":
            QMessageBox.critical(self, "Error", FIRSTNAME, QMessageBox.Retry)
            return False
        else:
            pass
        if lastname == "":
            QMessageBox.critical(self, "Error", LASTNAME, QMessageBox.Retry)
            return False
        else:
            pass

        if not password == passretype:
            QMessageBox.critical(self, "Password not matches", NOTMATCH, QMessageBox.Retry)
            return False
        else:
            return True

    def processNewAcountData(self, lastname, firstname, title, password):
        import ultilitis_user
        reload(ultilitis_user)
        ultilitis_user.CreateNewUser(lastname, firstname, title, password)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = NewAccount()
    dialog.show()
    sys.exit(app.exec_())