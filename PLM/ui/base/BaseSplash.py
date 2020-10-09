# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
from math                               import ceil

from .SplashProperty                    import SplashProperty


class BaseSplash(SplashProperty):

    key                                 = 'BaseSplash'

    def __init__(self, app=None):
        super(BaseSplash, self).__init__(app)

        # setting up palatte, windows flags, splash image
        self.applySetting()

        self.fontM                      = self.fontMetrics()

        # update splash widget size due to new content
        self.updateSize()

        # after update size, need to move to center spot of the screen
        self.moveToCenter()

    def start(self):
        """ show the layout and start counting """

        self.show()

        if not self.timer.isActive():
            self.timer.start()
            self._count = 0

    def stop(self):
        """ hide the layout and stop counting """

        self.hide()

        if self.timer.isActive():
            self.timer.stop()
            self._count = 0

    def writeNewText(self, painter=None, text='', line=1):

        """ this function is to write a new text, it requires current instance painter and the content """

        # calculate the position of text
        x, y = self.getTextPos(text, line)

        # draw a blank text to earse what ever in that position
        painter.drawText(x, y, '')
        self.update()

        # write new text
        painter.drawText(x, y, text)
        self.update()

    def distance(self, current, primary):
        distance = primary - current
        if distance < 0:
            distance += self.numOfitems
        return distance

    def getBrushColor(self, distance, color):
        if distance == 0:
            return color

        minAlphaF = self.minOpacity / 100.0
        distanceThreshold = ceil((self.numOfitems - 1) * self.fadeRate / 100.0)

        if distance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff = self.mainColor.alphaF() - minAlphaF
            gradient = alphaDiff / distanceThreshold + 1.0
            resultAlpha = color.alphaF() - gradient * distance
            result = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(result)

        return color

    def getTextPos(self, text, line):

        if self.width() + (self.lMargin + self.rMargin) <= self.textW(text) or self.width() <= self.textW(text):
            self.setFixedSize(self.height() * 2, self.width() * 2)

        if self.centerW:
            x = (self.width() + self.lMargin + self.rMargin - self.textW(text))/2
        else:
            x = (self.width() + self.lMargin + self.rMargin)

        if line == 1:
            y = self.height() - self.bMargin - self.textH()
        else:
            y = self.height() - self.bMargin

        return x, y

    def textW(self, text):
        return self.fontM.width(text)

    def textH(self):
        return self.fontM.height()

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved