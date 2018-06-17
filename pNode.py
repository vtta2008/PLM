# -*- coding: utf-8 -*-
"""

Script Name: Node.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, uuid

# PyQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QPointF
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsItem

# Plt
import appData as app

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.logger

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# -------------------------------------------------------------------------------------------------------------
""" Node """

class pNode(QGraphicsItem):

    Type = QGraphicsItem.UserType + 1

    def __init__(self, graphWidget):
        super(pNode, self).__init__(graphWidget)

        self.graph = graphWidget
        self.edgeList = []
        self.newPos = QPointF()

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(1)

    def type(self):
        return self.Type

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 17/06/2018 - 2:58 PM
# © 2017 - 2018 DAMGteam. All rights reserved