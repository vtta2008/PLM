# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import pkg_resources, subprocess

all_pkgs = pkg_resources.working_set
pkg_names = sorted(["%s" % (i.key) for i in all_pkgs])
for pkg in pkg_names:
    p = subprocess.Popen('pip install {0} --upgrade --user'.format(pkg), stdout = subprocess.PIPE)
    txt = p.communicate()[0].decode('utf8')
    print(txt)



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
