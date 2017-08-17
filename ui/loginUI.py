import os, sys, logging, json
from functools import partial
from tk import defaultVariable as var
from tk import proc
from ui import DesktopUI

NAMES = var.MAIN_NAMES
TITLE = var.MAIN_ID['LogIn']
PACKAGE = var.MAIN_PACKPAGE
USERNAME = var.USERNAME

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
# IMPORT PTQT5 ELEMENT TO MAKE UI
# -------------------------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def getIcon(name):
    iconName = name + '.icon.png'
    rootPth = os.getcwd().split('ui')[0]
    iconPth = os.path.join(os.path.join(rootPth, 'icons'), iconName)
    return iconPth

userDataPth = os.path.join(os.getenv('PIPELINE_TOOL'), os.path.join('scrInfo', 'user.info'))
with open(userDataPth, 'r') as f:
    userData = json.load(f)

class LoginUI(QDialog):

    def __init__(self):

        super(LoginUI, self).__init__()

        self.setWindowTitle(TITLE)

        self.setWindowIcon(QIcon(getIcon('Logo')))

        self.buildUI()

        # self.setCentralWidget(self.mainFrame)

    def buildUI(self):

        self.mainFrame = QGroupBox(self)
        self.mainFrame.setTitle('User Account')
        self.mainFrame.setFixedSize(300,125)

        hbox = QHBoxLayout()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(5,5,5,5)

        loginText = QLabel('User Name: ')
        self.layout.addWidget(loginText, 0,0,1,2)

        self.userName = QLineEdit()
        self.layout.addWidget(self.userName, 0,2,1,7)

        passText = QLabel('Password: ')
        self.layout.addWidget(passText, 1,0,1,2)

        self.passWord = QLineEdit()
        self.passWord.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.passWord, 1,2,1,7)

        rememberCheck = QLabel('Remember Me')
        self.layout.addWidget(rememberCheck, 2,0,1,2)

        self.rememberCheckBox = QCheckBox()
        self.layout.addWidget(self.rememberCheckBox, 2,2,1,1)

        self.loginBtn = QPushButton('Login')
        self.loginBtn.clicked.connect(self.checkLogin)
        self.layout.addWidget(self.loginBtn, 2,3,1,3)

        self.cancelBtn = QPushButton('Cancel')
        self.cancelBtn.clicked.connect(qApp.quit)
        self.layout.addWidget(self.cancelBtn, 2,6,1,3)

        hbox.addLayout(self.layout)
        self.mainFrame.setLayout(hbox)

    def checkLogin(self):
        user_name = str(self.userName.text())
        pass_word = str(proc.endconding(self.passWord.text()))

        if user_name == "":
            QMessageBox.information(self, 'Login Failed', 'Username can not be blank')
        elif userData[user_name] != None and pass_word == userData[user_name][0]:
            QMessageBox.information(self, 'Login Successful', 'Username and Password are corrected')
            from ui import DesktopUI
            reload(DesktopUI)
            DesktopUI.initialize()
        else:
            QMessageBox.information(self, 'Login Failed', 'Username or Password is incorrected')

            # if self.userName.text() == 'TrinhDo' and self.passWord.text() == proc.decoding(self.userName.text()):
            #     logger.info('on this case: %s and %s are corrected' % (self.userName.text(), self.passWord.text()))
            # else:
            #     QMessageBox.Warning(self, 'Login Failed', 'Wrong user or password')
            #     logger.info('Log in failed')

def initialize():
    app = QApplication(sys.argv)
    login = LoginUI()
    login.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    initialize()