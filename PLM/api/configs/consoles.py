# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import tempfile
from plumbum                    import local, virtualenv
from bin.loggers                import DamgLogger
from PLM                        import APP_LOG
logger                          = DamgLogger(__file__, filepth=APP_LOG)



def dry_run(command, dry_run):
    """Executes a shell command unless the dry run option is set"""
    if not dry_run:
        cmd_parts = command.split(' ')
        # http://plumbum.readthedocs.org/en/latest/local_commands.html#run-and-popen
        return local[cmd_parts[0]](cmd_parts[1:])
    else:
        logger.info('Dry run of %s, skipping' % command)
    return True



def create_venv(tmp_dir=None):
    if not tmp_dir:
        tmp_dir = tempfile.mkdtemp()

    virtualenv('--no-site-packages', tmp_dir)

    return tmp_dir



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
