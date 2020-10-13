# -*- coding: utf-8 -*-
"""

Script Name: baseVersion.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    This is how we construct a version object type.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from bin.base.obj import BaseTuple


class TypeTuple(BaseTuple):

    key                                 = 'TypeTuple'

    def __init__(self, *args, **kwargs):
        BaseTuple.__new__(self)

        self.kwargs                     = kwargs
        self.args                       = args


class BaseInfo(TypeTuple):

    Type                                = 'DAMGTYPEINFO'
    key                                 = 'TypeInfo'

    def __new__(self, content=tuple()):
        self.content                    = content
        return tuple.__new__(BaseInfo, self.content)

    def __bases__(self):
        if self.content:
            return tuple(BaseInfo, self.content)
        else:
            return tuple(BaseInfo, tuple())


def version_original():
    return (13, 0, 0)


def construct_class(infoObj, infoData, **info):

    obj                                 = infoObj
    doc_info                            = infoData['doc']
    name_info                           = infoData['name']
    module_info                         = infoData['module']
    str_info                            = '.'.join(str(i) for i in obj)
    type_info                           = '{0}: {1}'.format(name_info, str_info)
    infoKey                             = '__{0}__info__'.format(name_info.lower())

    info[infoKey]                       = obj
    info['__doc__']                     = doc_info
    info['__name__']                    = name_info
    info['__module__']                  = module_info
    info['__type__']                    = type_info
    info['__str__']                     = str_info

    return info


infoDoc                                 = 'version object'
versionContent                          = version_original()
versionInfo                             = BaseInfo(versionContent)
versionInfo.key                         = 'VersionInfo'
versionInfo.Type                        = 'DAMGVERSIONINFO'
versionDataInfo                         = {'doc': infoDoc, 'name': 'Version', 'module': 'PLM'}
versionConstruct                        = construct_class(versionInfo, versionDataInfo)


class BaseVersion(type):

    key                                 = 'BaseVersion'
    Type                                = 'DAMGVERSION'

    def __new__(cls, *args, **kwargs):
        newType = type.__new__(BaseVersion, 'Version', (BaseVersion,), versionConstruct)
        return newType

    def __init__(self, *args, **kwargs):
        # self.__new__(*args, **kwargs)
        super(BaseVersion, self).__init__(self, BaseVersion, *args, **kwargs)

    def __bases__(cls):
        return type.__new__(BaseVersion, 'Version', (BaseVersion,), versionConstruct)

    def __str__(self):
        return self.__str__

    def __repr__(self):
        return self.__str__

    def __call__(self):
        return isinstance(self, type)





# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved