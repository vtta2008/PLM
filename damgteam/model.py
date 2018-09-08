# -*- coding: utf-8 -*-
'''

Script Name: model.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

'''
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from damgteam.base import PERSON, DOB


class FOUNDER(PERSON):

    founder                                 = 'The founder of DAMGTEAM'

    def __init__(self):
        PERSON.__init__(self)

        self._pid                           = 'PPL.0000001'

        self._lastname                      = 'Trinh'
        self._firstname                     = 'Do'
        self._aka                           = 'Jimmy'
        self._title                         = 'Mr.'

        self._name                          = '{0} {1}'.format(self._firstname, self._lastname)
        self._fullname                      = '{0} {1} {2} (a.k.a {3})'.format(self._title, self._firstname, self._lastname, self._aka)
        self._coo                           = 'Viet Nam'
        self._coc                           = 'New Zealand'
        self._artistTitle                   = 'PipelineTD'
        self._eProfile                      = 'http://dot.damgteam.com/'
        self._email                         = 'dot@damgteam.com'

        self._dob                           = DOB(1, 1, 1984).__dob__

    __profile__                             = PERSON.__dict__


class COFOUNDER(PERSON):

    coFounder                               = 'The co-founder of DAMGTEAM'

    def __init__(self):
        PERSON.__init__(self)

        self._pid                           = 'PPL.0000002'

        self._lastname                      = 'Duong'
        self._firstname                     = 'Minh Duc'
        self._aka                           = 'Up'
        self._title                         = 'Mr.'

        self._name                          = '{0} {1}'.format(self._firstname, self._lastname)
        self._fullname                      = '{0} {1} {2} (a.k.a {3})'.format(self._title, self._firstname, self._lastname, self._aka)
        self._coo                           = 'Viet Nam'
        self._coc                           = 'Australia'
        self._artistTitle                   = 'Front End Developer'
        self._eProfile                      = 'https://up209d.github.io/UPPortfolio/'
        self._email                         = 'up@damgteam.com'

        self._dob                           = DOB(20, 9, 1987).__dob__

    __profile__                             = PERSON.__dict__


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 9/09/2018 - 5:21 AM
# © 2017 - 2018 DAMGteam. All rights reserved