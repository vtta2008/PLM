#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: {}.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
import sys
from functools import partial

# PyQt5
from PySide2.QtWidgets        import (QFileDialog)

# Plm
from PLM.configs import configPropText, QUESTIONS
p = configPropText()
from PLM.utils import (check_blank, check_match, getToken, getUnix, getTime, getDate)
from pyPLM.configs import get_avatar_image
from pyPLM.models import DamgSignals
from pyPLM.Widgets import (Widget, GridLayout, Label, Button, LineEdit, ComboBox, MessageBox, CheckBox, GroupGrid)
from pyPLM.Gui import AppIcon, Pixmap, Image


# -------------------------------------------------------------------------------------------------------------
""" Sign up ui """

class SignUp(Widget):

    key = 'SignUp'

    def __init__(self, parent=None):
        super(SignUp, self).__init__(parent)

        self.setWindowIcon(AppIcon(32, "SignUp"))
        self.signals = DamgSignals(self)
        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.avatar_section()
        self.account_section()
        self.profile_section()
        self.location_section()
        self.security_section()
        self.buttons_section()

        self.layout.addWidget(Label({'txt':"ALL FIELD ARE REQUIRED!!!"}), 0, 0, 1, 6)
        self.layout.addWidget(self.avaSection, 1, 0, 1, 2)
        self.layout.addWidget(self.accSection, 1, 2, 1, 4)
        self.layout.addWidget(self.prfSection, 2, 0, 1, 6)
        self.layout.addWidget(self.conSection, 3, 0, 1, 6)
        self.layout.addWidget(self.serSection, 4, 0, 1, 6)
        self.layout.addWidget(self.btnSection, 5, 0, 1, 6)

        self.applySetting()

    def avatar_section(self):
        self.avaSection     = GroupGrid("Avatar")
        avatar_grid         = self.avaSection.layout
        self.userAvatar     = Label({'pxm':'default', 'scc': True, 'sfs':[100, 100]})
        set_avatarBtn       = Button({'txt':'Set Avatar', 'tt':'Choose a showLayout_new avatar', 'cl': self.setAvaClicked})

        avatar_grid.addWidget(self.userAvatar, 0, 0, 2, 2)
        avatar_grid.addWidget(set_avatarBtn, 2, 0, 1, 2)

    def account_section(self):
        self.accSection     = GroupGrid("Account")
        account_grid        = self.accSection.layout
        self.userField      = LineEdit()
        self.pwField        = LineEdit({'fn': 'password'})
        self.cfpwField      = LineEdit({'fn': 'password'})

        account_grid.addWidget(Label({'txt':'User Name'}), 0, 0, 1, 2)
        account_grid.addWidget(Label({'txt':'Password'}), 1, 0, 1, 2)
        account_grid.addWidget(Label({'txt':'Confirm Password'}), 2, 0, 1, 2)

        account_grid.addWidget(self.userField, 0, 3, 1, 4)
        account_grid.addWidget(self.pwField, 1, 3, 1, 4)
        account_grid.addWidget(self.cfpwField, 2, 3, 1, 4)

    def profile_section(self):
        self.prfSection     = GroupGrid("Profile")
        profile_grid        = self.prfSection.layout

        profile_grid.addWidget(Label({'txt':'First Name'}), 0, 0, 1, 2)
        profile_grid.addWidget(Label({'txt':'Last Name'}), 1, 0, 1, 2)
        profile_grid.addWidget(Label({'txt':'Your Title'}), 2, 0, 1, 2)
        profile_grid.addWidget(Label({'txt':'Email'}), 3, 0, 1, 2)
        profile_grid.addWidget(Label({'txt':'Phone Number'}), 4, 0, 1, 2)

        self.titleField     = LineEdit()
        self.firstnameField = LineEdit()
        self.lastnameField  = LineEdit()
        self.emailField     = LineEdit()
        self.phoneField     = LineEdit()

        profile_grid.addWidget(self.firstnameField, 0, 2, 1, 4)
        profile_grid.addWidget(self.lastnameField, 1, 2, 1, 4)
        profile_grid.addWidget(self.titleField, 2, 2, 1, 4)
        profile_grid.addWidget(self.emailField, 3, 2, 1, 4)
        profile_grid.addWidget(self.phoneField, 4, 2, 1, 4)

    def location_section(self):
        self.conSection     = GroupGrid("Location")
        conGrid             = self.conSection.layout

        conGrid.addWidget(Label({'txt':"Address Line 1"}), 0, 0, 1, 2)
        conGrid.addWidget(Label({'txt':"Address Line 2"}), 1, 0, 1, 2)
        conGrid.addWidget(Label({'txt':"Postal"}), 2, 0, 1, 2)
        conGrid.addWidget(Label({'txt':"City"}), 3, 0, 1, 2)
        conGrid.addWidget(Label({'txt':"Country"}), 4, 0, 1, 2)

        self.addressLine1   = LineEdit()
        self.addressLine2   = LineEdit()
        self.postalCode     = LineEdit()
        self.city           = LineEdit()
        self.country        = LineEdit()

        conGrid.addWidget(self.addressLine1, 0, 2, 1, 4)
        conGrid.addWidget(self.addressLine2, 1, 2, 1, 4)
        conGrid.addWidget(self.city, 2, 2, 1, 4)
        conGrid.addWidget(self.postalCode, 3, 2, 1, 4)
        conGrid.addWidget(self.country, 4, 2, 1, 4)

    def security_section(self):

        self.serSection     = GroupGrid("Security Question")
        questions_grid      = self.serSection.layout

        self.ques1          = ComboBox({'items': [str(i) for i in QUESTIONS.split('\n')]})
        self.answ2          = LineEdit()

        self.ques2          = ComboBox({'items': [str(i) for i in QUESTIONS.split('\n')]})
        self.answ1          = LineEdit()

        questions_grid.addWidget(Label({'txt':'Question 1'}), 0, 0, 1, 3)
        questions_grid.addWidget(Label({'txt':'Answer 1'}), 1, 0, 1, 3)
        questions_grid.addWidget(Label({'txt':'Question 2'}), 2, 0, 1, 3)
        questions_grid.addWidget(Label({'txt':'Answer 2'}), 3, 0, 1, 3)

        questions_grid.addWidget(self.ques1, 0, 3, 1, 6)
        questions_grid.addWidget(self.answ1, 1, 3, 1, 6)
        questions_grid.addWidget(self.ques2, 2, 3, 1, 6)
        questions_grid.addWidget(self.answ2, 3, 3, 1, 6)

    def buttons_section(self):
        self.btnSection     = GroupGrid()
        btn_grid            = self.btnSection.layout

        self.user_agree_checkBox = CheckBox(txt=p['USER_CHECK_REQUIRED'])
        okBtn               = Button({'txt':'Create Account', 'tt':'Confirm to create an account', 'cl': self.createBtnClicked})
        cancelBtn           = Button({'txt':'Cancel', 'tt':'Go back to Login stage', 'cl': partial(self.signals.emit, 'showLayout', 'SignIn', 'SignIn')})
        quitBtn             = Button({'txt': 'Quit', 'tt': 'Quit the application', 'cl': sys.exit})

        btn_grid.addWidget(self.user_agree_checkBox, 0, 0, 1, 6)
        btn_grid.addWidget(okBtn, 1, 0, 1, 2)
        btn_grid.addWidget(cancelBtn, 1, 2, 1, 2)
        btn_grid.addWidget(quitBtn, 1,4,1,2)

    def setAvaClicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.rawAvatarPth, _ = QFileDialog.getOpenFileName(self, "Your Avatar", os.path.join('imgs', 'avatar'), "All Files (*);;Img Files (*.jpg)", options=options)

        if self.rawAvatarPth:
            self.userAvatar.setPixmap(Pixmap.fromImage(Image(self.rawAvatarPth)))
            self.userAvatar.update()

    def createBtnClicked(self):
        if self.check_all_conditions():
            self.generate_user_data()
            MessageBox(self, "Failed", "information", p['WAIT_LAYOUT_COMPLETE'], 'ok')
            return

    def collect_input(self):
        username            = str(self.userField.text())
        password            = str(self.pwField.text())
        confirm             = str(self.cfpwField.text())
        firstname           = str(self.firstnameField.text())
        lastname            = str(self.lastnameField.text())
        email               = str(self.emailField.text())
        phone               = str(self.phoneField.text())
        address1            = str(self.addressLine1.text())
        address2            = str(self.addressLine2.text())
        postal              = str(self.postalCode.text())
        city                = str(self.city.text())
        country             = str(self.country.text())
        answer1             = str(self.answ1.text())
        answer2             = str(self.answ2.text())
        return [username, password, confirm, firstname, lastname, email, phone, address1, address2, postal, city,
                country, answer1, answer2]

    def check_all_conditions(self):
        if self.check_all_field_blank():
            if self.check_user_agreement():
                if self.check_pw_matching():
                    return True
        else:
            return False

    def check_all_field_blank(self):
        regInput            = self.collect_input()
        secName             = ["Username", "Password", "Confirm Password", "Firstname", "Lastname", "Email", "Phone",
                                "Address line 1", "Address line 2", "Postal", "City", "Country", "Answer 1", "Answer 2"]
        for section in regInput:
            if check_blank(section):
                return True
            else:
                MessageBox(self, "Fail", secName[regInput.index(section)] + "Blank", MessageBox.Ok)
                break

    def check_user_agreement(self):
        return self.user_agree_checkBox.checkState()

    def applySetting(self):
        self.resize(450, 900)

    def generate_user_data(self):
        regInput            = self.collect_input()
        question1           = str(self.ques1.currentText())
        question2           = str(self.ques2.currentText())
        title               = str(self.titleField.text()) or "Guess"

        token               = getToken()
        timelog             = getTime()
        unix                = getUnix()
        datelog             = getDate()


        if not os.path.exists(self.rawAvatarPth):
            avatar = get_avatar_image('default')
        else:
            avatar = self.rawAvatarPth

        data = [regInput[0], regInput[1], regInput[3], regInput[4], title, regInput[5], regInput[6], regInput[7],
                regInput[8], regInput[9], regInput[10], regInput[11], token, timelog, unix, question1, regInput[12],
                question2, regInput[13], datelog, avatar]
        return data

    def check_pw_matching(self):
        password            = str(self.pwField.text())
        confirm             = str(self.cfpwField.text())
        check_pass          = check_match(password, confirm)

        if not check_pass:
            MessageBox(self, "Warning", p['PW_UNMATCH'], MessageBox.Retry)
            return False

        return True

    def loginChanged(self, login):
        self._login = login

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, newVal):
        self._login = newVal

