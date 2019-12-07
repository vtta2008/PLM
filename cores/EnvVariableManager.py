# -*- coding: utf-8 -*-
"""

Script Name: sys_config.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import glsetting
""" Import """

# Python
import os, subprocess

from bin import DAMG

class EnvVariableManager(DAMG):

    """
    This class is all about system environment variable, you can set showLayout_new, edit or delete or put path into PATH variable.
    This class works only at user level.
    """

    key = 'EnvVariableManager'

    _envKeys                                            = [k for k in os.environ.keys()]        # Environtment keys
    _envVals                                            = [v for v in os.environ.values()]      # Environtment variables
    _paths                                              = os.getenv('PATH').split(';')          # Paths in PATH
    _data                                               = dict()

    def __init__(self, envKey=None, envVal=None, mode='add'):

        """
        Dealing with environment variable.
        :param envKey: environment configKey.
        :param envVar: environment variable.
        """

        self.envKey                                     = envKey
        self.envVal                                     = envVal
        self.mode                                       = mode

        for key in self._envKeys:
            self._data[key]                             = os.getenv(key)

        if self.mode == 'add':
            if not self.envKey is None and not self.envVal is None:
                if glsetting.checks.report:
                    print('Adding configKey: {0} and value: {1}'.format(self.envKey, self.envVal))
                self.set_env_var(self.envKey, self.envVal)
        elif self.mode == 'remove' or self.add == 'del' or self.add == 'delete':
            if self.check_envKey(self.envKey):
                if glsetting.checks.report:
                    print('Removing configKey: {0}'.format(self.envKey))
                self.remove_env_var(self.envKey)
        elif self.mode == 'add_to_path':
            if not self.envVal is None:
                if glsetting.checks.report:
                    print('Add {0} to PATH variable.'.format(self.envVal))
                self.add_to_PATH(self.envVal)
        else:
            if glsetting.checks.report:
                print('Not recognise intention from user.')
            return

    def set_env_var(self, envKey, envVal):
        """
        Setting environment variable.
        """
        try:
            os.getenv(envKey)
        except KeyError:
            if glsetting.checks.report:
                print('{0} is not existed, create new environment configKey.'.format(envKey))
            subprocess.Popen('SetX {0} {1}'.format(envKey, envVal), shell=True).wait()
        else:
            if os.getenv(envKey) is None:
                if glsetting.checks.report:
                    print('{0} has value as None, assign showLayout_new value {1}'.format(envKey, envVal))
                subprocess.Popen('SetX {0} {1}'.format(envKey, envVal), shell=True).wait()
            else:
                if os.getenv(envKey) != envVal:
                    if glsetting.checks.report:
                        print('{0} has different value, edit to: {1}'.format(envKey, envVal))
                    subprocess.Popen('SetX {0} {1}'.format(envKey, envVal), shell=True).wait()
                else:
                    if glsetting.checks.report:
                        print('{0} has already been set to {1}'.format(envKey, envVal))

        self.register(envKey, envVal)

    def remove_env_var(self, envKey):
        """
        Remove environment variable
        """
        try:
            os.getenv(envKey)
        except KeyError:
            KeyError('Environment configKey: {0} does not exist'.format(envKey))
        else:
            if glsetting.checks.report:
                print('Delete environment configKey: {0}'.format(envKey))
            subprocess.Popen('REG delete HKCU\Environment /F /V {0}'.format(envKey), shell=True).wait()
            self.deregister(envKey)

    def register(self, envKey, envVal):
        """
        Add configKey and value into qssPths
        """
        if not envKey in self._envKeys:
            if glsetting.checks.report:
                print('append {0} to environment configKey list'.format(envKey))
            self._envKeys.append(envKey)

        if not envVal in self._envVals:
            if glsetting.checks.report:
                print('append {0} to environment value list'.format(envVal))
            self._envVals.append(envVal)

        if os.getenv(envKey) == envVal:
            if envKey in self._envKeys and envVal in self._envVals:
                if not envKey in self._data.keys() or self._data[envKey] != envVal:
                    if glsetting.checks.report:
                        print('append configKey: {0} and value: {1} into qssPths'.format(envKey, envVal))
                    self._data[envKey]                   = envVal
        else:
            if glsetting.checks.report:
                print('Key: {0}, value: {1} are already in qssPths.'.format(envKey, envVal))

    def deregister(self, envKey):
        """
        Remove environment variable.
        """
        if self.check_envKey(envKey):
            if self.check_envVal(os.getenv(envKey)):
                if glsetting.checks.report:
                    print('Remove environment value: {0}'.format(os.getenv(envKey)))

            if glsetting.checks.report:
                print('Remove environment configKey: {0}'.format(envKey))
            self._envKeys.remove(envKey)

        if envKey in self._data.keys():
            if glsetting.checks.report:
                print('Remove environment variable from qssPths.')
            self._data.pop(envKey)

    def add_to_PATH(self, val):
        """
        Add value into existing PATH
        """
        if not self.check_in_PATH(val):
            new_value = '{0};{1}'.format(val, os.getenv('PATH'))
        else:
            new_value = val

        self.set_env_var('PATH', new_value)
        self._paths.append(new_value)

    def update(self):
        """
        Update qssPths of system environment variables.
        """
        self._envKeys                                   = [k for k in os.environ.keys()]
        self._envVals                                   = [v for v in os.environ.values()]
        self._paths                                     = os.getenv('PATH').split(';')

        for key in self._envKeys:
            self._data[key]                             = os.environ[key]

        if glsetting.checks.report:
            print('Update environment variable successful.')

    def check_envKey(self, key):
        """
        Check if configKey is exist or not.
        :param key: configKey should be a string
        :return: True or False
        """
        if not key in self._envKeys:
            return False
        else:
            return True

    def check_envVal(self, val):
        """
        Check if value is exist or not.
        :param val: value should be a string
        :return: True or False
        """
        if not val in self._envVals:
            return False
        else:
            return True

    def check_in_PATH(self, envVal):
        """
        Check if value in path
        :return: True or False
        """
        if not envVal in self._paths:
            return False
        else:
            return True

    @property
    def keys(self):
        return self._envKeys

    @property
    def values(self):
        return self._envVals

    @property
    def paths(self):
        return self._paths

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/10/2019 - 12:18 PM
# © 2017 - 2018 DAMGteam. All rights reserved