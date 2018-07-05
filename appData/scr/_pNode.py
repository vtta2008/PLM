# -*- coding: utf-8 -*-
"""

Script Name: _pNode.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PyQt5.QtWidgets import QGraphicsItem

ITEMMOVEABLE = QGraphicsItem.ItemIsMovable
ITEMSENDGEOCHANGE = QGraphicsItem.ItemSendsGeometryChanges
ITEMSCALECHANGE = QGraphicsItem.ItemScaleChange
DEVICECACHE = QGraphicsItem.DeviceCoordinateCache

NODE = {

    "width": 200,
    "height": 25,
    "radius": 10,
    "border": 2,
    "attHeight": 30,
    "con_width": 2,

    "font": "Arial",
    "font_size": 12,
    "attFont": "Arial",
    "attFont_size": 10,
    "mouse_bounding_box": 80,

    "alternate": 20,
    "grid_color": [50, 50, 50, 255],
    "slot_border": [50, 50, 50, 255],
    "non_connectable_color": [100, 100, 100, 255],
    "connection_color": [255, 155, 0, 255],

}
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/06/2018 - 7:15 AM
# © 2017 - 2018 DAMGteam. All rights reserved