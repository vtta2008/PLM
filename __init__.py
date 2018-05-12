#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
import os
# print("Import from modules: {file}".format(file=__name__))
# print("Directory: {path}".format(path=__file__.split(__name__)[0]))
__root__ = "PLT_RT"
# -------------------------------------------------------------------------------------------------------------
""" Import """
os.environ[__root__] = os.getcwd()

from pkg_resources import get_distribution, DistributionNotFound

try:
    _dist = get_distribution("PipelineTool")
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'foobar')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version


__appname__ = get_distribution("PipelineTool").name

__author__ = get_distribution("PipelineTool").author



# -------------------------------------------------------------------------------------------------------------
# Format for logging

__format1__ = "%(asctime)s %(levelname)s %(message)s"

__format2__ = "%(asctime)-15s: %(name)-18s-%(levelname)-8s-%(module)-15s-%(funcName)-20s-%(lineno)-6d-%(message)s"

# -------------------------------------------------------------------------------------------------------------