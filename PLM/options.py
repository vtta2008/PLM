# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:

    Handling import to make option between PyQt5 or Pyside2. The option will be configed by global setting.
    I want make things more flexible to have more choice. But the main reason I want to have a chance to avoid some
    matter about liscening and so on, not a decision yet, but keep options available.

    Details: https://www.learnpyqt.com/blog/pyqt5-vs-pyside2/

"""
# -------------------------------------------------------------------------------------------------------------
from PLM                                 import globalSetting
from .plugins                            import Qt
from .cores                              import Loggers
from .utils

current_bindding                            = Qt.__binding__
bindingOpts                                 = globalSetting.binding_options


if globalSetting.bindingMode == 'PyQt5':
    from PyQt5 import QtWidgets, QtCore, QtGui, QtNetwork
elif globalSetting.bindingMode == 'PySide2':
    from PySide2 import QtWidgets, QtCore, QtGui, QtNetwork



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved