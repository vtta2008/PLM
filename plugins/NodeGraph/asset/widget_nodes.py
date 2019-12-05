# -*- coding: utf-8 -*-
"""

Script Name: widget_nodes.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from plugins.NodeGraph import BaseNode

class DropdownMenuNode(BaseNode):
    """
    An example node with a embedded added QCombobox menu.
    """

    # unique node identifier.
    __identifier__ = 'com.chantasticvfx'

    # initial default node name.
    NODE_NAME = 'menu'

    def __init__(self):
        super(DropdownMenuNode, self).__init__()

        # create input & output ports
        self.add_input('hello')
        self.add_output('world')
        self.add_output('out A')

        # create the QComboBox menu.
        items = ['item 1', 'item 2', 'item 3']
        self.add_combo_menu('my_menu', 'Menu Test', items=items)


class TextInputNode(BaseNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'com.chantasticvfx'

    # initial default node name.
    NODE_NAME = 'text'

    def __init__(self):
        super(TextInputNode, self).__init__()

        # create input & output ports
        self.add_input('in')
        self.add_output('out')

        # create QLineEdit text input widget.
        self.add_text_input('my_input', 'Text Input', tab='widgets')


class CheckboxNode(BaseNode):
    """
    An example of a node with 2 embedded QCheckBox widgets.
    """

    # set a unique node identifier.
    __identifier__ = 'com.chantasticvfx'

    # set the initial default node name.
    NODE_NAME = 'checkbox'

    def __init__(self):
        super(CheckboxNode, self).__init__()

        # create the checkboxes.
        self.add_checkbox('cb_hello', '', 'Hello', True)
        self.add_checkbox('cb_world', '', 'World', False)

        # create input and output port.
        self.add_input('in', color=(200, 100, 0))
        self.add_output('out', color=(0, 100, 200))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/12/2019 - 7:17 PM
# © 2017 - 2018 DAMGteam. All rights reserved