# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
from PyQt5.QtCore import pyqtSignal, QUrl, QUrlQuery
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest,QNetworkCookieJar


class NetworkManager(QNetworkAccessManager):
    requestFinished = pyqtSignal(QNetworkReply)

    def __init__(self):
        super().__init__()

    def finished(self, reply):
        super().finished(reply)
        self.requestFinished.emit(reply)


class Request:
    def __init__(self):
        super().__init__()

        self.network_manager = NetworkManager()
        self.network_manager.requestFinished.connect(self.request_finished)

        self.network_manager.setCookieJar(QNetworkCookieJar())

        self.url = ''
        self.cookie_url = ''

    def _read_cookie(self):
        request = QNetworkRequest(QUrl(self.cookie_url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")
        self.network_manager.get(request)

    def _post(self):
        post_data = QUrlQuery()
        post_data.addQueryItem("param1", "value")
        post_data.addQueryItem("param2", "value")

        request = QNetworkRequest(QUrl(self.url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")

        self.network_manager.post(request, post_data.toString(QUrl.FullyEncoded).toUtf8())

    def post_request(self, url, cookie_url):
        self.url = url
        self.cookie_url = cookie_url

        self._read_cookie()

    def request_finished(self, reply: QNetworkReply):
        reply.deleteLater()

        cookies = reply.header(QNetworkRequest.SetCookieHeader)
        if cookies:
            self.network_manager.cookieJar().setCookiesFromUrl(cookies, self.url)

        self._post()

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved