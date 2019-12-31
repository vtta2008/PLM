# -*- coding: utf-8 -*-
"""

Script Name: test.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from cmd import Cmd

class MyPromt(Cmd):

    prompt = 'pb> '
    intro = 'Welcome! Type ? to list commands'

    def do_exit(self, inp):
        '''exit the application.'''
        print('bye')
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        print('Default: {0}'.format(inp))

    def do_add(self, inp):
        print('Adding "{0}"'.format(inp))

    def help_add(self):
        print('Add a new entry to the system')

    do_EOF = do_exit
    help_EOF = help_exit

MyPromt().cmdloop()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:38 AM
# © 2017 - 2018 DAMGteam. All rights reserved