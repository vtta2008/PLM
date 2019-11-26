#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Footer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Plt
from ui.uikits.Widget                       import Widget
from ui.uikits.GridLayout                   import GridLayout
from ui.uikits.Label                        import Label, LCDNumber
from bin.dependencies.damg.damg             import DAMGTIMER

# -------------------------------------------------------------------------------------------------------------
class DigitalClock(LCDNumber):

    key = 'DigitalClock'

    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)

        self.parent = parent
        self.setSegmentStyle(LCDNumber.Flat)
        self.setDigitCount(8)
        timer = DAMGTIMER()
        timer.setParent(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()
        self.resize(60, 20)


    def showTime(self):
        time = self.currentTime()
        text = time.toString('hh:mm:ss')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:5] + ' ' + text[6:]
        self.display(text)


# -------------------------------------------------------------------------------------------------------------
""" Footer """

class Footer(Widget):

    key                         = 'Footer'
    _name                       = 'DAMG Footer'

    tags = dict(python          = "https://docs.anaconda.com/anaconda/reference/release-notes/",
                licence         = "https://github.com/vtta2008/damgteam/blob/master/LICENCE",
                version         = "https://github.com/vtta2008/damgteam/blob/master/appData/documentations/version.rst")

    def __init__(self, buttonManager, threadManager, parent=None):
        super(Footer, self).__init__(parent)

        self.parent             = parent
        self.buttonManager      = buttonManager
        self.threadManager       = threadManager

        layout = self.buildUI()
        self.setLayout(layout)

    def buildUI(self):
        layout          = GridLayout()

        for i in range(5):
            layout.addWidget(Label({'txt': " "}), 0, i, 1, 1)
            i += 1

        for button in self.buttonManager.tagButtonsFooterWidget(self.parent):
            layout.addWidget(button, 0, i, 1, 2)
            i = i + 2

        return layout

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/06/2018 - 4:24 AM