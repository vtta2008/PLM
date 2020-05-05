# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------


from urllib                     import parse
from cgi                        import parse_header
from PLM.commons.Core           import Url, FileInfo


def filenameFromHeader(header):
    value, params = parse_header(header)
    if 'filename*' in params:
        filename = params['filename*']
        if filename.startswith("UTF-8''"):
            filename = parse.unquote(filename[7:])
    elif 'filename' in params:
        filename = params['filename']
    else:
        filename = ''
    return filename


def filenameFromUrl(addr):
    link = Url.fromUserInput(addr)
    link.setFragment(None)
    link = Url.toString(Url.RemoveQuery)
    return FileInfo(parse.unquote_plus(link)).fileName()



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved