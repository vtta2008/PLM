#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: PlayBlast.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import logging

from maya import cmds

# -------------------------------------------------------------------------------------------------------------
# MAKE MAYA UNDERSTAND QT UI AS MAYA WINDOW,  FIX PLM_VERSION CONVENTION
# -------------------------------------------------------------------------------------------------------------
# We can configure the current level to make it disable certain logs when we don't want it.
logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


# -------------------------------------------------------------------------------------------------------------
# CHECK THE CORRECT BINDING THAT BE USING UNDER QT.PY
# -------------------------------------------------------------------------------------------------------------
# While Qt.py lets us abstract the actual Qt library, there are a few things it cannot do yet
# and a few support libraries we need that we have to import manually.
# if Qt.__binding__=='PySide':
#     logger.debug('Using PySide with shiboken')
#     from shiboken import wrapInstance
#     from Maya_tk.plugins.Qt.QtCore import Signal
# elif Qt.__binding__.startswith('PyQt'):
#     logger.debug('Using PyQt with sip')
#     from sip import wrapinstance as wrapInstance
#     from Maya_tk.plugins.Qt.QtCore import pyqtSignal as Signal
# else:
#     logger.debug('Using PySide2 with shiboken2')
#     from shiboken2 import wrapInstance
#     from Maya_tk.plugins.Qt.QtCore import Signal

def gui():
    win = "Playblast"
    # If statement for window
    if (cmds.window("Playblast", exists=True)):
        cmds.deleteUI("Playblast")
        print ("Window Playblast exists, Deleted")
    cmds.window("Playblast", title="Playblast", s=False)  # the window
    cmds.rowColumnLayout(nc=1, w=200)  # layout for window
    cmds.text("Playblast Options")  # text
    cmds.separator(style='in')
    cmds.rowColumnLayout(nc=2, w=200)  # another layout
    cmds.text("Width")
    cmds.intField("WidthField", value=720)  # field to specify width
    cmds.text("Height")
    cmds.intField("HeightField", value=405)  # field to specify height
    cmds.text("Quality")
    cmds.intField("QualityField", value=65, minValue=0, maxValue=100)
    cmds.text("Show Ornaments")
    cmds.checkBox("OrnamentsCheck", label=" ")
    cmds.setParent("..")  # layout
    cmds.rowColumnLayout(nc=1, w=200)  # layout
    cmds.separator(style='in', w=200)  # separator
    cmds.text("***MAKE SELECTED CAMERA***", bgc=[0, 0.5, 1], font="boldLabelFont")  # important text
    cmds.text("*****ONLY PANEL VISIBLE******", bgc=[0, 0.5, 1], font="boldLabelFont")  # important text
    cmds.separator(style='in', w=200)  # separator
    cmds.textField("FileNameGoesHere", text="FileName")  # field for file name/directory
    cmds.button(label="Name and Location", command=NameTheFileForLater)  # okButton find directory and file name
    cmds.button(label="Playblast", command=TimeToPlayBlast)  # okButton to playblast

    cmds.showWindow("Playblast")  # show the window


def NameTheFileForLater(*args):
    ## opens a window to name where the file is going and upon saving playblasts to there
    # make the text field query-able
    cmds.textField("FileNameGoesHere", q=True, text=True)
    # Open file directory window thing
    NameOfFile = cmds.fileDialog2(fileMode=0, caption="Save Playblast To")
    # returns file directory
    TheMagicalDirectory = cmds.file(NameOfFile[0], q=True, exn=True);
    # make file directory useable as a string, removes the .* at the end
    fileNamer = TheMagicalDirectory.replace(' ', '')[:-2]
    # place the directory/file name into the text field to edit if desired
    cmds.textField("FileNameGoesHere", e=True, text=fileNamer)


def TimeToPlayBlast(*args):
    # Playblasts The Scene
    # make the text field query-able
    FileNameGoesHere = cmds.textField("FileNameGoesHere", q=True, text=True)
    # what is in the text field is now the name of the file
    NameOfFile = (FileNameGoesHere)
    # make the integer field for width query-able
    WidthField = cmds.intField("WidthField", q=True, value=True)
    # make the integer field for height query-able
    HeightField = cmds.intField("HeightField", q=True, value=True)
    # make the integer field for quality 0-100
    QualityField = cmds.intField("QualityField", q=True, value=True)
    # Make the checkbox for the show ornaments
    OrnamentsCheck = cmds.checkBox("OrnamentsCheck", q=True, value=True)
    # get ready to print the width of the play blast in the script editor
    WidthPrint = ("Width is", + WidthField)
    # get ready to print the height of the playblast in the script editor
    HeightPrint = ("Height is", +HeightField)
    # print -_ to seperate these printed statements from other commands
    QualityPrint = ("Quality is", +QualityField, "out of 100")
    print("-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_")
    # printed statement
    print("Playblasted From Selected Camera As The Following")
    # printed statement
    print("Saved To")
    # print the name and directory of the file
    print(NameOfFile)
    # print the width of the playblast
    print(WidthPrint)
    # print the height of the playblast
    print(HeightPrint)
    # print the compression and filetype
    print("H.264 Compression, QuickTime Movie")
    # printed separator
    print("-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_")
    # make active view queryable as "editor"
    editor = cmds.playblast(activeEditor=True)
    # hide all objects in view
    cmds.modelEditor(editor, edit=True, allObjects=False)
    # make polygons visible only
    cmds.modelEditor(editor, edit=True, polymeshes=True)
    # make cv's hidden
    cmds.modelEditor(editor, edit=True, cv=False)
    # make hulls hidden
    cmds.modelEditor(editor, edit=True, hulls=False)
    # make grid hidden
    cmds.modelEditor(editor, edit=True, grid=False)
    # make selected items hidden
    cmds.modelEditor(editor, edit=True, sel=False)
    # make heads up display hidden
    cmds.modelEditor(editor, edit=True, hud=False)
    # playblast from selected glsetting
    cmds.playblast(filename=FileNameGoesHere, format="qt", sequenceTime=0, clearCache=1, viewer=True,
                   showOrnaments=OrnamentsCheck, framePadding=4, percent=100, compression="H.264",
                   quality=QualityField, widthHeight=(WidthField, HeightField), forceOverwrite=True)
