#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: ui_acc_setting.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    Setting your account.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, shutil

# PtQt5
from PyQt5.QtGui                    import QImage, QPixmap
from PyQt5.QtWidgets                import (QFileDialog)

# Plt
from appData                        import PW_BLANK, PW_UNMATCH, __envKey__
from toolkits.uiUtils               import GroupGrid
from toolkits.Widgets               import Widget, GridLayout, Label, Button, LineEdit, MessageBox
from utils                          import get_avatar_image, QuerryDB, text_to_hex, resize_image

# ----------------------------------------------------------------------------------------------------------- #
""" User setting layout """

class UserSetting(Widget):

    key = 'UserSetting'
    query = QuerryDB()

    def __init__(self, parent=None):

        super(UserSetting, self).__init__(parent)

        # self.setWindowIcon(AppIcon(32, "UserSetting"))
        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        password_section = self.change_pass_section()
        avatar_section = self.change_avatar_section()
        profile_section = self.change_profile_section()
        location_setion = self.change_location_section()

        self.layout.addWidget(avatar_section, 0, 0, 1, 1)
        self.layout.addWidget(password_section, 0, 1 , 1, 1)
        self.layout.addWidget(profile_section, 1, 0, 1, 1)
        self.layout.addWidget(location_setion, 1, 1, 1, 1)

    def change_avatar_section(self):

        try:
            self.username, token, cookie, remember = self.query.query_table('curUser')
        except (ValueError, IndexError):
            self.username = 'DemoUser'

        avatar_groupBox = GroupGrid('Change Avatar')
        avatar_layout = avatar_groupBox.layout

        self.avatar = Label()
        self.avatar.setPixmap(QPixmap.fromImage(QImage(get_avatar_image(self.username))))
        self.avatar.setScaledContents(True)
        self.avatar.setFixedSize(100, 100)

        change_avatar_btn = Button({'txt':'Change Avatar', 'cl': self.update_avatar})
        avatar_layout.addWidget(self.avatar)
        avatar_layout.addWidget(change_avatar_btn)

        return avatar_groupBox

    def change_pass_section(self):

        password_groupBox = GroupGrid('Change Password')
        password_layout = password_groupBox.layout

        self.old_pass                   = LineEdit({'echo': 'password'})
        self.new_pass                   = LineEdit({'echo': 'password'})
        self.confirm_pass               = LineEdit({'echo': 'password'})
        change_pass_btn                 = Button({'txt': 'Change Password', 'cl': self.update_password})

        password_layout.addWidget(Label({'txt': 'Old Password'}), 0, 0, 1, 2)
        password_layout.addWidget(Label({'txt': 'New Password'}), 1, 0, 1, 2)
        password_layout.addWidget(Label({'txt': 'Confirm Password'}), 2, 0, 1, 2)
        password_layout.addWidget(self.old_pass, 0, 2, 1, 4)
        password_layout.addWidget(self.new_pass, 1, 2, 1, 4)
        password_layout.addWidget(self.confirm_pass, 2, 2, 1, 4)
        password_layout.addWidget(change_pass_btn, 3, 0, 1, 6)

        return password_groupBox

    def change_profile_section(self):

        profile_groupBox = GroupGrid("Change Profile")
        profile_layout = profile_groupBox.layout

        profile_layout.addWidget(Label({'txt': 'First Name'}), 0, 0, 1, 2)
        profile_layout.addWidget(Label({'txt': 'Last Name'}), 1, 0, 1, 2)
        profile_layout.addWidget(Label({'txt': 'Your Title'}), 2, 0, 1, 2)
        profile_layout.addWidget(Label({'txt': 'Email'}), 3, 0, 1, 2)
        profile_layout.addWidget(Label({'txt': 'Phone Number'}), 4, 0, 1, 2)

        self.firstnameField             = LineEdit()
        self.lastnameField              = LineEdit()
        self.titleField                 = LineEdit()
        self.emailField                 = LineEdit()
        self.phoneField                 = LineEdit()

        change_profile_btn = Button({'txt': "Update Profile", 'cl': self.update_profile})

        profile_layout.addWidget(self.firstnameField, 0, 2, 1, 4)
        profile_layout.addWidget(self.lastnameField, 1, 2, 1, 4)
        profile_layout.addWidget(self.titleField, 2, 2, 1, 4)
        profile_layout.addWidget(self.emailField, 3, 2, 1, 4)
        profile_layout.addWidget(self.phoneField, 4, 2, 1, 4)
        profile_layout.addWidget(change_profile_btn, 5, 0, 1, 6)

        return profile_groupBox

    def change_location_section(self):

        location_groupBox = GroupGrid("Change Location")
        location_layout = location_groupBox.layout

        location_layout.addWidget(Label({'txt': 'Address Line 1'}), 0, 0, 1, 2)
        location_layout.addWidget(Label({'txt': 'Address Line 2'}), 1, 0, 1, 2)
        location_layout.addWidget(Label({'txt': 'Postal'}), 2, 0, 1, 2)
        location_layout.addWidget(Label({'txt': 'City'}), 3, 0, 1, 2)
        location_layout.addWidget(Label({'txt': 'Country'}), 4, 0, 1, 2)

        self.address1Field              = LineEdit()
        self.address2Field              = LineEdit()
        self.postalField                = LineEdit()
        self.cityField                  = LineEdit()
        self.countryField               = LineEdit()

        change_location_btn = Button({'txt': "Update Location", 'cl': self.update_location})

        location_layout.addWidget(self.address1Field, 0, 2, 1, 4)
        location_layout.addWidget(self.address2Field, 1, 2, 1, 4)
        location_layout.addWidget(self.postalField, 2, 2, 1, 4)
        location_layout.addWidget(self.cityField, 3, 2, 1, 4)
        location_layout.addWidget(self.countryField, 4, 2, 1, 4)
        location_layout.addWidget(change_location_btn, 5, 0, 1, 6)

        return location_groupBox

    def update_password(self):

        old_pass = text_to_hex(self.old_pass.text())
        new_pass = text_to_hex(self.new_pass.text())
        confirm_pass = text_to_hex(self.confirm_pass.text())

        if len(old_pass) == 0 or len(new_pass) == 0 or len(confirm_pass) == 0:
            MessageBox(self, title='Failed', level='critical', message=PW_BLANK, btn='ok')
            return
        elif new_pass is not confirm_pass:
            MessageBox(self, title='Failed', level='critical', message=PW_UNMATCH, btn='ok')
            return
        else:
            # checkPass = func.check_pw_match(self.username, old_pass)
            # if not checkPass:
            #     QMessageBox.critical(self, 'Failed', "Password not match")
            #     return
            # else:
            #     newpass = func.encode(self.newPassword.text())
            #     func.update_password(self.unix, newpass)
            #     QMessageBox.information(self, 'Updated', PW_CHANGED)
            pass

    def update_avatar(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        imgsDir = os.path.join(os.getenv(__envKey__), 'avatar')
        fileName, _ = QFileDialog.getOpenFileName(self, "Your Avatar", imgsDir, "All Files (*);;Img Files (*.jpg)",
                                                  options=options)
        if fileName:
            baseFileName = self.username + '.avatar.jpg'
            desPth = os.path.join(imgsDir, baseFileName)

            if desPth == fileName:
                pass
            elif os.path.exists(desPth):
                if os.path.exists(desPth + '.showLayout_old'):
                    os.remove(desPth + '.showLayout_old')

                os.rename(desPth, desPth + '.showLayout_old')
                resize_image(fileName, desPth)
                shutil.copy2(fileName, desPth)
                image = QPixmap.fromImage(QImage(desPth))
                self.avatar.setPixmap(image)
                self.avatar.update()
                self.settings.setValue(self.username, desPth)
                self.updateAvatar.emit(True)

    def update_profile(self):
        pass

    def update_location(self):
        pass