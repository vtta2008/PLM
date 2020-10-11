# -*- coding: utf-8 -*-
"""

Script Name: SplashUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, os
from math import sin, cos, pi

# PyQt5
from PySide2.QtWidgets                  import QApplication

# PLM
from PLM.options                        import ANTIALIAS, TRANSPARENT, NO_PEN, AUTO_COLOR
from PLM.configs                        import ORG_LOGO_DIR
from PLM.ui.base                        import BaseSplash
from bin.Gui                            import Image, Painter, Pen
from bin.Core                           import Timer, Rect, Slot

# class Worker(DAMG):
#
#     finished = Signal()
#
#     updateText = Signal(str, str)
#
#     @Slot(str, int)
#     def updateText(self, txt, ptxt):
#         """ send data to a function to change the text """
#
#         print("work started")
#         self.updateText.emit(txt, ptxt)
#         print("update finished")
#         self.finished.emit()


class SplashUI(BaseSplash):

    key                                 = 'SplashUI'
    _running                            = False

    def __init__(self, app=None):
        super(SplashUI, self).__init__(app)

        # Setup worker on a different therad than main
        # self.thread = QThread()
        # self.thread.start()

        # create worker and move it off the main thread
        # self.worker = Worker()
        # self.worker.moveToThread(self.thread)

        # Setup timer for counting
        self.timer = Timer(self)
        self.timer.timeout.connect(self.rotate)
        self.updateTimer()

    def updateTimer(self):
        self.timer.setInterval(1000 / (self.numOfitems * self.revolutionPerSec))

    @Slot()
    def rotate(self):
        self._count += 1
        if self._count > self._numOfitems:
            self._count = 0
        self.update()

    def paintEvent(self, event):

        """ start drawing animation layout """

        # setting painter for drawing
        painter = Painter()
        painter.begin(self)
        painter.setRenderHint(ANTIALIAS, True)
        painter.fillRect(event.rect(), TRANSPARENT)

        # load DAMGTEAM logo
        self.logo = Image(os.path.join(ORG_LOGO_DIR, '96x96.png'))
        self.logoRect = Rect((self.width() - self.logo.width())/2, (self.height() - self.logo.height())/2,
                             self.logo.width(), self.logo.height())

        # draw logo into layout
        painter.drawImage(self.logoRect, self.logo, self.logo.rect(), AUTO_COLOR)

        # change the setting of painter to draw animated busy loading layout
        painter.setPen(Pen(NO_PEN))

        # start a loop to draw multiple circles allocating around the logo
        for i in range(self.numOfitems):

            # calculate the distance to be able to define the position of curren circle
            distance = self.distance(i, self.count)

            # set brush color for painter
            self._brushColor = self.getBrushColor(distance, self.mainColor)
            painter.setBrush(self.brushColor)

            # start drawing a solid circle
            painter.drawEllipse(self.width() / 2 + self.innerR * cos(2 * pi * i / self.num) - (self.itemR / 2),
                                self.height() / 2 + self.innerR * sin(2 * pi * i / self.num) - (self.itemR / 2),
                                self.itemR, self.itemR)

        # # adjust setting of painter for writing text
        # painter.setPen(self.textColor)
        # painter.setFont(self.currentFont)
        # painter.setBrush(self.textBrushColor)
        #
        # # text line 1: current config which is being configured.
        # self.writeNewText(painter, self.text, 1)
        #
        # # text line 2: the percentage of configurations progress
        # self.writeNewText(painter, self.pText, 2)

        painter.end()


    @Slot(str)
    def setText(self, text):
        self._text = text


    @Slot(int)
    def setPText(self, val):
        value = val * 100 / self.num
        for i in range(int(value)):
            self._currentP += 1
            self._pText = '{0}%'.format(str(self.currentP))

            if self.currentP == 96:
                for i in range(4):
                    self._currentP += 1
                    self._pText = '{0}%'.format(str(self.currentP))


    def start(self):
        """ start counting when show """
        if self.isHidden():
            self.show()

        if not self.timer.isActive():
            print('start counting')
            self.timer.start()
            self._count = 0


    def stop(self):

        """ hide the layout and stop counting """

        print('stop counting')
        if self.timer.isActive():
            self.timer.stop()
            self._count = 0



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = SplashUI(app)
    ui.start()
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2020 - 3:56 PM
# © 2017 - 2019 DAMGteam. All rights reserved