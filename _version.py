#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: {}.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
# print("Import from modules: {file}".format(file=__name__))
# print("Directory: {path}".format(path=__file__.split(__name__)[0]))
__root__ = "PLT_RT"
# -------------------------------------------------------------------------------------------------------------
""" Import """
import os
import re
import globals as gl

VERSION = os.path.join(os.getcwd(), 'appData', 'VERSION')
VERSIONLOG = os.path.join(os.getcwd(), 'docs', 'version.rst')
METADATA = os.path.join(os.getcwd(), 'appData', 'METADATA')


gl.store_default_metadata()

def get_version(projectPth):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format('__version__'), open(projectPth + '/appData/VERSION').read())
    print(result)
    return result.group(1)

def get_property(prop, projectPth):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(projectPth + '/appData/METADATA').read())
    print(result)
    return result.group(1)

