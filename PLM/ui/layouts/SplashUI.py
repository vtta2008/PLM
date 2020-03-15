# -*- coding: utf-8 -*-
"""

Script Name: SplashUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import ROOT

""" Import """

# Python
import os

# PLM
from PLM.configs                import (STAY_ON_TOP, FRAMELESS, bottom, center, cyan, splashImagePth,
                                        ConfigPython, ConfigUrl, ConfigApps, ConfigPipeline, ConfigIcon,
                                        ConfigAvatar, ConfigLogo, ConfigImage, ConfigEnvVar,
                                        ConfigMachine, ConfigServer, ConfigFormats, ConfigDirectory, ConfigPath)
from PLM.commons.Widgets        import SplashScreen, ProgressBar
from PLM.commons.Gui            import Pixmap



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
    _value                      = 0
    _num                        = 15


    def __init__(self, app=None):
        super(SplashUI, self).__init__()

        self.app                = app
        self.pix                = Pixmap(splashImagePth)
        self.flag               = STAY_ON_TOP
        self.progressBar        = ProgressBar(self)

        self.setPixmap(self.pix)
        self.setWindowFlag(self.flag)
        self.setWindowFlags(STAY_ON_TOP | FRAMELESS)
        self.setMask(self.pix.mask())
        self.setEnabled(False)

        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(self.num*10)
        self.progressBar.setGeometry(50, self.pix.height() - 50, self.pix.width() - 100, 20)
        self.progressBar.setTextVisible(True)
        self.progressBar.setStyleSheet(progressBar_stylesheet)

        self.updateProgress(0)
        self.show()
        self.runPreConfig()
        self.app.processEvents()

    def runPreConfig(self):

        self.iconInfo = self.run_config('Icons', ConfigIcon)
        self.appInfo = self.run_config('Installed apps', ConfigApps)
        self.urlInfo = self.run_config('Url', ConfigUrl)
        self.dirInfo = self.run_config('Directories', ConfigDirectory)
        self.pthInfo = self.run_config('Paths', ConfigPath)

        self.show_message('Pipeline Configuration')
        self.plmInfo = ConfigPipeline(self.iconInfo, self.appInfo, self.urlInfo, self.dirInfo, self.pthInfo)
        self.updateProgress(1)

        self.deviceInfo = self.run_config('Local Device', ConfigMachine)
        self.pythonInfo = self.run_config('Python', ConfigPython)
        self.avatarInfo = self.run_config('Avatars', ConfigAvatar)
        self.logoInfo = self.run_config('Logo', ConfigLogo)
        self.imageInfo = self.run_config('Images', ConfigImage)
        self.envInfo = self.run_config('Evironment Variables', ConfigEnvVar)
        self.serverInfo = self.run_config('Server', ConfigServer)
        self.formatInfo = self.run_config('Formats', ConfigFormats)

    def run_config(self, name, config, value=1):
        self.show_message('Config {0}'.format(name))
        configed = config()
        self.updateProgress(value)
        return configed

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

    @property
    def value(self):
        return self._value

    @property
    def num(self):
        return self._num

    @value.setter
    def value(self, val):
        self._value                 = val

    @num.setter
    def num(self, val):
        self._num                   = val


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2020 - 3:56 PM
# © 2017 - 2019 DAMGteam. All rights reserved