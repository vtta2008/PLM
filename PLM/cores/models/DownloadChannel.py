# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

import time
from PLM                                    import p
from PLM.cores.base                         import Channel
from PLM.api.Core                           import File, FileInfo, DownloadFile, IODevice
from PLM.api.Widgets                        import MessageBox
from PLM.utils                              import autoRename, wait


class DownloadChannel(Channel):

    """ Create a channel to download """

    key                                     = 'Downloader'

    def __init__(self, manager):
        super(DownloadChannel, self).__init__(manager)

        self.updateFilePath()


    def loadDownload(self, filePath, url, size, timestamp):
        """ old downloads are created when browser is opened filepath, url, size, timestamp all are str"""

        self.setPath(filePath)
        self.downloadUrl                    = url
        self.totalSize                      = size
        self.timestamp                      = timestamp
        fileInfo                            = FileInfo(self.filePath)
        self.fileName                       = fileInfo.fileName()

        if fileInfo.exists():
            self.loadedSize                 = fileInfo.size()

    def startDownload(self, filePath, networkReply):

        self.download                       = networkReply
        self.filePath                       = filePath
        self.timestamp                      = str(time.time())
        self.updateMetadata()
        self.file                           = DownloadFile(self.filePath, self)
        self.loadedSize                     = 0

        if self.file.exists():

            msgBox                          = MessageBox(self.networkManager.app.desktop(), 'File Existsed', 'warning',
                                                         p['ASK_OVERWRITE'], ['Overwrite', 'Rename'])
            if self.resumable:
                msgBox.setDefaultButton(msgBox.addBtn('Resume'))

            msgBox.exec_()

            confirm                         = msgBox.clickedButton()
            if self.resumable and confirm == msgBox.buttons['Resume']:
                self.download.abort()
                self.download.deleteLater()
                self.resumeDownload()
            elif confirm == msgBox.buttons['Overwrite']:
                self.file.resize(0)
            else:
                self._filePath               = autoRename(self.filePath)
                self.file                   = File(self.filePath)

    def retry(self):
        """ Start download from breakpoint or from beginning (if not resume supported)"""
        self.resumeDownload()

        if self.resumable:
            if str(self.loadedsize) == self.totalsize: return
        self.connect_signals()
        print('Retry: ' + self.url)

    def resumeDownload(self):

        self.file                           = DownloadFile(self.filepath, self)
        request                             = self.getRequest()
        if self.support_resume:
            self.loadedsize = self.file.size()
            if str(self.loadedsize) == self.totalsize: return
            request.setRawHeader(b'Range', 'bytes={}-'.format(self.loadedsize).encode('ascii'))
            if self.page_url: request.setRawHeader(b'Referer', self.page_url.encode('utf-8'))
        else:
            self.file.resize(0)
            self.loadedsize = 0
        self.download = self.nam.get(request)

    def dataReceived(self):
        """ Add data to download buffer whenever data from network is received """
        self.loadedsize += self.download.size()
        self.downloadBuffer += self.download.readAll()
        if self.totalsize != 'Unknown' and self.totalsize != 0:
            self.progress = "{}%".format(int((float(self.loadedsize) / int(self.totalsize)) * 100))
        else:
            self.progress = "Unknown"
        self.datachanged.emit()
        if self.downloadBuffer.size() > 307200:
            self.saveToDisk()

    def downloadStopped(self):
        """ Auto save when stops"""
        self.progress = "- - -"
        self.saveToDisk()
        self.download.deleteLater()
        wait(300)
        if self.download_aborted == False and self.noerror:
            self.notify('Download Successful', "%s \n has been downloaded successfully" % self.filename, 'crit', 300)
        self.noerror = True
        self.download_aborted = False

    def downloadfailed(self, error):  # error = 5 if cancelled
        """ at download error """
        if (error == 5):
            self.download_aborted = True
            return
        self.noerror = False
        self.notify('Download Failed', "%s \n Error : %i" % (self.filename, error), 'crit', 300)

    def updateMetadata(self):
        """ Updates download header data in download (Resume support, url, Size)"""

        # update url path
        if self.networkManager.hasRawHeader(b'Location'):
            self.downloadUrl =               str(self.download.rawHeader(b'Location'))
        else:
            self.downloadUrl                = self.download.url().toString()

        # Update total size
        if self.totalsize == 'Unknown' and self.download.hasRawHeader(b'Content-Length'):
            self.totalsize = self.download.header(1)

        # Update pause/resume support
        if self.download.hasRawHeader(b'Accept-Ranges') or self.download.hasRawHeader(b'Content-Range'):
            self.resumable = True
        else:
            self.resumable = False

    def saveToDisk(self):
        """ Appends data to file, when data is received via network"""

        self.file.open(IODevice.Append)
        self.file.write(self.downloadBuffer)
        self.downloadBuffer.clear()
        self.file.close()

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved