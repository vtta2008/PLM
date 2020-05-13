# -*- coding: utf-8 -*-
"""

Script Name: SplashUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
from math import cos, sin, pi

# PyQt5
from PyQt5.QtWidgets                    import QApplication

# PLM
from PLM                                import globalSetting
from PLM.configs                        import (ConfigPython, ConfigUrl, ConfigApps, ConfigPipeline, ConfigIcon,
                                                ConfigAvatar, ConfigLogo, ConfigImage, ConfigEnvVar, ConfigMachine,
                                                ConfigServer, ConfigFormats, ConfigDirectory, ConfigPath, ConfigFonts,
                                                TRANSPARENT, AUTO_COLOR)
from PLM.ui.base                        import BaseSplash
from PLM.commons.Core                   import Rect



class SplashUI(BaseSplash):

    key                                 = 'SplashUI'

    def __init__(self, app=None, imagePth=None):
        super(SplashUI, self).__init__(app, imagePth)
        print(0)
        self.autoConfig()

    def paintEvent(self, event):

        self.painter.fillRect(event.rect(), TRANSPARENT)

        self.painter.begin(self)

        # Draw logo
        self.logoRect = Rect(self.width()/2 - self.logo.width()/2,
                                   self.height()/2 - self.logo.height()/2,
                                   self.logo.width(),
                                   self.logo.height())

        self.painter.drawImage(self.logoRect, self.logo, self.logo.rect(), AUTO_COLOR)

        # Draw loading animation
        self.setNoPen()

        if self.count > self.numOfitems:
            self._count                 = 0

        for i in range(self.numOfitems):

            distance                    = self.distance(i, self.count)
            self._brushColor            = self.getBrushColor(distance, self.mainColor)
            self.painter.setBrush(self.brushColor)
            self.painter.drawEllipse(self.width()/2 + self.innerRadius*cos(2*pi*i/self.num) - (self.itemRadius/2),
                                    self.height()/2 + self.innerRadius*sin(2*pi*i/self.num) - (self.itemRadius/2),
                                    self.itemRadius, self.itemRadius)

        self.setTextPen()

        x, y                            = self.getTextPos()
        self.painter.drawText(x, y, '')
        self.update()
        self.painter.drawText(x, y, self.text)
        self.update()

        x, y = self.getProgressTextPos()
        self.painter.drawText(x, y, '')
        self.update()
        self.painter.drawText(x, y, self.pText)
        self.update()

        self.painter.end()


    def autoConfig(self):

        words = ['Python', 'Directories', 'File Paths', 'Urls & Links', 'Environment Variable', 'Icons', 'Avatars',
                 'Logo', 'Images', 'Servers', 'Formats', 'Fonts', 'Local Devices', 'Installed Apps', 'Pipeline Functions']

        configs = [ConfigPython, ConfigDirectory, ConfigPath, ConfigUrl, ConfigEnvVar, ConfigIcon, ConfigAvatar,
                   ConfigLogo, ConfigImage, ConfigServer, ConfigFormats, ConfigFonts, ConfigMachine, ConfigApps,
                   ConfigPipeline]

        for i in range(len(words)):
            if not i == (len(words) - 1):
                self.setText('Config {0}'.format(words[i]))
                if i == 0:
                    self.pythonInfo = configs[i]()
                elif i == 1:
                    self.dirInfo    = configs[i]()
                elif i == 2:
                    self.pthInfo    = configs[i]()
                elif i == 3:
                    self.urlInfo    = configs[i]()
                elif i == 4:
                    self.envInfo    = configs[i]()
                elif i == 5:
                    self.iconInfo   = configs[i]()
                elif i == 6:
                    self.avatarInfo = configs[i]()
                elif i == 7:
                    self.logoInfo   = configs[i]()
                elif i == 8:
                    self.imageInfo  = configs[i]()
                elif i == 9:
                    self.serverInfo = configs[i]()
                elif i == 10:
                    self.formatInfo = configs[i]()
                elif i == 11:
                    self.fontInfo   = configs[i]()
                elif i == 12:
                    self.deviceInfo = configs[i]()
                elif i == 13:
                    self.appInfo    = configs[i]()
                self.setProgress(1)
            else:
                self.setText('Config {0}'.format('Pipeline Functions'))
                if self.iconInfo and self.appInfo and self.urlInfo and self.dirInfo and self.pthInfo:
                    self.plmInfo = ConfigPipeline(self.iconInfo, self.appInfo, self.urlInfo, self.dirInfo, self.pthInfo)
                    self.setProgress(2)
                else:
                    print('Can not conducting Pipeline Functions configurations, some of other configs has not been done yet.')
                    self.app.exit()

            self._cfgCount += 1
            self.processEvents()

        check = False

        if self.cfgCount == len(words):
            for info in [self.pythonInfo, self.dirInfo, self.pthInfo, self.urlInfo, self.envInfo, self.iconInfo,
                         self.avatarInfo, self.logoInfo, self.imageInfo, self.serverInfo, self.formatInfo,
                         self.fontInfo, self.deviceInfo, self.appInfo, self.plmInfo]:
                if not info:
                    print('{0} is None.'.format(info.key))
                    check = False
                else:
                    check = True
            # self.stopThreads()

        globalSetting.setCfgAll(check)


    def setProgress(self, val):
        value                   = (100*val)/self.num
        for i in range(int(value)):
            self._percentCount  += 1
            if self.progress:
                self.progress.setValue(self.percentCount)
            self.realtimeLoading.setProgress('{0}%'.format(str(self.percentCount)))

            if self.percentCount == 96:
                for i in range(4):
                    self._percentCount  += 1
                    if self.progress:
                        self.progress.setValue(self.percentCount)
                    self.realtimeLoading.setProgress('{0}%'.format(str(self.percentCount)))

    # def stopThreads(self):
    #     print('stop thread')
    #     self.autoThread.stop()
    #     # self.realtimeThread.stop()
    #     self.autoThread.wait()
    #     # self.realtimeThread.wait()
    #     self.killThreads()
    #     self.processEvents()
    #
    # def killThreads(self):
    #     self.autoThread.terminate()
    #     # self.realtimeThread.terminate()
    #
    # def rotate(self, bool):
    #     print(1)
    #     self.realtimeLoading.update()
    #     self.progress.update()
    #     return self.autoLoading.rotate()
    #
    # def realtimeUpdate(self, bool):
    #     return self.realtimeLoading.update()
    #
    # def updateTimmer(self):
    #     return self.timer.setInterval(1000/(self.autoLoading.numOfitems*self.autoLoading.revolutionPerSec))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ui = SplashUI(app)
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2020 - 3:56 PM
# © 2017 - 2019 DAMGteam. All rights reserved