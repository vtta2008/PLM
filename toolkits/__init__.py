# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from __buildtins__                          import copyright

from appData                                import (SETTING_FILEPTH, ST_FORMAT, appIconCfg, IGNORE_ICON_NAME, right,
                                                    datetTimeStamp, WAIT_LAYOUT_COMPLETE, PRS, ELIDE_RIGHT)

from ui.SignalManager                       import SignalManager
from cores.Settings                         import Settings
from cores.Loggers                          import Loggers
from .uiUtils                               import check_preset
from utils                                  import (data_handler, get_logo_icon, get_app_icon, get_tag_icon,
                                                    get_avatar_image, )


def getSetting(parent):
    return Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], parent)

def getSignals(parent):
    return SignalManager(parent)

def getCopyright():
    return copyright()



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 6:04 AM
# © 2017 - 2018 DAMGteam. All rights reserved