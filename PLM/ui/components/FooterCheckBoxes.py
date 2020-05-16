# -*- coding: utf-8 -*-
"""

Script Name: FooterCheckBoxes.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM.ui.framework.Widgets import GroupGrid


class FooterCheckBoxes(GroupGrid):
    key = 'FooterCheckBoxes'

    def __init__(self, title, parent=None):
        super(FooterCheckBoxes, self).__init__(title, parent)
        self.parent = parent



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 7:12 AM
# © 2017 - 2018 DAMGteam. All rights reserved