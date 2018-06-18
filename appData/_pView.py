# -*- coding: utf-8 -*-
"""

Script Name: _QgraphicsViewOpts.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem

RUBBERDRAG = QGraphicsView.RubberBandDrag
NODRAG = QGraphicsView.NoDrag

NOFRAME = QGraphicsView.NoFrame

NOANCHOR = QGraphicsView.NoAnchor
ANCHORUNDERMOUSE = QGraphicsView.AnchorUnderMouse
ANCHORVIEWCENTER = QGraphicsView.AnchorViewCenter

CACHEBACKGROUND = QGraphicsView.CacheBackground
UPDATEVIEWRECT = QGraphicsView.BoundingRectViewportUpdate

FULLVIEWUPDATE = QGraphicsView.FullViewportUpdate
BOUNDINGVIEWPORTUPDATE = QGraphicsView.BoundingRectViewportUpdate

SELECTABLE = QGraphicsItem.ItemIsSelectable
MOVEABLE = QGraphicsItem.ItemIsMovable

POSHASCHANGE = QGraphicsItem.ItemPositionChange


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/06/2018 - 4:29 AM
# © 2017 - 2018 DAMGteam. All rights reserved