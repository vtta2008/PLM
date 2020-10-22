# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:

    Generates a dictionary of ANSI escape codes.

    http://en.wikipedia.org/wiki/ANSI_escape_code

    Uses colorama as an optional dependency to support color on Windows

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

try:
    import colorama
except ImportError:
    pass
else:
    colorama.init(strip=False)


def esc(*x):
    return '\033[' + ';'.join(x) + 'm'


# The initial list of escape codes
escape_codes = {'reset': esc('0'), 'bold': esc('01'), 'thin': esc('02')}


# The color names
COLORS = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white']


            # Foreground without prefix
PREFIXES = [('3', ''), ('01;3', 'bold_'), ('02;3', 'thin_'),

            # Foreground with fg_ prefix
            ('3', 'fg_'), ('01;3', 'fg_bold_'), ('02;3', 'fg_thin_'),

            # Background with bg_ prefix - bold/light works differently
            ('4', 'bg_'), ('10', 'bg_bold_'), ]


def parse_colors(sequence):
    """Return escape codes from a color sequence."""
    # print('Get input sequence: ', sequence, type(sequence))
    try:
        ''.join(escape_codes[n] for n in sequence.split(',') if n)
    except KeyError:
        # print('getting keyerror here')
        # print('sequence: ', sequence)
        # print('type: ', type(sequence))
        # print("split ','", sequence.split(','))
        pass


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
