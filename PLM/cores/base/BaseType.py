# -*- coding: utf-8 -*-
"""

Script Name: TaskBase.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import os
from playsound                  import playsound
from PLM                        import SOUND_DIR
from pyPLM.damg                 import DAMGDICT, DAMG
from pyPLM.Core                 import Date, Time, DateTime, Signal


class TrackingSignal(DAMG):

    trackingReport = Signal(str, name='trackingReport')


    def __init__(self, parent=None):
        super(TrackingSignal, self).__init__(parent)

        self.parent = parent

    def _emit(self, val):
        self.trackingReport.emit(val)



class BaseType(DAMGDICT):

    key                         = 'BaseType'
    _status                     = 'status'

    days                        = 0
    hours                       = 0
    minutes                     = 0
    seconds                     = 0



    play_alarm                  = True

    _id                         = None
    _mode                       = None
    _type                       = None

    def __init__(self, id=None, name=None, mode=None, type=None, path=None, url=None, startdate=None, enddate=None):
        DAMGDICT.__init__(self)

        self.date               = Date()
        self.time               = Time()
        self.trackingReport     = TrackingSignal(self)

        self._id                = id
        self._name              = name
        self._mode              = mode
        self._type              = type
        self._path              = path
        self._url               = url

        self._startdate         = startdate
        self._enddate           = enddate

        if self._startdate is None:
            self._start         = DateTime(self.date.currentDate(), self.time.currentTime())
        else:
            self._start         = self.startdate

        self._end               = self.enddate

        self.countdown()

    def countter_format(self, format='sec'):
        if format in ['sec', 'second']:
            return 1000
        elif format in ['min', 'minute']:
            return 1000*60
        elif format in ['hr', 'hour']:
            return 1000*60*60
        else:
            return 1000

    def updateData(self):

        self.add('name', self._name)
        self.add('id', self._id)
        self.add('mode', self._mode)
        self.add('type', self._type)
        self.add('status', self.get_status())
        self.add('path', self._path)

        self.add('start', self._start.toString('dd/MM/yy - hh:mm:ss'))
        self.add('startdate', self._startdate.date().toString('dd/MM/yy'))
        self.add('starttime', self._startdate.time().toString('hh:mm:ss'))

        self.add('end', self._end.toString('dd/MM/yy - hh:mm:ss'))
        self.add('enddate', self._enddate.date().toString('dd/MM/yy'))
        self.add('endtime', self._enddate.time().toString('hh:mm:ss'))

        self.add('details', {})

        return self.update()

    def countdown(self):
        self.days               = self.start.daysTo(self.end)

        self.hours              = self.end.time().hour() - self.start.time().hour()
        if self.hours <= 0 and self.days > 0:
            self.days -= 1
            self.hours += 24

        self.minutes            = self.end.time().minute() - self.start.time().minute()
        if self.minutes <= 0 and self.hours > 0:
            self.hours -= 1
            self.minutes += 60

        self.seconds            = self.end.time().second() - self.start.time().second()
        if self.seconds <= 0 and self.minutes > 0:
            self.minutes -= 1
            self.seconds += 60

        self._status            = self.get_status()

        if self.days != 0:
            hrs                 = self.hours + self.days * 24
        else:
            hrs                 = self.hours

        report = '{0}:{1}:{2}'.format(hrs, self.minutes, self.seconds)

        self.trackingReport._emit(report)

        if self.days == 0 and self.hours == 0 and self.minutes == 0 and self.seconds <= 30:
            pth                 = os.path.join(SOUND_DIR, 'bell.wav')
            if not self.play_alarm:
                playsound(pth)
                self.play_alarm = True

        self.updateData()

    def get_status(self):
        if self.days < 0:
            self._status = 'Overdued'
        elif self.days == 0:
            if self.hours < 0:
                self._status = 'Overdued'
            elif self.hours == 0:
                if self.minutes <= 0:
                    self._status = 'Overdued'
                else:
                    self._status = 'Urgent'
            else:
                self._status = 'Urgent'
        elif self.days <= 2:
            self._status = 'Tomorrow'
        elif self.days in range(2, 7):
            self._status = '{0} days'.format(self.days)
        elif self.days == 7:
            self._status = '1 Week'
        else:
            self._status = '{0} days'.format(self.days)

        return self._status

    @property
    def status(self):
        return self._status

    @property
    def id(self):
        return self._id

    @property
    def mode(self):
        return self._mode

    @property
    def type(self):
        return self._type

    @property
    def path(self):
        return self._path

    @property
    def url(self):
        return self._url

    @property
    def start(self):
        return self._start

    @property
    def startdate(self):
        return self._startdate

    @property
    def end(self):
        return self._end

    @property
    def enddate(self):
        return self._enddate

    @property
    def starttime(self):
        return self._starttime

    @property
    def endtime(self):
        return self._endtime

    @starttime.setter
    def starttime(self, val):
        self._starttime = val

    @endtime.setter
    def endtime(self, val):
        self._endtime = val

    @enddate.setter
    def enddate(self, val):
        self._enddate = val

    @end.setter
    def end(self, val):
        self._end = val

    @startdate.setter
    def startdate(self, val):
        self._startdate = val

    @start.setter
    def start(self, val):
        self._start = val

    @url.setter
    def url(self, val):
        self._url = val

    @path.setter
    def path(self, val):
        self._path = val

    @type.setter
    def type(self, val):
        self._type = val

    @mode.setter
    def mode(self, val):
        self._mode = val

    @id.setter
    def id(self, val):
        self._id = val

    @status.setter
    def status(self, val):
        self._status = val



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 10:40 AM
# © 2017 - 2018 DAMGteam. All rights reserved