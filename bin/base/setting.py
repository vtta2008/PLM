# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from .obj import Base


class Setting(Base):

    key                                 = 'Setting'
    Type                                = 'DAMGSETTING'
    _name                               = 'DAMG Setting'

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)

        self.update()

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved