# -*- coding: utf-8 -*-
"""

Script Name: AnalogClock.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------


from pyPLM.Widgets import Widget
from pyPLM.Core import Time, Timer, Size, Point, Signal, Slot
from pyPLM.Gui import Painter, Brush, Color, Pen, Polygon
from PLM.options import ASPEC_RATIO, ANTIALIAS, NO_PEN


class AnalogClock(Widget):

    key                                 = 'DAMG Analog Clock'
    timeChanged                         = Signal(Time)
    timeZoneChanged                     = Signal(int)
    timeZoneOffset                      = 0

    def __init__(self, parent=None):
        super(AnalogClock, self).__init__(parent)

        timer = Timer(self)
        timer.timeout.connect(self.update)
        timer.timeout.connect(self.updateTime)
        timer.start(1000)

        self.setWindowTitle("Analog Clock")
        # self.setWindowFlags(FRAMELESS)

        self.hourHand                   = Polygon([Point(7, 8), Point(-7, 8), Point(0, -40)])
        self.minuteHand                 = Polygon([Point(7, 8), Point(-7, 8), Point(0, -70)])
        self.hourColor                  = Color(0, 127, 0)
        self.minuteColor                = Color(0, 127, 127, 191)

    def paintEvent(self, event):

        side                            = min(self.width(), self.height())
        time                            = Time.currentTime()
        time                            = time.addSecs(self.timeZoneOffset * 3600)

        painter                         = Painter()
        painter.begin(self)
        painter.setRenderHint(ANTIALIAS)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        painter.setPen(NO_PEN)
        painter.setBrush(Brush(self.hourColor))

        painter.save()
        painter.rotate(30.0 * (time.hour() + time.minute() / 60.0))
        painter.drawConvexPolygon(self.hourHand)
        painter.restore()

        painter.setPen(self.hourColor)

        for i in range(0, 12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)

        painter.setPen(NO_PEN)
        painter.setBrush(Brush(self.minuteColor))

        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(self.minuteHand)
        painter.restore()

        painter.setPen(Pen(self.minuteColor))

        for j in range(0, 60):
            if (j % 5) != 0:
                painter.drawLine(92, 0, 96, 0)
            painter.rotate(6.0)

        painter.end()

    def resizeEvent(self, event):
        size                    = Size(1, 1)
        size.scale(event.size(), ASPEC_RATIO)
        self.resize(size)

    def updateTime(self):
        self.timeChanged.emit(Time.currentTime())

    def getTimeZone(self):
        return self.timeZoneOffset

    @Slot(int)
    def setTimeZone(self, value):
        self.timeZoneOffset = value
        self.timeZoneChanged.emit(value)
        self.update()

    def resetTimeZone(self):
        self.timeZoneOffset = 0
        self.timeZoneChanged.emit(0)
        self.update()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:38 AM
# © 2017 - 2018 DAMGteam. All rights reserved