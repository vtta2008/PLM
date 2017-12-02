# -*- coding: utf-8 -*-
"""
Script Name: englishDict.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    It is a very fun english dictionary.

"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import json
import logging
import os
import sys
from difflib import get_close_matches

# -------------------------------------------------------------------------------------------------------------
# IMPORT PTQT5 ELEMENT TO MAKE UI
# -------------------------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import *

from tk import appFuncs as func

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


class EnglishDict(QDialog):
    def __init__(self):

        super(EnglishDict, self).__init__()

        self.setWindowTitle('English Dictionary')
        self.setWindowIcon(func.getIcon('Logo'))

        self.buildUI()

        # self.setCentralWidget(self.layout)

        self.setContentsMargins(5, 5, 5, 5)

    def buildUI(self):

        self.layout = QGroupBox(self)
        self.layout.setWindowTitle('English Dictionary')

        hbox = QHBoxLayout()

        GridLayout = QGridLayout()

        self.lineInput = QLineEdit()

        self.suggessLabel = QLabel()

        searchBtn = QPushButton('Translate')
        searchBtn.clicked.connect(self.translate)

        yesBtn = QPushButton('Yes')
        yesBtn.clicked.connect(self.translate)

        noBtn = QPushButton('No')
        noBtn.clicked.connect(self.translate)

        self.answer = QTextEdit()

        GridLayout.addWidget(self.lineInput, 0, 0, 1, 3)
        GridLayout.addWidget(self.suggessLabel, 1, 0, 1, 3)
        GridLayout.addWidget(searchBtn, 2, 0, 1, 1)
        GridLayout.addWidget(yesBtn, 2, 1, 1, 1)
        GridLayout.addWidget(noBtn, 2, 2, 1, 1)
        GridLayout.addWidget(self.answer, 3, 0, 4, 3)

        hbox.addLayout(GridLayout)

        self.layout.setLayout(hbox)

    def translate(self, *args):
        filePth = os.path.join(os.getcwd().split('ui')[0], os.path.join('sql_tk', 'englishDictionary.json'))

        data = json.load(open(filePth))

        w = self.lineInput.text().lower()

        if w in data:
            answer = str(data[w])
        elif len(get_close_matches(w, data.keys())) > 0:
            answer = "Did you mean %s instead?" % str(get_close_matches(w, data.keys())[0])
            if 'Yes':
                answer = str(data[get_close_matches(w, data.keys())[0]])
            elif 'No':
                answer = "The word doesn't exist. Please double check it."
            else:
                answer = "We did not understand your entry."
        else:
            answer = "The word doesn't exist. Please double check it."

        self.populateAnswer(answer)

    def populateAnswer(self, answer, *args):

        blocks = ["[u'", "']", "', u'", "', u", ", u'"]

        for block in blocks:
            if block in answer:
                stringToList = answer.split(block)
                answer = self.listToString(stringToList)

        self.answer.setPlainText("%s" % answer)

    def listToString(self, stringToList, *args):

        listToString = ""

        for i in stringToList:
            listToString += i

        return listToString


def initialize():
    app = QApplication(sys.argv)
    dictUI = EnglishDict()
    dictUI.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    initialize()
