# -*- coding: utf-8 -*-
"""

Script Name: PopupMessage.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PLM                                    import __copyright__
from PLM.api                                import QMessageBox
from PLM.ui.framework.Gui import AppIcon
from PLM.commons                    import DAMGDICT


class MessageBox(QMessageBox):

    Type                            = 'DAMGUI'
    key                             = 'Widget'
    _name                           = 'DAMG Widget'
    _copyright                      = __copyright__()

    buttons                         = DAMGDICT()

    def __init__(self, parent=None, title="auto", level="auto", message="test message", btns=[], flag=None):
        QMessageBox.__init__(self)

        self._parent                = parent
        self._title                 = title
        self._level                 = level
        self._message               = message
        self.btns                   = btns
        self.flag                   = flag

        if self._title == 'auto' or self._title is None:
            self.title             = self._level
        else:
            self.title             = self._title

        if self.flag:
            self.setWindowFlag(self.flag)

        self.icon                  = self.getIcon()
        self.level                 = self.getLevel()

        if type(self.btns) in [str]:
            self.btns                   = self.getBtnSetting('ok')
        else:
            for btn in self.btns:
                self.addButton(btn, self.getBtnSetting(btn))


    def addBtn(self, btn):
        button = self.addButton(btn, self.getBtnSetting(btn))
        self.buttons.add(btn, button)
        return button

    def getLevel(self):

        levels = dict(

            about                   = self.about,
            information             = self.information,
            question                = self.question,
            warning                 = self.warning,
            critical                = self.critical,

        )

        return levels[self._level]
        
    def getIcon(self):

        icons = dict(

            about                   = self.NoIcon,
            information             = self.Information,
            question                = self.Question,
            warning                 = self.Warning,
            critical                = self.Critical,

        )

        if self._level in icons.keys():
            return icons[self._level]
        else:
            AppIcon(self._level)

    def getBtnSetting(self, btn):
        
        buttons = dict(

            ok                      = self.Ok,
            open                    = self.Open,
            save                    = self.Save,
            cancel                  = self.Cancel,
            close                   = self.Close,
            yes                     = self.Yes,
            no                      = self.No,
            abort                   = self.Abort,
            retry                   = self.Retry,
            ignore                  = self.Ignore,
            discard                 = self.Discard,
            yes_no                  = self.Yes|QMessageBox.No,
            retry_close             = self.Retry|QMessageBox.Close,
            Overwrite               = self.NoRole,
            Rename                  = self.RejectRole,
            Resume                  = self.YesRole,
            
        )

        return buttons[btn]


    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/10/2019 - 8:57 AM
# © 2017 - 2018 DAMGteam. All rights reserved