# -*- coding: utf-8 -*-
"""

Script Name: Task.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM.commons.Core                       import ThreadPool



class ThreadManager(ThreadPool):

    key                                     = 'ThreadManager'



    def __init__(self, parent=None):
        super(ThreadManager, self).__init__(parent)

        self.parent                         = parent


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 20/10/2019 - 6:23 PM
# © 2017 - 2018 DAMGteam. All rights reserved