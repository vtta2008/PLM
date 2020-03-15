# -*- coding: utf-8 -*-
"""

Script Name: sys_config.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from PLM.__main__ import globalSetting

""" Import """

# Python
import os, sys, subprocess

# PLM
from bin                           import DAMG



class EnvironmentVariable(DAMG):

    key                            = 'EnvironmentVariable'
    _data                          = dict()

    for k,v in os.environ.items():
        _data[k]                   = v
    _paths                         = os.getenv('PATH')

    def __init__(self):
        super(EnvironmentVariable, self).__init__()

        pths = [p for p in os.getenv('PATH').split(';')[0:]]

        for p in pths:
            if os.path.exists(p):
                if not p in sys.path:
                    sys.path.insert(-1, p)

        self.create_envVariable('PATH', sys.path)

    def create_envVariable(self, key, value):
        try:
            os.getenv(key)
        except KeyError:
            if globalSetting.checks.report:
                print('{0} is not existed, create new environment configKey.'.format(key))
            subprocess.Popen('SetX {0} {1}'.format(key, value), shell=True).wait()
        else:
            if os.getenv(key) is None:
                if globalSetting.checks.report:
                    print('{0} has value as None, assign showLayout_new value {1}'.format(key, value))
                subprocess.Popen('SetX {0} {1}'.format(key, value), shell=True).wait()
            else:
                if os.getenv(key) != value:
                    if globalSetting.checks.report:
                        print('{0} has different value, edit to: {1}'.format(key, value))
                    subprocess.Popen('SetX {0} {1}'.format(key, value), shell=True).wait()
                else:
                    if globalSetting.checks.report:
                        print('{0} has already been set to {1}'.format(key, value))

        self.update()

    def remove_envVariable(self, envKey):
        try:
            os.getenv(envKey)
        except KeyError:
            print('EnvKeyError: {0} does not exist'.format(envKey))
            pass
        else:
            if globalSetting.checks.report:
                print('Delete environment configKey: {0}'.format(envKey))
            subprocess.Popen('REG delete HKCU\Environment /F /V {0}'.format(envKey), shell=True).wait()

        self.update()

    def update(self):
        for k, v in os.environ.items():
            self._data[k]                               = v

        self._paths                                     = os.getenv('PATH')

    def add_to_PATH(self, val):
        self.create_envVariable('PATH', sys.path.insert(-1, val))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/10/2019 - 12:18 PM
# © 2017 - 2018 DAMGteam. All rights reserved