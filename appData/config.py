# -*- coding: utf-8 -*-
"""

Script Name: config.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

try:
    from importlib import reload
except ImportError:
    pass

from core.paths import *

PLATFORM = 'Windows'
API_MINIMUM = 0.64

from core import Metadata as m

__envKey__ = m.__envKey__

from appData.scr._attr import *
from appData.scr._docs import *
from appData.scr._format import *
from appData.scr._layout import *
from appData.scr._name import *
from appData.scr._pref import *

# -------------------------------------------------------------------------------------------------------------
""" DAMG team """

__organization__ = m.__organization__
__damgSlogan__ = m.__damgSlogan__
__website__ = m.__website__
__author1__ = m.__author1__
__author2__ = m.__author2__
__Founder__ = m.__author1__
__CoFonder1__ = m.__author2__
__email1__ = m.__email1__
__email2__ = m.__email2__

# -------------------------------------------------------------------------------------------------------------
""" PipelineTool """

__project__ = m.__project__
__appname__ = m.__appname__
__appShortcut__ = m.__appShortcut__
__version__ = m.__version__
__cfgVersion__ = m.__cfgVersion__
__verType__ = m.__verType__
__reverType__ = m.__reverType__
__about__ = m.__about__
__homepage__ = m.__homepage__
__plmSlogan__ = m.__plmSlogan__
__plmWiki__ = m.__plmWiki__

# -------------------------------------------------------------------------------------------------------------
""" Server """

__serverLocal__ = m.__serverLocal__
__serverUrl__ = m.__serverUrl__
__serverCheck__ = m.__serverCheck__
__serverAutho__ = m.__serverAutho__

__google__ = m.__google__

__email__ = m.__email__

__packages_dir__ = m.__packages_dir__
__classifiers__ = m.__classifiers__
__download__ = m.__download__
__description__ = m.__description__
__readme__ = m.__readme__
__modules__ = m.__modules__
__pkgsReq__ = m.__pkgsReq__

# ----------------------------------------------------------------------------------------------------------- #

def reload_module(module):
    return reload(module)

def read_file(fileName):
    filePth = os.path.join(os.getenv(__envKey__), 'appData', 'docs', fileName)
    with open(filePth, 'r') as f:
        data = f.read()
    return data

QUESTIONS = read_file('QUESTION')
ABOUT = read_file('ABOUT')
CREDIT = read_file('CREDIT')
CODECONDUCT = read_file('CODECONDUCT')
CONTRIBUTING = read_file('CONTRIBUTING')
REFERENCE = read_file('REFERENCE')
LICENSE_MIT = read_file('LICENSE_MIT')

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:56 PM
# Pipeline manager - DAMGteam
