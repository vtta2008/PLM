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

SELECTABLE = QGraphicsItem.ItemIsSelectable
MOVEABLE = QGraphicsItem.ItemIsMovable
FOCUSABLE = QGraphicsItem.ItemIsFocusable
PANEL = QGraphicsItem.ItemIsPanel



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/06/2018 - 4:29 AM
# © 2017 - 2018 DAMGteam. All rights reserved