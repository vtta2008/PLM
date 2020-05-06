# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
from PyQt5 import QtNetwork, QtCore, QtGui
from PyQt5.QtCore import QCoreApplication, QUrl
import sys, json


class TestInternet:

    def __init__(self):

        self.doRequest()

    def doRequest(self):

        url = "http://localhost:20987/"
        req = QtNetwork.QNetworkRequest(QUrl(url))

        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.get(req)


    def handleResponse(self, reply):

        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:
            bytes_string = reply.readAll()
            print(str(bytes_string, 'utf-8'))
        else:
            print("Error occured: ", er)
            print(reply.errorString())

        QCoreApplication.quit()


class TestRequest:

    def __init__(self):

        self.doRequest()

    def doRequest(self):

        data = QtCore.QByteArray()
        data.append("name=Peter&")
        data.append("age=34")

        url = "https://httpbin.org/post"
        req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")

        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.post(req, data)

    def handleResponse(self, reply):

        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:

            bytes_string = reply.readAll()

            json_ar = json.loads(str(bytes_string, 'utf-8'))
            data = json_ar['form']

            print('Name: {0}'.format(data['name']))
            print('Age: {0}'.format(data['age']))

            print()

        else:
            print("Error occurred: ", er)
            print(reply.errorString())

        QtCore.QCoreApplication.quit()


class TestAuthentication:

    def __init__(self):

        self.doRequest()

    def doRequest(self):

        self.auth = 0

        url = "https://httpbin.org/basic-auth/user7/passwd7"
        req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))

        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.authenticationRequired.connect(self.authenticate)
        self.nam.finished.connect(self.handleResponse)
        self.nam.get(req)

    def authenticate(self, reply, auth):

        print("Authenticating")

        self.auth += 1

        if self.auth >= 3:
            reply.abort()

        auth.setUser("user7")
        auth.setPassword("passwd7")

    def handleResponse(self, reply):

        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:

            bytes_string = reply.readAll()

            data = json.loads(str(bytes_string, 'utf-8'))

            print('Authenticated: {0}'.format(data['authenticated']))
            print('User: {0}'.format(data['user']))

            print()

        else:
            print("Error occurred: ", er)
            print(reply.errorString())

        QtCore.QCoreApplication.quit()




app = QCoreApplication([])
ex = TestInternet()
sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved