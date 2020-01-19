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
                                        ConfigMaya, ConfigMachine, ConfigServer, ConfigFormats, dirInfo, pthInfo)
from devkit.Widgets             import SplashScreen, ProgressBar
from devkit.Gui                 import Pixmap



progressBar_stylesheet = '''

QProgressBar {
    
    width: 20px;
    margin: 2px;
    background-color: #19232D;
    background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #fff, stop: 0.4999 #eee, stop: 0.5 #ddd, stop: 1 #eee );
    text-align: center;
    border: 2px  solid #32414B;
    border-radius: 5px;
    border-color: beige;
    

}

QProgressBar::chunk {

    border-color: #19232D;
    border: 1px solid black;
    background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #78d, stop: 0.4999 #46a, stop: 0.5 #45a, stop: 1 #238 );

}


'''



class SplashUI(SplashScreen):

    key                         = 'SplashScreen'
    value                       = 0

    def __init__(self, app=None):
        super(SplashUI, self).__init__()

        self.app                = app
        self.pix                = Pixmap(os.path.join(ROOT, 'assets', 'pics', 'splash.png'))
        self.flag               = STAY_ON_TOP
        self.progressBar        = ProgressBar(self)

        self.setPixmap(self.pix)
        self.setWindowFlag(self.flag)
        self.setWindowFlags(STAY_ON_TOP | FRAMELESS)
        self.setMask(self.pix.mask())
        self.setEnabled(False)

        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setGeometry(50, self.pix.height() - 50, self.pix.width() - 100, 20)
        self.progressBar.setTextVisible(True)
        self.progressBar.setStyleSheet(progressBar_stylesheet)

        self.updateProgress(0)
        self.show()
        self.runPreConfig()
        self.app.processEvents()

    def runPreConfig(self):

        self.show_message("Config device.")
        self.deviceInfo         = ConfigMachine()
        self.updateProgress(1)

        self.show_message("Config Format")
        self.formatInfo         = ConfigFormats()
        self.updateProgress(1)

        self.show_message("Config python.")
        self.pythonInfo          = ConfigPython()
        self.updateProgress(1)

        self.show_message('Config evnironment')
        self.envInfo             = ConfigEnvVar()
        self.updateProgress(1)

        self.show_message('Config url')
        self.urlInfo             = ConfigUrl()
        self.updateProgress(1)

        self.show_message('Config server')
        self.serverInfo         = ConfigServer()
        self.updateProgress(1)

        self.show_message('Config Maya')
        self.mayaInfo            = ConfigMaya()
        self.updateProgress(1)

        self.show_message("Config icon.")
        self.iconInfo            = ConfigIcon()
        self.updateProgress(1)

        self.show_message("Config Installed apps.")
        self.appInfo             = ConfigApps()
        self.updateProgress(1)

        self.show_message("Config pipeline.")
        self.plmInfo             = ConfigPipeline(self.iconInfo, self.appInfo, self.urlInfo, dirInfo, pthInfo)
        self.updateProgress(1)

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