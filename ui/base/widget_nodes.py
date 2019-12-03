# -*- coding: utf-8 -*-
"""

Script Name: widget_nodes.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from plugins.NodeGraph.base.node import BaseNode


class DropdownMenuNode(BaseNode):

    __identifier__ = 'com.chantasticvfx'

    NODE_NAME = 'menu'

    def __init__(self):
        super(DropdownMenuNode, self).__init__()

        self.add_input('hello')
        self.add_output('world')
        self.add_output('out A')

        items = ['item 1', 'item 2', 'item 3']
        self.add_combo_menu('my_menu', 'Menu Test', items=items)


class TextInputNode(BaseNode):

    __identifier__ = 'com.chantasticvfx'

    NODE_NAME = 'text'

    def __init__(self):
        super(TextInputNode, self).__init__()

        self.add_input('in')
        self.add_output('out')
        self.add_text_input('my_input', 'Text Input', tab='widgets')


class CheckboxNode(BaseNode):
    __identifier__ = 'com.chantasticvfx'
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
# Created by panda on 4/12/2019 - 3:30 AM
# © 2017 - 2018 DAMGteam. All rights reserved