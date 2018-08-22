# -*- coding: utf-8 -*-
"""

Script Name: ptest.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
import subprocess
import pkg_resources

def update_python_packages():
    pkgs = [(d.project_name, d.version) for d in pkg_resources.working_set]

    for p in pkgs:
        pkg = p[0]
        print('upgrade python package: {0}'.format(pkg))
        subprocess.Popen("python -m pip install {0} --user -- upgrade".format(pkg), shell=True).wait()
        print('finished upgrade: {0}'.format(pkg))

    print('all finished')

subprocess.Popen("python -m pip install docker --user --upgrade")

import docker
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/08/2018 - 8:42 PM
# © 2017 - 2018 DAMGteam. All rights reserved