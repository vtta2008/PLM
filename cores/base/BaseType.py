# -*- coding: utf-8 -*-
"""

Script Name: TaskBase.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """



from PyQt5.QtCore               import pyqtSignal, QDate, QTime

from bin                        import DAMG, DAMGTIMER, DAMGDICT


class BaseType(DAMG):

    key                         = 'BaseType'
    Type                        = 'DAMGBASETYPE'
    _name                       = 'DAMG Base Type'
    _status                     = 'status'

    days                        = 0
    hours                       = 0
    minutes                     = 0
    seconds                     = 0

    countdown                   = pyqtSignal(str, name='CountDown')
    play_alarm                  = True

    dataForm                    = DAMGDICT()

    _id                         = None
    _mode                       = None
    _type                       = None

    def __init__(self, id=None, name=None, mode=None, type=None,
                       teamID=None, projectID=None, organisationID=None,
                       startdate=None, enddate=None, details={}):
        DAMG.__init__(self)

        self.date               = QDate()
        self.time               = QTime()

        self.timer              = DAMGTIMER()
        self.timer.setParent(self)

        self._id                = id
        self._name              = name
        self._mode              = mode
        self._type              = type

        self.teamID             = teamID
        self.projectID          = projectID
        self.organisationID     = organisationID

        self.startdate          = startdate
        self.enddate            = enddate
        self.details            = details

    def countter_format(self, format='sec'):
        if format in ['sec', 'second']:
            return 1000
        elif format in ['min', 'minute']:
            return 1000*60
        elif format in ['hr', 'hour']:
            return 1000*60*60
        else:
            return 1000

    def confirm_task_complete(self):
        self._status                = 'Completed'

    def change_name(self, name):
        self._name = name

    def change_id(self, id):
        self._id = id

    def change_details(self, details):
        self._details = details

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val):
        self._status = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 10:40 AM
# © 2017 - 2018 DAMGteam. All rights reserved