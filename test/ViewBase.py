# -*- coding: utf-8 -*-
"""

Script Name: ViewBase.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore               import QSize
from utils                      import _loadConfig
from toolkits.Widgets           import GraphicView, RubberBand
from toolkits.Gui               import PainterPath, Cursor, Transform
from toolkits.Core              import Rect, QRectF
from bin                        import DAMGLIST


from appData import (sceneGraphCfg, KEY_S, KEY_F, KEY_BACKSPACE, KEY_DEL, KEY_CTRL, KEY_SHIFT, ASPEC_RATIO, NO_MODIFIER,
                     SHIFT_MODIFIER, CLOSE_HAND_CUSOR, CTRL_MODIFIER, MOUSE_LEFT, MOUSE_RIGHT, ALT_MODIFIER, MOUSE_MIDDLE,
                     ANCHOR_CENTER, ANCHOR_NO, CURSOR_ARROW, ANCHOR_UNDERMICE, ANTIALIAS,
                     ANTIALIAS_HIGH_QUALITY, ANTIALIAS_TEXT, SMOOTH_PIXMAP_TRANSFORM, NON_COSMETIC_PEN, UPDATE_FULLVIEW, SCROLLBAROFF,
                     RUBBER_REC, )



class ViewBase(GraphicView):

    key = 'ViewBase'

    gridVisToggle               = True
    gridSnapToggle              = False

    _nodeSnap                   = False

    selectedNodes               = None

    drawingConnection           = False
    currentHoveredNode          = None
    sourceSlot                  = None

    previousMouseOffset         = 0
    zoomDirection               = 0
    zoomIncr                    = 0

    currentState                = 'DEFAULT'
    pressedKeys                 = DAMGLIST()

    def __init__(self, parent=None):
        super(ViewBase, self).__init__(parent)

        self.parent             = parent
        self.config             = _loadConfig(sceneGraphCfg)

        self.setRenderHint(ANTIALIAS, self.config['antialiasing'])
        self.setRenderHint(ANTIALIAS_TEXT, self.config['antialiasing'])
        self.setRenderHint(ANTIALIAS_HIGH_QUALITY, self.config['antialiasing_boost'])
        self.setRenderHint(SMOOTH_PIXMAP_TRANSFORM, self.config['smooth_pixmap'])
        self.setRenderHint(NON_COSMETIC_PEN, True)

        self.setViewportUpdateMode(UPDATE_FULLVIEW)
        self.setTransformationAnchor(ANCHOR_UNDERMICE)
        self.setHorizontalScrollBarPolicy(SCROLLBAROFF)
        self.setVerticalScrollBarPolicy(SCROLLBAROFF)

        self.rubberband = RubberBand(RUBBER_REC, self)

    def _initRubberband(self, position):
        self.rubberBandStart = position
        self.origin = position
        self.rubberband.setGeometry(Rect(self.origin, QSize()))
        self.rubberband.show()

    def _releaseRubberband(self):
        painterPath = PainterPath()
        rect = self.mapToScene(self.rubberband.geometry())
        painterPath.addPolygon(rect)
        self.rubberband.hide()
        return painterPath

    def _focus(self):
        if self.scene().selectedItems():
            itemsArea = self._getSelectionBoundingbox()
            self.fitInView(itemsArea, ASPEC_RATIO)
        else:
            itemsArea = self.scene().itemsBoundingRect()
            self.fitInView(itemsArea, ASPEC_RATIO)

    def _getSelectionBoundingbox(self):
        bbx_min = None
        bbx_max = None
        bby_min = None
        bby_max = None

        for item in self.scene().selectedItems():
            pos = item.scenePos()
            x = pos.x()
            y = pos.y()
            w = x + item.boundingRect().width()
            h = y + item.boundingRect().height()
            # bbx min
            if bbx_min is None:
                bbx_min = x
            elif x < bbx_min:
                bbx_min = x
            # bbx max
            if bbx_max is None:
                bbx_max = w
            elif w > bbx_max:
                bbx_max = w
            # bby min
            if bby_min is None:
                bby_min = y
            elif y < bby_min:
                bby_min = y
            # bby max
            if bby_max is None:
                bby_max = h
            elif h > bby_max:
                bby_max = h
            # end if
        # end if
        bbw = bbx_max - bbx_min
        bbh = bby_max - bby_min
        return QRectF(Rect(bbx_min, bby_min, bbw, bbh))

    def _deleteSelectedNodes(self):
        selected_nodes = list()
        for node in self.scene().selectedItems():
            selected_nodes.append(node.name)
            node._remove()
        # Emit signal.
        self.signal_NodeDeleted.emit(selected_nodes)

    def _returnSelection(self):
        selected_nodes = list()
        if self.scene().selectedItems():
            for node in self.scene().selectedItems():
                selected_nodes.append(node.name)
        # Emit signal.
        self.signal_NodeSelected.emit(selected_nodes)

    def wheelEvent(self, event):
        self.currentState       = 'ZOOM_VIEW'
        self.setTransformationAnchor(ANCHOR_UNDERMICE)

        moose = event.angleDelta().y() / 120
        if moose > 0:
            zoomFactor = 1.1
        elif moose < 0:
            zoomFactor = 0.9
        else:
            zoomFactor = 1

        self.scale(zoomFactor, zoomFactor)
        self.currentState = 'DEFAULT'

    def mousePressEvent(self, event):
        # Tablet zoom
        if event.button() == MOUSE_RIGHT and event.modifiers() == ALT_MODIFIER:
            self.currentState   = 'ZOOM_VIEW'
            self.initMousePos   = event.pos()
            self.zoomInitialPos = event.pos()
            self.initMouse      = Cursor.pos()

            self.setInteractive(False)
        # Drag view
        elif (event.button() == MOUSE_MIDDLE and event.modifiers() == ALT_MODIFIER):
            self.currentState   = 'DRAG_VIEW'
            self.prevPos        = event.pos()
            self.setCursor(CLOSE_HAND_CUSOR)
            self.setInteractive(False)
        # Rubber band selection
        elif (event.button() == MOUSE_LEFT and event.modifiers() == NO_MODIFIER and self.scene().itemAt(self.mapToScene(event.pos()), Transform()) is None):
            self.currentState   = 'SELECTION'
            self._initRubberband(event.pos())
            self.setInteractive(False)
        # Drag Item
        elif (event.button() == MOUSE_LEFT and event.modifiers() == NO_MODIFIER and self.scene().itemAt(self.mapToScene(event.pos()), Transform()) is not None):
            self.currentState   = 'DRAG_ITEM'

            self.setInteractive(True)
        # Add selection
        elif (event.button() == MOUSE_LEFT and KEY_SHIFT in self.pressedKeys and KEY_CTRL in self.pressedKeys):
            self.currentState   = 'ADD_SELECTION'

            self._initRubberband(event.pos())
            self.setInteractive(False)
        # Subtract selection
        elif (event.button() == MOUSE_LEFT and event.modifiers() == CTRL_MODIFIER):
            self.currentState = 'SUBTRACT_SELECTION'

            self._initRubberband(event.pos())
            self.setInteractive(False)
        # Toggle selection
        elif (event.button() == MOUSE_LEFT and event.modifiers() == SHIFT_MODIFIER):
            self.currentState = 'TOGGLE_SELECTION'

            self._initRubberband(event.pos())
            self.setInteractive(False)
        else:
            self.currentState = 'DEFAULT'

        super(ViewBase, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.currentState == 'ZOOM_VIEW':
            offset = self.zoomInitialPos.x() - event.pos().x()

            if offset > self.previousMouseOffset:
                self.previousMouseOffset = offset
                self.zoomDirection = -1
                self.zoomIncr -= 1
            elif offset == self.previousMouseOffset:
                self.previousMouseOffset = offset
                if self.zoomDirection == -1:
                    self.zoomDirection = -1
                else:
                    self.zoomDirection = 1
            else:
                self.previousMouseOffset = offset
                self.zoomDirection = 1
                self.zoomIncr += 1

            if self.zoomDirection == 1:
                zoomFactor = 1.03
            else:
                zoomFactor = 1 / 1.03

            pBefore = self.mapToScene(self.initMousePos)
            self.setTransformationAnchor(ANCHOR_CENTER)
            self.scale(zoomFactor, zoomFactor)
            pAfter = self.mapToScene(self.initMousePos)
            diff = pAfter - pBefore

            self.setTransformationAnchor(ANCHOR_NO)
            self.translate(diff.x(), diff.y())
        # Drag canvas.
        elif self.currentState == 'DRAG_VIEW':
            offset = self.prevPos - event.pos()
            self.prevPos = event.pos()
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + offset.y())
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + offset.x())
        # RuberBand selection.
        elif self.currentState in ['SELECTION', 'ADD_SELECTION', 'SUBTRACT_SELECTION', 'TOGGLE_SELECTION']:
            self.rubberband.setGeometry(Rect(self.origin, event.pos()).normalized())

        super(ViewBase, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.currentState == '.ZOOM_VIEW':
            self.offset = 0
            self.zoomDirection = 0
            self.zoomIncr = 0
            self.setInteractive(True)
        # Drag View.
        elif self.currentState == 'DRAG_VIEW':
            self.setCursor(CURSOR_ARROW)
            self.setInteractive(True)
        # Selection.
        elif self.currentState == 'SELECTION':
            self.rubberband.setGeometry(Rect(self.origin, event.pos()).normalized())
            painterPath = self._releaseRubberband()
            self.setInteractive(True)
            self.scene().setSelectionArea(painterPath)
        # Add Selection.
        elif self.currentState == 'ADD_SELECTION':
            self.rubberband.setGeometry(Rect(self.origin, event.pos()).normalized())
            painterPath = self._releaseRubberband()
            self.setInteractive(True)
            for item in self.scene().items(painterPath):
                item.setSelected(True)
        # Subtract Selection.
        elif self.currentState == 'SUBTRACT_SELECTION':
            self.rubberband.setGeometry(Rect(self.origin, event.pos()).normalized())
            painterPath = self._releaseRubberband()
            self.setInteractive(True)
            for item in self.scene().items(painterPath):
                item.setSelected(False)
        # Toggle Selection
        elif self.currentState == 'TOGGLE_SELECTION':
            self.rubberband.setGeometry(Rect(self.origin, event.pos()).normalized())
            painterPath = self._releaseRubberband()
            self.setInteractive(True)
            for item in self.scene().items(painterPath):
                if item.isSelected():
                    item.setSelected(False)
                else:
                    item.setSelected(True)
        self.currentState = 'DEFAULT'
        super(ViewBase, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() not in self.pressedKeys:
            self.pressedKeys.append(event.key())
        if event.key() in (KEY_DEL, KEY_BACKSPACE):
            self._deleteSelectedNodes()
        if event.key() == KEY_F:
            self._focus()
        if event.key() == KEY_S:
            self._nodeSnap = True

    def keyReleaseEvent(self, event):
        if event.key() == KEY_S:
            self._nodeSnap = False

        if event.key() in self.pressedKeys:
            self.pressedKeys.remove(event.key())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 4:28 AM
# © 2017 - 2018 DAMGteam. All rights reserved