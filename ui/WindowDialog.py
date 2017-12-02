# -*- coding: utf-8 -*-
"""
Script Name: WindowDialog.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to store everything for the pipeline app

"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import logging
import os
import sys
from functools import partial

from PyQt5.QtGui import *
# ------------------------------------------------------
# IMPORT PTQT5 ELEMENT TO MAKE UI
# ------------------------------------------------------
from PyQt5.QtWidgets import *

# ------------------------------------------------------
# IMPORT FROM PIPELINE TOOLS APP
# ------------------------------------------------------
from tk import appFuncs as func

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ----------------------------------------------------------------------------------------------------------- #
"""                                SUB CLASS: CUSTOM WINDOW POP UP LAYOUT                                   """


# ----------------------------------------------------------------------------------------------------------- #
class WindowDialog(QDialog):
    def __init__(self, id='Note', message=None, icon=func.getIcon('Logo'), parent=None):
        super(WindowDialog, self).__init__(parent)

        self.setWindowTitle(id)
        self.setWindowIcon(QIcon(icon))
        central_widget = QWidget(self)
        self.layout = QGridLayout(self)
        central_widget.setLayout(self.layout)

        self.buildUI(message)

    def buildUI(self, message):
        self.layout.addWidget(QLabel(message),0,0)

        self.checkBox = QCheckBox("Don't show it again")
        self.checkBox.setCheckState(False)
        self.layout.addWidget(self.checkBox,1,0,1,1)

        yesBtn = QPushButton('Yes')
        yesBtn.clicked.connect(partial(self.on_button_clicked, 'Yes'))
        self.layout.addWidget(yesBtn,1,1,1,2)

        noBtn = QPushButton('No')
        noBtn.clicked.connect(partial(self.on_button_clicked, 'No'))
        self.layout.addWidget(noBtn,1,3,1,2)

        self.setLayout(self.layout)

    def on_button_clicked(self, buttonClicked, *args):
        checkState = self.checkBox.setCheckState()
        checkBoxPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/db/sysTray.config')
        info = {}
        info["DontShowNextTime"] = checkState
        func.dataHandle('json', 'w', checkBoxPth, info)
        if not checkState:
            print "Dont do it again!!!"
        else:
            print "update!"

        if buttonClicked == 'Yes':
            return True
        else:
            return False

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = WindowDialog()
    window.show()
    sys.exit(app.exec_())