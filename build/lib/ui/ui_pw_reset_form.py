# -*- coding: utf-8 -*-
"""

Script Name: ui_password_reset_from.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is a form for you to reset your password.

"""

# -------------------------------------------------------------------------------------------------------------
""" About Plt """

__appname__ = "Pipeline Tool"
__module__ = "Plt"
__version__ = "13.0.1"
__organization__ = "DAMG team"
__website__ = "www.dot.damgteam.com"
__email__ = "dot@damgteam.com"
__author__ = "Trinh Do, a.k.a: Jimmy"
__root__ = "PLT_RT"
__db__ = "PLT_DB"
__st__ = "PLT_ST"

# -------------------------------------------------------------------------------------------------------------
""" Import modules """

# Python
import sys
import os

# PtQt5
from PyQt5.QtWidgets import (QApplication, QMessageBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel,
                             QLineEdit, QVBoxLayout)

# Plt tools
from utilities import sql_local as usql
from utilities import message as mess

# ----------------------------------------------------------------------------------------------------------- #
""" Reset Password layout """
# ----------------------------------------------------------------------------------------------------------- #
class Reset_password_form(QDialog):

    def __init__(self):
        super(Reset_password_form, self).__init__()

        self.setWindowTitle("Reset Password")
        self.setContentsMargins(0,0,0,0)

        self.layout = QVBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.step1_form = self.step1_layout()

        self.step2_form = self.step2_layout()
        self.step2_form.setVisible(False)

        self.layout.addWidget(self.step1_form)
        self.layout.addWidget(self.step2_form)

    def step1_layout(self):

        step1_groupBox = QGroupBox("Step 1")
        step1_layout = QFormLayout()
        step1_groupBox.setLayout(step1_layout)

        self.user_account = QLineEdit()
        self.user_email = QLineEdit()

        step1_btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        step1_btn_box.accepted.connect(self.on_step1_btn_clicked)
        step1_btn_box.rejected.connect(self.close)

        step1_layout.addRow(QLabel("Username:"), self.user_account)
        step1_layout.addRow(QLabel("Email adress:"), self.user_email)
        step1_layout.addRow(step1_btn_box)

        return step1_groupBox

    def step2_layout(self):

        step2_groupBox = QGroupBox("Step 2")
        step2_layout = QVBoxLayout()
        step2_groupBox.setLayout(step2_layout)

        self.question1 = QLabel("Question 1")
        self.question2 = QLabel("Question 2")

        self.answer1 = QLineEdit()
        self.answer2 = QLineEdit()

        step2_btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        step2_btn_box.accepted.connect(self.on_step2_btn_clicked)
        step2_btn_box.rejected.connect(self.close)

        step2_layout.addWidget(self.question1)
        step2_layout.addWidget(self.answer1)
        step2_layout.addWidget(self.question2)
        step2_layout.addWidget(self.answer2)
        step2_layout.addWidget(step2_btn_box)

        return step2_groupBox

    def on_step1_btn_clicked(self):

        question1 = "What is the question 1"
        question2 = "What is the question 2"

        self.question1.setText(question1)
        self.question2.setText(question2)

        self.step1_form.setDisabled(True)
        self.step2_form.setVisible(True)

        # username = self.user_account.text()
        #
        # if len(username) == 0:
        #     QMessageBox.critical(self, 'Failed', mess.USER_BLANK)
        # else:
        #     checkUserExists = usql.check_data_exists(username)
        #     if not checkUserExists:
        #         QMessageBox.critical(self, 'Failed', mess.USER_NOT_EXSIST)
        #         question1, question2 = usql.query_user_security_question(username)
        #
        #         self.question1.setText(question1)
        #         self.question2.setText(question2)
        #
        #         self.step1_form.setDisabled(True)
        #         self.step2_form.setVisible(True)

    def on_step2_btn_clicked(self):
        pass

def main():
    app = QApplication(sys.argv)
    reset_pw_layout = Reset_password_form()
    reset_pw_layout.show()
    sys.reset_pw_layout(app.exec_())


if __name__ == '__main__':
    main()