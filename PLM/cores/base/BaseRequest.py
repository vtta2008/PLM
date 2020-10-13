# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

import time

from PLM.utils import is_url, format_bytes, bytes2str
from bin.Network import NetworkRequest, NetworkReply, NetworkCookie, NetworkCookieJar
from bin.Core import Url
from bin.loggers import DamgLogger


class HTTPrequest(NetworkRequest):

    key                                     = 'HTTPrequest'

    def __init__(self, manager=None, url=None, header=False, opt=None):
        super(HTTPrequest, self).__init__(url)

        self.logger                         = DamgLogger(self)
        self.networkManager                 = manager
        self.header                         = header
        self.urlInfo                        = self.networkManager.app.urlInfo

        # start request
        start = time.time()
        self.logger.info('start recording time')

        if not is_url(url):
            if not is_url(self._link):
                self._link                  = self.urlInfo['google']
        else:
            self._link                      = url

        self.setUrl(Url(self.link))

        if self.header:
            self.setHeader(self.ContentTypeHeader, self.header)

        self.networkManager.finished.connect(self.response)
        self.networkManager.get(self)

        end = time.time()
        self.duration = end - start

        # finish dowload
        self.logger.info('stop recording time: {0}'.format(self.duration))


    def response(self, reply):
        err = reply.error()
        if err == NetworkReply.NoError:
            output = reply.readAll()
        else:
            output = reply.errorString()

        self.dataSize, result = format_bytes(output)
        self.logger.info('Download: {0}'.format(self.dataSize))
        reply.deleteLater()

        return bytes2str(output), result

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, val):
        self._link                          = val


class CookieRequest(NetworkRequest):

    key                                     = 'CookieRequest'

    def __init__(self, manager=None, server=None, verify=None, header=None, cookie=None):
        super(CookieRequest, self).__init__(server)

        self.logger                         = test_logger(self)
        self.networkManager                 = manager
        self.serverInfo                     = self.networkManager.app.serverInfo
        self._server                        = server
        self.verify                         = verify
        self.header                         = header
        self.cookie                         = cookie

        # start request
        start                               = time.time()
        self.logger.info('start recording time')
        self.setUrl(Url(self.server))
        if self.header:
            self.setHeader(self.ContentTypeHeader, self.header)

        if self.cookie:
            cookie                          = NetworkCookie(self.cookie)
            cookieJar                       = NetworkCookieJar()
            cookieJar.insertCookie(cookie)
            self.networkManager.setCookieJar(cookieJar)

        self.networkManager.finished.connect(self.response)
        self.networkManager.get(self)
        # End request
        end                                 = time.time()
        self.duration                       = end - start

    def response(self, reply):

        err = reply.error()
        if err == NetworkReply.NoError:
            output = reply.readAll()
        else:
            output = reply.errorString()

        self.dataSize, result = format_bytes(output)
        self.logger.info('Download: {0}'.format(self.dataSize))
        reply.deleteLater()

        return bytes2str(output), result

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, val):
        self._server                        = val


class AuthRequest(NetworkRequest):

    key                                     = 'AuthRequest'
    cookieUrl                               = ''

    def __init__(self, manager=None, server=None, username=None, password=None):
        super(AuthRequest, self).__init__(server)

        self.auth                           = 0
        self.logger                         = test_logger(self)
        self.networkManager                 = manager
        self.serverInfo                     = self.networkManager.app.serverInfo
        self.username                       = username
        self.password                       = password
        self._server                        = server

        # start request
        start                               = time.time()
        self.logger.info('start recording time')
        self.setUrl(Url(self.server))
        self.setHeader(self.ContentTypeHeader)

        self.networkManager.setCookieJar(NetworkCookieJar())
        self.networkManager.authenticationRequired.connect(self.authenticate)
        self.networkManager.finished.connect(self.response)
        self.networkManager.get(self)

        # End request
        end                                 = time.time()
        self.duration                       = end - start

    def authenticate(self, reply, auth):

        self.logger.info("Authenticating")

        self.auth += 1
        if self.auth >= 3:
            reply.abort()

        auth.setUser(self.username)
        auth.setPassword(self.password)

        cookies                             = reply.header(self.SetCookieHeader)
        if cookies:
            self.networkManager.cookieJar().setCookiesFromUrl(cookies, self.server)


    def response(self, reply):

        err = reply.error()
        if err == NetworkReply.NoError:
            output = reply.readAll()
        else:
            output = reply.errorString()

        self.dataSize, result = format_bytes(output)
        self.logger.info('Download: {0}'.format(self.dataSize))
        reply.deleteLater()

        return bytes2str(output), result

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, val):
        self._server = val


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved