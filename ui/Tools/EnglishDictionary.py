#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Name: EnglishDictionary.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    It is a very fun english dictionary.
"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import json
import os
import sys
from difflib import get_close_matches

# PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QGridLayout, QLineEdit, QTextEdit, QApplication, QWidget)

# PLM
from ui.uikits.UiPreset import Label, IconPth
from ui.uikits.Button import Button

class EnglishDictionary(QWidget):

    key = 'engDict'
    showLayout = pyqtSignal(str, str)

    def __init__(self, parent=None):

        super(EnglishDictionary, self).__init__(parent)
        self.setWindowIcon(IconPth(32, "EnglishDictionary"))

        self.layout = QGridLayout(self)
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.lineInput = QLineEdit()
        self.suggessLabel = Label()

        searchBtn   = Button({'txt': 'Translate', 'cl':self.translate})
        yesBtn      = Button({'txt': 'Yes', 'cl':self.translate})
        noBtn       = Button({'txt': 'No', 'cl':self.translate})

        self.answer = QTextEdit()

        self.layout.addWidget(self.lineInput, 0, 0, 1, 3)
        self.layout.addWidget(self.suggessLabel, 1, 0, 1, 3)
        self.layout.addWidget(searchBtn, 2, 0, 1, 1)
        self.layout.addWidget(yesBtn, 2, 1, 1, 1)
        self.layout.addWidget(noBtn, 2, 2, 1, 1)
        self.layout.addWidget(self.answer, 3, 0, 4, 3)

    def translate(self, *args):
        from appData import __envKey__
        filePth = os.path.join(os.getenv(__envKey__), 'appData', 'ED.json')
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
        blocks = ["[u'", "']", "', u'", "', u", ", u'", "['"]
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

    def hideEvent(self, event):
        pass

    def closeEvent(self, event):
        self.showLayout.emit(self.key, 'hide')
        event.ignore()

def initialize():
    app = QApplication(sys.argv)
    dictUI = EnglishDictionary()
    dictUI.show()
    app.exec_()

if __name__ == "__main__":
    initialize()