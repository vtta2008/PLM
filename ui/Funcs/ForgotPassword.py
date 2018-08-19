#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: ui_password_reset_from.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is a form for you to reset your password.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PtQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QDialogButtonBox, QFormLayout, QGroupBox, QLineEdit, QVBoxLayout)

# Plm
from ui.uikits.UiPreset import Label


class ForgotPassword(QWidget):

    key = 'forgotPW'
    showLayout = pyqtSignal(str, str)

    def __init__(self):
        super(ForgotPassword, self).__init__()
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

        step1_layout.addRow(Label({'txt': "Username: "}), self.user_account)
        step1_layout.addRow(Label({'txt': "Email adress: "}), self.user_email)
        step1_layout.addRow(step1_btn_box)

        return step1_groupBox

    def step2_layout(self):

        step2_groupBox = QGroupBox("Step 2")
        step2_layout = QVBoxLayout()
        step2_groupBox.setLayout(step2_layout)

        self.question1 = Label({'txt': "Question 1"})
        self.question2 = Label({'txt': "Question 2"})

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

    def closeEvent(self, event):
        self.showLayout.emit(self.key, 'hide')
        event.ignore()

def main():
    app = QApplication(sys.argv)
    reset_pw_layout = ForgotPassword()
    reset_pw_layout.show()
    app.exec_()


if __name__ == '__main__':
    main()