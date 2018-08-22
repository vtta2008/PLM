# -*- coding: utf-8 -*-
'''

Script Name: main.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

'''
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import os, subprocess
ROOT = os.path.dirname(__file__).split(__name__)[0]

try:
    os.getenv('ROOT')
except KeyError:
    subprocess.Popen('SetX ROOT %CD%', shell=True).wait()
else:
    if ROOT != os.getenv('ROOT'):
        subprocess.Popen('SetX ROOT %CD%', shell=True).wait()

from api.Server import Organization

__project__             = "Pipeline Manager (Plm)"
__appname__             = "PLM"
__appShortcut__         = "Plm.ink"
__version__             = "13.0.1"
__cfgVersion__          = "0.8.6"
__verType__             = "Dev"
__reverType__           = "2"
__about__               = "About Pipeline Manager"
__homepage__            = "https://pipeline.damgteam.com"
__plmSlogan__           = "Creative your own pipeline"
__plmWiki__             = "https://github.com/vtta2008/PipelineTool/wiki"








# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/08/2018 - 12:24 AM
# © 2017 - 2018 DAMGteam. All rights reserved