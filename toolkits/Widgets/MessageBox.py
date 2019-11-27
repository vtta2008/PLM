# -*- coding: utf-8 -*-
"""

Script Name: PopupMessage.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__

from PyQt5.QtWidgets                import QMessageBox

# PLM
from .Icon                          import AppIcon


class MessageBox(QMessageBox):

    Type                            = 'DAMGUI'
    key                             = 'Widget'
    _name                           = 'DAMG Widget'
    _copyright                      = __copyright__()

    def __init__(self, parent=None, title="auto", level="auto", message="test message", btn='ok'):
        QMessageBox.__init__(self)

        self._parent                = parent
        self._title                 = title
        self._level                 = level
        self._message               = message
        self._btn                   = btn

        if self._title == 'auto' or self._title is None:
            self.popupTitle             = self._level
        else:
            self.popupTitle             = self._title

        self.popupIcon                  = self.config_icon()
        self.popupLevel                 = self.config_level()
        self.btn                        = self.config_button()

        self.popupLevel(self._parent, self.popupTitle, self._message, self.btn)


    def config_level(self):

        levels = dict(

            about                   = self.about,
            information             = self.information,
            question                = self.question,
            warning                 = self.warning,
            critical                = self.critical,

        )

        return levels[self._level]
        
    def config_icon(self):

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

    def config_button(self):
        
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
            
        )

        return buttons[self._btn]


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