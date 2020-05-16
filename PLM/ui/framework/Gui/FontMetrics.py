# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM                                import __copyright__, QFontMetrics

class FontMetrics(QFontMetrics):

    Type                            = 'DAMGFONTMETRICS'
    key                             = 'FontMetrics'
    _name                           = 'DAMG Font Metrics'
    _copyright                      = __copyright__()

    def __init__(self, *__args):
        super(FontMetrics, self).__init__(*__args)

    @property
    def name(self):
        return self._name

    @property
    def copyright(self):
        return self._copyright

    @name.setter
    def name(self, val):
        self._name                  = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved