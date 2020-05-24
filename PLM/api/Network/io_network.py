# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from PLM import GLobalSetting


if GLobalSetting.qtBinding == 'PyQt5':
    from PyQt5.QtNetwork    import (QNetworkAccessManager, QNetworkCookie, QNetworkCookieJar, QNetworkReply, QNetworkRequest, )
elif GLobalSetting.qtBinding == 'PySide2':
    from PySide2.QtNetwork  import (QNetworkAccessManager, QNetworkCookie, QNetworkCookieJar, QNetworkReply, QNetworkRequest, )

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved