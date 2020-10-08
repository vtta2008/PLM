# -*- coding: utf-8 -*-
"""

Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    In this directory resides our test suite. I'm not gonna go into too much detail here as we will dedicate whole
    section to testing, but just briefly:

    1. test_app.py is a test file corresponding to app.py in source directory
    2. conftest.py is probably familiar to you if you ever used Pytest - it's a file used for specifying Pytest
        fixtures, hooks or loading external plugins.
    3. context.py helps with imports of source code files from blueprint directory by manipulating class path.
        We will see how that works in sec.

"""
# -------------------------------------------------------------------------------------------------------------

import pkg_resources, subprocess

PIPE = subprocess.PIPE

installed_packages = pkg_resources.working_set

installed_packages_list = sorted(["%s" % (i.key) for i in installed_packages])


for pkg in installed_packages_list:
    print('start upgrade {0}'.format(pkg))
    subprocess.Popen('python -m pip install {0} --user --upgrade'.format(pkg), stdout=PIPE, stderr=PIPE, shell=True).wait()
    print('-----------------------------------------------------------------------------------------------------')

    print('finished')

print('done')

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:11 PM
# © 2017 - 2019 DAMGteam. All rights reserved