# -*- coding: utf-8 -*-
"""

Script Name: setup.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script will build executable file.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import setuptools

from PLM import __appName__, __version__


setuptools.setup(
    name=__appName__,
    version=__version__,
    description='Does stuff',
    url='https://github.com/me/myproject',
    packages=['myproject'],
    entry_points={
        'console_scripts': ['my-script = myproject.cli:entry_point'],
    },
)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved