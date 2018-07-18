# -*- coding: utf-8 -*-
"""
Script Name: _setting.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPainter

POSX = 0
POSY = 0

NODE_WIDTH = 125
NODE_ROUND = 20
NODE_REC = 30
NODE_STAMP = 25

NODE_HEADER_HEIGHT = 40
NODE_FOOTER_HEIGHT = 20

ATTR_HEIGHT = 30
ATTR_ROUND = NODE_ROUND/2
ATTR_REC = NODE_REC/2

RADIUS = 10
COL = 10
ROW = 10
BLOCK = 100

FLTR = 'flow_left_to_right'
FRTL = 'flow_right_to_left'

MARGIN = 20
ROUNDNESS = 0
THICKNESS = 1
CURRENT_ZOOM = 1

# QGraphicsItem - FLAG
ITEMMOVEABLE = QGraphicsItem.ItemIsMovable
ITEMSENDGEOCHANGE = QGraphicsItem.ItemSendsGeometryChanges
ITEMSCALECHANGE = QGraphicsItem.ItemScaleChange
DEVICECACHE = QGraphicsItem.DeviceCoordinateCache
SELECTABLE = QGraphicsItem.ItemIsSelectable
MOVEABLE = QGraphicsItem.ItemIsMovable
FOCUSABLE = QGraphicsItem.ItemIsFocusable
PANEL = QGraphicsItem.ItemIsPanel

# QPainter
ANTIALIAS = QPainter.Antialiasing

# Brush: painter.setBrush()
BRUSH_NONE = Qt.NoBrush

# Pen: painter.setPen()
PEN_NONE = Qt.NoPen

# Pattern
PATTERN_SOLID = Qt.SolidPattern

# Line
LINE_SOLID = Qt.SolidLine

# Cursor
ARROW_NONE = Qt.NoArrow
CURSOR_ARROW = Qt.ArrowCursor
CURSOR_SIZEALL = Qt.SizeAllCursor

# Size
RELATIVE_SIZE = Qt.RelativeSize

# Color
WHITE = Qt.white
LIGHTGRAY = Qt.lightGray
GRAY = Qt.gray
DARKGRAY = Qt.darkGray
BLACK = Qt.black

RED = Qt.red
GREEN = Qt.green
BLUE = Qt.blue

DARKRED = Qt.darkGreen
DARKGREEN = Qt.darkGreen
DARKBLUE = Qt.darkBlue

CYAN = Qt.cyan
MAGENTA = Qt.magenta
YELLOW = Qt.yellow

DARKCYAN = Qt.darkCyan
DARKMAGENTA = Qt.darkMagenta
DARKYELLOW = Qt.darkYellow

# Keyboard
KEYBOARD = Qt.Key
KEY_ALT = Qt.Key_Alt
KEY_DEL = Qt.Key_Delete
KEY_TAB = Qt.Key_Tab

windows = os.name = 'nt'
DMK = Qt.AltModifier if windows else Qt.ControlModifier

# Mouse button
MOUSEBTN = Qt.MouseButton
MOUSE_LEFT = Qt.LeftButton
MOUSE_RIGHT = Qt.RightButton
MOUSE_MIDDLE = Qt.MiddleButton

# Scrollbar
SCROLLBAROFF = Qt.ScrollBarAlwaysOff
SCROLLBARON = Qt.ScrollBarAlwaysOn
SCROLLBARNEED = Qt.ScrollBarAsNeeded

# Scene Index
NOINDEX = QGraphicsScene.NoIndex

# Viewer
RUBBERDRAG = QGraphicsView.RubberBandDrag
POS_CHANGE = QGraphicsItem.ItemPositionChange

NODRAG = QGraphicsView.NoDrag
NOFRAME = QGraphicsView.NoFrame
NOANCHOR = QGraphicsView.NoAnchor

ANCHOR_UNDERMICE = QGraphicsView.AnchorUnderMouse
ANCHOR_VIEWCENTER = QGraphicsView.AnchorViewCenter

CACHE_BACKGROUND = QGraphicsView.CacheBackground

UPDATE_VIEWRECT = QGraphicsView.BoundingRectViewportUpdate
UPDATE_FULLVIEW = QGraphicsView.FullViewportUpdate
UPDATE_SMARTVIEW = QGraphicsView.SmartViewportUpdate
UPDATE_BOUNDINGVIEW = QGraphicsView.BoundingRectViewportUpdate
UPDATE_MINIMALVIEW = QGraphicsView.MinimalViewportUpdate

NODE = dict(

    width = NODE_WIDTH,
    height= 25,
    radius= 10,
    border= 2,
    attHeight= 30,
    con_width= 2,

    font= 'Arial',
    font_size= 12,
    attFont= 'Arial',
    attFont_size= 10,
    mouse_bounding_box= 80,

    alternate= 20,
    grid_color= [50, 50, 50, 255],
    slot_border= [50, 50, 50, 255],
    non_connectable_color= [100, 100, 100, 255],
    connection_color= [255, 155, 0, 255],
)

SCENE = dict(

    width = 2000,
    height = 2000,
    size = 36,
    antialiasing = True,
    antialiasing_boost = True,
    smooth_pixmap = True,

)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 7:50 PM
# © 2017 - 2018 DAMGteam. All rights reserved