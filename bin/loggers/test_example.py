# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

def test_example():
    """Tests the usage example from the README"""
    from bin.loggers import models

    handler = models.StreamHandler()
    handler.setFormatter(models.ColoredFormatter('%(log_color)s%(levelname)s:%(name)s:%(message)s'))
    logger = models.getLogger('example')
    logger.addHandler(handler)

    return logger


logger = test_example()

logger.info('text info logging')
logger.warning('test warn logging')
logger.debug('test debug logging')
logger.error('test error logging')
logger.critical('test critical logging')

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
