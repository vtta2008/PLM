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
from PLM                                import PRJ_DIR, DEFAULT_PROJECT_PATH, APP_LOG
from PLM.utils                          import get_file_path, create_datetime
from PLM.cores.models                   import SplashMonitor, Project
from PLM.options                        import ANTIALIAS, TRANSPARENT, NO_PEN, AUTO_COLOR
from PLM.configs                        import ORG_LOGO_DIR
from PLM.ui.base                        import BaseSplash
from pyPLM.loggers                      import DamgLogger
from pyPLM.Gui                          import Image, Painter, Pen
from pyPLM.Core                         import Rect, Slot, DateTime, Date, Time




class SplashUI(BaseSplash):

    key                                 = 'SplashUI'
    _running                            = False

    def __init__(self, app=None):
        super(SplashUI, self).__init__(app)

        self.app                        = app
        self.logger                     = DamgLogger(__name__, 'DEBUG', APP_LOG)
        self.start()
        worker = SplashMonitor(self)
        worker.rotate.connect(self.rotate)
        worker.start()

        # self.run_preconfig_task()

        # worker.stop_running()
        # worker.terminate()

    def run_preconfig_task(self):
        self.setText('Preconfig Projects')
        self.preconfig_projects()
        self.setPText('20')

    def preconfig_projects(self):
        projects = get_file_path(PRJ_DIR, '.projects')
        print(projects)

        if len(projects) == 0:
            self.createDefaultProjects()

    def createDefaultProjects(self):
        startdate = create_datetime(0, 0, 0, 5, 8, 2017)
        enddate = create_datetime(23, 59, 59, 5, 8, 2022)
        prj = Project('Default', 'Default', 'free', 'Default', DEFAULT_PROJECT_PATH, None, startdate, enddate)
        print(prj)
        return prj

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

        # adjust setting of painter for writing text
        painter.setPen(self.textColor)
        painter.setFont(self.currentFont)
        painter.setBrush(self.textBrushColor)

        # text line 1: current config which is being configured.
        self.writeNewText(painter, self.text, 1)

        # text line 2: the percentage of configurations progress
        self.writeNewText(painter, self.pText, 2)

        painter.end()

    @Slot(str)
    def setText(self, text):
        self._text = text

    @Slot(int)
    def setPText(self, val):
        for i in range(int(val)):
            if self.currentP < 100:
                self._currentP += 1
                self._pText = '{0}%'.format(str(self.currentP))
            else:
                self.logger.info("The number showing in Splash screen is already 100.")

    def start(self):
        if self.isHidden():
            self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = SplashUI(app)
    ui.start()
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2020 - 3:56 PM
# © 2017 - 2019 DAMGteam. All rights reserved