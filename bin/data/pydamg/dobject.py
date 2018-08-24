# -*- coding: utf-8 -*-
"""

Script Name: dobject.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import json

from bin.data.pydamg.build import DObj, DDict

from bin.data.pydamg.registry import ClassRegistry

damgteam    = ClassRegistry('damg').register
damgAssets  = ClassRegistry('assets').register
thefounder     = ClassRegistry('founder').register
thecoFounder   = ClassRegistry('coFounder').register

__all__ = ['damgteam', 'damgAssets', 'thecoFounder', 'thefounder', 'DAMG_SERVER', 'DAMG_COPYRIGHT', 'DAMG_VERSION',
           'DAMGTEAM', 'JimJim', 'DucDM', ]

class DAMG_VERSION(object):

    _id                     = "VER"
    _objname                = "VERSION"
    _name                   = "Version"
    _data                   = DDict()

    def __init__(self):
        super(DAMG_VERSION, self).__init__()

        self._version = "13.0.1"
        self._plugin_version = "DAMG.13.cfg.0.1"
        self._api_major_version = 0.69
        self._api_revision = 0
        self._api_version = float('{0}{1}'.format(self._api_major_version, self._api_revision))
        self._api_version_as_string = '%.02f.%d' % (self._api_major_version, self._api_revision)

    @property
    def data(self):
        self._data.add_item('version', self._version)
        self._data.add_item('plugin version', self._plugin_version)
        self._data.add_item('api version', self._api_version_as_string)
        return self._data

    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name:self.data}, indent=4)

    def __version__(self):
        return self._version

    def __plugin_version__(self):
        return self._plugin_version

    def __api_version__(self):
        return self._api_version_as_string

    @property
    def version(self):
        return self._version

    @property
    def plugin_version(self):
        return self._plugin_version

    @property
    def api_version(self):
        return self._api_version

    @property
    def api_version_as_string(self):
        return self._api_version_as_string

    @property
    def api_major_version(self):
        return self._api_major_version

    @property
    def api_revision(self):
        return self._api_revision

    __dict__ = _data

class DAMG_SERVER(object):

    _id                     = "SV"
    _name                   = "Damg server"
    _objname                = "SERVER"
    _data                   = DDict()

    def __init__(self):
        super(DAMG_SERVER, self).__init__()

        self._url           = "https://pipeline.damgteam.com"
        self._check         = "https://pipeline.damgteam.com/check"
        self._autho         = "https://pipeline.damgteam.com/auth"

    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name:self.data}, indent=4)

    @property
    def data(self):
        self._data.add_item('url', self._url)
        self._data.add_item('check', self._check)
        self._data.add_item('autho', self._autho)

        return self._data

    @property
    def url(self):
        return self._url

    @property
    def check(self):
        return self._check

    @property
    def autho(self):
        return self._autho

    __dict__ = _data

class DAMG_COPYRIGHT(object):

    _id                 = "(c)"
    _name               = "DAMG copyright"
    _objname            = "copyright (c)"
    _data               = DDict()

    def __init__(self, parent):
        super(DAMG_COPYRIGHT, self).__init__()
        self._parent            = parent
        self._year_start        = "2017"
        self._status            = "Continuing"
        self._year_end          = "2018"
        self._copyright         = "Copyright (c) {0} - {1} {2}. All Rights Reserved".format(self._year_start, self._year_end, self._parent._objname)

    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name:self.data}, indent=4)

    def __copyright__(self):
        return self._copyright

    @property
    def data(self):

        self._data.add_item('name', self._name)
        self._data.add_item('id', self._id)
        self._data.add_item('start', self._year_start)
        self._data.add_item('end', self._year_end)
        self._data.add_item('status', self._status)
        self._data.add_item('copyright', self._copyright)

        return self._data

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def yearstart(self):
        return self._year_start

    @property
    def yearend(self):
        return self._year_end

    @property
    def status(self):
        return self._status

    @property
    def copyright(self):
        return self._copyright

    __dict__ = _data

class JimJim(object):

    founder             = "The founder of DAMGTEAM"
    _id                 = "JimJim"
    _name               = "Trinh Do (a.k.a Jimmy)"
    _objname            = "Founder"
    _data               = DDict()

    def __init__(self):
        super(JimJim, self).__init__()

        self._eProfile  = "http://dot.damgteam.com/"
        self._title     = "PipelineTD"
        self._email     = "dot@damgteam.com"
        self._dob       = None

    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name:self.data}, indent=4)

    @property
    def data(self):
        self._data.add_item('name', self._name)
        self._data.add_item('id', self._id)
        self._data.add_item('title', self._title)
        self._data.add_item('DOB', self._dob)
        self._data.add_item('email', self._email)
        self._data.add_item('eProfile', self._eProfile)

        return self._data

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def title(self):
        return self._title

    @property
    def dob(self):
        return self._dob

    @property
    def eProfile(self):
        return self._eProfile

    @property
    def profile(self):
        return self.__dict__

@thecoFounder
class DucDM(object):

    coFounder           = "The co-founder of DAMGTEAM"
    _id                 = "DUCDM"
    _name               = "Duong Minh Duc (a.k.a Up)"
    _objname            = "co-Founder"
    _data               = DDict()

    def __init__(self):
        super(DucDM, self).__init__()

        self._eProfile  = "https://up209d.github.io/UPPortfolio/"
        self._title     = "Front End Developer"
        self._email     = "up@damgteam.com"
        self._dob       = None

    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name:self.data}, indent=4)

    @property
    def data(self):
        self._data.add_item('name', self._name)
        self._data.add_item('title', self._title)
        self._data.add_item('DOB', self._dob)
        self._data.add_item('email', self._email)
        self._data.add_item('eProfile', self._eProfile)

        return self._data

    @property
    def email(self):
        return self._email

    @property
    def title(self):
        return self._title

    @property
    def dob(self):
        return self._dob

    @property
    def eProfile(self):
        return self._eProfile

    @property
    def profile(self):
        return self.__dict__

    __dict__ = _data

dolsm = JimJim()
duclsm = DucDM()

@damgteam
class DAMGTEAM(object):

    _id                         = "DAMG"
    _name                       = "DAMGTEAM"
    _objname                    = "DAMGTEAM"
    _data                       = DDict()
    damg                        = _name
    _envKey                     = "DAMG_TEAM"

    def __init__(self):
        super(DAMGTEAM, self).__init__()

        self.damg_version       = DAMG_VERSION()
        self.damg_server        = DAMG_SERVER()
        self.damg_copyright     = DAMG_COPYRIGHT(self)

        self._trinhdo           = dolsm._name
        self._duongminhduc      = duclsm._name

        self._founder           = self._trinhdo
        self._cofounder         = self._duongminhduc
        self._email             = "dot@damgteam.com"

        self._organization      = "Digital Animation Motion Graphic"
        self._members           = DDict(founder = self._trinhdo, co_founder= self._duongminhduc)
        self._groupname         = "DAMGteam"
        self._slogan            = "Comprehensive Design Solution"
        self._website           = "https://damgteam.com"

        self._serverurl         = "https://pipeline.damgteam.com"
        self._servercheck       = "https://pipeline.damgteam.com/check"
        self._serverautho       = "https://pipeline.damgteam.com/auth"

        self._version           = self.damg_version.__version__()
        self._plugin_version    = self.damg_version.__plugin_version__()
        self._api_version       = self.damg_version.__api_version__()
        self._copyright         = self.damg_copyright.__copyright__()

    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name:self.data}, indent=4)

    def __name__(self):
        return self._name

    def __organization__(self):
        return self._organization

    def __version__(self):
        return self._version

    def __api_version__(self):
        return self._api_version

    def __author__(self):
        return self._trinhdo

    def __email__(self):
        return self._email

    def __envKey__(self):
        return self._envKey

    @property
    def data(self):

        self._data.add_item('name',  self._name)
        self._data.add_item('organization', self.organization)
        self._data.add_item('id', self._id)
        self._data.add_item('envKey', self._envKey)
        self._data.add_item('groupname', self._groupname)

        self._data.add_item('slogan', self._slogan)
        self._data.add_item('website', self._website)

        self._data.add_item('version', self._version)
        self._data.add_item('plugin version', self._plugin_version)
        self._data.add_item('api version', self._api_version)
        self._data.add_item('copyright', self._copyright)

        self._data.add_item('founder', self._founder)
        self._data.add_item('co-founder', self._cofounder),
        self._data.add_item('serverUrl', self._serverurl)
        self._data.add_item('serverautho', self._serverautho)
        self._data.add_item('servercheck', self._servercheck)

        return self._data

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def organization(self):
        return self._organization

    @property
    def envKey(self):
        return self._envKey

    @property
    def groupname(self):
        return self._groupname

    @property
    def members(self):
        return self._members

    @property
    def servercheck(self):
        return self._servercheck

    @property
    def serverautho(self):
        return self._serverautho

    @property
    def serverurl(self):
        return self._serverurl

    @property
    def website(self):
        return self._website

    @property
    def slogan(self):
        return self._slogan

    @property
    def trinhdo(self):
        return self._trinhdo

    @property
    def duongminhduc(self):
        return self._duongminhduc

    @property
    def founder(self):
        return self._founder

    @property
    def cofounder(self):
        return self._cofounder

    @property
    def email(self):
        return self._email

    @property
    def version(self):
        return self._version

    @property
    def api_version(self):
        return self._api_version

    @property
    def plugin_version(self):
        return self._plugin_version

    @property
    def copyright(self):
        return self._copyright

    __dict__ = _data

organization = DAMGTEAM()

__organization__        = organization.__organization__()
__envKey__              = organization.__envKey__()
__version__             = organization.__version__()
__api_version__         = organization.__api_version__()
__author__              = organization.__author__()
__email__               = organization.__email__()
__copyright__           = organization._copyright

class PLM(object):
    key = "PLM"
    _name = "PLM"
    _id = "{0}.{1}.{2}".format(__organization__, _name, __version__)
    _objname = "Pipeline Manager"
    _data = DDict()
    assets = __organization__

    __product__ = "application/software"
    __appShortcut__ = "PLM.ink"
    __state__ = "2"
    __status__ = "Development/Unstable"
    __about__ = "Pipeline Manager (PLM)"
    __website__ = organization._website
    __slogan__ = "Comprehensive Design Solution"
    __wiki__ = "https://github.com/vtta2008/PipelineTool/wiki"
    __version__ = "13.0.1"
    __version_info__ = "{0} v{1}.{2}-{3}".format(__organization__, __version__, __state__, __status__)
    __api_version__ = "0.8.6",
    __author__ = __author__

    def __init__(self):
        super(PLM, self).__init__()

        self._name = "PLM"
        self._product = "application/software"
        self._shortcut = "PLM.ink"
        self._state = "2"
        self._status = "Development/Unstable"
        self._about = "Pipeline Manager (PLM)"
        self._website = organization.__website__
        self._slogan = "Comprehensive Design Solution"
        self._wiki = "https://github.com/vtta2008/PipelineTool/wiki"
        self._version = "13.0.1"
        self._version_info = "{0} v{1}.{2}-{3}".format(__organization__, __version__, self._state, self._status)
        self._api_version = organization.__api_version__
        self._author = __author__
        self._copyright = "{0} software (c) 2017-2018 {1}. All rights reserved.".format(self.__about__,  organization.__organization__())

        self._data = dict()

        self._data['key'] = "PLM"
        self._data['name'] = "PLM"
        self._data['id'] = self.id
        self._data['product'] = "application/software"
        self._data['shortcut'] = "PLM.ink"
        self._data['state'] = "2"
        self._data['status'] = "Development/Unstable"
        self._data['about'] = "Pipeline Manager (PLM)"
        self._data['website'] = organization.__website__
        self._data['slogan'] = "Comprehensive Design Solution"
        self._data['wiki'] = "https://github.com/vtta2008/PipelineTool/wiki"
        self._data['version'] = "13.0.1"
        self._data['version_info'] = "{0} v{1}.{2}-{3}".format(__organization__, __version__, self._state, self._status)
        self._data['api_version'] = organization.__api_version__
        self._data['authors'] = __author__
        self._data['copyright'] = "{0} software (c) 2017-2018 {1}. All rights reserved.".format(self.__about__, organization.__organization__())

    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name: self.data}, indent=4)

    @property
    def data(self):
        return self._data

    @property
    def __name__(self):
        return self._name

    @property
    def product(self):
        return self._product

    @property
    def shortcut(self):
        return self._shortcut

    @property
    def state(self):
        return self._state

    @property
    def status(self):
        return self._status

    @property
    def about(self):
        return self._about

    @property
    def website(self):
        return self._website

    @property
    def slogan(self):
        return self._slogan

    @property
    def wiki(self):
        return self._website

    @property
    def version(self):
        return self._version

    @property
    def version_info(self):
        return self._version_info

    @property
    def api_version(self):
        return self._api_version

    @property
    def author(self):
        return self._author

    @property
    def copyright(self):
        return self._copyright

    __dict__ = _data


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/08/2018 - 11:09 AM
# © 2017 - 2018 DAMGteam. All rights reserved