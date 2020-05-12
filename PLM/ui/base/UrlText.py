# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

from .TextBase import TextBase

class UrlText(TextBase):

    key = 'UrlText'

    def __init__(self, parent=None):
        super(UrlText, self).__init__(parent)

        self._urlType = None
        self.setObjectName(self.__class__.__name__)


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved