# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from pyPLM.Widgets                  import LCDNumber
from pyPLM.Core                     import Timer


class DigitalClock(LCDNumber):

    key = 'DigitalClock'

    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)

        self.parent = parent
        self.setSegmentStyle(LCDNumber.Flat)
        self.setDigitCount(8)
        timer = Timer()
        timer.setParent(self.parent)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()
        # self.resize(70, 20)

    def showTime(self):
        time = self.currentTime()
        text = time.toString('hh:mm:ss')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:5] + ' ' + text[6:]
        self.display(text)


class DigitalDate(LCDNumber):

    key = 'DigitalDate'

    def __init__(self, parent=None):
        super(DigitalDate, self).__init__(parent)

        self.parent = parent
        self.setSegmentStyle(LCDNumber.Flat)
        self.setDigitCount(8)
        timer = Timer()
        timer.setParent(self.parent)
        timer.timeout.connect(self.showdate)
        timer.start(1000)
        self.showdate()
        # self.resize(70, 20)

    def showdate(self):
        date = self.currentDate()
        text = date.toString('dd/MM/yy')
        self.display(text)




# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
