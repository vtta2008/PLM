#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Footer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtWidgets                        import QApplication

# Plt
from ui.uikits.Widget                       import Widget
from ui.uikits.GridLayout                   import GridLayout
from ui.uikits.Label                        import Label, LCDNumber
from bin.data.damg                          import DAMGTIMER

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
        self.threaManager       = threadManager

        layout = self.buildUI()
        self.setLayout(layout)

        worker = self.threaManager.serviceThread()
        worker.cpu.connect(self.update_cpu_useage)
        worker.ram.connect(self.update_ram_useage)
        worker.start()

    def buildUI(self):
        layout          = GridLayout()

        for i in range(6):
            layout.addWidget(Label({'txt': " "}), 0, i, 1, 1)
            i += 1

        # i = 4
        # for button in self.buttonManager.tagButtonsFooterWidget(self.parent):
        #     layout.addWidget(button, 0, i, 1, 2)
        #     i = i + 2

        self.usage_cpu = Label({'txt': 'CPU: 0%'})
        self.usage_ram = Label({'txt': 'RAM: 0%'})
        self.clock = DigitalClock(self)
        layout.addWidget(self.usage_cpu, 0, 6, 1, 2)
        layout.addWidget(self.usage_ram, 0, 8, 1, 2)
        layout.addWidget(self.clock, 1, 7, 1, 3)

        return layout

    def update_cpu_useage(self, val):
        return self.usage_cpu.setText('CPU: {0}%'.format(val))

    def update_ram_useage(self, val):
        return self.usage_ram.setText('RAM: {0}%'.format(val))

def main():
    app = QApplication(sys.argv)
    layout = Footer()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/06/2018 - 4:24 AM