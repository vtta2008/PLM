# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import logging


class CustomAdapter(logging.LoggerAdapter):

    """
    This example adapter expects the passed in dict-like object to have a
    'connid' key, whose value in brackets is prepended to the log message.
    """

    # which you can use like this:
    #
    # logger = logging.getLogger(__name__)
    # adapter = CustomAdapter(logger, {'connid': some_conn_id})

    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['connid'], msg), kwargs



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
