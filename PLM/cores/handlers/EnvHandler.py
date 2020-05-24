# -*- coding: utf-8 -*-
"""

Script Name: sys_config.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import globalSettings

""" Import """

# Python
import os, sys, subprocess

# PLM
from PLM.api.damg                          import DAMG


class EnvHandler(DAMG):

    key                                     = 'EnvHandler'
    _data                                   = {}

    for k,v in os.environ.items():
        _data[k]                            = v

    PATH                                    = os.getenv('PATH')

    def __init__(self):
        super(EnvHandler, self).__init__()

        pths = [p.replace('\\', '/') for p in self.PATH.split(';')[0:]]

        for p in pths:
            if os.path.exists(p):
                if not p in sys.path:
                    sys.path.insert(-1, p)

        self.create_envVariable('PATH', sys.path)

    def create_envVariable(self, key, value):
        try:
            os.getenv(key)
        except KeyError:
            if globalSettings.checks.report:
                print('{0} is not existed, create new environment configKey.'.format(key))
            subprocess.Popen('SetX {0} {1}'.format(key, value), shell=True).wait()
        else:
            if os.getenv(key) is None:
                if globalSettings.checks.report:
                    print('{0} has value as None, assign showLayout_new value {1}'.format(key, value))
                subprocess.Popen('SetX {0} {1}'.format(key, value), shell=True).wait()
            else:
                if os.getenv(key) != value:
                    if globalSettings.checks.report:
                        print('{0} has different value, edit to: {1}'.format(key, value))
                    subprocess.Popen('SetX {0} {1}'.format(key, value), shell=True).wait()
                else:
                    if globalSettings.checks.report:
                        print('{0} has already been set to {1}'.format(key, value))

        self.update()

    def remove_envVariable(self, envKey):
        try:
            os.getenv(envKey)
        except KeyError:
            print('EnvKeyError: {0} does not exist'.format(envKey))
            pass
        else:
            if globalSettings.checks.report:
                print('Delete environment configKey: {0}'.format(envKey))
            subprocess.Popen('REG delete HKCU\Environment /F /V {0}'.format(envKey), shell=True).wait()

        self.update()

    def update(self):
        for k, v in os.environ.items():
            self._data[k]                               = v

        self.PATH                                     = os.getenv('PATH')

    def add_to_PATH(self, val):
        self.create_envVariable('PATH', sys.path.insert(-1, val))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/10/2019 - 12:18 PM
# © 2017 - 2018 DAMGteam. All rights reserved