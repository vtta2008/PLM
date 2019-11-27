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
import json, os, sys
from difflib                    import get_close_matches

# PyQt5
from PyQt5.QtWidgets            import QTextEdit, QApplication

# PLM
from appData                    import JSON_DIR
from toolkits.Widgets           import Widget, GridLayout, LineEdit, Label, Button

class EnglishDictionary(Widget):

    key = 'EnglishDictionary'

    with open(os.path.join(JSON_DIR, 'ED.json'), 'r') as f:
        data = json.load(f)

    def __init__(self, parent=None):
        super(EnglishDictionary, self).__init__(parent)

        self.setWindowIcon(AppIcon(32, "EnglishDictionary"))
        self.inputText = ""
        self.buildUI()

    def buildUI(self):

        self.layout             = GridLayout(self)
        self.lineInput          = LineEdit()
        self.lineInput.textChanged.connect(self.getText)

        self.suggessLabel       = Label()

        searchBtn               = Button({'txt': 'Translate', 'cl':self.btn_clicked})
        yesBtn                  = Button({'txt': 'Yes'      , 'cl':self.btn_clicked})
        noBtn                   = Button({'txt': 'No'       , 'cl':self.btn_clicked})

        self.answer             = QTextEdit()
        self.answer.setPlainText(" ")

        self.layout.addWidget(self.lineInput, 0, 0, 1, 3)
        self.layout.addWidget(self.suggessLabel, 1, 0, 1, 3)
        self.layout.addWidget(searchBtn, 2, 0, 1, 1)
        self.layout.addWidget(yesBtn, 2, 1, 1, 1)
        self.layout.addWidget(noBtn, 2, 2, 1, 1)
        self.layout.addWidget(self.answer, 3, 0, 4, 3)

        self.setLayout(self.layout)

    def getText(self, text):
        self.inputText = text

    def btn_clicked(self):
        anwser = self.translate(self.inputText.lower())
        self.answer.setPlainText(anwser)

    def translate(self, w):

        if w in self.data:
            answer = str(self.data[w])
        elif len(get_close_matches(w, self.data.keys())) > 0:
            answer = "Did you mean %s instead?" % str(get_close_matches(w, self.data.keys())[0])
            if 'Yes':
                answer = str(self.data[get_close_matches(w, self.data.keys())[0]])
            elif 'No':
                answer = "The word doesn't exist. Please double check it."
            else:
                answer = "We did not understand your entry."
        else:
            answer = "The word doesn't exist. Please double check it."

        return self.populateAnswer(answer)

    def populateAnswer(self, answer):
        blocks = ["[u'", "']", "', u'", "', u", ", u'", "['"]
        for block in blocks:
            if block in answer:
                stringToList = answer.split(block)
                answer = self.listToString(stringToList)

        return answer

    def listToString(self, stringToList, *args):
        listToString = ""
        for i in stringToList:
            listToString += i
        return listToString


def initialize():
    app = QApplication(sys.argv)
    dictUI = EnglishDictionary()
    dictUI.show()
    app.exec_()

if __name__ == "__main__":
    initialize()