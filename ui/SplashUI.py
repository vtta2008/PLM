# -*- coding: utf-8 -*-
"""

Script Name: SplashUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import ROOT

""" Import """

# Python
import os

# PLM
from appData                    import (STAY_ON_TOP, FRAMELESS, bottom, center, cyan,
                                        ConfigPython, ConfigUrl, ConfigApps, ConfigPipeline, ConfigIcon, ConfigEnvVar,
                                        ConfigMaya, ConfigMachine, dirInfo, pthInfo)
from devkit.Widgets             import SplashScreen, ProgressBar
from devkit.Gui                 import Pixmap


class SplashUI(SplashScreen):

    key                         = 'SplashScreen'
    value                       = 0

    def __init__(self, app=None):
        super(SplashUI, self).__init__()

        self.app                = app
        self.pix                = Pixmap(os.path.join(ROOT, 'assets', 'pics', 'splash.png'))
        self.flag               = STAY_ON_TOP

        self.setPixmap(self.pix)
        self.setWindowFlag(self.flag)
        self.setWindowFlags(STAY_ON_TOP | FRAMELESS)
        self.setMask(self.pix.mask())
        self.setEnabled(False)

        self.progressBar        = ProgressBar(self)
        self.progressBar.setTextVisible(False)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setGeometry(50, self.pix.height() - 50, self.pix.width() - 100, 20)
        self.updateProgress(0)
        self.show()
        self.runPreConfig()
        self.app.processEvents()

    def runPreConfig(self):

        self.show_message("Config python.")
        self.pythonInfo          = ConfigPython()
        self.envInfo             = ConfigEnvVar()
        self.urlInfo             = ConfigUrl()
        self.mayaInfo            = ConfigMaya()
        self.updateProgress(3)

        self.show_message("Config icon.")
        self.iconInfo            = ConfigIcon()
        self.updateProgress(1)

        self.show_message("Config Installed apps.")
        self.appInfo             = ConfigApps()
        self.updateProgress(2)

        self.show_message("Config device.")
        self.deviceInfo          = ConfigMachine()
        self.updateProgress(2)

        self.show_message("Config pipeline.")
        self.plmInfo             = ConfigPipeline(self.iconInfo, self.appInfo, self.urlInfo, dirInfo, pthInfo)
        self.updateProgress(2)

    def show_message(self, mess):
        return self.showMessage(mess, bottom|center, cyan)

    def updateProgress(self, value):
        if value == 0:
            self.progressBar.setValue(0)
        else:
            value = value*10
            for i in range(value):
                self.value += 1
                self.progressBar.setValue(self.value)
                i += 1


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2020 - 3:56 PM
# © 2017 - 2019 DAMGteam. All rights reserved