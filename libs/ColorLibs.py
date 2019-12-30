# -*- coding: utf-8 -*-
"""

Script Name: ColorLibs.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from bin import DAMGDICT

class ColorLibs(DAMGDICT):

    key                 = 'ColorLibs'

    WHITE           = Qt.white
    LIGHTGRAY       = Qt.lightGray
    GRAY            = Qt.gray
    DARKGRAY        = Qt.darkGray
    BLACK           = Qt.black
    RED             = Qt.red
    GREEN           = Qt.green
    BLUE            = Qt.blue
    DARKRED         = Qt.darkGreen
    DARKGREEN       = Qt.darkGreen
    DARKBLUE        = Qt.darkBlue
    CYAN            = Qt.cyan
    MAGENTA         = Qt.magenta
    YELLOW          = Qt.yellow
    DARKCYAN        = Qt.darkCyan
    DARKMAGENTA     = Qt.darkMagenta
    DARKYELLOW      = Qt.darkYellow

    blush           = QColor(246, 202, 203, 255)
    petal           = QColor(247, 170, 189, 255)
    petunia         = QColor(231, 62, 151, 255)
    deep_pink       = QColor(229, 2, 120, 255)
    melon           = QColor(241, 118, 110, 255)
    pomegranate     = QColor(178, 27, 32, 255)
    poppy_red       = QColor(236, 51, 39, 255)
    orange_red      = QColor(240, 101, 53, 255)
    olive           = QColor(174, 188, 43, 255)
    spring          = QColor(227, 229, 121, 255)
    yellow          = QColor(255, 240, 29, 255)
    mango           = QColor(254, 209, 26, 255)
    cantaloupe      = QColor(250, 176, 98, 255)
    tangelo         = QColor(247, 151, 47, 255)
    burnt_orange    = QColor(236, 137, 36, 255)
    bright_orange   = QColor(242, 124, 53, 255)
    moss            = QColor(176, 186, 39, 255)
    sage            = QColor(212, 219, 145, 255)
    apple           = QColor(178, 215, 140, 255)
    grass           = QColor(111, 178, 68, 255)
    forest          = QColor(69, 149, 62, 255)
    peacock         = QColor(21, 140, 167, 255)
    teal            = QColor(24, 157, 193, 255)
    aqua            = QColor(153, 214, 218, 255)
    violet          = QColor(55, 52, 144, 255)
    deep_blue       = QColor(15, 86, 163, 255)
    hydrangea       = QColor(150, 191, 229, 255)
    sky             = QColor(139, 210, 244, 255)
    dusk            = QColor(16, 102, 162, 255)
    midnight        = QColor(14, 90, 131, 255)
    seaside         = QColor(87, 154, 188, 255)
    poolside        = QColor(137, 203, 225, 255)
    eggplant        = QColor(86, 5, 79, 255)
    lilac           = QColor(222, 192, 219, 255)
    chocolate       = QColor(87, 43, 3, 255)
    blackout        = QColor(19, 17, 15, 255)
    stone           = QColor(125, 127, 130, 255)
    gravel          = QColor(181, 182, 185, 255)
    pebble          = QColor(217, 212, 206, 255)
    sand            = QColor(185, 172, 151, 255)

    def __init__(self):
        super(ColorLibs, self).__init__()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 30/12/2019 - 13:36
# © 2017 - 2019 DAMGteam. All rights reserved