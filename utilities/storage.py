# -*- coding: utf-8 -*-
"""

Script Name: storage.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, os, pickle

# PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget

# Plt

from ui import uirc as rc
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

from appData import logger, APP_DATA_DIR

# -------------------------------------------------------------------------------------------------------------
""" Variables """

FILEPATH = os.path.join(APP_DATA_DIR, 'PLM.pkl')
ELEMENTS = 'elements'
LAST_ELEMENT_ID = 'last_elements_id'

# -------------------------------------------------------------------------------------------------------------
""" storage """

class Storage:
    """ Store the message. """

    def __init__(self):
        if os.path.exists(FILEPATH):
            logger.debug("Loading from {0}".format(FILEPATH))
            self.data = self._load()
        else:
            logger.debug("Fine not found, starting empty")
            self.data = {
                ELEMENTS: {},
                LAST_ELEMENT_ID: None,
            }

    def _load(self):
        """Load and migrate."""
        with open(FILEPATH, 'rb') as fh:
            data = pickle.load(fh)

        # add the media type, if not there
        for elem in data[ELEMENTS].values():
            elem.media_type = getattr(elem, 'media_type', None)

        return data

    def get_last_element_id(self):
        """Return the last stored element, None if nothing stored."""
        return self.data[LAST_ELEMENT_ID]

    def get_elements(self):
        """Return the elements."""
        elements = [element for _, element in sorted(self.data[ELEMENTS].items())]
        return elements

    def delete_elements(self, elements):
        """Remove elements from the storage."""
        logger.debug("Deleting elements: %s", elements)
        stored_elements = self.data[ELEMENTS]
        for element in elements:
            del stored_elements[element.message_id]
            if element.extfile_path is not None:
                os.remove(element.extfile_path)
        self._save()

    def add_elements(self, elements):
        """Add the new elements (or replace them) to the storage."""
        logger.debug("Adding elements: %s", elements)
        new_elements_dict = {elem.message_id: elem for elem in elements if elem.useful}
        self.data[ELEMENTS].update(new_elements_dict)
        self.data[LAST_ELEMENT_ID] = max(elem.message_id for elem in elements)
        self._save()

    def _save(self):
        """Save the data to disk."""
        # we don't want to pickle this class, but the dict itself
        logger.debug("Saving in %r", FILEPATH)
        with func.SafeSaver(FILEPATH) as fh:
            pickle.dump(self.data, fh)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 16/06/2018 - 3:22 AM
# © 2017 - 2018 DAMGteam. All rights reserved