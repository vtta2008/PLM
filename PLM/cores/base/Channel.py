# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

import os

from PLM.commons                            import DAMG
from PLM.ui.framework import ByteArray, Url
from PLM.ui.framework import NetworkRequest


class Channel(DAMG):

    """ A download channel """

    key                                     = 'Channel'

    totalSize                               = 'UnKnown'
    loadedSize                              = 'UnKnown'
    progress                                = 'UnKnown'

    noerror                                 = True
    dlaborted                               = False
    resumable                               = True

    downloadBuffer                          = ByteArray()

    _channelDir                             = None
    _fileName                               = None
    _filePath                               = None

    def __init__(self, url=None, manager=None):
        super(Channel, self).__init__(manager)

        self.networkManager                 = manager
        self._source                        = url

    def updateFilePath(self):
        if not self.filePath:
            self._filePath                  = os.path.join(self.channelDir, self.fileName)
        else:
            if not os.path.exists(self.filePath):
                self.resumable              = False
            else:
                self.resumable              = True

    def setPath(self, filePath):
        self._filePath                      = filePath
        return self._filePath

    def getRequest(self):
        return NetworkRequest(Url(self.sourceUrl))

    def notify(self, title, message, icon, delay):
        return self.networkManager.app.notifier(title, message, icon, delay)

    @property
    def sourceUrl(self):
        return self._sourceUrl

    @property
    def channelDir(self):
        return self._channelDir

    @property
    def fileName(self):
        return self._fileName

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, val):
        self._filePath                      = val

    @fileName.setter
    def fileName(self, val):
        self._fileName                      = val

    @channelDir.setter
    def channelDir(self, val):
        self._channelDir                    = val

    @sourceUrl.setter
    def sourceUrl(self, val):
        self._sourceUrl                     = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved