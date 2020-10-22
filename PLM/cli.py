# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import re, parser, argparse
from PLM import __envKey__, __appName__, __version__
from .configs import ABOUT


def parse(pattern, metadata):
    return re.search(pattern, metadata).group(1).replace('"', '').strip()

def current_version(module_name):
    return



def entry_point():

    parser =argparse.ArgumentParser(description="Welcome to {0} CVS {0}".format(__appName__, current_version('vcs')),
                                    epilog = ABOUT)

    parser.add_argument('--verbose', '-v', action='count',
                        help='increase verbosity.  Specify multiple times '
                             'for increased diagnostic output')

    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__),
                        help = 'show the version number and exit')



    args = parser.parse_args()

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
