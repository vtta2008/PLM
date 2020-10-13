# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
import os
import tempfile

from plumbum import local
from plumbum.cmd import virtualenv


def create_venv(tmp_dir=None):
    if not tmp_dir:
        tmp_dir = tempfile.mkdtemp()
    virtualenv('--no-site-packages', tmp_dir)
    return tmp_dir


def install(package_name, venv_dir):
    if not os.path.exists(venv_dir):
        venv_dir = create_venv()
    pip = '%s/bin/pip' % venv_dir
    local[pip]('install', package_name)

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
