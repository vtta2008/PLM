# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import subprocess
import pkg_resources

installed_packages = pkg_resources.working_set
installed = sorted(["%s" % i.key for i in installed_packages])

for p in installed:
    cmd = "pip install {0} --upgrade".format(p)
    subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=True).wait()

print('finish')

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
