# -*- coding: utf-8 -*-
"""

Script Name: Project.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, json

# PLM
from PLM.cores.base                     import BaseType
from PLM                                import PRJ_DIR


class Project(BaseType):

    key                                 = 'Project'

    def __init__(self, id=None, name=None, mode=None, type=None, path=None, url=None, startdate=None, enddate=None):
        super(Project, self).__init__(id, name, mode, type, path, url, startdate, enddate)

        self.configs()
        # format = self.countter_format()
        # timer = Timer()
        # timer.timeout.connect(self.countdown)
        # timer.start(format)

    def configs(self, update=False):

        cfgPath = os.path.join(PRJ_DIR, '{0}.projects'.format(self._id)).replace('\\', '/')

        if update:
            with open(cfgPath, 'w') as f:
                return json.dump(self, f, indent=4)
        else:
            if not os.path.exists(cfgPath):
                with open(cfgPath, 'w') as f:
                    return json.dump(self, f, indent=4)

    def update_details(self, details):
        self._details = details
        self.update()
        self.configs(True)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 1:46 PM
# © 2017 - 2018 DAMGteam. All rights reserved