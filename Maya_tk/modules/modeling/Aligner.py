# -*-coding:utf-8 -*

"""

Script Name: Aligner.py
Author: Do Trinh/Jimmy - TD artist

Description:

"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA MODULES
# -------------------------------------------------------------------------------------------------------------

from maya import cmds

class Aligner(object):
    
    def __init__(self):
        super(Aligner, self).__init__()

        self.buildUI()

    def buildUI(self):
        # Add radio buttons for axis

        # Add radio buttons for mode

        # Add apply button

        pass

    def onApplyClick(self, *args):
        # Get the axis

        # Get the mode

        # Call the algin function

        pass

    def align(self, nodes=None, axis='x', mode='mid', *args):
        # Default nodes to selection if not provided

        # Get the dimensions of our objects

        # Calculating the alignment point

        # Figure out the distance to the alignment point

        # Move objects to the target

        pass