#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: TimelineMarker.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
print("Import from modules: {file}".format(file=__name__))
print("Directory: {path}".format(path=__file__.split(__name__)[0]))
__root__ = "PLT_RT"
# -------------------------------------------------------------------------------------------------------------
""" Import """

import json
from maya import OpenMaya, OpenMayaUI, cmds, mel

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    import shiboken2 as shiboken
except:
    from PySide.QtGui import *
    from PySide.QtCore import *
    import shiboken


def mayaToQT(name):
    # Maya -> QWidget
    ptr = OpenMayaUI.MQtUtil.findControl(name)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout(name)

    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findMenuItem(name)

    if ptr is not None:
        return shiboken.wrapInstance(long(ptr), QWidget)


# -----------------------------------------------------------------------------------------------------------------

def getTimeline():
    qtTimeline = mayaToQT("timeControl1")

    # Catch Children Widgets for 2016.5
    for child in qtTimeline.children():
        if type(child) == QWidget:
            return child

    return qtTimeline


def getTimelineMenu():
    # Initialize menu
    mel.eval("updateTimeSliderMenu TimeSliderMenu;")

    qtTimelineMenu = mayaToQT("TimeSliderMenu")
    return qtTimelineMenu


def getTimelineRange():
    r = cmds.timeControl("timeControl1", query=True, ra=True)
    return range(int(r[0]), int(r[1]))


# -----------------------------------------------------------------------------------------------------------------

class TimelineMarkers(QWidget):
    def __init__(self, timeline=getTimeline()):
        super(TimelineMarkers, self).__init__(timeline)

        # Find layout
        layout = timeline.layout()

        if not layout:
            layout = QVBoxLayout(timeline)
            layout.setContentsMargins(0, 0, 0, 0)
            timeline.setLayout(layout)

        # Find / Remove old Marker Widget
        for child in timeline.children():
            if child.objectName() == "timelineMarkers":
                # Remove Menu
                child.menu.deleteLater()

                # Remove Markers
                child.removeCallbacks()
                child.deleteLater()

        # Add QWidget
        layout.addWidget(self)
        self.setObjectName("timelineMarkers")

        # Variables
        self.menu = Menu(self)

        self.start = None
        self.end = None
        self.total = None
        self.step = None

        self.initialize()
        self.addCallbacks()

    def initialize(self, *args):
        # Decode stored information
        stored = cmds.fileInfo("timelineMarkers", query=True)

        if stored:
            info = json.loads(stored[0].replace('\\"', '"'))
        else:
            info = dict()

        self.frames = info.get("frames") or []
        self.comments = info.get("comments") or []
        self.colors = info.get("colors") or []

        # Update QWidget
        self.update()

    # -------------------------------------------------------------------------------------------------------------

    def paintEvent(self, event):
        self.draw()

    def event(self, event):
        """
        Subclass the event function in order to capture the ToolTip event. The hovered frame is calculated
        and checked to see if it is marked and commented, if so the toolTip will show.
        """
        if event.type() == QEvent.ToolTip:
            QToolTip.hideText()

            # Find comment for frame at mouse pointer
            frame = int(((event.x() - (self.total * 0.005)) / self.step) + self.start)
            if frame in self.frames:
                index = self.frames.index(frame)
                comment = self.comments[index]

                QToolTip.showText(event.globalPos(), comment, self)

        return QWidget.event(self, event)

    # -------------------------------------------------------------------------------------------------------------

    def store(self):
        """
        Get all the marker information ( frames, comments and colors ) and store this with the
        fileInfo command in the maya file.
        """
        encoded = json.dumps({"frames": self.frames, "comments": self.comments, "colors": self.colors})
        cmds.fileInfo("timelineMarkers", encoded)

    # -------------------------------------------------------------------------------------------------------------

    def add(self):
        """
        Add the parsed comment and color the the selected frames in the timeline. If the frames are already
        marked this information will be overwritten.
        """
        comment = self.menu.commentL.text()
        color = self.menu.colorA.property("rgb")

        # Get selected frames
        for f in getTimelineRange():
            if not f in self.frames:
                self.frames.append(f)
                self.colors.append(color)
                self.comments.append(comment)
            else:
                index = self.frames.index(f)

                self.colors[index] = color
                self.comments[index] = comment

        self.menu.commentL.setText("")

        self.store()
        self.update()

    # -------------------------------------------------------------------------------------------------------------

    def remove(self):
        """
        Remove marker information for selected frames.
        """
        for f in getTimelineRange():
            if f in self.frames:
                index = self.frames.index(f)

                self.frames.pop(index)
                self.colors.pop(index)
                self.comments.pop(index)

        self.store()
        self.update()

    def clear(self):
        # type: () -> object
        """
        Remove all marker information.
        """
        self.frames = []
        self.colors = []
        self.comments = []

        self.store()
        self.update()

    # -------------------------------------------------------------------------------------------------------------

    def draw(self):
        """
        Take all the marker information and fill in the QWidget covering the timeline. This function will
        be called by update and paintEvent function.
        """

        # Get plt_anim range
        self.start = cmds.playbackOptions(query=True, min=True)
        self.end = cmds.playbackOptions(query=True, max=True)

        # Calculate frame width
        self.total = self.width()
        self.step = (self.total - (self.total * 0.01)) / (self.end - self.start + 1)

        # Validate marker information
        if not self.frames or not self.colors:
            return

        # Setup painter and pen
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(self.step)

        # Draw Lines for each frame
        for f, c in zip(self.frames, self.colors):
            pen.setColor(QColor(c[0], c[1], c[2], 50))

            # Calculate line position
            pos = (f - self.start + 0.5) * self.step + (self.total * 0.005)
            line = QLineF(QPointF(pos, 0), QPointF(pos, 100))

            painter.setPen(pen)
            painter.drawLine(line)

    # -------------------------------------------------------------------------------------------------------------

    def addCallbacks(self):
        """
        Add Callbacks that will clear all marker information on the timeline every time a new file is created
        or a file is opened.
        """
        self.newID = OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterNew, self.initialize)
        self.openID = OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterOpen, self.initialize)

    def removeCallbacks(self):
        """
        Remove Callbacks.
        """
        if "newID" in dir(self):      OpenMaya.MMessage.removeCallback(self.newID)
        if "openID" in dir(self):      OpenMaya.MMessage.removeCallback(self.openID)


class Menu(object):
    def __init__(self, parent, menu=getTimelineMenu()):
        # Variable
        self.menu = menu

        # Separator
        self.separatorA1 = QAction(menu)
        self.separatorA1.setSeparator(True)

        menu.addAction(self.separatorA1)

        # Comment field
        self.commentL = QLineEdit(menu)

        self.commentA = QWidgetAction(menu)
        self.commentA.setDefaultWidget(self.commentL)

        menu.addAction(self.commentA)

        # Color picker
        self.colorA = QAction(menu)
        self.colorA.setText("Pick Color")
        self.colorA.setProperty("rgb", [0, 255, 0])
        self.colorA.triggered.connect(self.picker)

        pixmap = QPixmap(12, 12)
        pixmap.fill(QColor(0, 255, 0))

        self.colorA.setIcon(QIcon(pixmap))

        menu.addAction(self.colorA)

        # Separator
        self.separatorA2 = QAction(menu)
        self.separatorA2.setSeparator(True)

        menu.addAction(self.separatorA2)

        # Add button
        self.addA = QAction(menu)
        self.addA.setText("Add Marker")
        self.addA.triggered.connect(parent.add)

        menu.addAction(self.addA)

        # Remove button
        self.removeA = QAction(menu)
        self.removeA.setText("Remove Marker")
        self.removeA.triggered.connect(parent.remove)

        menu.addAction(self.removeA)

        # Clear button
        self.clearA = QAction(menu)
        self.clearA.setText("Clear All Markers")
        self.clearA.triggered.connect(parent.clear)

        menu.addAction(self.clearA)

    # -------------------------------------------------------------------------------------------------------------

    def picker(self):
        """
        The picker will change the color of the button and will store the rgb values in a property,
        this property will be read when a marker is added via the menu.
        """
        rgbL = self.colorA.property("rgb")
        rgbQt = QColor(rgbL[0], rgbL[1], rgbL[2])

        dialog = QColorDialog.getColor(rgbQt, self.menu)
        if dialog.isValid():
            rgb = [dialog.red(), dialog.green(), dialog.blue()]

            pixmap = QPixmap(12, 12)
            pixmap.fill(QColor(rgb[0], rgb[1], rgb[2]))

            self.colorA.setProperty("rgb", rgb)
            self.colorA.setIcon(QIcon(pixmap))

    # -------------------------------------------------------------------------------------------------------------

    def deleteLater(self):
        """
        Remove all marker related QActions from the timeline menu.
        """
        self.separatorA1.deleteLater()
        self.separatorA2.deleteLater()
        self.colorA.deleteLater()
        self.commentA.deleteLater()
        self.addA.deleteLater()
        self.removeA.deleteLater()
        self.clearA.deleteLater()


# -----------------------------------------------------------------------------------------------------------------

def initialize():
    """
    Install Timeline Marker.
    """
    global markers
    markers = TimelineMarkers()


def hotkey(action):
    """
    This is a function that can be used to setup a hotkey to manage the timeline markers. There
    are three options, this is to either add, remove or clear the markers. Make sure the language
    is set to python.

    import TimelineMarker; TimelineMarker.hotkey( "add" )
    import TimelineMarker; TimelineMarker.hotkey( "remove" )
    import TimelineMarker; TimelineMarker.hotkey( "clear" )
    """
    global markers

    if not "markers" in globals().keys():
        return
    elif action == "add":
        markers.add()
    elif action == "remove":
        markers.remove()
    elif action == "clear":
        markers.clear()



        # -------------------------------------------------------------------------------------------------------------
        # END OF CODE
        # -------------------------------------------------------------------------------------------------------------
